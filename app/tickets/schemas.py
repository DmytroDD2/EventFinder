from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime, date, time

class BaseTicket(BaseModel):
    event_name: str
    user_name: str
    data: Optional[datetime] = None
    creator: str
    price: float
    description: str
class BaseTicketCreate(BaseModel):
    ticket_id: int


class BaseTicketCreate2(BaseTicket):
    creator: int
    event_id: int
    friend_id: int

