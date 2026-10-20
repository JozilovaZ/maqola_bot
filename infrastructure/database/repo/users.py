from typing import Optional

from sqlalchemy import func, select, text, update
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import User
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        user_id: int,
        full_name: str,
        language: str,
        username: Optional[str] = None,
    ):
        """
        Creates or updates a new user in the database and returns the user object.
        :param user_id: The user's ID.
        :param full_name: The user's full name.
        :param language: The user's language.
        :param username: The user's username. It's an optional parameter.
        :return: User object, None if there was an error while making a transaction.
        """

        insert_stmt = (
            insert(User)
            .values(
                user_id=user_id,
                username=username,
                full_name=full_name,
                # Telegram tilni har doim ham bermaydi, ustun esa NULL qabul qilmaydi
                language=language or "en",
            )
            .on_conflict_do_update(
                index_elements=[User.user_id],
                set_=dict(
                    username=username,
                    full_name=full_name,
                    # Botni bloklab, keyin yana yozgan foydalanuvchi rassilkaga qaytadi
                    active=True,
                ),
            )
            .returning(User)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()

    async def register(
        self, user_id: int, real_name: str, phone: str, role: str, direction_id: int
    ) -> User:
        """Ro'yxatdan o'tish ma'lumotlarini saqlash."""
        user = await self.session.get(User, user_id)
        user.real_name = real_name
        user.phone = phone
        user.role = role
        user.direction_id = direction_id
        user.registered_at = func.now()
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def registered(self) -> list[User]:
        """/export uchun: ro'yxatdan o'tgan foydalanuvchilar, yangilari birinchi."""
        return list(await self.session.scalars(
            select(User).where(User.registered_at.is_not(None)).order_by(User.registered_at.desc())
        ))

    async def active_ids(self, direction_id: Optional[int] = None) -> list[int]:
        """Rassilka uchun: botni bloklamagan foydalanuvchilar; direction_id berilsa — faqat shu yo'nalishdagilar."""
        query = select(User.user_id).where(User.active)
        if direction_id is not None:
            query = query.where(User.direction_id == direction_id)
        return list(await self.session.scalars(query))

    async def count_active_by_direction(self) -> dict[int, int]:
        """{direction_id: botni bloklamagan foydalanuvchilar soni} — rassilka tugmalari uchun."""
        result = await self.session.execute(
            select(User.direction_id, func.count())
            .where(User.active, User.direction_id.is_not(None))
            .group_by(User.direction_id)
        )
        return dict(result.all())

    async def set_inactive(self, user_ids: list[int]) -> None:
        """Botni bloklagan (xabar yetib bormagan) foydalanuvchilarni belgilash."""
        if user_ids:
            await self.session.execute(update(User).where(User.user_id.in_(user_ids)).values(active=False))
            await self.session.commit()

    async def stats(self) -> dict[str, int]:
        today = func.date(User.created_at) == func.current_date()
        week = User.created_at >= func.now() - text("interval '7 days'")
        row = (await self.session.execute(
            select(
                func.count(),
                func.count().filter(today),
                func.count().filter(week),
                func.count().filter(User.active.is_(False)),
                func.count().filter(User.registered_at.is_not(None)),
            )
        )).one()
        return {"total": row[0], "today": row[1], "week": row[2], "blocked": row[3], "registered": row[4]}
