from enum import Enum
from typing import Union, Optional, Any, Dict, List
from datetime import datetime, date
from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi import Header, HTTPException, UploadFile, File
from pydantic import BaseModel, Field, field_validator, ValidationError, model_validator, ConfigDict


class Category(Enum):
    music = "Music"
    sports = "Sport"
    arts = "Arts"
    technology = "Technology"
    other = "Other"

class BaseFilter(Filter):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    location: Optional[str] = None
    category: Optional[Category] = None
    search_term: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    page: int = 1
    per_page: int = 10
    totalCount: Optional[bool] = None

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


class EventImageBase(BaseModel):
    id: int
    event_id: int
    image_url: str



class EventBase(BaseModel):
    category: Optional[Category] = None
    name: Optional[str] = None
    venue: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    total_tickets: Optional[int] = None
    data: Optional[Union[datetime, None]] = Field(default=None)

class ResponseMyEvent(EventBase):
    id: int

class BaseEventFirst(EventBase):
    # category: Optional[Category] = None
    # name: Optional[str] = None
    # venue: Optional[str] = None
    # description: Optional[str] = None
    # price: Optional[float] = None
    # total_tickets: Optional[int] = None
    # data: Optional[Union[datetime, None]] = Field(default=None)

    @field_validator("data")
    def validate_future_date(cls, value):
        if value and value.date() < datetime.now(value.tzinfo).date():
            raise ValueError("The date must be in the future")
        return value



class ResponseEvent(BaseEventFirst):
    id: int
    images: List[EventImageBase] = None


class PaginatedEvents(BaseModel):
    items: List[ResponseEvent]
    totalCount: Optional[int] = None

class ResponseSingleEvent(ResponseEvent):
    creator: int

class UniqEvent(BaseEventFirst):

    name : str
    category: Category
    images: List[EventImageBase] = None

    @field_validator("data")
    def validate_future_date(cls, value):
        if value and value <= datetime.now(value.tzinfo):
            raise ValueError("The date must be in the future")
        return value

    model_config = ConfigDict(from_attributes=True)


class BaseEvent(UniqEvent):
    images: Optional[List[UploadFile]] = File(None)



class BaseEventEdit(BaseEvent):
    event_id: int
    category: Optional[Category] = None
    name: Optional[str] = None




class EventParams(BaseModel):
    page: int = 1
    per_page: int = 10



