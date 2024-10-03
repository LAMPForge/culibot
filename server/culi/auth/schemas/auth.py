from pydantic import field_validator

from culi.user.schemas.user import UserBase


class UserLogin(UserBase):
    password: str

    @field_validator("password")
    def password_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string")
        return v
