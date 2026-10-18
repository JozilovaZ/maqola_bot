from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.callbacks import Nav


def main_menu_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🎁 Foydali materiallar", callback_data=Nav(to="guides"))
    keyboard.button(text="🏛 Maqolalar akademiyasi haqida", callback_data=Nav(to="about"))
    keyboard.button(text="💬 Bepul maslahat", callback_data=Nav(to="consult"))
    keyboard.button(text="🔎 Scopus’da jurnalni tekshirish", callback_data=Nav(to="scopus"))
    keyboard.button(text="💼 Maqolalar akademiyasi xizmatlari", callback_data=Nav(to="services"))
    keyboard.button(text="🤝 Scopus / Web of Science’da hammualliflik", callback_data=Nav(to="coauth"))
    keyboard.adjust(1)
    return keyboard.as_markup()
