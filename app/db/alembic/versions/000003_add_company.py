"""add_company

Revision ID: 000003
Revises: 000002
Create Date: 2024-04-30 07:41:15.015272

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "000003"
down_revision: Union[str, None] = "000002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.Column("is_hidden", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("companies")
