"""add user registration

Revision ID: b8e41f2c6d7a
Revises: 3cd39969fa39
Create Date: 2026-10-19 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b8e41f2c6d7a'
down_revision: Union[str, None] = '3cd39969fa39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('real_name', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('phone', sa.String(length=32), nullable=True))
    op.add_column('users', sa.Column('role', sa.String(length=16), nullable=True))
    op.add_column('users', sa.Column('study_place', sa.String(length=256), nullable=True))
    op.add_column('users', sa.Column('direction', sa.String(length=256), nullable=True))
    op.add_column('users', sa.Column('registered_at', postgresql.TIMESTAMP(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'registered_at')
    op.drop_column('users', 'direction')
    op.drop_column('users', 'study_place')
    op.drop_column('users', 'role')
    op.drop_column('users', 'phone')
    op.drop_column('users', 'real_name')
