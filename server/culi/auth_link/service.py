import datetime
from math import ceil
from urllib.parse import urlencode

from sqlalchemy.ext.asyncio import AsyncSession
from culi.auth_link.schemas import AuthLinkCreate, AuthLinkUpdate
from culi.common.crypto import generate_token_hash_pair, get_token_hash
from culi.common.services import ResourceService
from culi.common.utils import utc_now
from culi.config import settings
from culi.email.renderer import get_email_renderer
from culi.email.sender import get_email_sender
from culi.exceptions import CuliError
from culi.models.auth_link import AuthLink
from culi.models.user import User
from culi.user.services.user import user as user_service


TOKEN_PREFIX = "culi_"


class AuthLinkError(CuliError): ...


class AuthLinkService(ResourceService[AuthLink, AuthLinkCreate, AuthLinkUpdate]):
    @staticmethod
    async def request(
        session: AsyncSession,
        email: str,
        *,
        expires_at: datetime.datetime | None = None,
    ) -> tuple[AuthLink, str]:
        user = await user_service.get_by_email(session, email)

        token, token_hash = generate_token_hash_pair(
            secret=settings.SECRET, prefix=TOKEN_PREFIX
        )
        auth_link_create = AuthLinkCreate(
            token_hash=token_hash,
            expires_at=expires_at,
            user_email=email,
            user_id=user.id if user else None,
        )

        auth_link = AuthLink(**auth_link_create.model_dump())
        session.add(auth_link)
        await session.commit()

        return auth_link, token

    @staticmethod
    async def send(
        auth_link: AuthLink,
        token: str,
        base_url: str,
        *,
        extra_url_params: dict[str, str] = {},
    ) -> None:
        email_renderer = get_email_renderer({"auth_link": "culi.auth_link"})
        email_sender = get_email_sender()

        delta = auth_link.expires_at - utc_now()
        token_lifetime_minutes = int(ceil(delta.seconds / 60))

        url_params = {"token": token, **extra_url_params}
        subject, body = email_renderer.render_from_template(
            "Sign in to Culi Chatbot",
            "auth_link/auth_link.html",
            {
                "token_lifetime_minutes": token_lifetime_minutes,
                "url": f"{base_url}?{urlencode(url_params)}",
                "current_year": datetime.datetime.now().year,
            },
        )

        email_sender.send_to_user(
            to_email_addr=auth_link.user_email, subject=subject, html_content=body
        )

    async def authenticate(self, session: AsyncSession, token: str) -> User:
        token_hash = get_token_hash(token, secret=settings.SECRET)
        magic_link = await self._get_valid_magic_link_by_token_hash(session, token_hash)

        if magic_link is None:
            raise InvalidMagicLink()

        user = magic_link.user
        if user is None:
            user = await user_service.get_by_email_or_signup(
                session, magic_link.user_email
            )

        user.email_verified = True
        session.add(user)

        await session.delete(magic_link)

        return user


auth_link = AuthLinkService(AuthLink)