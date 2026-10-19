from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from misc import texts


def role_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    for title in texts.REG_ROLES.values():
        keyboard.button(text=title)
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)


def direction_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    for title in texts.REG_DIRECTIONS:
        keyboard.button(text=title)
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)
