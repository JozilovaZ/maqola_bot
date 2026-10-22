from typing import Optional

from sqlalchemy import delete, func, select, update

from infrastructure.database.models import Journal
from infrastructure.database.repo.base import BaseRepo


class JournalRepo(BaseRepo):
    async def count_by_direction(self) -> dict[int, int]:
        """{direction_id: jurnallar soni}"""
        result = await self.session.execute(
            select(Journal.direction_id, func.count()).group_by(Journal.direction_id)
        )
        return dict(result.all())

    async def direction_journals(self, direction_id: int, offset: int = 0, limit: Optional[int] = None) -> list[Journal]:
        query = (
            select(Journal).where(Journal.direction_id == direction_id)
            .order_by(Journal.base, Journal.title).offset(offset).limit(limit)
        )
        return list(await self.session.scalars(query))

    async def get(self, journal_id: int) -> Optional[Journal]:
        return await self.session.get(Journal, journal_id)

    async def add(
        self, direction_id: int, title: str, base: str, url: Optional[str], description: Optional[str] = None
    ) -> Journal:
        journal = Journal(direction_id=direction_id, title=title, base=base, url=url, description=description)
        self.session.add(journal)
        await self.session.commit()
        await self.session.refresh(journal)
        return journal

    async def update(self, journal_id: int, **values) -> None:
        await self.session.execute(update(Journal).where(Journal.id == journal_id).values(**values))
        await self.session.commit()

    async def delete(self, journal_id: int) -> None:
        await self.session.execute(delete(Journal).where(Journal.id == journal_id))
        await self.session.commit()
