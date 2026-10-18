from aiogram import Bot, Router, types

from config import Config
from misc import texts
from services.notify import forward_to_admins

echo_router = Router()


@echo_router.message()
async def any_message(message: types.Message, bot: Bot, config: Config):
    """
    Bo'limlarga tegishli bo'lmagan har qanday xabar (matn, rasm, fayl, ovozli xabar ...).
    Foydalanuvchiga javob beriladi, xabar esa adminlarga yuboriladi — menejer o'zi bog'lanadi.
    """
    await message.answer(texts.FALLBACK)
    if message.from_user.id not in config.tg_bot.admin_ids:
        await forward_to_admins(bot, config.tg_bot.admin_ids, message)


@echo_router.callback_query()
async def stale_button(call: types.CallbackQuery):
    """Eski yoki noma'lum tugma bosilganda "soat" belgisi aylanib qolmasligi uchun."""
    await call.answer()
