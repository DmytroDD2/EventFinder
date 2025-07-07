from typing import Optional, Union, List

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime, date, time

from app.events.models import Event
from app.events.schemas import ResponseEvent, EventImageBase
from app.users.models import User


class BaseTicket(BaseModel):
    event_name: str
    user_name: str
    data: Optional[datetime] = None
    creator: str
    price: float
    description: str
class BaseTicketCreate(BaseModel):
    ticket_id: int

class BaseResponseTickets(BaseModel):
    ticket_id: int
    event_id: int
    event_name: str
    data: Optional[datetime] = None
    creator: str
    description: Optional[str]
    images: List[str | None]

    model_config = ConfigDict(from_attributes=True)


class BaseResponseFriendsTickets(BaseResponseTickets):
    profile_picture: Optional[str] = None
    friend_id: int
    friend_name: str



class BaseTicketCreate2(BaseTicket):
    creator: int
    event_id: int
    friend_id: int

