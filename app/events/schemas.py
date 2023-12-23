from enum import Enum
from typing import Union, Optional, Any, Dict
from datetime import datetime, date

from fastapi import Header, HTTPException
from pydantic import BaseModel, Field, field_validator, ValidationError, model_validator
from pydantic.v1 import root_validator


class Category(Enum):
    music = "Music"
    sports = "Sports"
    arts = "Arts"
    technology = "Technology"
    other = "Other"

class BaseFilter(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    location: Optional[str] = None
    category: Optional[Category] = None
    search_term: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    page: int = 1
    per_page: int = 10

    @model_validator(mode='before')
    def validate_atts(cls, data: Any):
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        min_price = data.get("min_price")
        max_price = data.get("max_price")

        if start_date and end_date and start_date > end_date:
            raise HTTPException(status_code=400, detail="start_date should not be greater than end_date")

        if min_price is not None and max_price is not None and min_price > max_price:
            raise HTTPException(status_code=400, detail="min_price should not be greater than max_price")

        return data



class BaseEventFirst(BaseModel):
    id: int
    creator: int


class ResponseEvent(BaseModel):
    category: Category
    name: str
    venue: str | None = None
    description: str | None = None
    price: float | None = None
    total_tickets: int | None = None
    data: Optional[Union[datetime, None]] = Field(default=None)


class BaseEvent(ResponseEvent):


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