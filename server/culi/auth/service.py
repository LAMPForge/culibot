from datetime import datetime

from culi.common.schemas import Schema
from fastapi import Request, Response

from culi.config import settings


class LogoutResponse(Schema):
    success: bool


class AuthService:
    @staticmethod
    def set_auth_cookie(
        *,
        response: Response,
        value: str,
        expires: int = settings.AUTH_COOKIE_TTL_SECONDS,
        secure: bool = True,
    ) -> None:
        response.set_cookie(
            settings.AUTH_COOKIE_KEY,
            value=value,
            expires=expires,
            path="/",
            domain=settings.AUTH_COOKIE_DOMAIN,
            secure=secure,
            httponly=True,
            samesite="lax",
        )

    @classmethod
    def generate_token(cls, user: User) -> tuple[str, datetime]:
        expires_at = jwt.create_expiration_dt(seconds=settings.AUTH_COOKIE_TTL_SECONDS)
        return (
            jwt.encode(
                data={
                    "user_id": str(user.id),
                },
                secret=settings.SECRET,
                expires_at=expires_at,
                type="auth",
            ),
            expires_at,
        )

    @classmethod
    def generate_logout_response(cls, *, response: Response) -> LogoutResponse:
        cls.set_auth_cookie(response=response, value="", expires=0)
        return LogoutResponse(success=True)
