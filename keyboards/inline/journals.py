from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from infrastructure.database.models import Direction, Journal
from keyboards.inline.callbacks import AdminJournal, JournalPage, Nav


# ---------- Foydalanuvchi ----------

def journal_directions_kb(directions: list[Direction], counts: dict[int, int]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for direction in directions:
        keyboard.button(
            text=f"{direction.title} ({counts.get(direction.id, 0)})",
            callback_data=JournalPage(direction_id=direction.id),
        )
    keyboard.button(text="⬅️ Bosh menyu", callback_data=Nav(to="main"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def journals_page_kb(direction_id: int, page: int, has_next: bool) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    if page > 0:
        keyboard.button(text="⬅️ Oldingi", callback_data=JournalPage(direction_id=direction_id, page=page - 1))
    if has_next:
        keyboard.button(text="Keyingi ➡️", callback_data=JournalPage(direction_id=direction_id, page=page + 1))
    keyboard.adjust(2)
    keyboard.row(InlineKeyboardButton(text="💬 Bepul maslahat", callback_data=Nav(to="consult").pack()))
    keyboard.row(InlineKeyboardButton(text="📚 Yo‘nalishlar", callback_data=Nav(to="journals").pack()))
    return keyboard.as_markup()


# ---------- Admin: /shelf ----------

def admin_journal_directions_kb(directions: list[Direction], counts: dict[int, int]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for direction in directions:
        keyboard.button(
            text=f"{direction.title} ({counts.get(direction.id, 0)})",
            callback_data=AdminJournal(action="direction", id=direction.id),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def admin_direction_journals_kb(direction_id: int, journals: list[Journal]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for journal in journals:
        keyboard.button(
            text=f"#{journal.id} {journal.base} | {journal.title[:40]}",
            callback_data=AdminJournal(action="journal", id=journal.id),
        )
    keyboard.button(text="➕ Jurnal qo‘shish", callback_data=AdminJournal(action="add", id=direction_id))
    keyboard.button(text="⬅️ Yo‘nalishlar", callback_data=AdminJournal(action="directions"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def admin_journal_kb(journal: Journal) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✏️ Nomi", callback_data=AdminJournal(action="edit_title", id=journal.id))
    keyboard.button(text="🏷 Baza", callback_data=AdminJournal(action="edit_base", id=journal.id))
    keyboard.button(text="🔗 Havola", callback_data=AdminJournal(action="edit_url", id=journal.id))
    keyboard.button(text="🗑 O‘chirish", callback_data=AdminJournal(action="delete", id=journal.id))
    keyboard.button(text="⬅️ Orqaga", callback_data=AdminJournal(action="direction", id=journal.direction_id))
    keyboard.adjust(3, 1, 1)
    return keyboard.as_markup()


def admin_journal_delete_kb(journal: Journal) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Ha, o‘chirish", callback_data=AdminJournal(action="delete_yes", id=journal.id))
    keyboard.button(text="Yo‘q", callback_data=AdminJournal(action="journal", id=journal.id))
    keyboard.adjust(2)
    return keyboard.as_markup()
