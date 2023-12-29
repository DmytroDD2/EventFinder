from pydantic import BaseModel, EmailStr, Field
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


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    email: EmailStr
    role: Role


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