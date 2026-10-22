"""add journal description

Revision ID: c7e3a9f1d2b5
Revises: b9e2f4a6c8d1
Create Date: 2026-10-22 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c7e3a9f1d2b5'
down_revision: Union[str, None] = 'b9e2f4a6c8d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Jurnal kartochkasidagi qisqa ma'lumot. Oldin qo'shilgan jurnallarda — NULL (admin /shelf orqali to'ldiradi)
    op.add_column('journals', sa.Column('description', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('journals', 'description')
