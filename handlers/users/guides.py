from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from config import Config
from keyboards.inline.callbacks import Checklist, Nav
from keyboards.inline.guides import blog_kb, checklists_kb, guides_kb
from misc import texts
from misc.media import send_document, send_photo

guides_router = Router()

# files/ papkasidagi PDF nomlari (kengaytmasiz)
CHECKLIST_FILES = {
    "phd": "checklist_phd",
    "rejected": "checklist_rejected",
    "reply": "checklist_reply",
    "redflags": "checklist_redflags",
}


async def show_guides(message: Message):
    # Originalda avval matn, keyin rasm keladi
    await message.answer(texts.GUIDES, reply_markup=guides_kb())
    await send_photo(message, "guides")


@guides_router.message(Command("guides"))
async def cmd_guides(message: Message):
    await show_guides(message)


@guides_router.callback_query(Nav.filter(F.to == "guides"))
async def nav_guides(call: CallbackQuery):
    await call.answer()
    await show_guides(call.message)


@guides_router.callback_query(Nav.filter(F.to == "checklists"))
async def nav_checklists(call: CallbackQuery):
    await call.answer()
    await call.message.answer(texts.CHECKLISTS, reply_markup=checklists_kb())


@guides_router.callback_query(Checklist.filter())
async def send_checklist(call: CallbackQuery, callback_data: Checklist):
    await call.answer()
    await call.message.answer(texts.CHECKLIST_TEXTS[callback_data.key])
    await send_document(call.message, CHECKLIST_FILES[callback_data.key])


@guides_router.callback_query(Nav.filter(F.to == "blog"))
async def nav_blog(call: CallbackQuery, config: Config):
    await call.answer()
    await call.message.answer(texts.BLOG, reply_markup=blog_kb(config.links.blog))
