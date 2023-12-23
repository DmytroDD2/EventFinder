from typing import Any

from pydantic import BaseModel

class BaseUserFriend(BaseModel):
    first_name: str
    last_name: str
    username: str
    id: int
