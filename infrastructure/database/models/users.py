from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy import text, BIGINT, Boolean, true
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, TableNameMixin
from .directions import Direction


class User(Base, TimestampMixin, TableNameMixin):

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[Optional[str]] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(String(128))
    active: Mapped[bool] = mapped_column(Boolean, server_default=true())
    language: Mapped[str] = mapped_column(String(10), server_default=text("'en'"))

    # Ro'yxatdan o'tishda foydalanuvchi o'zi kiritgan ma'lumotlar (full_name — Telegram'dagi ism, har safar yangilanadi)
    real_name: Mapped[Optional[str]] = mapped_column(String(128))
    phone: Mapped[Optional[str]] = mapped_column(String(32))
    role: Mapped[Optional[str]] = mapped_column(String(16))  # student, young_scientist, professor — misc.texts.REG_ROLES
    direction_id: Mapped[Optional[int]] = mapped_column(ForeignKey("directions.id", ondelete="SET NULL"), index=True)
    registered_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)  # NULL — hali ro'yxatdan o'tmagan

    direction: Mapped[Optional[Direction]] = relationship(lazy="selectin")

    def __repr__(self):
        return f"<User {self.user_id} {self.username} {self.full_name}>"
