from enum import Enum
from typing import Union, Optional
from datetime import datetime

from fastapi import Header
from pydantic import BaseModel, Field, field_validator




class Category(Enum):
    music = "Music"
    sports = "Sports"
    arts = "Arts"
    technology = "Technology"
    other = "Other"

class BaseFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    category: Optional[Category] = None
    search_term: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    page: int = 1
    per_page: int = 10
class BaseEventFirst(BaseModel):
    id: int
    creator: int


class BaseEvent(BaseModel):
    category: Category
    name: str
    venue: str | None = None
    description: str | None = None
    price: float | None = None
    total_tickets: int | None = None
    data: Optional[Union[datetime, None]] = Field(default=None)


    @field_validator("data")
    def validate_future_date(cls, value):
        if value and value <= datetime.now(value.tzinfo):
            raise ValueError("The date must be in the future")
        return value


#Optional[Union[time, None]]

class EventResponse(BaseEvent, BaseEventFirst):
    pass




class EventDelete(BaseModel):
    event_id: int
    Authorization: str = Header(..., description="Bearer <your_token>")


class EventParams(BaseModel):
    page: int = 1
    per_page: int = 10