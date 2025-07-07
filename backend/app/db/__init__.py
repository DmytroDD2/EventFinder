from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
# from app.users.models import User
# from app.events.models import Event
# from app.tickets.models import Tickets
# from app.notifications.models import Notification
import os
from dotenv import load_dotenv




load_dotenv()

SQLALCHEMY_DATABASE_URL = "postgresql://username:password@db/nudges"

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/postgres"
# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/nudges"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
#,  echo=True
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




# user = os.getenv("POSTGRES_USER")
# password = os.getenv("POSTGRES_PASSWORD")
# postgres_db = os.getenv("POSTGRES_DB")
#
# SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@db/{postgres_db}"