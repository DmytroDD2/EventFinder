from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.users.models import User
from app.users.schemas import BaseUser, Role, ChangeUserDate, ChangePassword, RechargeRequest
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


def get_user_exist(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


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
    # Збереження історії транзакцій (опціонально)
    # save_transaction_history(user.id, recharge_data.amount, "Recharge")
