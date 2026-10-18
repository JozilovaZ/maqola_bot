import logging
from datetime import datetime
from html import escape
from typing import Optional

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Message

from infrastructure.database.models import Lead
from keyboards.inline.admin import lead_status_kb

REASON_TITLES = {
    "consult": "💬 Bepul maslahat",
    "order": "🛒 Xizmatga buyurtma",
    "coauth": "🎯 Hammualliflik — individual tanlov",
    "coauth_order": "🤝 Hammualliflikka buyurtma",
    "suggest": "💡 Hammualliflik — mavzu taklifi (kalit so‘zlar)",
    "scopus": "🔎 Scopus — jurnalni qo‘lda tekshirish",
    "audit": "📝 Maqola auditi (Scopus tekshiruvidan)",
}

STATUS_TITLES = {
    "new": "🆕 Yangi",
    "contacted": "📞 Bog‘lanildi",
    "closed": "✅ Yopildi",
    "rejected": "❌ Rad etildi",
}

REPLY_HINT = "<i>↩️ Javob yozish uchun shu xabarga reply qiling.</i>"


def format_user(user_id: int, full_name: str, username: Optional[str]) -> str:
    return (
        f"Ism: <a href=\"tg://user?id={user_id}\">{escape(full_name)}</a>\n"
        f"Username: {'@' + username if username else '—'}\n"
        f"ID: <code>{user_id}</code>"
    )


def fmt_time(value: Optional[datetime]) -> str:
    return value.strftime("%d.%m.%Y %H:%M") if value else ""


def render_lead(lead: Lead, full_name: str, username: Optional[str]) -> str:
    """Ariza kartochkasi: yangi ariza xabari, /lead_N va holat o'zgarganda bir xil ko'rinadi."""
    lines = [
        f"🆕 <b>Ariza #{lead.id}</b> · {fmt_time(lead.created_at)}",
        f"Bo‘lim: {REASON_TITLES.get(lead.reason, lead.reason)}",
    ]
    if lead.details:
        lines.append(f"Tafsilot: {escape(lead.details)}")
    lines.append(format_user(lead.user_id, full_name, username))
    if lead.phone:
        lines.append(f"Telefon: {escape(lead.phone)}")
    status = f"Holat: <b>{STATUS_TITLES.get(lead.status, lead.status)}</b>"
    if lead.status_by:
        status += f" — {escape(lead.status_by)}, {fmt_time(lead.status_at)}"
    lines += [status, "", REPLY_HINT]
    return "\n".join(lines)


async def notify_admins(
    bot: Bot, admin_ids: list[int], text: str, reply_markup: Optional[InlineKeyboardMarkup] = None
) -> None:
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, text, reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Adminga ariza yuborilmadi [ID:{admin_id}]: {e}")


async def forward_to_admins(bot: Bot, admin_ids: list[int], message: Message) -> None:
    """Foydalanuvchi yozgan xabarni adminlarga: avval kimdan ekani, keyin xabarning o'zi (forward)."""
    user = message.from_user
    header = f"✉️ <b>Foydalanuvchidan xabar</b>\n{format_user(user.id, user.full_name, user.username)}\n\n{REPLY_HINT}"
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, header)
            await message.forward(admin_id)
        except Exception as e:
            logging.error(f"Xabar adminga yuborilmadi [ID:{admin_id}]: {e}")


async def notify_new_lead(bot: Bot, admin_ids: list[int], lead: Lead, full_name: str, username: Optional[str]) -> None:
    await notify_admins(bot, admin_ids, render_lead(lead, full_name, username), reply_markup=lead_status_kb(lead.id))
