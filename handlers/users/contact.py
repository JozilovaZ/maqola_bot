from html import escape

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import Config
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.default.contact import share_contact_kb
from misc import texts
from services.notify import notify_new_lead

contact_router = Router()


@contact_router.message(F.contact)
async def get_contact(message: Message, state: FSMContext, bot: Bot, config: Config, repo: RequestsRepo):
    user = message.from_user
    if message.contact.user_id != user.id:
        await message.answer(texts.CONTACT_NOT_OWN, reply_markup=share_contact_kb())
        return

    phone = message.contact.phone_number
    if not phone.startswith("+"):
        phone = f"+{phone}"

    # ask_contact() saqlagan: raqam qaysi bo'limdan va qaysi xizmat uchun
    data = await state.get_data()
    reason = data.get("reason", "consult")
    details = data.get("details")
    await state.clear()

    lead = await repo.leads.add_lead(user.id, reason, phone=phone, details=details)
    await notify_new_lead(bot, config.tg_bot.admin_ids, lead, user.full_name, user.username)

    tail = texts.CONTACT_TAILS.get(reason, texts.CONTACT_TAILS["consult"])
    await message.answer(
        texts.CONTACT_THANKS.format(name=escape(user.full_name), tail=tail),
        reply_markup=ReplyKeyboardRemove(),
    )
