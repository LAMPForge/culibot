from datetime import datetime
from typing import Annotated

from email_validator import EmailNotValidError
from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
    EmailStr,
    AfterValidator
)
from pydantic_core import PydanticCustomError

from culi.common.email import validate_email


def _validate_email_dns(email: str) -> str:
    try:
        validate_email(email)
    except EmailNotValidError as e:
        raise PydanticCustomError(
            "value_error",
            "value is not a valid email address: {reason}",
            {"reason": str(e)},
        ) from e
    else:
        return email


EmailStrDNS = Annotated[EmailStr, AfterValidator(_validate_email_dns)]


class Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IDSchema(Schema):
    id: UUID4 = Field(..., description="The ID of the object.")


class TimestampedSchema(Schema):
    created_at: datetime = Field(description="Creation timestamp of the object.")
    modified_at: datetime | None = Field(
        description="Last modification timestamp of the object."
    )