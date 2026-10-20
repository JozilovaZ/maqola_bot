"""add article prices

Revision ID: a7d4e1f9c3b2
Revises: f3c8d2e5b7a4
Create Date: 2026-10-20 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a7d4e1f9c3b2'
down_revision: Union[str, None] = 'f3c8d2e5b7a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Har bir hammuallif o'rnining narxi ($), 1-o'rindan boshlab. Oldin yuborilgan maqolalarda — NULL (kelishiladi)
    op.add_column('articles', sa.Column('prices', postgresql.ARRAY(sa.Integer()), nullable=True))


def downgrade() -> None:
    op.drop_column('articles', 'prices')
