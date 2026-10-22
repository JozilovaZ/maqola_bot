"""create admins table

Revision ID: d8f4b2a6e1c3
Revises: c7e3a9f1d2b5
Create Date: 2026-10-22 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd8f4b2a6e1c3'
down_revision: Union[str, None] = 'c7e3a9f1d2b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # /admins orqali qo'shilgan adminlar (.env dagi ADMINS bu yerda saqlanmaydi)
    op.create_table(
        'admins',
        sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column('added_by', sa.BIGINT(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
    )


def downgrade() -> None:
    op.drop_table('admins')
