"""CAJMNS journal details from its site

Revision ID: f6b2d4e8a1c3
Revises: e5a1c3f7b9d2
Create Date: 2026-10-23 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f6b2d4e8a1c3'
down_revision: Union[str, None] = 'e5a1c3f7b9d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TITLE = 'Central Asian Journal of Medical and Natural Science'
OLD_BASE = 'Jurnal'
OLD_DESCRIPTION = '🔤 Qisqartma: CAJMNS\n🌍 Toifa: Xalqaro nashr'
# cajmns.casjournal.org saytidagi ma'lumotlar (2026-10-23)
NEW_BASE = 'Jurnal · ISSN 2660-4159'
NEW_DESCRIPTION = (
    'Tibbiyot, farmakologiya va tabiiy fanlar boʻyicha taqrizlanadigan, ochiq kirishli xalqaro jurnal. '
    'Ilmiy va sharh maqolalar, klinik holatlar, qisqa xabarlar, kitob taqrizlari, '
    'texnologik hisobotlar va fikr-mulohaza maqolalari qabul qilinadi.\n\n'
    '🔤 Qisqartma: CAJMNS\n'
    '🌍 Toifa: Xalqaro nashr\n'
    '🏢 Nashriyot: Central Asian Studies (Ispaniya)\n'
    '🗓 Davriylik: Choraklik (yanvar, aprel, iyul, oktyabr)\n'
    '📊 Indeksatsiya: Google Scholar, Index Copernicus, PKP Index, Scilit\n'
    '🔓 Litsenziya: ochiq kirish, CC BY 4.0'
)

journals = sa.table(
    'journals', sa.column('title', sa.Text), sa.column('base', sa.String), sa.column('description', sa.Text),
)


def upgrade() -> None:
    op.execute(journals.update().where(journals.c.title == TITLE, journals.c.base == OLD_BASE).values(base=NEW_BASE))
    # Admin /shelf orqali o'zi yozgan bo'lsa — tegmaymiz
    op.execute(
        journals.update()
        .where(journals.c.title == TITLE, sa.or_(journals.c.description.is_(None), journals.c.description == OLD_DESCRIPTION))
        .values(description=NEW_DESCRIPTION)
    )


def downgrade() -> None:
    op.execute(journals.update().where(journals.c.title == TITLE, journals.c.base == NEW_BASE).values(base=OLD_BASE))
    op.execute(
        journals.update()
        .where(journals.c.title == TITLE, journals.c.description == NEW_DESCRIPTION)
        .values(description=OLD_DESCRIPTION)
    )
