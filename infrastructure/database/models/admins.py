from typing import Optional

from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TableNameMixin, TimestampMixin


class Admin(Base, TimestampMixin, TableNameMixin):
    """Bot orqali (/admins) qo'shilgan admin. .env dagi ADMINS — asosiy adminlar, ular bu jadvalda yo'q."""

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    added_by: Mapped[Optional[int]] = mapped_column(BIGINT)  # qo'shgan adminning Telegram ID'si

    def __repr__(self):
        return f"<Admin {self.user_id}>"
