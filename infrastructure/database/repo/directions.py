from typing import Optional

from sqlalchemy import delete, func, select, update

from infrastructure.database.models import Direction
from infrastructure.database.repo.base import BaseRepo


class DirectionRepo(BaseRepo):
    async def list_all(self) -> list[Direction]:
        result = await self.session.scalars(select(Direction).order_by(Direction.sort_order, Direction.id))
        return list(result)

    async def get(self, direction_id: int) -> Optional[Direction]:
        return await self.session.get(Direction, direction_id)

    async def get_by_title(self, title: str) -> Optional[Direction]:
        """Ro'yxatdan o'tishda bosilgan tugma matni bo'yicha."""
        return await self.session.scalar(select(Direction).where(Direction.title == title))

    async def add(self, title: str) -> Direction:
        last = await self.session.scalar(select(func.max(Direction.sort_order)))
        direction = Direction(title=title, sort_order=(last or 0) + 1)
        self.session.add(direction)
        await self.session.commit()
        return direction

    async def rename(self, direction_id: int, title: str) -> None:
        await self.session.execute(update(Direction).where(Direction.id == direction_id).values(title=title))
        await self.session.commit()

    async def delete(self, direction_id: int) -> None:
        """Yo'nalishdagi jurnallar o'chadi (CASCADE), foydalanuvchi va maqolalarda yo'nalish bo'sh qoladi (SET NULL)."""
        await self.session.execute(delete(Direction).where(Direction.id == direction_id))
        await self.session.commit()
