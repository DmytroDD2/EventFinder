from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from app.db import Base
from app.reviews.models import Review
from app.events.schemas import Category


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text())
    price = Column(Float, default=0.0)
    data = Column(DateTime, default=None)
    venue = Column(String)
    category = Column(Enum(Category), default="Other")
    creator = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    total_tickets = Column(Integer, default=5)
    created_by = relationship("User", back_populates="created_events")
    tickets = relationship("Tickets", back_populates="event", overlaps='events,tickets', cascade="all, delete-orphan")
    review = relationship("Review", back_populates="event", overlaps="review,event", cascade="all, delete-orphan")
