"""oauth_accounts

Revision ID: 68abda1d42ff
Revises: 55e35779e745
Create Date: 2024-10-04 13:36:38.811381

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# Culi Custom Imports

# revision identifiers, used by Alembic.
revision = "68abda1d42ff"
down_revision = "55e35779e745"
branch_labels: tuple[str] | None = None
depends_on: tuple[str] | None = None


def upgrade() -> None:
    op.create_table(
        "oauth_accounts",
        sa.Column("platform", sa.String(length=32), nullable=False),
        sa.Column("access_token", sa.String(length=1024), nullable=False),
        sa.Column("expires_at", sa.Integer(), nullable=True),
        sa.Column("refresh_token", sa.String(length=1024), nullable=True),
        sa.Column("account_id", sa.String(length=320), nullable=False),
        sa.Column("account_email", sa.String(length=320), nullable=False),
        sa.Column("account_username", sa.String(length=320), nullable=True),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("modified_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("oauth_accounts_user_id_fkey"),
            ondelete="cascade",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("oauth_accounts_pkey")),
        sa.UniqueConstraint(
            "platform",
            "account_id",
            name=op.f("oauth_accounts_platform_account_id_key"),
        ),
    )
    op.create_index(
        "idx_user_id_platform", "oauth_accounts", ["user_id", "platform"], unique=False
    )
    op.create_index(
        op.f("ix_oauth_accounts_created_at"),
        "oauth_accounts",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_oauth_accounts_deleted_at"),
        "oauth_accounts",
        ["deleted_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_oauth_accounts_modified_at"),
        "oauth_accounts",
        ["modified_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_oauth_accounts_modified_at"), table_name="oauth_accounts")
    op.drop_index(op.f("ix_oauth_accounts_deleted_at"), table_name="oauth_accounts")
    op.drop_index(op.f("ix_oauth_accounts_created_at"), table_name="oauth_accounts")
    op.drop_index("idx_user_id_platform", table_name="oauth_accounts")
    op.drop_table("oauth_accounts")