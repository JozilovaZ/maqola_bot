import asyncio
import re
from html import escape

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import Config
from filters.admin import AdminFilter
from infrastructure.database.models import Article, User
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.inline.articles import admin_article_kb, announce_kb
from keyboards.inline.callbacks import AdminArticle
from misc import texts
from misc.articles import STATUS_TITLES, cut, parse_prices, render_admin, render_prices, render_public
from misc.states import ArticlePrices, ArticleReject
from services.broadcaster import send_to_users

admin_articles_router = Router()
admin_articles_router.message.filter(AdminFilter())
admin_articles_router.callback_query.filter(AdminFilter())


async def load(repo: RequestsRepo, article_id: int) -> tuple[Article, User] | None:
    article = await repo.articles.get(article_id)
    if article is None:
        return None
    await repo.session.refresh(article)  # holat boshqa admin tomonidan o'zgargan bo'lishi mumkin
    return article, await repo.session.get(User, article.author_id)


async def notify_author(bot: Bot, article: Article, text: str) -> None:
    try:
        await bot.send_message(article.author_id, text)
    except Exception:
        # Muallif botni bloklagan bo'lsa ham holat saqlanadi
        pass


async def announce_article(bot: Bot, session_pool, article_id: int, admin_id: int, skip_ids: set[int]):
    """Yangi tasdiqlangan maqola haqida shu yo'nalishdagi foydalanuvchilarga xabar. Fonda ishlaydi."""
    async with session_pool() as session:
        repo = RequestsRepo(session)
        article = await repo.articles.get(article_id)
        if article is None or article.direction_id is None:
            return
        user_ids = [uid for uid in await repo.users.active_ids(article.direction_id) if uid not in skip_ids]
        text = texts.ARTICLE_ANNOUNCE.format(card=render_public(article))
        sent, blocked, failed = await send_to_users(bot, user_ids, text, reply_markup=announce_kb(article))
        await repo.users.set_inactive(blocked)
    await bot.send_message(
        admin_id,
        f"📣 Maqola #{article_id} haqida yo‘nalishdagilarga xabar yuborildi: {sent} ta"
        + (f" (botni bloklagan: {len(blocked)}, xato: {failed})" if blocked or failed else ""),
    )


@admin_articles_router.message(Command("articles"))
async def cmd_articles(message: Message, repo: RequestsRepo):
    counts = await repo.articles.count_by_status()
    pending = await repo.articles.by_status("pending")
    lines = ["🤝 <b>Hammualliflik maqolalari</b>\n"]
    lines += [f"{title}: {counts.get(status, 0)}" for status, title in STATUS_TITLES.items()]
    if pending:
        lines.append("\n<b>Ko‘rib chiqilishi kerak:</b>")
        lines += [f"#{a.id} {escape(cut(a.title, 60))} → /article_{a.id}" for a in pending]
    else:
        lines.append("\n✅ Ko‘rib chiqilmagan maqola yo‘q.")
    lines.append("\nIstalgan maqolani ochish: /article_N (N — maqola raqami)")
    await message.answer("\n".join(lines)[:4096])


@admin_articles_router.message(F.text.regexp(r"^/article_(\d+)$").as_("match"))
async def cmd_article(message: Message, match: re.Match, repo: RequestsRepo):
    found = await load(repo, int(match.group(1)))
    if found is None:
        await message.answer("Maqola topilmadi.")
        return
    article, author = found
    await message.answer_document(article.file_id, caption=render_admin(article, author), reply_markup=admin_article_kb(article))


async def update_card(message: Message, repo: RequestsRepo, article_id: int) -> None:
    found = await load(repo, article_id)
    if found is not None:
        article, author = found
        await message.edit_caption(caption=render_admin(article, author), reply_markup=admin_article_kb(article))


@admin_articles_router.callback_query(AdminArticle.filter(F.action == "approve"))
async def approve(
    call: CallbackQuery, callback_data: AdminArticle, bot: Bot, repo: RequestsRepo, config: Config, session_pool
):
    found = await load(repo, callback_data.id)
    if found is None:
        await call.answer("Maqola topilmadi", show_alert=True)
        return
    article, _ = found
    if article.status == "approved":
        # Boshqa admin allaqachon tasdiqlagan — muallif va yo'nalishdagilarga ikkinchi marta xabar bormasin
        await call.answer("Maqola allaqachon joylangan")
        await update_card(call.message, repo, article.id)
        return
    first_time = article.status == "pending"
    await repo.articles.set_status(article.id, "approved", call.from_user.full_name)
    await call.answer("Maqola joylandi")
    await update_card(call.message, repo, article.id)
    await notify_author(bot, article, texts.ARTICLE_APPROVED.format(id=article.id, title=escape(article.title)))
    if first_time:
        # Qayta joylanganda (yopilgan/rad etilgandan keyin) e'lon takrorlanmaydi
        skip_ids = {article.author_id, *config.tg_bot.admin_ids}
        asyncio.create_task(announce_article(bot, session_pool, article.id, call.from_user.id, skip_ids))


@admin_articles_router.callback_query(AdminArticle.filter(F.action == "close"))
async def close(call: CallbackQuery, callback_data: AdminArticle, repo: RequestsRepo):
    if await repo.articles.get(callback_data.id) is None:
        await call.answer("Maqola topilmadi", show_alert=True)
        return
    await repo.articles.set_status(callback_data.id, "closed", call.from_user.full_name)
    await call.answer("Maqola yopildi — foydalanuvchilarga endi ko‘rinmaydi")
    await update_card(call.message, repo, callback_data.id)


@admin_articles_router.callback_query(AdminArticle.filter(F.action == "reject"))
async def reject(call: CallbackQuery, callback_data: AdminArticle, state: FSMContext):
    await call.answer()
    await state.set_state(ArticleReject.reason)
    # Sabab yozilgach, shu kartochka yangilanadi
    await state.update_data(reject_id=callback_data.id, reject_message_id=call.message.message_id)
    await call.message.answer(
        f"Maqola #{callback_data.id} ni rad etish sababini yozing — u muallifga yuboriladi.\n"
        "Sababsiz rad etish uchun <code>-</code> yozing.\n\nBekor qilish: /cancel"
    )


@admin_articles_router.message(ArticleReject.reason, F.text)
async def reject_reason(message: Message, state: FSMContext, bot: Bot, repo: RequestsRepo):
    data = await state.get_data()
    await state.set_state(None)
    found = await load(repo, data.get("reject_id", 0))
    if found is None:
        await message.answer("Maqola topilmadi.")
        return
    article, author = found
    reason = None if message.text.strip() == "-" else message.text.strip()
    await repo.articles.set_status(article.id, "rejected", message.from_user.full_name, reject_reason=reason)
    await repo.session.refresh(article)

    await message.answer(f"❌ Maqola #{article.id} rad etildi. Muallifga xabar yuborildi.")
    try:
        await bot.edit_message_caption(
            chat_id=message.chat.id, message_id=data.get("reject_message_id"),
            caption=render_admin(article, author), reply_markup=admin_article_kb(article),
        )
    except Exception:
        # Kartochka o'chirilgan yoki eskirgan bo'lsa — muhim emas
        pass
    tail = f"\n\nSabab: {escape(reason)}" if reason else ""
    await notify_author(bot, article, texts.ARTICLE_REJECTED.format(id=article.id, title=escape(article.title), reason=tail))


# ---------- Narxlarni o'zgartirish ----------

@admin_articles_router.callback_query(AdminArticle.filter(F.action == "prices"))
async def prices(call: CallbackQuery, callback_data: AdminArticle, state: FSMContext, repo: RequestsRepo):
    await call.answer()
    article = await repo.articles.get(callback_data.id)
    if article is None:
        return
    await state.set_state(ArticlePrices.value)
    # Narxlar yozilgach, shu kartochka yangilanadi
    await state.update_data(prices_id=article.id, prices_message_id=call.message.message_id)
    current = " ".join(str(price) for price in article.prices) if article.prices else "—"
    await call.message.answer(
        f"Maqola #{article.id} uchun o‘rinlar narxini ($) 1-o‘rindan boshlab bo‘sh joy bilan yozing.\n"
        "Nechta narx yozsangiz, shuncha o‘rin bo‘ladi (10 tagacha).\n\n"
        f"Hozirgisi: <code>{current}</code>\n\nBekor qilish: /cancel"
    )


@admin_articles_router.message(ArticlePrices.value, F.text)
async def prices_value(message: Message, state: FSMContext, bot: Bot, repo: RequestsRepo):
    new_prices = parse_prices(message.text)
    if new_prices is None:
        await message.answer(texts.ARTICLE_PRICES_INVALID)
        return
    data = await state.get_data()
    await state.set_state(None)
    found = await load(repo, data.get("prices_id", 0))
    if found is None:
        await message.answer("Maqola topilmadi.")
        return
    article, author = found
    await repo.articles.set_prices(article.id, new_prices)
    await repo.session.refresh(article)

    await message.answer(f"✅ Maqola #{article.id} narxlari saqlandi:\n{render_prices(article.prices, separator=chr(10))}")
    try:
        await bot.edit_message_caption(
            chat_id=message.chat.id, message_id=data.get("prices_message_id"),
            caption=render_admin(article, author), reply_markup=admin_article_kb(article),
        )
    except Exception:
        # Kartochka o'chirilgan yoki eskirgan bo'lsa — muhim emas
        pass
