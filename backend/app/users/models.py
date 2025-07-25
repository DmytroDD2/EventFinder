from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Enum, Float
from sqlalchemy.orm import relationship
from app.db import Base
from app.users.schemas import Role
from app.tickets.models import Tickets

from app.friends.models import Friendship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    profile_picture = Column(String)
    balance = Column(Float, default=0.0)
    username = Column(String, unique=True, index=True)
    password = Column(String, unique=False, index=True)
    role = Column(Enum(Role, back_populates="user"))
    created_events = relationship("Event", back_populates="created_by", cascade="all, delete-orphan")
    review = relationship("Review", back_populates="users", overlaps="user, user_review", cascade="all, delete-orphan")
    tickets = relationship("Tickets", back_populates="user",  overlaps="user,user_tickets", cascade="all, delete-orphan")
    password_reset_question = Column(String)
    friends = relationship(
        "User",
        secondary=lambda: Friendship.__table__,
        primaryjoin=lambda: User.id == Friendship.user_id,
        secondaryjoin=lambda: User.id == Friendship.friend_id, viewonly=True
    )

