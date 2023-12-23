from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from app.users.models import User
# from app.events.models import Event
# from app.tickets.models import Tickets
# from app.notifications.models import Notification
import os
from dotenv import load_dotenv

load_dotenv()

# print(f"DATABASE_URL from os.getenv: {os.getenv('DATABASE_URL')}", '='*100)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
#
engine = create_engine(SQLALCHEMY_DATABASE_URL)
#,  echo=True
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
