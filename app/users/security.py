from datetime import timedelta, datetime

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from fastapi import Depends, HTTPException, status, Header
from jose import JWTError, jwt
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.users.schemas import UserToken, Role
import os
from dotenv import load_dotenv

load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def get_password_hash(password: str):
    return pwd_context.hash(password)


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

api_key_header = APIKeyHeader(name="Authorization")


def create_token(data: dict, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user_token(token:  str = Depends(api_key_header)):#token: str = Depends(oauth2_scheme),
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user = UserToken(id=payload.get('id'), role=payload.get('role'))

        if user is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    return user


def permission(admin: UserToken):
    if admin.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="insufficient level of access"
        )
    return True

def mail_data():
    required_variables = ["MAIL_USERNAME_ENV", "MAIL_APP_PASSWORD_ENV"]
    my_mail = list(map(os.getenv, required_variables))
    if all(my_mail):

        MAIL_CONF = ConnectionConfig(
            MAIL_USERNAME=my_mail[0],
            MAIL_PASSWORD=my_mail[1],
            MAIL_FROM=os.getenv("MAIL_USERNAME_ENV"),
            MAIL_PORT=465,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=True,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        return MAIL_CONF


fastmail = FastMail(mail_data())


class AsyncEmailSender:
    def __init__(self, message):
        self.message = message

    async def __aenter__(self):
        await fastmail.send_message(self.message)
        return self.message

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise HTTPException(status_code=500, detail="Error sending email")
