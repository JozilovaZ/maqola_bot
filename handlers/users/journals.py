from html import escape

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, LinkPreviewOptions, Message

from infrastructure.database.models import Journal
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.inline.callbacks import JournalPage, Nav
from keyboards.inline.journals import journal_directions_kb, journals_page_kb
from misc import texts

journals_router = Router()

# Bitta xabarda nechta jurnal ko'rsatiladi
PAGE_SIZE = 10


def render_journal(number: int, journal: Journal) -> str:
    title = escape(journal.title)
    if journal.url:
        title = f"<a href=\"{escape(journal.url)}\">{title}</a>"
    return f"{number}. {title} — <i>{escape(journal.base)}</i>"


async def show_directions(message: Message, repo: RequestsRepo):
    directions = await repo.directions.list_all()
    counts = await repo.journals.count_by_direction()
    await message.answer(texts.JOURNALS, reply_markup=journal_directions_kb(directions, counts))


@journals_router.message(Command("journals"))
async def cmd_journals(message: Message, repo: RequestsRepo):
    await show_directions(message, repo)


@journals_router.callback_query(Nav.filter(F.to == "journals"))
async def nav_journals(call: CallbackQuery, repo: RequestsRepo):
    await call.answer()
    await show_directions(call.message, repo)


@journals_router.callback_query(JournalPage.filter())
async def journals_page(call: CallbackQuery, callback_data: JournalPage, repo: RequestsRepo):
    await call.answer()
    direction = await repo.directions.get(callback_data.direction_id)
    if direction is None:
        return
    page = callback_data.page
    # Keyingi sahifa bormi — bittasini ortiqcha olib tekshiramiz
    journals = await repo.journals.direction_journals(direction.id, offset=page * PAGE_SIZE, limit=PAGE_SIZE + 1)
    has_next = len(journals) > PAGE_SIZE
    journals = journals[:PAGE_SIZE]

    lines = [f"📚 <b>{escape(direction.title)}</b>\n"]
    if journals:
        lines += [render_journal(page * PAGE_SIZE + i, journal) for i, journal in enumerate(journals, start=1)]
        lines.append(texts.JOURNALS_HINT)
    else:
        lines.append(texts.JOURNALS_EMPTY)
    await call.message.edit_text(
        "\n".join(lines),
        reply_markup=journals_page_kb(direction.id, page, has_next),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
