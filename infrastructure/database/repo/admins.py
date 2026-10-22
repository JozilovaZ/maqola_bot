from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import Admin
from infrastructure.database.repo.base import BaseRepo


class AdminRepo(BaseRepo):
    async def list_ids(self) -> list[int]:
        return list(await self.session.scalars(select(Admin.user_id).order_by(Admin.created_at)))

    async def add(self, user_id: int, added_by: int) -> None:
        await self.session.execute(
            insert(Admin).values(user_id=user_id, added_by=added_by).on_conflict_do_nothing()
        )
        await self.session.commit()

    async def remove(self, user_id: int) -> None:
        await self.session.execute(delete(Admin).where(Admin.user_id == user_id))
        await self.session.commit()
