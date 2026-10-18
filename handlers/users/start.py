from html import escape

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, User

from keyboards.inline.callbacks import Nav
from keyboards.inline.main_menu import main_menu_kb
from misc import texts
from misc.media import send_photo

user_router = Router()


async def show_main_menu(message: Message, user: User):
    await send_photo(message, "hero")
    await message.answer(
        texts.MAIN_MENU.format(name=escape(user.full_name)),
        reply_markup=main_menu_kb(),
    )


@user_router.message(CommandStart())
@user_router.message(Command("hero"))
async def user_start(message: Message):
    await show_main_menu(message, message.from_user)


@user_router.callback_query(Nav.filter(F.to == "main"))
async def back_to_main(call: CallbackQuery):
    await call.answer()
    await show_main_menu(call.message, call.from_user)
