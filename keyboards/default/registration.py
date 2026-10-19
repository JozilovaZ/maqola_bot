from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from misc import texts


def role_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    for title in texts.REG_ROLES.values():
        keyboard.button(text=title)
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)


def choice_kb(options: list[str], other: str, columns: int) -> ReplyKeyboardMarkup:
    """Variantlar + oxirida alohida qatorda "Boshqa" (qo'lda yozish) tugmasi."""
    keyboard = ReplyKeyboardBuilder()
    for title in options:
        keyboard.button(text=title)
    keyboard.adjust(columns)
    keyboard.row(KeyboardButton(text=other))
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)


def university_kb() -> ReplyKeyboardMarkup:
    return choice_kb(texts.REG_UNIVERSITIES, texts.REG_UNIVERSITY_OTHER, columns=3)


def direction_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    for title in texts.REG_DIRECTIONS:
        keyboard.button(text=title)
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)
