from aiogram.types import KeyboardButtonRequestUsers, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# KeyboardButtonRequestUsers so'rovining raqami: javobda (users_shared) qaytadi
REQUEST_ADMIN_ID = 1


def pick_admin_kb() -> ReplyKeyboardMarkup:
    """Telegram kontaktlar ro'yxatidan foydalanuvchini tanlash tugmasi."""
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text="👤 Foydalanuvchini tanlash",
        request_users=KeyboardButtonRequestUsers(request_id=REQUEST_ADMIN_ID, user_is_bot=False, max_quantity=1),
    )
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)
