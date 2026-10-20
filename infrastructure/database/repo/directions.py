from typing import Optional

from sqlalchemy import select

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
