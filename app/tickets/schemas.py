from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime, date, time


class BaseTicketCreate(BaseModel):
    event_name: str
    user_name: str
    data: Optional[datetime] = None
    creator: str
    price: float
    description: str
    ticket_id: int
