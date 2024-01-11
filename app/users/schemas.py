import re

from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum


class Role(Enum):
    user = "user"
    admin = "admin"


class UserToken(BaseModel):
    id: int
    role: Role


class UserLogin(BaseModel):
    username: str
    password: str


class ResetPassword(BaseModel):
    username: str
    password_reset_question: str
    new_password: str

class BaseUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    password_reset_question: str = ...
    email: EmailStr
    role: Role

    @field_validator("password_reset_question")
    def check_password_reset_question(cls, value):
        if not value.strip():
            raise ValueError("password_reset_question cannot be an empty string")
        return value

    @field_validator("email")
    def validate_email(cls, value):
        if not re.match(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+', value):
            raise ValueError('The user entered an invalid email format')
        return value


class UserData(BaseUser):
    balance: float
    class Config:
        from_attributes = True


class ChangeUserDate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr


class ChangePassword(BaseModel):
    password: str


class ChangeUserRole(BaseModel):
    password: str


class RechargeRequest(BaseModel):
    amount: float = Field(..., gt=0)