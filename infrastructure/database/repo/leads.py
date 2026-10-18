from typing import Optional

from sqlalchemy import func, select, update

from infrastructure.database.models import Lead, User
from infrastructure.database.repo.base import BaseRepo


class LeadRepo(BaseRepo):
    async def add_lead(
        self,
        user_id: int,
        reason: str,
        phone: Optional[str] = None,
        details: Optional[str] = None,
    ) -> Lead:
        lead = Lead(user_id=user_id, reason=reason, phone=phone, details=details)
        self.session.add(lead)
        await self.session.commit()
        await self.session.refresh(lead)  # created_at, status — bazada qo'yiladi
        return lead

    async def get_with_user(self, lead_id: int) -> Optional[tuple[Lead, User]]:
        row = (await self.session.execute(
            select(Lead, User).join(User, User.user_id == Lead.user_id).where(Lead.id == lead_id)
        )).first()
        return tuple(row) if row else None

    async def set_status(self, lead_id: int, status: str, by: str) -> None:
        await self.session.execute(
            update(Lead).where(Lead.id == lead_id).values(status=status, status_by=by, status_at=func.now())
        )
        await self.session.commit()

    async def list_with_users(self, open_only: bool = False, limit: Optional[int] = None) -> list[tuple[Lead, User]]:
        """Arizalar (yangilari birinchi). open_only — faqat yangi va bog'lanilgan (yopilmagan) arizalar."""
        query = select(Lead, User).join(User, User.user_id == Lead.user_id).order_by(Lead.id.desc()).limit(limit)
        if open_only:
            query = query.where(Lead.status.in_(["new", "contacted"]))
        return [tuple(row) for row in (await self.session.execute(query)).all()]

    async def stats(self) -> dict:
        """Telefon raqamli arizalar: jami, bugun, bo'limlar bo'yicha; hamda mavzu takliflari soni."""
        with_phone = Lead.phone.is_not(None)
        today = func.date(Lead.created_at) == func.current_date()
        total, today_count, suggestions = (await self.session.execute(
            select(
                func.count().filter(with_phone),
                func.count().filter(with_phone, today),
                func.count().filter(Lead.reason == "suggest"),
            )
        )).one()
        by_reason = dict((await self.session.execute(
            select(Lead.reason, func.count()).where(with_phone).group_by(Lead.reason).order_by(func.count().desc())
        )).all())
        return {"total": total, "today": today_count, "suggestions": suggestions, "by_reason": by_reason}
