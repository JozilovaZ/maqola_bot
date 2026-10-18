from html import escape

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, User

from config import Config
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.inline.callbacks import FieldPage, Nav
from keyboards.inline.coauth import (
    coauth_final_kb, coauth_kb, coauth_topics_kb, fields_kb, suggest_done_kb, topics_page_kb,
)
from misc import texts
from misc.contact import ask_contact
from misc.media import send_photo
from misc.states import CoauthSuggest
from misc.topics import render_topic
from services.notify import notify_new_lead

coauthor_router = Router()

# Bitta xabarda nechta mavzu ko'rsatiladi (originalda 5 ta)
PAGE_SIZE = 5


async def show_coauth(message: Message, user: User):
    await send_photo(message, "coauth")
    await message.answer(texts.COAUTH.format(name=escape(user.full_name)), reply_markup=coauth_kb())


@coauthor_router.message(Command("co_authorship"))
async def cmd_coauth(message: Message):
    await show_coauth(message, message.from_user)


@coauthor_router.callback_query(Nav.filter(F.to == "coauth"))
async def nav_coauth(call: CallbackQuery):
    await call.answer()
    await show_coauth(call.message, call.from_user)


@coauthor_router.callback_query(Nav.filter(F.to == "coauth_individual"))
async def individual(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await ask_contact(call.message, state, texts.COAUTH_INDIVIDUAL, reason="coauth")


@coauthor_router.callback_query(Nav.filter(F.to == "coauth_topics"))
async def topics_intro(call: CallbackQuery):
    await call.answer()
    await send_photo(call.message, "coauth_topics")
    await call.message.answer(
        texts.COAUTH_TOPICS_INTRO.format(name=escape(call.from_user.full_name)),
        reply_markup=coauth_topics_kb(),
    )


@coauthor_router.callback_query(Nav.filter(F.to == "coauth_fields"))
async def choose_field(call: CallbackQuery, repo: RequestsRepo):
    await call.answer()
    await call.message.answer(texts.COAUTH_FIELDS, reply_markup=fields_kb(await repo.topics.list_fields()))


@coauthor_router.callback_query(FieldPage.filter())
async def field_topics(call: CallbackQuery, callback_data: FieldPage, state: FSMContext, repo: RequestsRepo):
    await call.answer()
    field = await repo.topics.get_field(callback_data.field_id)
    if field is None:
        return
    # Buyurtma arizasida qaysi soha ekanini ko'rsatish uchun
    await state.update_data(field=field.title)

    # Keyingi sahifa bormi — bilish uchun bittaga ko'proq olinadi
    topics = await repo.topics.field_topics(field.id, offset=callback_data.page * PAGE_SIZE, limit=PAGE_SIZE + 1)
    has_more = len(topics) > PAGE_SIZE
    text = "\n\n".join(render_topic(topic) for topic in topics[:PAGE_SIZE])

    if callback_data.page == 0 and text:
        await send_photo(call.message, "coauth_field")
    if has_more:
        await call.message.answer(text, reply_markup=topics_page_kb(field.id, callback_data.page + 1))
        return
    if text:
        await call.message.answer(text)
    await call.message.answer(texts.COAUTH_FINAL, reply_markup=coauth_final_kb())


@coauthor_router.callback_query(Nav.filter(F.to == "coauth_order"))
async def coauth_order(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await ask_contact(call.message, state, texts.COAUTH_ORDER, reason="coauth_order", details=data.get("field"))


@coauthor_router.callback_query(Nav.filter(F.to == "coauth_suggest"))
async def suggest(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await ask_contact(call.message, state, texts.COAUTH_SUGGEST, reason="coauth")
    await state.set_state(CoauthSuggest.keywords)


@coauthor_router.message(CoauthSuggest.keywords, F.text)
async def suggest_keywords(message: Message, state: FSMContext, bot: Bot, config: Config, repo: RequestsRepo):
    await state.set_state(None)
    user = message.from_user
    lead = await repo.leads.add_lead(user.id, "suggest", details=message.text)
    await notify_new_lead(bot, config.tg_bot.admin_ids, lead, user.full_name, user.username)
    await message.answer(texts.COAUTH_SUGGEST_THANKS, reply_markup=suggest_done_kb())
