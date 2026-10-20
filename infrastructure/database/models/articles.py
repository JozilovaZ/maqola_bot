from datetime import datetime
from typing import Optional

from sqlalchemy import BIGINT, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin, TimestampMixin, int_pk
from .directions import Direction


class Article(Base, TimestampMixin, TableNameMixin):
    """Hammualliflik uchun foydalanuvchi yuborgan maqola. Admin tasdiqlagach, boshqalar ko'radi.

    Boshqa foydalanuvchilarga faqat sarlavha, annotatsiya, baza va o'rinlar soni ko'rinadi;
    fayl va muallif — faqat adminlarga.
    """

    id: Mapped[int_pk]
    author_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    direction_id: Mapped[Optional[int]] = mapped_column(ForeignKey("directions.id", ondelete="SET NULL"), index=True)
    base: Mapped[str] = mapped_column(String(64))  # Scopus, Web of Science, OAK, Boshqa
    title: Mapped[str] = mapped_column(Text)
    annotation: Mapped[str] = mapped_column(Text)
    slots: Mapped[int] = mapped_column(Integer)  # nechta hammuallif kerak (= len(prices))
    prices: Mapped[Optional[list[int]]] = mapped_column(ARRAY(Integer))  # har bir o'rin narxi ($); NULL — kelishiladi
    file_id: Mapped[str] = mapped_column(String(256))
    file_name: Mapped[Optional[str]] = mapped_column(String(256))

    # pending — ko'rib chiqilmoqda, approved — joylangan, rejected — rad etilgan, closed — o'rinlar to'lgan
    status: Mapped[str] = mapped_column(String(16), server_default="pending")
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(128))  # holatni o'zgartirgan admin ismi
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
    reject_reason: Mapped[Optional[str]] = mapped_column(Text)

    direction: Mapped[Optional[Direction]] = relationship(lazy="selectin")

    def __repr__(self):
        return f"<Article {self.id} {self.status} {self.title[:30]}>"
