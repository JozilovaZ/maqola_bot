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
    admin_direction_delete_kb, admin_direction_journals_kb, admin_journal_delete_kb, admin_journal_directions_kb,
    admin_journal_kb, admin_journal_move_kb,
)
from misc.states import AddJournal, EditDirection, EditJournal

admin_journals_router = Router()
admin_journals_router.message.filter(AdminFilter())
admin_journals_router.callback_query.filter(AdminFilter())

NO_PREVIEW = LinkPreviewOptions(is_disabled=True)
BASE_EXAMPLE = "Masalan: <code>Scopus Q3</code>, <code>Web of Science</code> yoki <code>OAK</code>"
URL_EXAMPLE = "Masalan: <code>https://example.com</code>. Havola bo‘lmasa <code>-</code> yozing."
DESC_EXAMPLE = (
    "2–4 jumla: jurnal nimani chop etadi, qaysi bazalarda indekslanadi, nashr muddati va hokazo. "
    "Foydalanuvchi buni jurnal kartochkasida ko‘radi. Ma’lumotsiz qoldirish uchun <code>-</code> yozing."
)
DESC_MAX = 1000
DESC_TOO_LONG = f"Ma’lumot {DESC_MAX} belgidan oshmasin."


def parse_url(text: str) -> tuple[bool, Optional[str]]:
    """(to'g'rimi, havola). "-" — havolasiz."""
    value = text.strip()
    if value == "-":
        return True, None
    if value.startswith(("http://", "https://")) and " " not in value and len(value) <= 512:
        return True, value
    return False, None


def parse_description(text: str) -> tuple[bool, Optional[str]]:
    """(to'g'rimi, ma'lumot). "-" — ma'lumotsiz."""
    value = text.strip()
    if value == "-":
        return True, None
    return len(value) <= DESC_MAX, value


def journal_view(journal: Journal) -> str:
    return (
        f"📗 <b>Jurnal #{journal.id}</b>\n\n"
        f"Nomi: {escape(journal.title)}\n"
        f"Baza: {escape(journal.base)}\n"
        f"Havola: {escape(journal.url) if journal.url else '—'}\n"
        f"Ma’lumot: {escape(journal.description) if journal.description else '—'}"
    )


# ---------- Ro'yxatlar ----------

async def directions_view(repo: RequestsRepo):
    directions = await repo.directions.list_all()
    counts = await repo.journals.count_by_direction()
    return "📚 <b>Jurnallar javoni</b>\n\n" \
        "Yo‘nalishni tanlang (qavsda — jurnallar soni).\n" \
        "<i>Yo‘nalishlar ro‘yxatdan o‘tish, rassilka va hammualliflik maqolalarida ham ishlatiladi.</i>", \
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
    "edit_desc": "Jurnal haqida qisqa ma’lumot yozing.\n" + DESC_EXAMPLE,
}


@admin_journals_router.callback_query(AdminJournal.filter(F.action.in_(EDIT_PROMPTS)))
async def admin_edit_start(call: CallbackQuery, callback_data: AdminJournal, state: FSMContext, repo: RequestsRepo):
    await call.answer()
    journal = await repo.journals.get(callback_data.id)
    if journal is None:
        return
    value = {
        "edit_title": journal.title, "edit_base": journal.base,
        "edit_url": journal.url or "-", "edit_desc": journal.description or "-",
    }[callback_data.action]
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
    elif action == "edit_desc":
        valid, description = parse_description(value)
        if not valid:
            await message.answer(DESC_TOO_LONG)
            return
        await repo.journals.update(journal_id, description=description)
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


# ---------- Yangi jurnal qo'shish: nomi → bazasi → havolasi → qisqa ma'lumot ----------

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
    await state.update_data(url=url)
    await state.set_state(AddJournal.description)
    await message.answer("Jurnal haqida qisqa ma’lumot yozing.\n" + DESC_EXAMPLE)


@admin_journals_router.message(AddJournal.description, F.text)
async def admin_add_description(message: Message, state: FSMContext, repo: RequestsRepo):
    valid, description = parse_description(message.text)
    if not valid:
        await message.answer(DESC_TOO_LONG)
        return
    data = await state.get_data()
    await state.set_state(None)
    journal = await repo.journals.add(data["direction_id"], data["title"], data["base"], data["url"], description)
    await message.answer(
        "✅ Jurnal qo‘shildi:\n\n" + journal_view(journal),
        reply_markup=admin_journal_kb(journal),
        link_preview_options=NO_PREVIEW,
    )


# ---------- Jurnalni boshqa yo'nalishga ko'chirish ----------

@admin_journals_router.callback_query(AdminJournal.filter(F.action == "move"))
async def admin_move(call: CallbackQuery, callback_data: AdminJournal, repo: RequestsRepo):
    await call.answer()
    journal = await repo.journals.get(callback_data.id)
    if journal is None:
        return
    await call.message.edit_text(
        journal_view(journal) + "\n\n<b>Qaysi yo‘nalishga ko‘chiramiz?</b>",
        reply_markup=admin_journal_move_kb(journal, await repo.directions.list_all()),
        link_preview_options=NO_PREVIEW,
    )


@admin_journals_router.callback_query(AdminJournal.filter(F.action == "move_to"))
async def admin_move_to(call: CallbackQuery, callback_data: AdminJournal, repo: RequestsRepo):
    journal = await repo.journals.get(callback_data.id)
    direction = await repo.directions.get(callback_data.to)
    if journal is None or direction is None:
        await call.answer()
        return
    await repo.journals.update(journal.id, direction_id=direction.id)
    await repo.session.refresh(journal)
    await call.answer(f"Ko‘chirildi: {direction.title}")
    await call.message.edit_text(journal_view(journal), reply_markup=admin_journal_kb(journal), link_preview_options=NO_PREVIEW)


# ---------- Yo'nalishlar: qo'shish, nomini o'zgartirish, o'chirish ----------

DIRECTION_EXAMPLE = "Boshida emoji bo‘lsin, masalan: <code>🧪 Kimyo va ekologiya</code>"


@admin_journals_router.callback_query(AdminJournal.filter(F.action.in_({"dir_add", "dir_rename"})))
async def admin_direction_edit_start(call: CallbackQuery, callback_data: AdminJournal, state: FSMContext, repo: RequestsRepo):
    await call.answer()
    text = "Yangi yo‘nalish nomini yozing.\n" + DIRECTION_EXAMPLE
    if callback_data.action == "dir_rename":
        direction = await repo.directions.get(callback_data.id)
        if direction is None:
            return
        text = f"Yo‘nalishning yangi nomini yozing.\n{DIRECTION_EXAMPLE}\n\nHozirgisi: <code>{escape(direction.title)}</code>"
    await state.set_state(EditDirection.value)
    await state.update_data(dir_edit=callback_data.action, dir_id=callback_data.id)
    await call.message.answer(text + "\n\nBekor qilish: /cancel")


@admin_journals_router.message(EditDirection.value, F.text)
async def admin_direction_edit_value(message: Message, state: FSMContext, repo: RequestsRepo):
    title = " ".join(message.text.split())
    if not 2 <= len(title) <= 128:
        await message.answer("Nom 2–128 belgi bo‘lsin.")
        return
    # Ro'yxatdan o'tishda yo'nalish tugma matni bo'yicha topiladi — nomlar takrorlanmasin
    existing = await repo.directions.get_by_title(title)
    data = await state.get_data()
    if existing is not None and existing.id != data.get("dir_id"):
        await message.answer("Bunday nomli yo‘nalish allaqachon bor. Boshqa nom yozing.")
        return
    await state.set_state(None)
    if data.get("dir_edit") == "dir_add":
        direction_id = (await repo.directions.add(title)).id
    else:
        direction_id = data.get("dir_id")
        if await repo.directions.get(direction_id) is None:
            await message.answer("Yo‘nalish topilmadi.")
            return
        await repo.directions.rename(direction_id, title)
    text, markup = await direction_view(repo, direction_id)
    await message.answer("✅ Saqlandi\n\n" + text, reply_markup=markup)


@admin_journals_router.callback_query(AdminJournal.filter(F.action == "dir_delete"))
async def admin_direction_delete(call: CallbackQuery, callback_data: AdminJournal, repo: RequestsRepo):
    await call.answer()
    direction = await repo.directions.get(callback_data.id)
    if direction is None:
        return
    journals = (await repo.journals.count_by_direction()).get(direction.id, 0)
    await call.message.edit_text(
        f"📂 <b>{escape(direction.title)}</b>\n\n"
        f"Yo‘nalish o‘chirilsa, undagi <b>{journals} ta jurnal ham o‘chadi</b>. Shu yo‘nalishni tanlagan "
        "foydalanuvchilar va maqolalarda yo‘nalish bo‘sh qoladi.\n\n<b>O‘chirasizmi?</b>",
        reply_markup=admin_direction_delete_kb(direction.id),
    )


@admin_journals_router.callback_query(AdminJournal.filter(F.action == "dir_delete_yes"))
async def admin_direction_delete_yes(call: CallbackQuery, callback_data: AdminJournal, repo: RequestsRepo):
    if await repo.directions.get(callback_data.id) is not None:
        await repo.directions.delete(callback_data.id)
    await call.answer("Yo‘nalish o‘chirildi")
    text, markup = await directions_view(repo)
    await call.message.edit_text(text, reply_markup=markup)
