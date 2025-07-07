from datetime import timedelta, datetime, timezone

import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError

from fastapi.security import OAuth2PasswordBearer, APIKeyHeader, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Header, Security

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, fastmail
from app.users.schemas import UserToken, Role
import os
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
load_dotenv()


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


SECRET_KEY = "your_secret_key"


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1200

REFRESH_TOKEN_EXPIRE_DAYS = 7
# api_key_header = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

# api_key_header = APIKeyHeader(name="Authorization")
http_bearer = HTTPBearer()

def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_token(data: dict, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user_token(token: HTTPAuthorizationCredentials = Security(http_bearer)):#token: str = Depends(oauth2_scheme),
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = token.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user = UserToken(id=payload.get('id'), role=payload.get('role'))

        if user is None:
            raise credentials_exception

    except InvalidTokenError:
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


# fastmail = FastMail(mail_data())




class AsyncEmailSender:
    def __init__(self, message):

        self.message = message
    async def __aenter__(self):
        await fastmail.send_message(self.message)
        return self.message

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise HTTPException(status_code=500, detail="Error sending email")


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(message):

    required_variables = ["MAIL_USERNAME_ENV", "MAIL_APP_PASSWORD_ENV"]
    EMAIL, PASSWORD = list(map(os.getenv, required_variables))

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = message["recipients"]
    msg['Subject'] = message["subject"]
    msg.attach(MIMEText(message["body"], 'plain'))


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL, PASSWORD)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
