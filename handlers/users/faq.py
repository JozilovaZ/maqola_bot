from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, LinkPreviewOptions, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.callbacks import Faq, Nav
from misc import texts

faq_router = Router()

NO_PREVIEW = LinkPreviewOptions(is_disabled=True)


def faq_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for index, (question, _) in enumerate(texts.FAQ_ITEMS):
        keyboard.button(text=question, callback_data=Faq(index=index))
    keyboard.button(text="💬 Bepul maslahat", callback_data=Nav(to="consult"))
    keyboard.button(text="⬅️ Bosh menyu", callback_data=Nav(to="main"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def answer_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅️ Savollar", callback_data=Nav(to="faq_back"))
    keyboard.button(text="💬 Bepul maslahat", callback_data=Nav(to="consult"))
    keyboard.adjust(2)
    return keyboard.as_markup()


@faq_router.message(Command("faq"))
async def cmd_faq(message: Message):
    await message.answer(texts.FAQ, reply_markup=faq_kb())


@faq_router.callback_query(Nav.filter(F.to == "faq"))
async def nav_faq(call: CallbackQuery):
    await call.answer()
    await call.message.answer(texts.FAQ, reply_markup=faq_kb())


# Javobdan savollar ro'yxatiga qaytish — o'sha xabarning o'zi almashtiriladi
@faq_router.callback_query(Nav.filter(F.to == "faq_back"))
async def faq_back(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(texts.FAQ, reply_markup=faq_kb())


@faq_router.callback_query(Faq.filter())
async def faq_answer(call: CallbackQuery, callback_data: Faq):
    await call.answer()
    if not 0 <= callback_data.index < len(texts.FAQ_ITEMS):
        return
    question, answer = texts.FAQ_ITEMS[callback_data.index]
    await call.message.edit_text(
        f"❓ <b>{question}</b>\n\n{answer}", reply_markup=answer_kb(), link_preview_options=NO_PREVIEW
    )
