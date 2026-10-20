from html import escape
from typing import Optional

from infrastructure.database.models import Article, User
from misc.texts import REG_ROLES
from services.notify import REPLY_HINT, fmt_time, format_user

# Maqola mo'ljallangan baza (tugmalar tartibi bilan; callback'da indeksi yuboriladi)
BASES = ["Scopus", "Web of Science", "OAK", "Boshqa"]

STATUS_TITLES = {
    "pending": "⏳ Ko‘rib chiqilmoqda",
    "approved": "✅ Joylangan",
    "rejected": "❌ Rad etilgan",
    "closed": "🔒 Yopilgan (o‘rinlar to‘lgan)",
}


# Hammuallif o'rinlari: 1–10 ta, har biri 1–100 000 $
MAX_SLOTS = 10
MAX_PRICE = 100_000


def cut(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def parse_prices(text: str) -> Optional[list[int]]:
    """"550 540 530" yoki "550, 540, 530$" -> [550, 540, 530]; noto'g'ri bo'lsa None."""
    parts = text.replace(",", " ").replace("$", " ").split()
    if not 1 <= len(parts) <= MAX_SLOTS or not all(part.isdigit() for part in parts):
        return None
    prices = [int(part) for part in parts]
    return prices if all(1 <= price <= MAX_PRICE for price in prices) else None


def render_prices(prices: Optional[list[int]], separator: str = " · ") -> str:
    """[550, 540] -> "1-o'rin: 550$ · 2-o'rin: 540$"."""
    if not prices:
        return "kelishiladi"
    return separator.join(f"{position}-o‘rin: {price}$" for position, price in enumerate(prices, start=1))


def render_public(article: Article, annotation_limit: int = 350) -> str:
    """Foydalanuvchilarga ko'rinadigan kartochka: muallif va fayl yo'q."""
    return (
        f"📄 <b>#{article.id}</b> · {escape(article.base)}\n"
        f"<b>{escape(article.title)}</b>\n"
        f"{escape(cut(article.annotation, annotation_limit))}\n"
        f"👥 Hammualliflar uchun o‘rinlar: {article.slots}\n"
        f"💲 {render_prices(article.prices)}"
    )


def render_summary(title: str, direction: str, base: str, annotation: str, prices: list[int], file_name: str) -> str:
    """Muallif yuborishdan oldin ko'radigan qisqa ma'lumot."""
    return (
        f"<b>Sarlavha:</b> {escape(title)}\n"
        f"<b>Yo‘nalish:</b> {escape(direction)}\n"
        f"<b>Baza:</b> {escape(base)}\n"
        f"<b>Annotatsiya:</b> {escape(cut(annotation, 600))}\n"
        f"<b>Hammualliflar:</b> {len(prices)} ta\n"
        f"<b>Narxlar:</b> {render_prices(prices)}\n"
        f"<b>Fayl:</b> {escape(file_name)}"
    )


def render_admin(article: Article, author: User) -> str:
    """Admin uchun kartochka — maqola faylining izohi (1024 belgigacha), shuning uchun matnlar qisqartiriladi.

    "ID: ..." qatori bor — admin shu xabarga reply qilsa, javob muallifga boradi.
    """
    lines = [
        f"🤝 <b>Hammualliflik maqolasi #{article.id}</b> · {fmt_time(article.created_at)}",
        f"Holat: <b>{STATUS_TITLES.get(article.status, article.status)}</b>"
        + (f" — {escape(cut(article.reviewed_by, 40))}" if article.reviewed_by else ""),
        f"Sarlavha: {escape(cut(article.title, 120))}",
        f"Yo‘nalish: {escape(article.direction.title if article.direction else '—')}",
        f"Baza: {escape(article.base)} · Hammualliflar: {article.slots} ta",
        f"Narxlar ($): {' / '.join(map(str, article.prices)) if article.prices else 'kelishiladi'}",
        f"Annotatsiya: {escape(cut(article.annotation, 120))}",
    ]
    if article.reject_reason:
        lines.append(f"Rad etish sababi: {escape(cut(article.reject_reason, 80))}")
    lines += [
        "",
        "<b>Muallif</b>",
        f"Ism-familiya: {escape(cut(author.real_name or '—', 60))} · {REG_ROLES.get(author.role, author.role or '—')}",
        f"Telefon: {escape(author.phone or '—')}",
        format_user(author.user_id, cut(author.full_name, 60), author.username),
        "",
        REPLY_HINT,
    ]
    return "\n".join(lines)
