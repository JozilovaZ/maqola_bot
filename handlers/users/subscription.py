from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from config import Config
from handlers.users.start import show_main_menu
from keyboards.inline.callbacks import CheckSub
from keyboards.inline.subscription import subscription_kb
from misc import texts
from services.subscription import get_missing_chats

subscription_router = Router()


@subscription_router.callback_query(CheckSub.filter())
async def check_subscription(call: CallbackQuery, bot: Bot, config: Config):
    missing = await get_missing_chats(bot, call.from_user.id, config.subscription.chat_ids)
    if missing:
        await call.answer(texts.SUBSCRIBE_NOT_YET, show_alert=True)
        # foydalanuvchi bir guruhga qo'shilgan bo'lsa, tugmalarda faqat qolganlari ko'rinsin
        try:
            await call.message.edit_reply_markup(reply_markup=subscription_kb(missing))
        except TelegramBadRequest:
            pass  # tugmalar o'zgarmagan
        return

    await call.answer(texts.SUBSCRIBE_DONE)
    await call.message.delete()
    await show_main_menu(call.message, call.from_user)
