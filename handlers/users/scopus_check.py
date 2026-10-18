import datetime
from html import escape

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import Config
from keyboards.inline.callbacks import Nav
from keyboards.inline.scopus import scopus_found_kb, scopus_intro_kb, scopus_not_found_kb
from misc import texts
from misc.contact import ask_contact
from misc.states import ScopusCheck
from services.scopus import find_journal

scopus_router = Router()


@scopus_router.message(Command("scopus_check"))
async def cmd_scopus(message: Message):
    await message.answer(texts.SCOPUS_INTRO, reply_markup=scopus_intro_kb())


@scopus_router.callback_query(Nav.filter(F.to == "scopus"))
async def nav_scopus(call: CallbackQuery):
    await call.answer()
    await call.message.answer(texts.SCOPUS_INTRO, reply_markup=scopus_intro_kb())


@scopus_router.callback_query(Nav.filter(F.to == "scopus_start"))
async def scopus_start(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await ask_contact(call.message, state, texts.SCOPUS_ASK, reason="scopus")
    await state.set_state(ScopusCheck.query)


@scopus_router.message(ScopusCheck.query, F.text)
async def scopus_query(message: Message, state: FSMContext, config: Config):
    await state.set_state(None)
    await message.bot.send_chat_action(message.chat.id, "typing")
    journal = await find_journal(message.text, config.scopus.api_key)

    if journal is None:
        await state.update_data(reason="scopus", details=f"Topilmadi: {message.text}")
        await message.answer(texts.SCOPUS_NOT_FOUND, reply_markup=scopus_not_found_kb())
        return

    await state.update_data(reason="audit", details=f"{journal.title} (ISSN: {journal.issn})")
    today = datetime.date.today()
    await message.answer(
        texts.SCOPUS_FOUND.format(
            title=escape(journal.title),
            publisher=escape(journal.publisher),
            issn=journal.issn,
            status=texts.SCOPUS_STATUS_ACTIVE if journal.active else texts.SCOPUS_STATUS_INACTIVE,
            coverage=journal.coverage,
            subjects=journal.subjects,
            date=f"{texts.MONTHS[today.month - 1]} {today.year}",
        ),
        reply_markup=scopus_found_kb(),
    )


@scopus_router.callback_query(Nav.filter(F.to == "scopus_audit"))
async def scopus_audit(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await ask_contact(call.message, state, texts.SCOPUS_AUDIT, reason="audit", details=data.get("details"))


@scopus_router.callback_query(Nav.filter(F.to == "scopus_manual"))
async def scopus_manual(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await ask_contact(call.message, state, texts.SCOPUS_LEAVE_NUMBER, reason="scopus", details=data.get("details"))
