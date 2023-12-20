from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db import Base
from app.tickets.models import Tickets
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text())
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete='SET NULL'))
    is_read = Column(Boolean, default=False)
    ticket = relationship("Tickets", backref="notifications")