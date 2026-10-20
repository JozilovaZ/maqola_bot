import logging
from html import escape
from pathlib import Path

from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import Config
from handlers.users.plagiat import EXTENSIONS, MAX_SIZE
from infrastructure.database.models import User as DbUser
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.inline.articles import (
    admin_article_kb, article_bases_kb, article_cancel_kb, article_confirm_kb, article_directions_kb,
    article_slots_kb, browse_directions_kb, browse_page_kb,
)
from keyboards.inline.callbacks import ArticleApply, ArticleBrowse, ArticleForm, Nav
from misc import texts
from misc.articles import BASES, STATUS_TITLES, cut, render_admin, render_public, render_summary
from misc.contact import request_lead
from misc.states import ArticleSubmit

articles_router = Router()

# Bitta xabarda nechta maqola ko'rsatiladi
PAGE_SIZE = 5

# Maqola yuborishda FSM'da saqlanadigan qiymatlar
FORM_KEYS = ("art_title", "art_direction_id", "art_base", "art_annotation", "art_slots", "art_file_id", "art_file_name")


async def clear_form(state: FSMContext):
    data = await state.get_data()
    await state.set_data({key: value for key, value in data.items() if key not in FORM_KEYS})
    await state.set_state(None)


# ---------- Maqola yuborish: sarlavha → yo'nalish → baza → annotatsiya → o'rinlar → fayl → tasdiq ----------

@articles_router.callback_query(Nav.filter(F.to == "article_submit"))
async def submit_start(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await clear_form(state)
    await state.set_state(ArticleSubmit.title)
    await call.message.answer(texts.ARTICLE_SUBMIT, reply_markup=article_cancel_kb())


@articles_router.message(ArticleSubmit.title, F.text)
async def submit_title(message: Message, state: FSMContext, repo: RequestsRepo):
    title = " ".join(message.text.split())
    if not 5 <= len(title) <= 300:
        await message.answer(texts.ARTICLE_TITLE_INVALID, reply_markup=article_cancel_kb())
        return
    await state.update_data(art_title=title)
    await state.set_state(None)
    await message.answer(texts.ARTICLE_DIRECTION, reply_markup=article_directions_kb(await repo.directions.list_all()))


@articles_router.callback_query(ArticleForm.filter(F.field == "direction"))
async def submit_direction(call: CallbackQuery, callback_data: ArticleForm, state: FSMContext, repo: RequestsRepo):
    await call.answer()
    data = await state.get_data()
    if not data.get("art_title") or await repo.directions.get(callback_data.value) is None:
        await call.message.edit_text(texts.ARTICLE_EXPIRED)
        return
    await state.update_data(art_direction_id=callback_data.value)
    await call.message.edit_text(texts.ARTICLE_BASE, reply_markup=article_bases_kb())


@articles_router.callback_query(ArticleForm.filter(F.field == "base"))
async def submit_base(call: CallbackQuery, callback_data: ArticleForm, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    if not data.get("art_direction_id") or not 0 <= callback_data.value < len(BASES):
        await call.message.edit_text(texts.ARTICLE_EXPIRED)
        return
    await state.update_data(art_base=BASES[callback_data.value])
    await state.set_state(ArticleSubmit.annotation)
    await call.message.edit_text(texts.ARTICLE_ANNOTATION, reply_markup=article_cancel_kb())


@articles_router.message(ArticleSubmit.annotation, F.text)
async def submit_annotation(message: Message, state: FSMContext):
    annotation = message.text.strip()
    if not 30 <= len(annotation) <= 1000:
        await message.answer(texts.ARTICLE_ANNOTATION_INVALID, reply_markup=article_cancel_kb())
        return
    await state.update_data(art_annotation=annotation)
    await state.set_state(None)
    await message.answer(texts.ARTICLE_SLOTS, reply_markup=article_slots_kb())


@articles_router.callback_query(ArticleForm.filter(F.field == "slots"))
async def submit_slots(call: CallbackQuery, callback_data: ArticleForm, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    if not data.get("art_annotation") or callback_data.value < 1:
        await call.message.edit_text(texts.ARTICLE_EXPIRED)
        return
    await state.update_data(art_slots=callback_data.value)
    await state.set_state(ArticleSubmit.file)
    await call.message.edit_text(texts.ARTICLE_FILE, reply_markup=article_cancel_kb())


@articles_router.message(ArticleSubmit.file, F.document)
async def submit_file(message: Message, state: FSMContext, repo: RequestsRepo):
    document = message.document
    if Path(document.file_name or "").suffix.lower() not in EXTENSIONS:
        await message.answer(texts.PLAGIAT_WRONG, reply_markup=article_cancel_kb())
        return
    if (document.file_size or 0) > MAX_SIZE:
        await message.answer(texts.PLAGIAT_TOO_BIG, reply_markup=article_cancel_kb())
        return
    await state.update_data(art_file_id=document.file_id, art_file_name=document.file_name[:256])
    await state.set_state(None)

    data = await state.get_data()
    direction = await repo.directions.get(data["art_direction_id"])
    summary = render_summary(
        data["art_title"], direction.title if direction else "—", data["art_base"], data["art_annotation"],
        data["art_slots"], document.file_name,
    )
    await message.answer(texts.ARTICLE_CONFIRM.format(summary=summary), reply_markup=article_confirm_kb())


@articles_router.message(ArticleSubmit.file)
async def submit_file_wrong(message: Message):
    await message.answer(texts.PLAGIAT_WRONG, reply_markup=article_cancel_kb())


@articles_router.message(StateFilter(ArticleSubmit.title, ArticleSubmit.annotation))
async def submit_text_wrong(message: Message):
    """Sarlavha yoki annotatsiya o'rniga rasm, stiker va h.k. yuborilsa."""
    await message.answer(texts.REG_TEXT_ONLY, reply_markup=article_cancel_kb())


@articles_router.callback_query(ArticleForm.filter(F.field == "send"))
async def submit_send(
    call: CallbackQuery, state: FSMContext, bot: Bot, config: Config, repo: RequestsRepo, user: DbUser
):
    await call.answer()
    data = await state.get_data()
    if any(data.get(key) is None for key in FORM_KEYS):
        await call.message.edit_text(texts.ARTICLE_EXPIRED)
        return
    await clear_form(state)
    article = await repo.articles.add(
        author_id=user.user_id,
        direction_id=data["art_direction_id"],
        base=data["art_base"],
        title=data["art_title"],
        annotation=data["art_annotation"],
        slots=data["art_slots"],
        file_id=data["art_file_id"],
        file_name=data["art_file_name"],
    )
    await call.message.edit_text(texts.ARTICLE_SENT.format(id=article.id))

    caption = render_admin(article, user)
    for admin_id in config.tg_bot.admin_ids:
        try:
            await bot.send_document(admin_id, article.file_id, caption=caption, reply_markup=admin_article_kb(article))
        except Exception as e:
            logging.error(f"Maqola adminga yuborilmadi [ID:{admin_id}]: {e}")


@articles_router.callback_query(ArticleForm.filter(F.field == "cancel"))
async def submit_cancel(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await clear_form(state)
    await call.message.edit_text(texts.ARTICLE_CANCELLED)


@articles_router.message(Command("cancel"), StateFilter(ArticleSubmit))
async def submit_cancel_command(message: Message, state: FSMContext):
    await clear_form(state)
    await message.answer(texts.ARTICLE_CANCELLED)


# ---------- Maqolalarni ko'rish va hammuallif bo'lish ----------

@articles_router.callback_query(Nav.filter(F.to == "articles"))
async def browse(call: CallbackQuery, repo: RequestsRepo):
    await call.answer()
    directions = await repo.directions.list_all()
    counts = await repo.articles.count_approved_by_direction()
    await call.message.answer(texts.ARTICLES, reply_markup=browse_directions_kb(directions, counts))


@articles_router.callback_query(ArticleBrowse.filter())
async def browse_page(call: CallbackQuery, callback_data: ArticleBrowse, repo: RequestsRepo):
    await call.answer()
    direction = await repo.directions.get(callback_data.direction_id)
    if direction is None:
        return
    page = callback_data.page
    # Keyingi sahifa bormi — bittasini ortiqcha olib tekshiramiz
    articles = await repo.articles.approved(direction.id, offset=page * PAGE_SIZE, limit=PAGE_SIZE + 1)
    has_next = len(articles) > PAGE_SIZE
    articles = articles[:PAGE_SIZE]

    lines = [f"📖 <b>{escape(direction.title)}</b>"]
    lines += [render_public(article) for article in articles] or [texts.ARTICLES_EMPTY]
    await call.message.edit_text("\n\n".join(lines), reply_markup=browse_page_kb(direction.id, page, articles, has_next))


@articles_router.callback_query(ArticleApply.filter())
async def apply(
    call: CallbackQuery, callback_data: ArticleApply, state: FSMContext,
    user: DbUser, repo: RequestsRepo, bot: Bot, config: Config,
):
    article = await repo.articles.get(callback_data.id)
    if article is None or article.status != "approved":
        await call.answer(texts.ARTICLE_UNAVAILABLE, show_alert=True)
        return
    if article.author_id == user.user_id:
        await call.answer(texts.ARTICLE_OWN, show_alert=True)
        return
    await call.answer()
    await request_lead(
        call.message, state, user, repo, bot, config, texts.ARTICLE_APPLY, reason="coauth_article",
        details=f"Maqola #{article.id}: {cut(article.title, 150)} → /article_{article.id}",
    )


@articles_router.callback_query(Nav.filter(F.to == "my_articles"))
async def my_articles(call: CallbackQuery, repo: RequestsRepo, user: DbUser):
    await call.answer()
    articles = await repo.articles.by_author(user.user_id)
    if not articles:
        await call.message.answer(texts.MY_ARTICLES_EMPTY)
        return
    lines = ["🗂 <b>Mening maqolalarim</b>"]
    for article in articles[:20]:
        line = f"<b>#{article.id}</b> {escape(cut(article.title, 80))}\n{STATUS_TITLES.get(article.status, article.status)}"
        if article.status == "rejected" and article.reject_reason:
            line += f": {escape(cut(article.reject_reason, 200))}"
        lines.append(line)
    await call.message.answer("\n\n".join(lines))
