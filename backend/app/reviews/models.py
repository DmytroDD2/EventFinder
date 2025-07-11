from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db import Base


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer,primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    description = Column(Text())
    event_id = Column(ForeignKey("events.id", ondelete="CASCADE"))
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    event = relationship("Event", back_populates="review", overlaps="user, user_review")
    users = relationship("User", back_populates="review", overlaps="review, users")
