"""create articles table

Revision ID: f3c8d2e5b7a4
Revises: e2b7c9d4a1f6
Create Date: 2026-10-20 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f3c8d2e5b7a4'
down_revision: Union[str, None] = 'e2b7c9d4a1f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.BIGINT(), nullable=False),
    sa.Column('direction_id', sa.Integer(), nullable=True),
    sa.Column('base', sa.String(length=64), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('annotation', sa.Text(), nullable=False),
    sa.Column('slots', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.String(length=256), nullable=False),
    sa.Column('file_name', sa.String(length=256), nullable=True),
    sa.Column('status', sa.String(length=16), server_default='pending', nullable=False),
    sa.Column('reviewed_by', sa.String(length=128), nullable=True),
    sa.Column('reviewed_at', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('reject_reason', sa.Text(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['direction_id'], ['directions.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_articles_author_id', 'articles', ['author_id'])
    op.create_index('ix_articles_direction_id', 'articles', ['direction_id'])


def downgrade() -> None:
    op.drop_index('ix_articles_direction_id', table_name='articles')
    op.drop_index('ix_articles_author_id', table_name='articles')
    op.drop_table('articles')
