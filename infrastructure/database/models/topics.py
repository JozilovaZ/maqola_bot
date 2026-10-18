from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, false, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TableNameMixin, TimestampMixin, int_pk


class Field(Base, TableNameMixin):
    """Hammualliflik bilim sohasi (Tibbiyot, Agronomiya, ...)."""

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(128))
    sort_order: Mapped[int] = mapped_column(Integer, server_default="0")

    def __repr__(self):
        return f"<Field {self.id} {self.title}>"


class Topic(Base, TimestampMixin, TableNameMixin):
    """Hammualliflik mavzusi: "Scopus Q3 | <nom>" va muallif o'rinlari."""

    id: Mapped[int_pk]
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id", ondelete="CASCADE"))
    base: Mapped[str] = mapped_column(String(64))  # masalan: "Scopus Q3", "Web of Science Q4"
    title: Mapped[str] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, server_default=true())

    slots: Mapped[list["TopicSlot"]] = relationship(
        back_populates="topic",
        order_by="TopicSlot.position",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def free_slots(self) -> int:
        return sum(not slot.sold for slot in self.slots)

    def __repr__(self):
        return f"<Topic {self.id} {self.base} {self.title[:30]}>"


class TopicSlot(Base):
    """Mavzudagi bitta muallif o'rni: tartib raqami, narxi ($) va sotilganmi."""

    __tablename__ = "topic_slots"

    id: Mapped[int_pk]
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"))
    position: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    sold: Mapped[bool] = mapped_column(Boolean, server_default=false())

    topic: Mapped[Topic] = relationship(back_populates="slots")
