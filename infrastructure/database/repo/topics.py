from typing import Optional

from sqlalchemy import delete, func, select, update

from infrastructure.database.models import Field, Topic, TopicSlot
from infrastructure.database.repo.base import BaseRepo


class TopicRepo(BaseRepo):
    async def list_fields(self) -> list[Field]:
        result = await self.session.scalars(select(Field).order_by(Field.sort_order, Field.id))
        return list(result)

    async def get_field(self, field_id: int) -> Optional[Field]:
        return await self.session.get(Field, field_id)

    async def count_by_field(self) -> dict[int, int]:
        """{field_id: faol mavzular soni}"""
        result = await self.session.execute(
            select(Topic.field_id, func.count()).where(Topic.active).group_by(Topic.field_id)
        )
        return dict(result.all())

    async def field_topics(
        self, field_id: int, offset: int = 0, limit: Optional[int] = None, include_hidden: bool = False
    ) -> list[Topic]:
        """Sohadagi mavzular. include_hidden — admin uchun yashirilganlarini ham ko'rsatish."""
        query = select(Topic).where(Topic.field_id == field_id).order_by(Topic.id).offset(offset).limit(limit)
        if not include_hidden:
            query = query.where(Topic.active)
        return list(await self.session.scalars(query))

    async def update_topic(self, topic_id: int, **values) -> None:
        """base, title yoki active ni o'zgartirish."""
        await self.session.execute(update(Topic).where(Topic.id == topic_id).values(**values))
        await self.session.commit()

    async def set_prices(self, topic_id: int, prices: list[int]) -> None:
        """Narxlarni almashtirish. O'rinlar soni o'zgarishi mumkin; mavjud o'rinlarning "sotilgan" belgisi saqlanadi."""
        topic = await self.get_topic(topic_id)
        sold = {slot.position: slot.sold for slot in topic.slots}
        topic.slots = [
            TopicSlot(position=i, price=price, sold=sold.get(i, False)) for i, price in enumerate(prices, start=1)
        ]
        await self.session.commit()

    # ---------- Sohalar ----------

    async def add_field(self, title: str) -> Field:
        last = await self.session.scalar(select(func.max(Field.sort_order)))
        field = Field(title=title, sort_order=(last or 0) + 1)
        self.session.add(field)
        await self.session.commit()
        return field

    async def rename_field(self, field_id: int, title: str) -> None:
        await self.session.execute(update(Field).where(Field.id == field_id).values(title=title))
        await self.session.commit()

    async def delete_field(self, field_id: int) -> None:
        """Soha va undagi barcha mavzular o'chadi (CASCADE)."""
        await self.session.execute(delete(Field).where(Field.id == field_id))
        await self.session.commit()

    async def get_topic(self, topic_id: int) -> Optional[Topic]:
        return await self.session.get(Topic, topic_id)

    async def add_topic(self, field_id: int, base: str, title: str, prices: list[int]) -> Topic:
        topic = Topic(
            field_id=field_id,
            base=base,
            title=title,
            slots=[TopicSlot(position=i, price=price) for i, price in enumerate(prices, start=1)],
        )
        self.session.add(topic)
        await self.session.commit()
        return topic

    async def toggle_slot(self, slot_id: int) -> Optional[TopicSlot]:
        slot = await self.session.get(TopicSlot, slot_id)
        if slot is None:
            return None
        slot.sold = not slot.sold
        await self.session.commit()
        return slot

    async def delete_topic(self, topic_id: int) -> None:
        await self.session.execute(delete(Topic).where(Topic.id == topic_id))
        await self.session.commit()
