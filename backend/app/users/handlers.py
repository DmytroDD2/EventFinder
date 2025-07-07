from typing import Optional

from fastapi import Form, UploadFile, File, HTTPException
from pydantic import EmailStr, ValidationError
from fastapi.exceptions import RequestValidationError
from app.users.schemas import ChangeUserDate
from app.utils.file_operations import save_file


class FormHandler:
    def __init__(
            self,
            first_name: str = Form(None),
            last_name: str = Form(None),
            username: str = Form(None),
            email: Optional[EmailStr] = Form(None),
            profile_picture: Optional[UploadFile] = File(None)
    ):

        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.profile_picture = profile_picture

    async def get_user_data(self) -> ChangeUserDate:
        try:

            user_data = ChangeUserDate(
                first_name=self.first_name,
                last_name=self.last_name,
                username=self.username,
                email=self.email,
                profile_picture=await save_file(self.profile_picture) if self.profile_picture else None,
            )

        except ValidationError as e:
            res = e.errors()[0]
            # res.exclude("url")
            # del res["url"]
            raise RequestValidationError(res)

        return user_data



