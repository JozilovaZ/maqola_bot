import asyncio
import logging
from html import escape
from pathlib import Path
from typing import Optional

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.callbacks import Nav, Service
from misc import texts
from misc.states import AlphabetConvert
from services.alphabet import Mode, Result, convert_docx, convert_plain

text_tools_router = Router()

# Telegram bot 20 MB dan katta faylni yuklab ololmaydi
MAX_SIZE = 20 * 1024 * 1024
# Bundan uzun matn xabar emas, .txt fayl bo'lib qaytadi
MAX_MESSAGE = 3500

# FSM'dagi "alphabet" qiymati: new — yangi alifbo, latcyr — Lotin ↔ Kirill (yo'nalish matnga qarab)
PROMPTS = {"new": texts.ALPHABET, "latcyr": texts.LATCYR}
FILE_SUFFIXES = {Mode.NEW: "yangi_alifbo", Mode.TO_LAT: "lotin", Mode.TO_CYR: "kirill"}


def text_tools_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✏️ Maqolani tahrirlash", callback_data=Service(key="edit"))
    keyboard.button(text="🌐 Maqolani tarjima qilish", callback_data=Service(key="translate"))
    keyboard.button(text="🔤 Yangi alifboga o‘girish", callback_data=Nav(to="alphabet"))
    keyboard.button(text="🔁 Lotin ↔ Kirill", callback_data=Nav(to="latcyr"))
    keyboard.button(text="💼 Barcha xizmatlar", callback_data=Nav(to="services"))
    keyboard.button(text="⬅️ Bosh menyu", callback_data=Nav(to="main"))
    keyboard.adjust(1, 1, 1, 1, 2)
    return keyboard.as_markup()


def convert_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✏️ Maqolani tahrirlash xizmati", callback_data=Service(key="edit"))
    keyboard.button(text="⬅️ Matn bilan ishlash", callback_data=Nav(to="text_tools"))
    keyboard.adjust(1)
    return keyboard.as_markup()


# ---------- Bo'lim ----------

@text_tools_router.message(Command("matn"))
async def cmd_text_tools(message: Message):
    await message.answer(texts.TEXT_TOOLS, reply_markup=text_tools_kb())


@text_tools_router.callback_query(Nav.filter(F.to == "text_tools"))
async def nav_text_tools(call: CallbackQuery):
    await call.answer()
    await call.message.answer(texts.TEXT_TOOLS, reply_markup=text_tools_kb())


# ---------- Yangi alifbo va Lotin ↔ Kirill: fayl yoki matn kutiladi ----------

async def ask_text(message: Message, state: FSMContext, kind: str):
    await state.set_state(AlphabetConvert.text)
    await state.update_data(alphabet=kind)
    await message.answer(PROMPTS[kind], reply_markup=convert_kb())


@text_tools_router.message(Command("alifbo"))
async def cmd_alphabet(message: Message, state: FSMContext):
    await ask_text(message, state, "new")


@text_tools_router.message(Command("kirill"))
async def cmd_latcyr(message: Message, state: FSMContext):
    await ask_text(message, state, "latcyr")


@text_tools_router.callback_query(Nav.filter(F.to.in_({"alphabet", "latcyr"})))
async def nav_convert(call: CallbackQuery, callback_data: Nav, state: FSMContext):
    await call.answer()
    await ask_text(call.message, state, "new" if callback_data.to == "alphabet" else "latcyr")


async def current_mode(state: FSMContext) -> Optional[Mode]:
    """None — Lotin ↔ Kirill: yo'nalish matnning o'ziga qarab tanlanadi."""
    return Mode.NEW if (await state.get_data()).get("alphabet", "new") == "new" else None


def done_text(result: Result) -> str:
    return texts.ALPHABET_DONE.format(direction=texts.ALPHABET_DIRECTIONS[result.mode.value], changed=result.changed)


@text_tools_router.message(AlphabetConvert.text, F.document)
async def convert_file(message: Message, state: FSMContext, bot: Bot):
    document = message.document
    suffix = Path(document.file_name or "").suffix.lower()
    if suffix not in {".docx", ".txt"}:
        await message.answer(texts.ALPHABET_WRONG, reply_markup=convert_kb())
        return
    if (document.file_size or 0) > MAX_SIZE:
        await message.answer(texts.ALPHABET_TOO_BIG, reply_markup=convert_kb())
        return

    mode = await current_mode(state)
    await bot.send_chat_action(message.chat.id, "upload_document")
    data = (await bot.download(document)).getvalue()
    try:
        if suffix == ".docx":
            # Katta faylda bir necha soniya ketadi — bot boshqalarga javob berishda davom etsin
            output, result = await asyncio.to_thread(convert_docx, data, mode)
        else:
            try:
                text = data.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = data.decode("cp1251")
            converted, result = convert_plain(text, mode)
            output = converted.encode("utf-8")
    except Exception as e:
        logging.warning(f"Matnni o'girish: fayl ochilmadi ({document.file_name}): {e}")
        await message.answer(texts.ALPHABET_BROKEN, reply_markup=convert_kb())
        return

    if not result.changed:
        await message.answer(texts.ALPHABET_NOTHING, reply_markup=convert_kb())
        return
    file_name = f"{Path(document.file_name).stem[:100]}_{FILE_SUFFIXES[result.mode]}{suffix}"
    await message.answer_document(
        BufferedInputFile(output, filename=file_name), caption=done_text(result), reply_markup=convert_kb()
    )


@text_tools_router.message(AlphabetConvert.text, F.text)
async def convert_message(message: Message, state: FSMContext):
    converted, result = convert_plain(message.text, await current_mode(state))
    if not result.changed:
        await message.answer(texts.ALPHABET_NOTHING, reply_markup=convert_kb())
        return
    if len(converted) <= MAX_MESSAGE:
        await message.answer(escape(converted))
        await message.answer(done_text(result), reply_markup=convert_kb())
    else:
        await message.answer_document(
            BufferedInputFile(converted.encode("utf-8"), filename=f"matn_{FILE_SUFFIXES[result.mode]}.txt"),
            caption=done_text(result),
            reply_markup=convert_kb(),
        )


@text_tools_router.message(AlphabetConvert.text)
async def convert_wrong(message: Message):
    await message.answer(texts.ALPHABET_WRONG, reply_markup=convert_kb())
