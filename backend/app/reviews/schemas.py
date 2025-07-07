from typing import Union, Optional
from datetime import date, time

from fastapi import Header
from pydantic import BaseModel, Field, field_validator, ConfigDict


class BaseReview(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    description: str

    # @field_validator("rating")
    # def validate_future_date(cls, value):
    #     if 1 <= value <= 10:
    #         return value
    #     raise ValueError("Rating must be between 1 and 10")


class ReviewParams(BaseModel):
    page: int = 1
    per_page: int = 10


class ResponseEventReviews(BaseModel):
    id: int
    rating: int
    description: str
    user_id: int
    event_id: int
    image_url: Optional[str] = None
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ResponseUserReview(BaseModel):
    id: int
    rating: int
    description: str
    user_id: int
    event_id: int
    image_url: Optional[str] = None
    name: Optional[str] = None


