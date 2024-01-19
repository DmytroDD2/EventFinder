import json
import os
from datetime import timedelta, datetime
from typing import Tuple, Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, status, Form
from sqlalchemy.orm import Session
from app.main import app
from app.users.models import User
from app.users.schemas import BaseUser, UserLogin, ChangeUserDate, ChangePassword, Role, UserToken, RechargeRequest, \
    UserData, ResetPassword
from app.db.session import get_db
from app.users.security import get_password_hash, get_current_user_token, permission, fastmail, AsyncEmailSender, \
    mail_data, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS, create_token
from app.users.crud import create_user, get_user_exist, authenticate_user, change_data_user, change_password_user, \
    increase_access, recharge_user_account, find_user, reset_pysword, existing_user_by_email
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jose import JWTError, jwt

router = APIRouter()
load_dotenv()



@router.post("/token", tags=["users"])
async def login_access_token(form_data: UserLogin, db: Session = Depends(get_db)):
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
    except JWTError:
        raise credentials_exception

    access_token = create_token({"id": id_us, "role": role}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", tags=["users"], response_model=BaseUser, status_code=201)
async def register_user(user: BaseUser, db: Session = Depends(get_db)):
    existing_user = get_user_exist(db, user.username, user.email)

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    db_user = create_user(db, user=user)

    if mail_data():
        message = MessageSchema(
            subject="Registration was successful",
            recipients=[user.email],
            body=f"{user.first_name}! You have successfully registered on our website.",
            subtype="plain"

        )

        async with AsyncEmailSender(message):
            pass

    return db_user


@router.get("", response_model=UserData, status_code=200)
async def get_user_data(db: Session = Depends(get_db), user: UserToken = Depends(get_current_user_token)):
    return find_user(db, user.id)


@router.put("/change", tags=["users"], status_code=status.HTTP_200_OK)
async def edit_user_data(
        user_data: ChangeUserDate,
        user: UserToken = Depends(get_current_user_token),
        db: Session = Depends(get_db)
):

    return change_data_user(db, user.id, user_data)


@router.patch("/password", tags=["users"], status_code=status.HTTP_200_OK)
async def edit_password(
        password: str,
        user: UserToken = Depends(get_current_user_token),
        db: Session = Depends(get_db)
):

    hash_password = get_password_hash(password)
    return change_password_user(db, user.id, hash_password)


@router.patch("/password-reset", tags=["users"], status_code=status.HTTP_200_OK,response_model=None)
async def request_password_reset(user: ResetPassword, db: Session = Depends(get_db)):
    user.new_password = get_password_hash(user.new_password)
    return reset_pysword(db, user)


@router.post("/generate-reset-token", tags=["users"], status_code=status.HTTP_200_OK)
async def reset_password(
    email: str,
    db: Session = Depends(get_db)
):
    user = existing_user_by_email(db, email)
    if user:

        reset_token = create_token(
{"id": user.id, "role": user.role.value}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        if mail_data():
            message = MessageSchema(
                subject="Password Reset",
                recipients=[email],
                body=f"Hello {user.username}! You have requested a password reset. Your reset token is: {reset_token}",
                subtype="plain"
            )
            async with AsyncEmailSender(message):
                pass
        else:
            return f"Your reset token: {reset_token}"

        return f'Reset token sent to {email}'


@router.patch("/role", tags=["users"], status_code=status.HTTP_200_OK, response_model=None)
async def edit_role(user_id: int,
              db: Session = Depends(get_db),
              admin: UserToken = Depends(get_current_user_token)
):

    permission(admin)
    return increase_access(db, user_id)


@app.post("/recharge", tags=["users"], status_code=status.HTTP_200_OK)
async def recharge_account(
    recharge_data: RechargeRequest,
    db: Session = Depends(get_db),
    user: UserToken = Depends(get_current_user_token)
):

    recharge, balance = recharge_user_account(db, recharge_data, user.id)

    return {"message": f"Account successfully recharged: {recharge}. New balance: {balance}"}
