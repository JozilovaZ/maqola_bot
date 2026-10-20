"""create directions table

Revision ID: d5f1a8b3c2e9
Revises: c4a92d7e1f3b
Create Date: 2026-10-20 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd5f1a8b3c2e9'
down_revision: Union[str, None] = 'c4a92d7e1f3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('directions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('sort_order', sa.Integer(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    # Ro'yxatdan o'tishdagi 7 ta yo'nalish (tartibi bilan)
    directions = sa.table('directions', sa.column('title', sa.String), sa.column('sort_order', sa.Integer))
    op.bulk_insert(directions, [
        {'title': title, 'sort_order': i}
        for i, title in enumerate([
            '🧬 Tibbiyot va biologiya', '🔭 Aniq va tabiiy fanlar', '📚 Ta’lim va pedagogika',
            '💼 Iqtisodiyot va biznes', '💻 Texnika va IT', '🏛 Ijtimoiy va gumanitar', '🌐 Ko‘p tarmoqli',
        ], start=1)
    ])

    op.add_column('users', sa.Column('direction_id', sa.Integer(), nullable=True))
    op.create_foreign_key('users_direction_id_fkey', 'users', 'directions', ['direction_id'], ['id'], ondelete='SET NULL')
    op.create_index('ix_users_direction_id', 'users', ['direction_id'])

    # Oldin ro'yxatdan o'tganlar: matn bo'yicha yo'nalishga bog'lanadi
    op.execute("UPDATE users SET direction_id = d.id FROM directions d WHERE users.direction = d.title")
    op.drop_column('users', 'direction')


def downgrade() -> None:
    op.add_column('users', sa.Column('direction', sa.String(length=256), nullable=True))
    op.execute("UPDATE users SET direction = d.title FROM directions d WHERE users.direction_id = d.id")
    op.drop_index('ix_users_direction_id', table_name='users')
    op.drop_constraint('users_direction_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'direction_id')
    op.drop_table('directions')
