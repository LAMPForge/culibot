import httpx
from httpx_oauth.clients.google import GoogleOAuth2
from sqlalchemy.ext.asyncio import AsyncSession

from culi.config import settings
from culi.integrations.google.schemas import GoogleUserProfile, GoogleServiceError
from culi.models.oauth2_token import OAuth2Token
from culi.models.user import User, OAuthPlatform, OAuthAccount
from culi.user.oauth_service import oauth_account_service
from culi.user.services.user import user as user_service

google_oauth_client = GoogleOAuth2(
    settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET
)


class AccountLinkedToAnotherUserError(GoogleServiceError):
    def __init__(self) -> None:
        message = (
            "This Google account is already linked to another user on Polar. "
            "You may have already created another account "
            "with a different email address."
        )
        super().__init__(message, 403)


class GoogleService:
    async def login_or_signup(
        self,
        session: AsyncSession,
        *,
        token: OAuth2Token,
    ) -> User:
        google_profile = await self._get_profile(token["access_token"])
        user = await user_service.get_by_oauth_account(
            session, OAuthPlatform.google, google_profile["id"]
        )
        if user is not None:
            oauth_account = user.get_oauth_account(OAuthPlatform.google)
            assert oauth_account is not None
            oauth_account.access_token = token["access_token"]
            oauth_account.expires_at = token["expires_at"]
            oauth_account.account_username = google_profile["email"]
            session.add(oauth_account)
            return user

        oauth_account = OAuthAccount(
            platform=OAuthPlatform.google,
            account_id=google_profile["id"],
            account_email=google_profile["email"],
            account_username=google_profile["email"],
            access_token=token["access_token"],
            expires_at=token["expires_at"],
        )

        user = await user_service.get_by_email(session, google_profile["email"])

    async def link_user(
        self,
        session: AsyncSession,
        *,
        user: User,
        token: OAuth2Token,
    ) -> User:
        google_profile = await self._get_profile(token["access_token"])

        oauth_account = await oauth_account_service.get_by_platform_and_account_id(
            session, OAuthPlatform.google, google_profile["id"]
        )

        if oauth_account is not None:
            if oauth_account.user_id != user.id:
                raise AccountLinkedToAnotherUserError()
        else:
            oauth_account = OAuthAccount(
                platform=OAuthPlatform.google,
                account_id=google_profile["id"],
                account_email=google_profile["email"],
            )
            user.oauth_accounts.append(oauth_account)

        oauth_account.access_token = token["access_token"]
        oauth_account.expires_at = token["expires_at"]
        oauth_account.account_username = google_profile["email"]
        session.add(user)

        await session.flush()

        return user

    @staticmethod
    async def _get_profile(token: str) -> GoogleUserProfile:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {token}"},
            )
            res.raise_for_status()

            data = res.json()
            return GoogleUserProfile(**data)


google = GoogleService()
