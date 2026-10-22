from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.callbacks import Nav, Order, Service

SERVICE_BUTTONS = {
    "scopus": "📝 Scopus’da maqola chop etish",
    "wos": "📝 Web of Science’da maqola chop etish",
    "oak": "🎓 OAK jurnallarida maqola chop etish",
    "diss": "📚 Dissertatsiyalar bo‘yicha xizmatlar",
    "hirsh": "📈 Ilmiy profil va Hirsh indeksi",
    "conf": "🎤 Konferensiya tezislarini chop etish",
    "edit": "✏️ Maqolani tahrirlash",
    "translate": "🌐 Maqolani tarjima qilish",
    "board": "🏅 Tahririyatga a’zolik",
    "isbn": "📕 ISBN va DOI olish",
    "ehm": "💾 EHM dasturi guvohnomasi",
}


def services_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for key, text in SERVICE_BUTTONS.items():
        keyboard.button(text=text, callback_data=Service(key=key))
    keyboard.adjust(1)
    return keyboard.as_markup()


def service_kb(key: str, url: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🛒 Xizmatga buyurtma berish", callback_data=Order(key=key))
    keyboard.button(text="💬 Bepul maslahat olish", callback_data=Nav(to="consult"))
    if url:
        keyboard.button(text="ℹ️ Xizmat haqida batafsil", web_app=WebAppInfo(url=url))
    keyboard.adjust(1)
    return keyboard.as_markup()
