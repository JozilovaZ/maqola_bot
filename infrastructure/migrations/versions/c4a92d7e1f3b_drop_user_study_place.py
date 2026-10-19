"""drop user study_place

Revision ID: c4a92d7e1f3b
Revises: b8e41f2c6d7a
Create Date: 2026-10-19 15:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c4a92d7e1f3b'
down_revision: Union[str, None] = 'b8e41f2c6d7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ro'yxatdan o'tishda o'qish/ish joyi endi so'ralmaydi
    op.drop_column('users', 'study_place')


def downgrade() -> None:
    op.add_column('users', sa.Column('study_place', sa.String(length=256), nullable=True))
