from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TableNameMixin, TimestampMixin, int_pk


class Journal(Base, TimestampMixin, TableNameMixin):
    """«Jurnallar javoni»: admin qo'shgan jurnal. Foydalanuvchilar yo'nalish bo'yicha ko'radi."""

    id: Mapped[int_pk]
    direction_id: Mapped[int] = mapped_column(ForeignKey("directions.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(Text)
    base: Mapped[str] = mapped_column(String(64))  # masalan: "Scopus Q3", "Web of Science", "OAK"
    url: Mapped[Optional[str]] = mapped_column(String(512))  # jurnal sayti (ixtiyoriy)
    description: Mapped[Optional[str]] = mapped_column(Text)  # foydalanuvchiga ko'rinadigan qisqa ma'lumot

    def __repr__(self):
        return f"<Journal {self.id} {self.base} {self.title[:30]}>"
