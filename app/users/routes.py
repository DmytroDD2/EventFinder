import json
from typing import Tuple

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.main import app
from app.users.models import User
from app.users.schemas import BaseUser, UserLogin, ChangeUserDate, ChangePassword, Role, UserToken, RechargeRequest
from app.db.session import get_db
from app.users.security import get_password_hash, get_current_user_token, permission, fastmail, AsyncEmailSender
from app.users.crud import create_user, get_user_exist, authenticate_user, change_data_user, change_password_user, \
    increase_access, recharge_user_account, find_user
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jose import JWTError, jwt

router = APIRouter()


@router.post("/token", tags=["users"])
async def login_access_token(form_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login details"
        )
    token_data = {"id": user.id, "role": user.role.value}
    token = jwt.encode(token_data, "your_secret_key",  algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

@router.get("", response_model=BaseUser, status_code=200)
async def get_user_data(db: Session = Depends(get_db), user: UserToken = Depends(get_current_user_token)):
    return find_user(db, user.id)

@router.put("/change", tags=["users"], status_code=status.HTTP_200_OK)
def edit_user_data(
        user_data: ChangeUserDate,
        user: UserToken = Depends(get_current_user_token),
        db: Session = Depends(get_db)
):

    return change_data_user(db, user.id, user_data)


@router.put("/password", tags=["users"], status_code=status.HTTP_200_OK)
def edit_password(
        password: str,
        user: UserToken = Depends(get_current_user_token),
        db: Session = Depends(get_db)
):

    hash_password = get_password_hash(password)
    return change_password_user(db, user.id, hash_password)


@router.patch("/role", tags=["users"], status_code=status.HTTP_200_OK, response_model=None)
def edit_role(user_id: int,
              db: Session = Depends(get_db),
              admin: UserToken = Depends(get_current_user_token)):

    permission(admin)
    return increase_access(db, user_id)


@router.post("/register", tags=["users"], response_model=BaseUser, status_code=201)
async def register_user(user: BaseUser, db: Session = Depends(get_db)):
    existing_user = get_user_exist(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    db_user = create_user(db, user=user)

    message = MessageSchema(
        subject="Registration was successful",
        recipients=[user.email],
        body=f"{user.first_name}! You have successfully registered on our website.",
        subtype="plain"

    )

    async with AsyncEmailSender(message):
        pass

    return db_user


@app.post("/recharge", tags=["users"], status_code=status.HTTP_200_OK)
async def recharge_account(
    recharge_data: RechargeRequest,
    db: Session = Depends(get_db),
    user: UserToken = Depends(get_current_user_token)
):

    recharge, balance = recharge_user_account(db, recharge_data, user.id)

    return {"message": f"Account successfully recharged: {recharge}. New balance: {balance}"}
