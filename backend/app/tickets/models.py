from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Date, Time, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base
from app.events.models import Event
class Tickets(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="tickets", overlaps='user,user_tickets')
    event = relationship("Event", back_populates="tickets", overlaps='events,tickets')

    __table_args__ = (UniqueConstraint('event_id', 'user_id', name='_event_user_uc'),)


