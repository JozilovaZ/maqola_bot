from html import escape

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, User

from keyboards.inline.about import about_kb, about_next_kb
from keyboards.inline.callbacks import Nav
from misc import texts
from misc.media import send_photo

about_router = Router()

SECTIONS = {
    "why": texts.ABOUT_WHY,
    "process": texts.ABOUT_PROCESS,
}


async def show_about(message: Message, user: User):
    await send_photo(message, "about")
    await message.answer(texts.ABOUT.format(name=escape(user.full_name)), reply_markup=about_kb())


@about_router.message(Command("about"))
async def cmd_about(message: Message):
    await show_about(message, message.from_user)


@about_router.callback_query(Nav.filter(F.to == "about"))
async def nav_about(call: CallbackQuery):
    await call.answer()
    await show_about(call.message, call.from_user)


@about_router.callback_query(Nav.filter(F.to.in_(SECTIONS)))
async def about_section(call: CallbackQuery, callback_data: Nav):
    await call.answer()
    await call.message.answer(SECTIONS[callback_data.to], reply_markup=about_next_kb())
