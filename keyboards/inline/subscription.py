from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.callbacks import CheckSub
from services.subscription import RequiredChat


def subscription_kb(chats: list[RequiredChat]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for chat in chats:
        keyboard.button(text=f"➕ {chat.title}", url=chat.url)
    keyboard.button(text="✅ Tekshirish", callback_data=CheckSub())
    keyboard.adjust(1)
    return keyboard.as_markup()
