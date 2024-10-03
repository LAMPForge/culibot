from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import String, TIMESTAMP, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship

from culi.common.db.models.base import RecordModel
from culi.common.utils import utc_now
from culi.config import settings
from culi.models.user import User


def get_expires_at() -> datetime:
    return utc_now() + timedelta(seconds=settings.AUTH_LINK_TTL_SECONDS)

class AuthLink(RecordModel):
    __tablename__ = "auth_links"

    token_hash: Mapped[str] = mapped_column(String, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=get_expires_at
    )

    user_email: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="cascade"),
        nullable=True,
    )

    @declared_attr
    def user(cls) -> Mapped[User | None]:
        return relationship(User)
