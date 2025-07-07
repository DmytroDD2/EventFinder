from typing import Any, Optional

from pydantic import BaseModel, EmailStr


class BaseUserFriend(BaseModel):
    first_name: str
    last_name: str
    username: str
    profile_picture: Optional[str] = None
    email: EmailStr
    id: int
