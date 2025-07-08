import json
import os
import time
from datetime import timedelta, datetime
from pathlib import Path
from typing import Tuple, Optional

import jwt
from celery.bin.result import result
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, status, Form, UploadFile, File
from pydantic import EmailStr, ValidationError, BaseModel
from sqlalchemy.orm import Session
from app.main import app
from app.users.handlers import FormHandler
from app.users.models import User
from app.users.schemas import BaseCreateUser, UserLogin, ChangeUserDate, ChangePassword, Role, UserToken, \
    Recharge, \
    UserData, ResetPassword, BaseRegisterUser, SomeBase, BasePassword, UsersResponse
from app.db.session import get_db
from app.users.security import get_password_hash, get_current_user_token, permission, \
    mail_data, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS, create_token, \
    AsyncEmailSender
from app.users.crud import create_user, get_user_exist, authenticate_user, change_data_user, change_password_user, \
    change_access, recharge_user_account, find_user, reset_pysword, existing_user_by_email, change_user_image, \
    find_all_users
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi.responses import FileResponse

from app.utils.file_operations import save_file
from celery_worker import send_email_task
import uuid
router = APIRouter()
load_dotenv()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)





@router.post("/token", tags=["users"])
async def login_access_token(form_data: UserLogin, db: Session = Depends(get_db)):
    print(form_data, "+" * 100)
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login details"
        )

    access_token = create_token(
        {"id": user.id, "role": user.role.value}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        {"id": user.id, "role": user.role.value}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}




@router.post("/token/refresh", tags=["users"])
async def refresh_access_token(refresh_token: str = Form(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        id_us: str = payload.get("id")
        role: str = payload.get("role")
        if id is None or role is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    access_token = create_token({"id": id_us, "role": role}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", tags=["users"], response_model=BaseRegisterUser, status_code=201)
async def register_user(user: BaseCreateUser, db: Session = Depends(get_db)):
    existing_user = get_user_exist(db, user.username, user.email)

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    db_user = create_user(db, user)
    access_token = create_token(
        {"id": user.id, "role": user.role.value}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        {"id": user.id, "role": user.role.value}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    token = {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    if mail_data():
        message = {
            "subject": "Registration was successful",
            "recipients": user.email,
            "body": f"{user.first_name}! You have successfully registered on our website.",
            "subtype": "plain",
        }

        send_email_task.delay(message)


    return {"user": db_user, "token":token}


@router.get("", response_model=UserData, status_code=200)
async def get_user_data(db: Session = Depends(get_db), user: UserToken = Depends(get_current_user_token)):
    return find_user(db, user.id)

@router.get("/admin/{user_id}", response_model=UserData, status_code=200)
async def get_user_by_id(
        user_id: int,
        db: Session = Depends(get_db),
        admin: UserToken = Depends(get_current_user_token)
):
    permission(admin)
    user = find_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return find_user(db, user_id)

@router.get("/all-users", tags=["users"], response_model=list[UsersResponse], status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db), user: UserToken = Depends(get_current_user_token)):
    return find_all_users(db)




@router.put("/change", tags=["users"], status_code=status.HTTP_200_OK)
async def edit_user_data(
        form: FormHandler = Depends(),
        user: UserToken = Depends(get_current_user_token),
        db: Session = Depends(get_db)
):

    user_data = await form.get_user_data()

    return change_data_user(db, user.id, user_data)


@router.patch("/image", tags=["users"], status_code=status.HTTP_200_OK)
async def edit_user_data(
        image: UploadFile = File(None),
        user: UserToken = Depends(get_current_user_token),
        db: Session = Depends(get_db)
):
    image = await save_file(image)
    return change_user_image(db, user.id, image)



@router.patch("/admin/{user_id}/image", tags=["users"], status_code=status.HTTP_200_OK)
async def edit_user_data_by_admin(
        user_id: int,
        image: UploadFile = File(...),
        db: Session = Depends(get_db),
        admin: UserToken = Depends(get_current_user_token)
):
    permission(admin)
    image = await save_file(image)

    return change_user_image(db, user_id, image)


@router.patch("/password", tags=["users"], status_code=status.HTTP_200_OK)
async def edit_password(
        # password: str,
        password: BasePassword,
        user: UserToken = Depends(get_current_user_token),
        db: Session = Depends(get_db)
):

    hash_password = get_password_hash(password.password)
    return change_password_user(db, user.id, hash_password)


@router.patch("/admin/{user_id}/password", tags=["users"], status_code=status.HTTP_200_OK)
async def edit_password_by_admin(
        user_id: int,
        password: BasePassword,
        db: Session = Depends(get_db),
        admin: UserToken = Depends(get_current_user_token)
):
    permission(admin)
    hash_password = get_password_hash(password.password)
    return change_password_user(db, user_id, hash_password)




@router.patch("/password-reset", tags=["users"], status_code=status.HTTP_200_OK,response_model=None)
async def request_password_reset(user: ResetPassword, db: Session = Depends(get_db)):
    user.new_password = get_password_hash(user.new_password)
    return reset_pysword(db, user)


@router.post("/generate-reset-token", tags=["users"], status_code=status.HTTP_200_OK)
async def reset_password(
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    user = existing_user_by_email(db, email)
    if user:

        reset_token = create_token(

       {
           "id": user.id,
           "role": user.role.value
       },
           timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        if mail_data():
            message = {
                "subject": "Password Reset",
                "recipients": email,
                "body": f"Hello {user.username}! You have requested a password reset. Your reset token is: {reset_token}",
                "subtype": "plain",
            }
            send_email_task.delay(message)
        else:
            return f"Your reset token: {reset_token}"

        return f'Reset token sent to {email}'


@router.patch("/role", tags=["users"], status_code=status.HTTP_200_OK, response_model=None)
async def edit_role(
        user_id: int = Form(...),
        db: Session = Depends(get_db),
        admin: UserToken = Depends(get_current_user_token)
):

    permission(admin)
    return change_access(db, user_id)


@router.post("/recharge", tags=["users"], status_code=status.HTTP_200_OK)
async def recharge_account(
    recharge: Recharge,
    db: Session = Depends(get_db),
    user: UserToken = Depends(get_current_user_token)
):
  
    recharge, balance = recharge_user_account(db, recharge, user.id)

    return {"message": f"Account successfully recharged: {recharge}. New balance: {balance}"}


@router.post("/admin/{user_id}/recharge", tags=["users"], status_code=status.HTTP_200_OK)
async def admin_recharge_account(
    user_id: int,
    recharge: Recharge,
    db: Session = Depends(get_db),
    admin: UserToken = Depends(get_current_user_token)
):
    permission(admin)
    recharge, balance = recharge_user_account(db, recharge, user_id)

    return {"message": f"Account successfully recharged: {recharge}. New balance: {balance}"}
