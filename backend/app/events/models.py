from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from app.db import Base
from app.reviews.models import Review
from app.events.schemas import Category


class Event(Base):
    __tablename__ = "events"

    __mapper_args__ = {

        'confirm_deleted_rows': False
    }
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
    images = relationship("EventImage", back_populates="event", cascade="all, delete-orphan")


class EventImage(Base):
    __tablename__ = "event_images"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))  # Зв'язок із подією
    image_url = Column(String, nullable=False)  # Шлях до зображення

    event = relationship("Event", back_populates="images")

