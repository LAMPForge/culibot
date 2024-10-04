from typing import cast, Any

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from culi.auth.scope import Scope, scope_to_set
from culi.common.db.models.base import RecordModel
from authlib.integrations.sqla_oauth2 import OAuth2TokenMixin

from culi.oauth2.sub_type import SubTypeModelMixin


class OAuth2Token(RecordModel, OAuth2TokenMixin, SubTypeModelMixin):
    __tablename__ = "oauth2_tokens"

    nonce: Mapped[str | None] = mapped_column(String, index=True, nullable=True)

    @property
    def expires_at(self) -> int:
        return cast(int, self.issued_at) + cast(int, self.expires_in)

    @property
    def scopes(self) -> set[Scope]:
        return scope_to_set(cast(str, self.get_scope()))

    def get_introspection_data(self, issuer: str) -> dict[str, Any]:
        return {
            "active": not cast(bool, self.is_revoked())
                      and not cast(bool, self.is_expired()),
            "client_id": self.client_id,
            "token_type": self.token_type,
            "scope": self.get_scope(),
            "sub_type": self.sub_type,
            "sub": str(self.sub.id),
            "aud": self.client_id,
            "iss": issuer,
            "exp": self.expires_at,
            "iat": self.issued_at,
        }
