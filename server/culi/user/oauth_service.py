from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from culi.common.services import ResourceServiceReader
from culi.models.user import OAuthAccount, OAuthPlatform


class OAuthAccountService(ResourceServiceReader[OAuthAccount]):
    async def get_by_platform_and_account_id(
        self, session: AsyncSession, platform: OAuthPlatform, account_id: str
    ) -> OAuthAccount | None:
        return await self.get_by(session, platform=platform, account_id=account_id)

    async def get_by_platform_and_user_id(
        self, session: AsyncSession, platform: OAuthPlatform, user_id: UUID
    ) -> OAuthAccount | None:
        return await self.get_by(session, platform=platform, user_id=user_id)

    async def get_by_platform_and_username(
        self, session: AsyncSession, platform: OAuthPlatform, username: str
    ) -> OAuthAccount | None:
        return await self.get_by(session, platform=platform, account_username=username)


oauth_account_service = OAuthAccountService(OAuthAccount)
