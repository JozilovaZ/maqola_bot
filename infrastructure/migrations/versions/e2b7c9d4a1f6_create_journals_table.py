"""create journals table

Revision ID: e2b7c9d4a1f6
Revises: d5f1a8b3c2e9
Create Date: 2026-10-20 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e2b7c9d4a1f6'
down_revision: Union[str, None] = 'd5f1a8b3c2e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('journals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('direction_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('base', sa.String(length=64), nullable=False),
    sa.Column('url', sa.String(length=512), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['direction_id'], ['directions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_journals_direction_id', 'journals', ['direction_id'])


def downgrade() -> None:
    op.drop_index('ix_journals_direction_id', table_name='journals')
    op.drop_table('journals')
