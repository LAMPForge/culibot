from enum import StrEnum
from uuid import UUID

from sqlalchemy import String, ForeignKey, Uuid
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship

from culi.models.user import User


class SubType(StrEnum):
    user = "user"


SubTypeValue = tuple[SubType, "User"]


class SubTypeModelMixin:
    sub_type: Mapped[SubType] = mapped_column(String, nullable=False)
    user_id: Mapped[UUID | None] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="cascade"), nullable=True
    )

    @declared_attr
    def user(cls) -> Mapped["User | None"]:
        return relationship("User", lazy="joined")

    @hybrid_property
    def sub(self) -> "User | Organization":
        sub: User | None = None
        if self.sub_type == SubType.user:
            sub = self.user
        else:
            raise NotImplementedError()

        if sub is None:
            raise ValueError("Sub is not found.")

        return sub

    @sub.inplace.setter
    def _sub_setter(self, value: "User | Organization") -> None:
        if self.sub_type == SubType.user:
            self.user_id = value.id
        else:
            raise NotImplementedError()

    def get_sub_type_value(self) -> SubTypeValue:
        return self.sub_type, self.sub
