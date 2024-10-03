import time

from culi.common.db.models.base import RecordModel
from sqlalchemy.schema import Index
from sqlalchemy import (
    Column,
    String,
    Integer,
    func, Boolean,
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
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
