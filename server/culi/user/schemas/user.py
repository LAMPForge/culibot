from culi.auth.scope import Scope
from culi.common.schemas import Schema, TimestampedSchema
from culi.models.user import User as UserModel
from pydantic import UUID4, EmailStr, Field


class User(Schema):
    username: str

    @classmethod
    def from_db(cls, o: UserModel):
        return cls(
            username=o.username,
        )


class UserBase(Schema):
    username: str = Field(..., max_length=50)
    email: EmailStr


class UserRead(UserBase, TimestampedSchema):
    id: UUID4
    username: str
    email: EmailStr


class UserScopes(Schema):
    scopes: list[Scope]


class UserCreate(UserBase): ...


class UserUpdate(UserBase): ...