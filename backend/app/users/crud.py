
from fastapi import HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.users.models import User
from app.users.schemas import BaseCreateUser, Role, ChangeUserDate, ChangePassword, Recharge, ResetPassword
from typing import Optional

from app.users.security import check_password
from app.utils.file_operations import save_file, delete_file


def find_all_users(db: Session):
    users = db.query(User).all()
    return users

def find_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user


def authenticate_user(db, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if user and check_password(password, user.password):

        return user
    return None


def create_user(db:Session, user: BaseCreateUser):

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
        if value:
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

def change_user_image(db: Session, user_id: int, image):
    user_now = db.query(User).filter(User.id == user_id).first()
    previous_image = user_now.profile_picture
    if user_now:
        user_now.profile_picture = image
        db.commit()
        db.refresh(user_now)

        if previous_image:
            delete_file(previous_image)

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


def change_access(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    user.role = "admin" if user.role == Role.user else Role.user
    db.commit()

    return


def recharge_user_account(db: Session, recharge_data: Recharge, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.balance += recharge_data.amount
    db.commit()

    return recharge_data.amount, user.balance

