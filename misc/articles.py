from html import escape

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


def cut(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def render_public(article: Article, annotation_limit: int = 350) -> str:
    """Foydalanuvchilarga ko'rinadigan kartochka: muallif va fayl yo'q."""
    return (
        f"📄 <b>#{article.id}</b> · {escape(article.base)}\n"
        f"<b>{escape(article.title)}</b>\n"
        f"{escape(cut(article.annotation, annotation_limit))}\n"
        f"👥 Hammualliflar uchun o‘rinlar: {article.slots}"
    )


def render_summary(title: str, direction: str, base: str, annotation: str, slots: int, file_name: str) -> str:
    """Muallif yuborishdan oldin ko'radigan qisqa ma'lumot."""
    return (
        f"<b>Sarlavha:</b> {escape(title)}\n"
        f"<b>Yo‘nalish:</b> {escape(direction)}\n"
        f"<b>Baza:</b> {escape(base)}\n"
        f"<b>Annotatsiya:</b> {escape(cut(annotation, 600))}\n"
        f"<b>Hammualliflar:</b> {slots} ta\n"
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
        f"Sarlavha: {escape(cut(article.title, 150))}",
        f"Yo‘nalish: {escape(article.direction.title if article.direction else '—')}",
        f"Baza: {escape(article.base)} · Hammualliflar: {article.slots} ta",
        f"Annotatsiya: {escape(cut(article.annotation, 200))}",
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
