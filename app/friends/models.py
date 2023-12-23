from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Enum, Float, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base


class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    friend_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_id])

    __table_args__ = (UniqueConstraint('user_id', 'friend_id', name='_friends_user_uc'), )

