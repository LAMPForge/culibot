import datetime
from typing import Literal

from pydantic import UUID4, EmailStr, field_validator

from culi.common.http import get_safe_return_url
from culi.common.schemas import EmailStrDNS, Schema


class AuthLinkRequest(Schema):
    email: EmailStrDNS
    return_to: str | None = None

    @field_validator("return_to")
    @classmethod
    def validate_return_to(cls, v: str | None) -> str:
        return get_safe_return_url(v)


class AuthLinkCreate(Schema):
    token_hash: str
    user_email: EmailStr
    user_id: UUID4 | None = None
    expires_at: datetime.datetime | None = None


class AuthLinkUpdate(Schema): ...