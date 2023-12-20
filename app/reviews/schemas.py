from typing import Union, Optional
from datetime import date, time

from fastapi import Header
from pydantic import BaseModel, Field, field_validator


class BaseReview(BaseModel):
    rating: int = Field(min=1, max=5)
    description: str

    @field_validator("rating")
    def validate_future_date(cls, value):
        if 1 <= value <= 5:
            return value
        raise ValueError("Rating must be between 1 and 5")

