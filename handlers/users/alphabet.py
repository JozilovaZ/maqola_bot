import asyncio
import logging
from html import escape
from pathlib import Path

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.callbacks import Nav, Service
from misc import texts
from misc.states import AlphabetConvert
from services.alphabet import Result, convert_docx, convert_plain

alphabet_router = Router()

# Telegram bot 20 MB dan katta faylni yuklab ololmaydi
MAX_SIZE = 20 * 1024 * 1024
# Bundan uzun matn xabar emas, .txt fayl bo'lib qaytadi
MAX_MESSAGE = 3500


def alphabet_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✏️ Maqolani tahrirlash xizmati", callback_data=Service(key="edit"))
    keyboard.button(text="⬅️ Bosh menyu", callback_data=Nav(to="main"))
    keyboard.adjust(1)
    return keyboard.as_markup()


async def ask_text(message: Message, state: FSMContext):
    await state.set_state(AlphabetConvert.text)
    await message.answer(texts.ALPHABET, reply_markup=alphabet_kb())


@alphabet_router.message(Command("alifbo"))
async def cmd_alphabet(message: Message, state: FSMContext):
    await ask_text(message, state)


@alphabet_router.callback_query(Nav.filter(F.to == "alphabet"))
async def nav_alphabet(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await ask_text(call.message, state)


async def answer_result(message: Message, result: Result) -> bool:
    """O'zgarish bo'lmasa sababini aytadi va False qaytaradi."""
    if result.changed:
        return True
    await message.answer(texts.ALPHABET_CYRILLIC if result.cyrillic else texts.ALPHABET_NOTHING, reply_markup=alphabet_kb())
    return False


def new_name(file_name: str, suffix: str) -> str:
    return f"{Path(file_name).stem[:100]}_yangi_alifbo{suffix}"


@alphabet_router.message(AlphabetConvert.text, F.document)
async def alphabet_file(message: Message, bot: Bot):
    document = message.document
    suffix = Path(document.file_name or "").suffix.lower()
    if suffix not in {".docx", ".txt"}:
        await message.answer(texts.ALPHABET_WRONG, reply_markup=alphabet_kb())
        return
    if (document.file_size or 0) > MAX_SIZE:
        await message.answer(texts.ALPHABET_TOO_BIG, reply_markup=alphabet_kb())
        return

    await bot.send_chat_action(message.chat.id, "upload_document")
    data = (await bot.download(document)).getvalue()
    try:
        if suffix == ".docx":
            # Katta faylda bir necha soniya ketadi — bot boshqalarga javob berishda davom etsin
            output, result = await asyncio.to_thread(convert_docx, data)
        else:
            try:
                text = data.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = data.decode("cp1251")
            converted, result = convert_plain(text)
            output = converted.encode("utf-8")
    except Exception as e:
        logging.warning(f"Alifbo: fayl ochilmadi ({document.file_name}): {e}")
        await message.answer(texts.ALPHABET_BROKEN, reply_markup=alphabet_kb())
        return

    if await answer_result(message, result):
        await message.answer_document(
            BufferedInputFile(output, filename=new_name(document.file_name, suffix)),
            caption=texts.ALPHABET_DONE.format(changed=result.changed),
            reply_markup=alphabet_kb(),
        )


@alphabet_router.message(AlphabetConvert.text, F.text)
async def alphabet_text(message: Message):
    converted, result = convert_plain(message.text)
    if not await answer_result(message, result):
        return
    if len(converted) <= MAX_MESSAGE:
        await message.answer(escape(converted))
        await message.answer(texts.ALPHABET_DONE.format(changed=result.changed), reply_markup=alphabet_kb())
    else:
        await message.answer_document(
            BufferedInputFile(converted.encode("utf-8"), filename="matn_yangi_alifbo.txt"),
            caption=texts.ALPHABET_DONE.format(changed=result.changed),
            reply_markup=alphabet_kb(),
        )


@alphabet_router.message(AlphabetConvert.text)
async def alphabet_wrong(message: Message):
    await message.answer(texts.ALPHABET_WRONG, reply_markup=alphabet_kb())
