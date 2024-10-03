from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from culi.common.ext.sqlalchemy import sql
from culi.common.services import ResourceService
from culi.exceptions import CuliError
from culi.models.user import User
from culi.user.schemas.user import UserCreate, UserUpdate


class UserError(CuliError): ...


class UserService(ResourceService[User, UserCreate, UserUpdate]):
    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> User | None:
        query = sql.select(User).where(
            func.lower(User.email) == email.lower(),
            User.deleted_at.is_(None),
        )
        res = await session.execute(query)
        return res.scalars().unique().one_or_none()

    @staticmethod
    async def get_by_username(session: AsyncSession, username: str) -> User | None:
        query = sql.select(User).where(
            func.lower(User.username) == username.lower(),
            User.deleted_at.is_(None),
        )
        res = await session.execute(query)
        return res.scalars().unique().one_or_none()


user = UserService(User)
