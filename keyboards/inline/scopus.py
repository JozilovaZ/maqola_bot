from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.callbacks import Nav


def scopus_intro_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔎 Scopus’da jurnalni tekshirish", callback_data=Nav(to="scopus_start"))
    return keyboard.as_markup()


def scopus_found_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Maqola auditi", callback_data=Nav(to="scopus_audit"))
    keyboard.button(text="Boshqa jurnalni tekshirish", callback_data=Nav(to="scopus_start"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def scopus_not_found_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Raqam qoldirish", callback_data=Nav(to="scopus_manual"))
    keyboard.button(text="Boshqa jurnalni tekshirish", callback_data=Nav(to="scopus_start"))
    keyboard.adjust(1)
    return keyboard.as_markup()
