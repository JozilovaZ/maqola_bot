from html import escape
from pathlib import Path

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config
from handlers.users.start import show_main_menu
from infrastructure.database.models import User
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.inline.callbacks import Nav
from misc import texts
from misc.states import PlagiatCheck
from services.notify import notify_new_file_lead

plagiat_router = Router()

EXTENSIONS = {".doc", ".docx", ".pdf"}
# Telegram bot 20 MB dan katta faylni yuklab ololmaydi
MAX_SIZE = 20 * 1024 * 1024


def cancel_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="❌ Bekor qilish", callback_data=Nav(to="plagiat_cancel"))
    return keyboard.as_markup()


async def ask_file(message: Message, state: FSMContext):
    await state.set_state(PlagiatCheck.file)
    await message.answer(texts.PLAGIAT, reply_markup=cancel_kb())


@plagiat_router.message(Command("plagiat"))
async def cmd_plagiat(message: Message, state: FSMContext):
    await ask_file(message, state)


@plagiat_router.callback_query(Nav.filter(F.to == "plagiat"))
async def nav_plagiat(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await ask_file(call.message, state)


@plagiat_router.callback_query(Nav.filter(F.to == "plagiat_cancel"))
async def plagiat_cancel(call: CallbackQuery, state: FSMContext):
    await call.answer()
    if await state.get_state() == PlagiatCheck.file.state:
        await state.set_state(None)
    await show_main_menu(call.message, call.from_user)


@plagiat_router.message(PlagiatCheck.file, F.document)
async def plagiat_file(message: Message, state: FSMContext, bot: Bot, config: Config, repo: RequestsRepo, user: User):
    document = message.document
    if Path(document.file_name or "").suffix.lower() not in EXTENSIONS:
        await message.answer(texts.PLAGIAT_WRONG, reply_markup=cancel_kb())
        return
    if (document.file_size or 0) > MAX_SIZE:
        await message.answer(texts.PLAGIAT_TOO_BIG, reply_markup=cancel_kb())
        return
    await state.set_state(None)

    # Foydalanuvchi ro'yxatdan o'tgan — telefon raqami bazada bor
    lead = await repo.leads.add_lead(user.user_id, "plagiat", phone=user.phone, details=document.file_name[:200])
    await notify_new_file_lead(
        bot, config.tg_bot.admin_ids, lead, message.from_user.full_name, message.from_user.username, document.file_id
    )
    await message.answer(texts.PLAGIAT_DONE.format(name=escape(user.real_name or message.from_user.full_name)))
    await show_main_menu(message, message.from_user)


@plagiat_router.message(PlagiatCheck.file)
async def plagiat_wrong(message: Message):
    await message.answer(texts.PLAGIAT_WRONG, reply_markup=cancel_kb())
