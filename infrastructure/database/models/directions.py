from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TableNameMixin, int_pk


class Direction(Base, TableNameMixin):
    """Ro'yxatdan o'tishdagi yo'nalish (Tibbiyot va biologiya, Texnika va IT, ...). Har bir foydalanuvchi bittasiga tegishli."""

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(128))  # tugma matni, emoji bilan
    sort_order: Mapped[int] = mapped_column(Integer, server_default="0")

    @property
    def name(self) -> str:
        """Emojisiz nomi (Excel varag'i uchun): "🧬 Tibbiyot va biologiya" -> "Tibbiyot va biologiya"."""
        return self.title.split(" ", 1)[-1]

    def __repr__(self):
        return f"<Direction {self.id} {self.title}>"
