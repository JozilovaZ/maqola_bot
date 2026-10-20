from html import escape
from typing import Optional

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LinkPreviewOptions, Message

from filters.admin import AdminFilter
from infrastructure.database.models import Journal
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.inline.callbacks import AdminJournal
from keyboards.inline.journals import (
    admin_direction_journals_kb, admin_journal_delete_kb, admin_journal_directions_kb, admin_journal_kb,
)
from misc.states import AddJournal, EditJournal

admin_journals_router = Router()
admin_journals_router.message.filter(AdminFilter())
admin_journals_router.callback_query.filter(AdminFilter())

NO_PREVIEW = LinkPreviewOptions(is_disabled=True)
BASE_EXAMPLE = "Masalan: <code>Scopus Q3</code>, <code>Web of Science</code> yoki <code>OAK</code>"
URL_EXAMPLE = "Masalan: <code>https://example.com</code>. Havola bo‘lmasa <code>-</code> yozing."


def parse_url(text: str) -> tuple[bool, Optional[str]]:
    """(to'g'rimi, havola). "-" — havolasiz."""
    value = text.strip()
    if value == "-":
        return True, None
    if value.startswith(("http://", "https://")) and " " not in value and len(value) <= 512:
        return True, value
    return False, None


def journal_view(journal: Journal) -> str:
    return (
        f"📗 <b>Jurnal #{journal.id}</b>\n\n"
        f"Nomi: {escape(journal.title)}\n"
        f"Baza: {escape(journal.base)}\n"
        f"Havola: {escape(journal.url) if journal.url else '—'}"
    )


# ---------- Ro'yxatlar ----------

async def directions_view(repo: RequestsRepo):
    directions = await repo.directions.list_all()
    counts = await repo.journals.count_by_direction()
    return "📚 <b>Jurnallar javoni</b>\n\nYo‘nalishni tanlang (qavsda — jurnallar soni):", \
        admin_journal_directions_kb(directions, counts)


async def direction_view(repo: RequestsRepo, direction_id: int):
    direction = await repo.directions.get(direction_id)
    journals = await repo.journals.direction_journals(direction_id)
    text = f"📂 <b>{escape(direction.title)}</b>\n\n" + (
        f"Jurnallar: {len(journals)} ta. Tahrirlash uchun tanlang." if journals else "Hozircha jurnal yo‘q."
    )
    return text, admin_direction_journals_kb(direction_id, journals)


@admin_journals_router.message(Command("shelf"))
async def cmd_shelf(message: Message, state: FSMContext, repo: RequestsRepo):
    await state.set_state(None)
    text, markup = await directions_view(repo)
    await message.answer(text, reply_markup=markup)


@admin_journals_router.callback_query(AdminJournal.filter(F.action == "directions"))
async def admin_directions(call: CallbackQuery, repo: RequestsRepo):
    await call.answer()
    text, markup = await directions_view(repo)
    await call.message.edit_text(text, reply_markup=markup)


@admin_journals_router.callback_query(AdminJournal.filter(F.action == "direction"))
async def admin_direction(call: CallbackQuery, callback_data: AdminJournal, repo: RequestsRepo):
    await call.answer()
    if await repo.directions.get(callback_data.id) is None:
        return
    text, markup = await direction_view(repo, callback_data.id)
    await call.message.edit_text(text, reply_markup=markup)


@admin_journals_router.callback_query(AdminJournal.filter(F.action == "journal"))
async def admin_journal(call: CallbackQuery, callback_data: AdminJournal, repo: RequestsRepo):
    await call.answer()
    journal = await repo.journals.get(callback_data.id)
    if journal is None:
        return
    await call.message.edit_text(journal_view(journal), reply_markup=admin_journal_kb(journal), link_preview_options=NO_PREVIEW)


# ---------- O'chirish ----------

@admin_journals_router.callback_query(AdminJournal.filter(F.action == "delete"))
async def admin_delete(call: CallbackQuery, callback_data: AdminJournal, repo: RequestsRepo):
    await call.answer()
    journal = await repo.journals.get(callback_data.id)
    if journal is None:
        return
    await call.message.edit_text(
        journal_view(journal) + "\n\n<b>Shu jurnalni o‘chirasizmi?</b>",
        reply_markup=admin_journal_delete_kb(journal),
        link_preview_options=NO_PREVIEW,
    )


@admin_journals_router.callback_query(AdminJournal.filter(F.action == "delete_yes"))
async def admin_delete_yes(call: CallbackQuery, callback_data: AdminJournal, repo: RequestsRepo):
    journal = await repo.journals.get(callback_data.id)
    if journal is None:
        await call.answer()
        return
    direction_id = journal.direction_id
    await repo.journals.delete(journal.id)
    await call.answer("Jurnal o‘chirildi")
    text, markup = await direction_view(repo, direction_id)
    await call.message.edit_text(text, reply_markup=markup)


# ---------- Bitta qiymatni tahrirlash: nomi / bazasi / havolasi ----------

EDIT_PROMPTS = {
    "edit_title": "Jurnalning yangi nomini yozing.",
    "edit_base": "Yangi bazani yozing.\n" + BASE_EXAMPLE,
    "edit_url": "Yangi havolani yozing.\n" + URL_EXAMPLE,
}


@admin_journals_router.callback_query(AdminJournal.filter(F.action.in_(EDIT_PROMPTS)))
async def admin_edit_start(call: CallbackQuery, callback_data: AdminJournal, state: FSMContext, repo: RequestsRepo):
    await call.answer()
    journal = await repo.journals.get(callback_data.id)
    if journal is None:
        return
    value = {"edit_title": journal.title, "edit_base": journal.base, "edit_url": journal.url or "-"}[callback_data.action]
    await state.set_state(EditJournal.value)
    await state.update_data(edit=callback_data.action, edit_id=journal.id)
    await call.message.answer(
        f"{EDIT_PROMPTS[callback_data.action]}\n\nHozirgisi: <code>{escape(value)}</code>\n\nBekor qilish: /cancel",
        link_preview_options=NO_PREVIEW,
    )


@admin_journals_router.message(EditJournal.value, F.text)
async def admin_edit_value(message: Message, state: FSMContext, repo: RequestsRepo):
    data = await state.get_data()
    action, journal_id, value = data.get("edit"), data.get("edit_id"), message.text.strip()
    if action == "edit_url":
        valid, url = parse_url(value)
        if not valid:
            await message.answer("Havola noto‘g‘ri. " + URL_EXAMPLE)
            return
        await repo.journals.update(journal_id, url=url)
    elif action == "edit_base":
        await repo.journals.update(journal_id, base=value[:64])
    else:
        await repo.journals.update(journal_id, title=value)
    await state.set_state(None)

    journal = await repo.journals.get(journal_id)
    if journal is None:
        await message.answer("Jurnal topilmadi.")
        return
    await repo.session.refresh(journal)
    await message.answer(
        "✅ Saqlandi\n\n" + journal_view(journal), reply_markup=admin_journal_kb(journal), link_preview_options=NO_PREVIEW
    )


# ---------- Yangi jurnal qo'shish: nomi → bazasi → havolasi ----------

@admin_journals_router.callback_query(AdminJournal.filter(F.action == "add"))
async def admin_add(call: CallbackQuery, callback_data: AdminJournal, state: FSMContext):
    await call.answer()
    await state.set_state(AddJournal.title)
    await state.update_data(direction_id=callback_data.id)
    await call.message.answer("Jurnal nomini yozing.\n\nBekor qilish: /cancel")


@admin_journals_router.message(AddJournal.title, F.text)
async def admin_add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddJournal.base)
    await message.answer("Bazasini yozing.\n" + BASE_EXAMPLE)


@admin_journals_router.message(AddJournal.base, F.text)
async def admin_add_base(message: Message, state: FSMContext):
    await state.update_data(base=message.text.strip()[:64])
    await state.set_state(AddJournal.url)
    await message.answer("Jurnal saytining havolasini yozing.\n" + URL_EXAMPLE)


@admin_journals_router.message(AddJournal.url, F.text)
async def admin_add_url(message: Message, state: FSMContext, repo: RequestsRepo):
    valid, url = parse_url(message.text)
    if not valid:
        await message.answer("Havola noto‘g‘ri. " + URL_EXAMPLE)
        return
    data = await state.get_data()
    await state.set_state(None)
    journal = await repo.journals.add(data["direction_id"], data["title"], data["base"], url)
    await message.answer(
        "✅ Jurnal qo‘shildi:\n\n" + journal_view(journal),
        reply_markup=admin_journal_kb(journal),
        link_preview_options=NO_PREVIEW,
    )
