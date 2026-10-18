from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def share_contact_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Kontaktni ulashish", request_contact=True)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)
