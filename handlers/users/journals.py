from html import escape

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LinkPreviewOptions, Message

from config import Config
from infrastructure.database.models import Journal, User as DbUser
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.inline.callbacks import JournalApply, JournalPage, JournalView, Nav
from keyboards.inline.journals import journal_card_kb, journal_directions_kb, journal_site_kb, journals_page_kb
from misc import texts
from misc.contact import request_lead

journals_router = Router()

# Bitta xabarda nechta jurnal ko'rsatiladi
PAGE_SIZE = 10

NO_PREVIEW = LinkPreviewOptions(is_disabled=True)


def render_journal(number: int, journal: Journal) -> str:
    return f"{number}. {escape(journal.title)} — <i>{escape(journal.base)}</i>"


def render_card(journal: Journal, direction_title: str) -> str:
    return "\n".join([
        f"📗 <b>{escape(journal.title)}</b>",
        f"🏷 {escape(journal.base)}",
        f"📂 {escape(direction_title)}",
        "",
        escape(journal.description) if journal.description else texts.JOURNAL_NO_DESCRIPTION,
        "",
        texts.JOURNAL_CARD_HELP,
        "",
        texts.JOURNAL_CARD_HINT,
    ])


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

    numbered = list(enumerate(journals, start=page * PAGE_SIZE + 1))
    lines = [f"📚 <b>{escape(direction.title)}</b>\n"]
    if journals:
        lines += [render_journal(number, journal) for number, journal in numbered]
        lines.append(texts.JOURNALS_HINT)
    else:
        lines.append(texts.JOURNALS_EMPTY)
    await call.message.edit_text(
        "\n".join(lines),
        reply_markup=journals_page_kb(direction.id, page, has_next, numbered),
        link_preview_options=NO_PREVIEW,
    )


@journals_router.callback_query(JournalView.filter())
async def journal_card(call: CallbackQuery, callback_data: JournalView, repo: RequestsRepo):
    journal = await repo.journals.get(callback_data.id)
    if journal is None:
        await call.answer(texts.JOURNAL_UNAVAILABLE, show_alert=True)
        return
    await call.answer()
    direction = await repo.directions.get(journal.direction_id)
    await call.message.edit_text(
        render_card(journal, direction.title if direction else "—"),
        reply_markup=journal_card_kb(journal, callback_data.page),
        link_preview_options=NO_PREVIEW,
    )


@journals_router.callback_query(JournalApply.filter())
async def journal_apply(
    call: CallbackQuery, callback_data: JournalApply, state: FSMContext,
    user: DbUser, repo: RequestsRepo, bot: Bot, config: Config,
):
    journal = await repo.journals.get(callback_data.id)
    if journal is None:
        await call.answer(texts.JOURNAL_UNAVAILABLE, show_alert=True)
        return
    await call.answer()
    await request_lead(
        call.message, state, user, repo, bot, config, texts.JOURNAL_APPLY, reason="journal",
        details=f"Jurnal #{journal.id}: {journal.title} ({journal.base})",
    )
    # Sayt havolasi ariza qabul qilingandan keyin beriladi (raqam bazada bo'lsa ariza darhol yaratiladi)
    if user.phone and journal.url:
        await call.message.answer(texts.JOURNAL_SITE, reply_markup=journal_site_kb(journal))
