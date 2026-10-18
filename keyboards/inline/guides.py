from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.callbacks import Checklist, Nav

CHECKLIST_BUTTONS = {
    "phd": "📁 PhD himoyasi uchun hujjatlar checklisti",
    "rejected": "📘 Maqola rad etilgandan keyingi 5 qadam",
    "reply": "📝 Taqrizchi izohlariga javob xati checklisti",
    "redflags": "🔎 Scopus jurnalini tanlash: 7 ta xavf belgisi",
}


def guides_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✅ Chek-listlar", callback_data=Nav(to="checklists"))
    keyboard.button(text="📝 Blog maqolalari", callback_data=Nav(to="blog"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def checklists_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for key, text in CHECKLIST_BUTTONS.items():
        keyboard.button(text=text, callback_data=Checklist(key=key))
    keyboard.adjust(1)
    return keyboard.as_markup()


def blog_kb(url: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    if url:
        keyboard.button(text="📚 Maqolalar katalogini ochish", web_app=WebAppInfo(url=url))
    keyboard.button(text="🏠 Bosh menyuga qaytish", callback_data=Nav(to="main"))
    keyboard.adjust(1)
    return keyboard.as_markup()
