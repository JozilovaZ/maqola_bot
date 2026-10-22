import asyncio
import datetime
import logging
from html import escape
from pathlib import Path
from typing import Optional

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Document, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config
from keyboards.inline.callbacks import Nav, Service
from misc import texts
from misc.states import AlphabetConvert, SavodxonCheck
from services import savodxon
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
    keyboard.button(text="📝 Savodxon — imlo tekshiruvi", callback_data=Nav(to="savodxon"))
    keyboard.button(text="💼 Barcha xizmatlar", callback_data=Nav(to="services"))
    keyboard.button(text="⬅️ Bosh menyu", callback_data=Nav(to="main"))
    keyboard.adjust(1, 1, 1, 1, 1, 2)
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


async def accepted_suffix(message: Message, document: Document) -> Optional[str]:
    """.docx yoki .txt va 20 MB gacha bo'lsa — kengaytma, aks holda foydalanuvchiga sababi aytiladi."""
    suffix = Path(document.file_name or "").suffix.lower()
    if suffix not in {".docx", ".txt"}:
        await message.answer(texts.ALPHABET_WRONG, reply_markup=convert_kb())
        return None
    if (document.file_size or 0) > MAX_SIZE:
        await message.answer(texts.ALPHABET_TOO_BIG, reply_markup=convert_kb())
        return None
    return suffix


def decode_text(data: bytes) -> str:
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data.decode("cp1251")


@text_tools_router.message(AlphabetConvert.text, F.document)
async def convert_file(message: Message, state: FSMContext, bot: Bot):
    document = message.document
    suffix = await accepted_suffix(message, document)
    if suffix is None:
        return

    mode = await current_mode(state)
    await bot.send_chat_action(message.chat.id, "upload_document")
    data = (await bot.download(document)).getvalue()
    try:
        if suffix == ".docx":
            # Katta faylda bir necha soniya ketadi — bot boshqalarga javob berishda davom etsin
            output, result = await asyncio.to_thread(convert_docx, data, mode)
        else:
            converted, result = convert_plain(decode_text(data), mode)
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


# ---------- Savodxon — imlo tekshiruvi (Claude API) ----------

# Kunlik cheklov: {user_id: (sana, tekshiruvlar soni)}. Xotirada — bot qayta ishga tushsa, nolga qaytadi
usage: dict[int, tuple[datetime.date, int]] = {}
# Tekshiruvi davom etayotgan foydalanuvchilar — bir vaqtda faqat bittadan
busy: set[int] = set()
# Natija xabarida ko'rsatiladigan tuzatishlar soni
MAX_ITEMS = 30


def used_today(user_id: int) -> int:
    day, count = usage.get(user_id, (None, 0))
    return count if day == datetime.date.today() else 0


def render_report(report: savodxon.Report) -> str:
    lines = [
        f"• <s>{escape(c.wrong)}</s> → <b>{escape(c.right)}</b>" + (f" — {escape(c.note)}" if c.note else "")
        for c in report.corrections[:MAX_ITEMS]
    ]
    if len(report.corrections) > MAX_ITEMS:
        lines.append(texts.SAVODXON_MORE.format(count=len(report.corrections) - MAX_ITEMS))
    return texts.SAVODXON_DONE.format(total=report.total, items="\n".join(lines))[:4096]


async def ask_savodxon(message: Message, state: FSMContext, config: Config):
    if not config.savodxon.api_key:
        await message.answer(texts.SAVODXON_OFF, reply_markup=convert_kb())
        return
    await state.set_state(SavodxonCheck.text)
    await message.answer(texts.SAVODXON.format(limit=config.savodxon.daily_limit), reply_markup=convert_kb())


@text_tools_router.message(Command("savodxon"))
async def cmd_savodxon(message: Message, state: FSMContext, config: Config):
    await ask_savodxon(message, state, config)


@text_tools_router.callback_query(Nav.filter(F.to == "savodxon"))
async def nav_savodxon(call: CallbackQuery, state: FSMContext, config: Config):
    await call.answer()
    await ask_savodxon(call.message, state, config)


async def run_check(message: Message, config: Config, check) -> Optional[tuple]:
    """Cheklovlar, "kuting" xabari va xatolar. check — korutina qaytaruvchi funksiya; natijasi qaytariladi."""
    user_id = message.from_user.id
    is_admin = user_id in config.tg_bot.admin_ids
    if not is_admin and used_today(user_id) >= config.savodxon.daily_limit:
        await message.answer(texts.SAVODXON_LIMIT.format(limit=config.savodxon.daily_limit), reply_markup=convert_kb())
        return None
    if user_id in busy:
        await message.answer(texts.SAVODXON_BUSY)
        return None

    busy.add(user_id)
    wait = await message.answer(texts.SAVODXON_WAIT)
    try:
        result = await check()
    except savodxon.TooLong:
        await message.answer(texts.SAVODXON_TOO_LONG, reply_markup=convert_kb())
        return None
    except savodxon.SavodxonError:
        await message.answer(texts.SAVODXON_OFF, reply_markup=convert_kb())
        return None
    except Exception as e:
        logging.warning(f"Savodxon: fayl ochilmadi: {e}")
        await message.answer(texts.ALPHABET_BROKEN, reply_markup=convert_kb())
        return None
    finally:
        busy.discard(user_id)
        try:
            await wait.delete()
        except Exception:
            pass
    usage[user_id] = (datetime.date.today(), used_today(user_id) + 1)
    return result


@text_tools_router.message(SavodxonCheck.text, F.document)
async def savodxon_file(message: Message, bot: Bot, config: Config):
    document = message.document
    suffix = await accepted_suffix(message, document)
    if suffix is None:
        return
    data = (await bot.download(document)).getvalue()
    settings = config.savodxon

    async def check():
        if suffix == ".docx":
            return await savodxon.check_docx(data, settings.api_key, settings.model)
        fixed, report = await savodxon.check_plain(decode_text(data), settings.api_key, settings.model)
        return fixed.encode("utf-8"), report

    result = await run_check(message, config, check)
    if result is None:
        return
    output, report = result
    if not report.corrections:
        await message.answer(texts.SAVODXON_CLEAN, reply_markup=convert_kb())
        return
    await message.answer_document(
        BufferedInputFile(output, filename=f"{Path(document.file_name).stem[:100]}_tuzatilgan{suffix}"),
    )
    await message.answer(render_report(report), reply_markup=convert_kb())


@text_tools_router.message(SavodxonCheck.text, F.text)
async def savodxon_text(message: Message, config: Config):
    settings = config.savodxon
    result = await run_check(
        message, config, lambda: savodxon.check_plain(message.text, settings.api_key, settings.model)
    )
    if result is None:
        return
    fixed, report = result
    if not report.corrections:
        await message.answer(texts.SAVODXON_CLEAN, reply_markup=convert_kb())
        return
    if len(fixed) <= MAX_MESSAGE:
        await message.answer(escape(fixed))
    else:
        await message.answer_document(BufferedInputFile(fixed.encode("utf-8"), filename="matn_tuzatilgan.txt"))
    await message.answer(render_report(report), reply_markup=convert_kb())


@text_tools_router.message(SavodxonCheck.text)
async def savodxon_wrong(message: Message):
    await message.answer(texts.ALPHABET_WRONG, reply_markup=convert_kb())
