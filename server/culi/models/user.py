import time

from culi.common.db.models.base import RecordModel
from sqlalchemy.schema import Index
from sqlalchemy import (
    Column,
    String,
    Integer,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column


class User(RecordModel):
    __tablename__ = "users"
    __table_args__ = (
        Index(
            "ix_users_email_case_insensitive", func.lower(Column("email")), unique=True
        ),
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    access_token: Mapped[str] = mapped_column(String(1024), nullable=False)
    expires_at: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    refresh_token: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )
    refresh_token_expires_at: Mapped[int | None] = mapped_column(
        Integer, nullable=True, default=None
    )

    def is_access_token_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

    def should_refresh_access_token(self, unless_ttl_gt: int = 60 * 30) -> bool:
        if (
                self.expires_at
                and self.refresh_token
                and self.expires_at <= (time.time() + unless_ttl_gt)
        ):
            return True
        return False
