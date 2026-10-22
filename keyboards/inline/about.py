from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.callbacks import Nav


def about_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🌟 Nega aynan bizni tanlashadi", callback_data=Nav(to="why"))
    keyboard.button(text="🤝 Qanday ishlaymiz", callback_data=Nav(to="process"))
    keyboard.button(text="❓ Ko‘p beriladigan savollar", callback_data=Nav(to="faq"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def about_next_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="💼 Xizmatni tanlash", callback_data=Nav(to="services"))
    keyboard.button(text="🤝 Hammualliflik uchun mavzularni tanlash", callback_data=Nav(to="coauth"))
    keyboard.button(text="💬 Bepul maslahat olish", callback_data=Nav(to="consult"))
    keyboard.adjust(1)
    return keyboard.as_markup()
