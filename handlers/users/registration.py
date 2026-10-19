import re
from html import escape

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, User

from config import Config
from handlers.users.start import show_main_menu
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.default.contact import share_contact_kb
from keyboards.default.registration import direction_kb, role_kb, university_kb
from misc import texts
from misc.states import Registration
from services.notify import notify_new_user

registration_router = Router()


async def start_registration(bot: Bot, user: User, state: FSMContext):
    """Ro'yxatdan o'tishni boshlash. RegistrationMiddleware ro'yxatdan o'tmagan foydalanuvchi uchun chaqiradi."""
    await state.set_state(Registration.full_name)
    await bot.send_message(
        user.id,
        texts.REG_START.format(name=escape(user.full_name)),
        reply_markup=ReplyKeyboardRemove(),
    )


def clean_text(message: Message, max_len: int) -> str | None:
    """Bo'shliqlarni tozalaydi; javob juda qisqa/uzun yoki buyruq bo'lsa — None."""
    value = " ".join(message.text.split())
    if len(value) < 2 or len(value) > max_len or value.startswith("/"):
        return None
    return value


@registration_router.message(Registration.full_name, F.text)
async def reg_full_name(message: Message, state: FSMContext):
    name = clean_text(message, 128)
    if not name or len(name.split()) < 2:
        await message.answer(texts.REG_NAME_INVALID)
        return
    await state.update_data(real_name=name)
    await state.set_state(Registration.phone)
    await message.answer(texts.REG_PHONE, reply_markup=share_contact_kb())


async def save_phone(message: Message, state: FSMContext, phone: str):
    await state.update_data(phone=phone)
    await state.set_state(Registration.role)
    await message.answer(texts.REG_ROLE, reply_markup=role_kb())


@registration_router.message(Registration.phone, F.contact)
async def reg_phone_contact(message: Message, state: FSMContext):
    if message.contact.user_id != message.from_user.id:
        await message.answer(texts.CONTACT_NOT_OWN, reply_markup=share_contact_kb())
        return
    phone = message.contact.phone_number
    await save_phone(message, state, phone if phone.startswith("+") else f"+{phone}")


@registration_router.message(Registration.phone, F.text)
async def reg_phone_text(message: Message, state: FSMContext):
    digits = re.sub(r"[\s\-()]", "", message.text).lstrip("+")
    if not digits.isdigit() or not 9 <= len(digits) <= 15:
        await message.answer(texts.REG_PHONE_INVALID, reply_markup=share_contact_kb())
        return
    if len(digits) == 9:
        # mahalliy ko'rinish: 901234567 -> +998901234567
        digits = "998" + digits
    await save_phone(message, state, f"+{digits}")


@registration_router.message(Registration.role, F.text)
async def reg_role(message: Message, state: FSMContext):
    role = next((key for key, title in texts.REG_ROLES.items() if title == message.text), None)
    if not role:
        await message.answer(texts.REG_CHOOSE_BUTTON, reply_markup=role_kb())
        return
    await state.update_data(role=role, custom_input=False)
    await state.set_state(Registration.study_place)
    hint = texts.REG_STUDY_PLACE_HINT.format(other=texts.REG_UNIVERSITY_OTHER)
    await message.answer(texts.REG_STUDY_PLACE[role] + hint, reply_markup=university_kb())


async def pick_option(
    message: Message,
    state: FSMContext,
    options: list[str],
    other: str,
    custom_prompt: str,
    keyboard: ReplyKeyboardMarkup,
) -> str | None:
    """Tugmadan tanlash yoki "Boshqa" bosib qo'lda yozish. Javob hali tayyor bo'lmasa — None."""
    if message.text == other:
        # ro'yxatda yo'q — keyingi xabarda qo'lda yoziladi
        await state.update_data(custom_input=True)
        await message.answer(custom_prompt, reply_markup=ReplyKeyboardRemove())
        return None
    if message.text in options:
        return message.text
    if (await state.get_data()).get("custom_input"):
        value = clean_text(message, 256)
        if not value:
            await message.answer(texts.REG_TEXT_INVALID)
        return value
    await message.answer(texts.REG_CHOOSE_BUTTON, reply_markup=keyboard)
    return None


@registration_router.message(Registration.study_place, F.text)
async def reg_study_place(message: Message, state: FSMContext):
    study_place = await pick_option(
        message, state, texts.REG_UNIVERSITIES, texts.REG_UNIVERSITY_OTHER, texts.REG_STUDY_PLACE_CUSTOM,
        university_kb(),
    )
    if not study_place:
        return
    await state.update_data(study_place=study_place, custom_input=False)
    await state.set_state(Registration.direction)
    await message.answer(texts.REG_DIRECTION, reply_markup=direction_kb())


@registration_router.message(Registration.direction, F.text)
async def reg_direction(message: Message, state: FSMContext, bot: Bot, config: Config, repo: RequestsRepo):
    direction = message.text
    if direction not in texts.REG_DIRECTIONS:
        await message.answer(texts.REG_CHOOSE_BUTTON, reply_markup=direction_kb())
        return
    data = await state.get_data()
    await state.clear()

    user = await repo.users.register(
        message.from_user.id,
        real_name=data["real_name"],
        phone=data["phone"],
        role=data["role"],
        study_place=data["study_place"],
        direction=direction,
    )
    await message.answer(texts.REG_DONE.format(name=escape(user.real_name)), reply_markup=ReplyKeyboardRemove())
    await notify_new_user(bot, config.tg_bot.admin_ids, user)
    await show_main_menu(message, message.from_user)


@registration_router.message(StateFilter(Registration))
async def reg_wrong_type(message: Message, state: FSMContext):
    """Ro'yxatdan o'tish paytida rasm, stiker va h.k. yuborilsa."""
    if await state.get_state() == Registration.phone.state:
        await message.answer(texts.REG_PHONE_INVALID, reply_markup=share_contact_kb())
    else:
        await message.answer(texts.REG_TEXT_ONLY)
