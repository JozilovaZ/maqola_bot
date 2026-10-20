from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from infrastructure.database.models import Article, Direction
from keyboards.inline.callbacks import AdminArticle, ArticleApply, ArticleBrowse, ArticleForm, Nav
from misc.articles import BASES

# ---------- Maqola yuborish ----------

def cancel_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(text="❌ Bekor qilish", callback_data=ArticleForm(field="cancel").pack())


def article_cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[cancel_button()]])


def article_directions_kb(directions: list[Direction]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for direction in directions:
        keyboard.button(text=direction.title, callback_data=ArticleForm(field="direction", value=direction.id))
    keyboard.adjust(1)
    keyboard.row(cancel_button())
    return keyboard.as_markup()


def article_bases_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for index, base in enumerate(BASES):
        keyboard.button(text=base, callback_data=ArticleForm(field="base", value=index))
    keyboard.adjust(2)
    keyboard.row(cancel_button())
    return keyboard.as_markup()


def article_confirm_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✅ Yuborish", callback_data=ArticleForm(field="send"))
    keyboard.button(text="❌ Bekor qilish", callback_data=ArticleForm(field="cancel"))
    keyboard.adjust(2)
    return keyboard.as_markup()


# ---------- Maqolalarni ko'rish ----------

def browse_directions_kb(directions: list[Direction], counts: dict[int, int]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for direction in directions:
        keyboard.button(
            text=f"{direction.title} ({counts.get(direction.id, 0)})",
            callback_data=ArticleBrowse(direction_id=direction.id),
        )
    keyboard.button(text="⬅️ Hammualliflik", callback_data=Nav(to="coauth"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def browse_page_kb(direction_id: int, page: int, articles: list[Article], has_next: bool) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for article in articles:
        keyboard.button(text=f"🤝 #{article.id} — hammuallif bo‘lish", callback_data=ArticleApply(id=article.id))
    keyboard.adjust(1)
    navigation = []
    if page > 0:
        navigation.append(InlineKeyboardButton(
            text="⬅️ Oldingi", callback_data=ArticleBrowse(direction_id=direction_id, page=page - 1).pack()
        ))
    if has_next:
        navigation.append(InlineKeyboardButton(
            text="Keyingi ➡️", callback_data=ArticleBrowse(direction_id=direction_id, page=page + 1).pack()
        ))
    if navigation:
        keyboard.row(*navigation)
    keyboard.row(InlineKeyboardButton(text="📖 Yo‘nalishlar", callback_data=Nav(to="articles").pack()))
    return keyboard.as_markup()


def announce_kb(article: Article) -> InlineKeyboardMarkup:
    """Yangi maqola haqidagi xabar ostida."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🤝 Hammuallif bo‘lish", callback_data=ArticleApply(id=article.id))
    keyboard.button(
        text="📖 Yo‘nalishdagi boshqa maqolalar", callback_data=ArticleBrowse(direction_id=article.direction_id or 0)
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


# ---------- Admin ----------

def admin_article_kb(article: Article) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    if article.status == "pending":
        keyboard.button(text="✅ Tasdiqlash", callback_data=AdminArticle(action="approve", id=article.id))
        keyboard.button(text="❌ Rad etish", callback_data=AdminArticle(action="reject", id=article.id))
    elif article.status == "approved":
        keyboard.button(text="🔒 Yopish (o‘rinlar to‘ldi)", callback_data=AdminArticle(action="close", id=article.id))
        keyboard.button(text="❌ Rad etish", callback_data=AdminArticle(action="reject", id=article.id))
    else:
        keyboard.button(text="✅ Qayta joylash", callback_data=AdminArticle(action="approve", id=article.id))
    keyboard.button(text="💲 Narxlarni o‘zgartirish", callback_data=AdminArticle(action="prices", id=article.id))
    keyboard.adjust(1)
    return keyboard.as_markup()
