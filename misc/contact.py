from html import escape
from typing import Optional

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import Config
from infrastructure.database.models import User
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.default.contact import share_contact_kb
from misc import texts
from services.notify import notify_new_lead


async def ask_contact(message: Message, state: FSMContext, text: str, reason: str, details: str | None = None):
    """Telefon raqamini so'rash: matn + alohida "⬇️" xabari "Kontaktni ulashish" tugmasi bilan.

    reason — raqam qaysi bo'limdan qoldirilgani (consult, order, ...), details — qo'shimcha ma'lumot
    (masalan, xizmat nomi). Ikkalasi FSM'da saqlanadi va raqam kelganda arizaga yoziladi.
    """
    await state.update_data(reason=reason, details=details)
    await message.answer(text)
    await message.answer(texts.CONTACT_ARROW, reply_markup=share_contact_kb())


async def request_lead(
    message: Message,
    state: FSMContext,
    user: User,
    repo: RequestsRepo,
    bot: Bot,
    config: Config,
    text: str,
    reason: str,
    details: Optional[str] = None,
):
    """Ariza qoldirish. Ro'yxatdan o'tishda olingan raqam bazada bor — ariza darhol adminlarga yuboriladi,
    raqam qayta so'ralmaydi. Raqam yo'q bo'lsa (ro'yxatdan o'tmagan admin) — eskicha, ask_contact() orqali.
    """
    if not user.phone:
        await ask_contact(message, state, text, reason, details)
        return
    lead = await repo.leads.add_lead(user.user_id, reason, phone=user.phone, details=details)
    await repo.session.refresh(user, ["direction"])
    await notify_new_lead(bot, config.tg_bot.admin_ids, lead, user.full_name, user.username, profile=user)
    tail = texts.CONTACT_TAILS.get(reason, texts.CONTACT_TAILS["consult"])
    await message.answer(texts.LEAD_THANKS.format(
        name=escape(user.real_name or user.full_name), phone=escape(user.phone), tail=tail,
    ))
