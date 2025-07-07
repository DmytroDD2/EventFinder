import re
from pyclbr import Class
from typing import Optional

from fastapi import Form, UploadFile, File
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from enum import Enum


class UsersResponse(BaseModel):
    first_name: str
    last_name: str
    username: str
    profile_picture: Optional[str] = None
    email: EmailStr
    id: int



class Role(Enum):
    user = "user"
    admin = "admin"


class UserToken(BaseModel):
    id: int
    role: Role

class BasePassword(BaseModel):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


class ResetPassword(BaseModel):
    username: str
    password_reset_question: str
    new_password: str



class BaseUser(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    username: str
    profile_picture: Optional[str] = None
    email: EmailStr
    role: Role


class Validate:
    @field_validator("email", mode="before", check_fields=False)
    def validate_email(cls, value: str) -> str:
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, value):
            raise ValueError("The user entered an invalid email format")
        return value

    @field_validator("password_reset_question", mode="before", check_fields=False)
    def check_password_reset_question(cls, value: str) -> str:

        if not value.strip():
            raise ValueError("password_reset_question cannot be an empty string")
        return value



class BaseCreateUser(BaseUser, Validate):
    password: str
    password_reset_question: str = ...





class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class BaseRegisterUser(BaseModel):
    user: BaseUser
    token: Token

    model_config = ConfigDict(from_attributes=True)



class UserData(BaseUser):
    id: int
    balance: float
    model_config = ConfigDict(from_attributes=True)



class ChangeUserDate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_picture: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("email", mode="before", check_fields=False)
    def validate_email(cls, value: str) -> str:
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        if value and not re.match(email_pattern, value):
            raise ValueError("The user entered an invalid email format")
        return value




class ChangePassword(BaseModel):
    password: str


class ChangeUserRole(BaseModel):
    password: str


class Recharge(BaseModel):
    amount: float = Field(..., gt=0)



class SomeBase(BaseModel, Validate):
    first_name: str = Form(...),
    last_name: str = Form(...),
    username: str = Form(...),
    email: EmailStr = Form(...),
    profile_picture: Optional[UploadFile] = File(None)

# class SomeBase(BaseModel):
#     first_name: str = None
#     last_name: str = None
#     username: str | None
#     email: EmailStr = None
#     profile_picture: Optional[UploadFile] = File(None)