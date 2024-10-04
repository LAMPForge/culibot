from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from culi.common.http import get_safe_return_url
from culi.common.schemas import Schema
from fastapi import Request, Response

from culi.config import settings
from culi.models.user import User
from culi.common import jwt
from culi.user.services.user import user as user_service


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
            ),
            expires_at,
        )

    @classmethod
    def generate_logout_response(cls, *, response: Response) -> LogoutResponse:
        cls.set_auth_cookie(response=response, value="", expires=0)
        return LogoutResponse(success=True)

    @classmethod
    def generate_login_cookie_response(
        cls,
        *,
        request: Request,
        user: User,
        return_to: str | None = None,
    ) -> RedirectResponse:
        token, _ = cls.generate_token(user=user)

        is_localhost = request.url.hostname in ["127.0.0.1", "localhost"]
        secure = False if is_localhost else True

        return_url = get_safe_return_url(return_to)
        response = RedirectResponse(return_url, 303)
        cls.set_auth_cookie(response=response, value=token, secure=secure)
        return response

    @classmethod
    async def get_user_from_cookie(
        cls, session: AsyncSession, *, cookie: str
    ) -> User | None:
        try:
            decoded = jwt.decode_unsafe(token=cookie, secret=settings.SECRET)
            return await user_service.get(session, id=decoded["user_id"])
        except (KeyError, jwt.DecodeError, jwt.ExpiredSignatureError):
            return None