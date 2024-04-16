"""update-user

Revision ID: 000002
Revises: 000001
Create Date: 2024-04-16 22:31:25.764932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '000002'
down_revision: Union[str, None] = '000001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index('ix_users_email', table_name='users')
    op.create_unique_constraint(None, 'users', ['email'])


def downgrade() -> None:
    op.drop_constraint(None, 'users', type_='unique')
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
