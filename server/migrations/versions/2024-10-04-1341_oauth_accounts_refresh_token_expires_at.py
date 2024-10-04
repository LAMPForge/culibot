"""oauth_accounts_refresh_token_expires_at

Revision ID: 7701facf2a9f
Revises: 68abda1d42ff
Create Date: 2024-10-04 13:41:08.677577

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# Culi Custom Imports

# revision identifiers, used by Alembic.
revision = "7701facf2a9f"
down_revision = "68abda1d42ff"
branch_labels: tuple[str] | None = None
depends_on: tuple[str] | None = None


def upgrade() -> None:
    op.add_column(
        "oauth_accounts",
        sa.Column("refresh_token_expires_at", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("oauth_accounts", "refresh_token_expires_at")