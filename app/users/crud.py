from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.users.models import User
from app.users.schemas import BaseUser, Role, ChangeUserDate, ChangePassword, RechargeRequest, ResetPassword
from typing import Optional
from app.users.security import pwd_context


def find_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user


def authenticate_user(db, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if user and pwd_context.verify(password, user.password):

        return user
    return None


def create_user(db:Session, user: BaseUser):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_exist(db: Session, username: str, email: str = None):
    existing_user_by_username = db.query(User).filter(User.username == username).first()
    if existing_user_by_username:
        raise HTTPException(
            status_code=409,
            detail=f"User with the name '{username}' already exists."
        )

    existing_user_by_email = db.query(User).filter(User.email == email).first()
    if existing_user_by_email:
        raise HTTPException(
            status_code=409,
            detail=f"User with the email '{email}' already exists."
        )



def change_data_user(db: Session, user_id: int, new_user: ChangeUserDate):
    user_now = db.query(User).filter(User.id == user_id).first()

    for key, value in new_user:
        if value not in ["string", "user@example.com"]:
            setattr(user_now, key, value)

    db.commit()
    db.refresh(user_now)
    return user_now


def change_password_user(db: Session, user_id: int, password: str):
    user_now = db.query(User).filter(User.id == user_id).first()
    user_now.password = password
    db.commit()
    db.refresh(user_now)
    return user_now


def existing_user_by_email(db: Session, email: str):
    user_now = (db.query(User).filter(User.email == email).first())
    if not user_now:
        raise HTTPException(status_code=404, detail=f"User with the email '{email}' does not exist.")
    return user_now


def reset_pysword(db: Session, user: ResetPassword):
    user_now = db.query(User).filter(User.username == user.username,
                                     User.password_reset_question == user.password_reset_question
                                     ).first()
    if not user_now:
        raise HTTPException(status_code=404, detail="Invalid credentials. Please check your information.")

    user_now.password = user.new_password
    db.commit()
    db.refresh(user_now)
    return user_now


def increase_access(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    user.role = "admin"
    db.commit()
    return


def recharge_user_account(db: Session, recharge_data: RechargeRequest, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.balance += recharge_data.amount
    db.commit()

    return recharge_data.amount, user.balance

