from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.callbacks import Nav


def main_menu_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🏛 Fihria Academic haqida", callback_data=Nav(to="about"))
    keyboard.button(text="💼 Xizmatlar", callback_data=Nav(to="services"))
    keyboard.button(text="💬 Bepul maslahat", callback_data=Nav(to="consult"))
    keyboard.button(text="🔎 Scopus’da jurnalni tekshirish", callback_data=Nav(to="scopus"))
    keyboard.button(text="📚 Jurnallar javoni", callback_data=Nav(to="journals"))
    keyboard.button(text="🧾 Plagiatga tekshirish", callback_data=Nav(to="plagiat"))
    keyboard.button(text="🤝 Hammualliflik", callback_data=Nav(to="coauth"))
    keyboard.button(text="❓ Savollar", callback_data=Nav(to="faq"))
    keyboard.button(text="✍️ Matn bilan ishlash", callback_data=Nav(to="text_tools"))
    keyboard.adjust(1, 2, 1, 2, 2, 1)
    return keyboard.as_markup()
