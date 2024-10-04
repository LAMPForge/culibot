from typing import TypedDict

from culi.exceptions import CuliError


class GoogleUserProfile(TypedDict):
    id: str
    email: str
    email_verified: bool


class GoogleServiceError(CuliError): ...
