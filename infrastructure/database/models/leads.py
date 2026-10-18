from datetime import datetime
from typing import Optional

from sqlalchemy import BIGINT, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TableNameMixin, TimestampMixin, int_pk


class Lead(Base, TimestampMixin, TableNameMixin):
    """Ariza: foydalanuvchi qoldirgan telefon raqam (yoki taklif) va u qaysi bo'limdan kelgani."""

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id", ondelete="CASCADE"))
    phone: Mapped[Optional[str]] = mapped_column(String(32))
    reason: Mapped[str] = mapped_column(String(32))
    details: Mapped[Optional[str]] = mapped_column(Text)

    # Arizaning holati: new, contacted, closed, rejected — admin tugmalar orqali o'zgartiradi
    status: Mapped[str] = mapped_column(String(16), server_default="new")
    status_by: Mapped[Optional[str]] = mapped_column(String(128))  # holatni o'zgartirgan admin ismi
    status_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)

    def __repr__(self):
        return f"<Lead {self.id} {self.user_id} {self.reason} {self.status}>"
