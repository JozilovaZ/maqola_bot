from typing import Optional

from sqlalchemy import func, select, update

from infrastructure.database.models import Article
from infrastructure.database.repo.base import BaseRepo


class ArticleRepo(BaseRepo):
    async def add(self, **values) -> Article:
        article = Article(**values)
        self.session.add(article)
        await self.session.commit()
        await self.session.refresh(article)  # id, created_at, status — bazada qo'yiladi
        return article

    async def get(self, article_id: int) -> Optional[Article]:
        return await self.session.get(Article, article_id)

    async def set_status(self, article_id: int, status: str, by: str, reject_reason: Optional[str] = None) -> None:
        await self.session.execute(
            update(Article).where(Article.id == article_id)
            .values(status=status, reviewed_by=by, reviewed_at=func.now(), reject_reason=reject_reason)
        )
        await self.session.commit()

    async def count_approved_by_direction(self) -> dict[int, int]:
        """{direction_id: joylangan maqolalar soni}"""
        result = await self.session.execute(
            select(Article.direction_id, func.count())
            .where(Article.status == "approved")
            .group_by(Article.direction_id)
        )
        return dict(result.all())

    async def approved(self, direction_id: int, offset: int = 0, limit: Optional[int] = None) -> list[Article]:
        """Foydalanuvchilarga ko'rinadigan maqolalar, yangilari birinchi."""
        query = (
            select(Article).where(Article.status == "approved", Article.direction_id == direction_id)
            .order_by(Article.created_at.desc()).offset(offset).limit(limit)
        )
        return list(await self.session.scalars(query))

    async def by_author(self, author_id: int) -> list[Article]:
        return list(await self.session.scalars(
            select(Article).where(Article.author_id == author_id).order_by(Article.created_at.desc())
        ))

    async def by_status(self, status: str, limit: int = 30) -> list[Article]:
        return list(await self.session.scalars(
            select(Article).where(Article.status == status).order_by(Article.created_at).limit(limit)
        ))

    async def count_by_status(self) -> dict[str, int]:
        result = await self.session.execute(select(Article.status, func.count()).group_by(Article.status))
        return dict(result.all())
