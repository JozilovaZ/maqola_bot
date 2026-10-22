from html import escape
from typing import Optional

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, MessageOriginUser, ReplyKeyboardRemove

from config import Config
from filters.admin import AdminFilter
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.default.admins import pick_admin_kb
from keyboards.inline.admin import admin_remove_kb, admins_kb
from keyboards.inline.callbacks import AdminManage
from misc.bot_commands import remove_admin_commands, set_admin_commands
from misc.states import AddAdmin

admin_admins_router = Router()
admin_admins_router.message.filter(AdminFilter())
admin_admins_router.callback_query.filter(AdminFilter())

ADD_PROMPT = (
    "👮 <b>Yangi admin qo‘shish</b>\n\n"
    "Quyidagilardan birini yuboring:\n"
    "• pastdagi «👤 Foydalanuvchini tanlash» tugmasi orqali kontaktni tanlang;\n"
    "• Telegram ID raqamini yozing, masalan: <code>123456789</code>;\n"
    "• @username yozing (u botga oldin /start bosgan bo‘lishi kerak);\n"
    "• undan kelgan istalgan xabarni shu yerga forward qiling.\n\n"
    "Bekor qilish: /cancel"
)
NEW_ADMIN_HELLO = (
    "👮 Sizga Fihria Academic botida <b>admin</b> huquqi berildi.\n\n"
    "Admin buyruqlari menyuda ko‘rinadi: /leads, /shelf, /topics, /articles, /media, /stat, /broadcast, /admins."
)


async def admin_name(repo: RequestsRepo, user_id: int) -> str:
    user = await repo.users.get(user_id)
    if user is None:
        return f"ID {user_id}"
    name = user.real_name or user.full_name
    return f"{name} (@{user.username})" if user.username else name


async def admins_view(repo: RequestsRepo, config: Config):
    lines = ["👮 <b>Adminlar</b>\n"]
    removable = []
    for user_id in config.tg_bot.admin_ids:
        name = await admin_name(repo, user_id)
        if user_id in config.tg_bot.main_admin_ids:
            lines.append(f"🔒 {escape(name)} — <code>{user_id}</code>, asosiy")
        else:
            lines.append(f"• {escape(name)} — <code>{user_id}</code>")
            removable.append((user_id, name))
    lines.append(
        "\n<i>🔒 Asosiy adminlar .env faylidagi ADMINS da yoziladi, ularni bu yerdan o‘chirib bo‘lmaydi. "
        "Adminlikdan olish uchun ismini bosing.</i>"
    )
    return "\n".join(lines), admins_kb(removable)


@admin_admins_router.message(Command("admins"))
async def cmd_admins(message: Message, repo: RequestsRepo, config: Config):
    text, markup = await admins_view(repo, config)
    await message.answer(text, reply_markup=markup)


@admin_admins_router.callback_query(AdminManage.filter(F.action == "list"))
async def admins_list(call: CallbackQuery, repo: RequestsRepo, config: Config):
    await call.answer()
    text, markup = await admins_view(repo, config)
    await call.message.edit_text(text, reply_markup=markup)


# ---------- Qo'shish ----------

@admin_admins_router.callback_query(AdminManage.filter(F.action == "add"))
async def admin_add(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(AddAdmin.user)
    await call.message.answer(ADD_PROMPT, reply_markup=pick_admin_kb())


async def resolve_user_id(message: Message, repo: RequestsRepo) -> tuple[Optional[int], Optional[str]]:
    """(Telegram ID, xato matni). Kontakt tanlash, forward, raqam yoki @username'dan ID topiladi."""
    if message.users_shared:
        return message.users_shared.user_ids[0], None
    if message.forward_origin is not None:
        if isinstance(message.forward_origin, MessageOriginUser):
            return message.forward_origin.sender_user.id, None
        return None, (
            "Bu foydalanuvchi forward qilingan xabarlarda profilini yashirgan. "
            "«👤 Foydalanuvchini tanlash» tugmasidan foydalaning yoki ID raqamini yozing."
        )
    value = (message.text or "").strip()
    if value.isdigit():
        return int(value), None
    if value.startswith("@") and len(value) > 1:
        user = await repo.users.get_by_username(value[1:])
        if user is None:
            return None, "Bu username bilan foydalanuvchi topilmadi — u botga hali /start bosmagan. ID raqamini yozing."
        return user.user_id, None
    return None, "Tushunmadim. ID raqam, @username yoki forward qilingan xabar yuboring.\n\nBekor qilish: /cancel"


@admin_admins_router.message(AddAdmin.user)
async def admin_add_user(message: Message, state: FSMContext, repo: RequestsRepo, bot: Bot, config: Config):
    user_id, error = await resolve_user_id(message, repo)
    if error:
        await message.answer(error, reply_markup=pick_admin_kb())
        return
    await state.set_state(None)
    if user_id in config.tg_bot.admin_ids:
        await message.answer("Bu foydalanuvchi allaqachon admin.", reply_markup=ReplyKeyboardRemove())
    else:
        await repo.admins.add(user_id, added_by=message.from_user.id)
        config.tg_bot.admin_ids.append(user_id)
        await set_admin_commands(bot, user_id)
        name = escape(await admin_name(repo, user_id))
        try:
            await bot.send_message(user_id, NEW_ADMIN_HELLO)
            note = ""
        except Exception:
            note = "\n\n⚠️ Unga xabar yuborib bo‘lmadi — u botga hali /start bosmagan. /start bosgach, admin buyruqlari ishlaydi."
        await message.answer(f"✅ {name} admin qilindi.{note}", reply_markup=ReplyKeyboardRemove())
    text, markup = await admins_view(repo, config)
    await message.answer(text, reply_markup=markup)


# ---------- Adminlikdan olish ----------

@admin_admins_router.callback_query(AdminManage.filter(F.action == "remove"))
async def admin_remove(call: CallbackQuery, callback_data: AdminManage, repo: RequestsRepo, config: Config):
    user_id = callback_data.id
    if user_id in config.tg_bot.main_admin_ids:
        await call.answer("Asosiy adminni o‘chirib bo‘lmaydi.", show_alert=True)
        return
    if user_id == call.from_user.id:
        await call.answer("O‘zingizni adminlikdan ola olmaysiz — buni boshqa admin qiladi.", show_alert=True)
        return
    await call.answer()
    name = escape(await admin_name(repo, user_id))
    await call.message.edit_text(
        f"👮 <b>{name}</b> (<code>{user_id}</code>) adminlikdan olinsinmi?", reply_markup=admin_remove_kb(user_id)
    )


@admin_admins_router.callback_query(AdminManage.filter(F.action == "remove_yes"))
async def admin_remove_yes(call: CallbackQuery, callback_data: AdminManage, repo: RequestsRepo, bot: Bot, config: Config):
    user_id = callback_data.id
    if user_id in config.tg_bot.main_admin_ids or user_id == call.from_user.id:
        await call.answer()
        return
    await repo.admins.remove(user_id)
    if user_id in config.tg_bot.admin_ids:
        config.tg_bot.admin_ids.remove(user_id)
    await remove_admin_commands(bot, user_id)
    await call.answer("Adminlikdan olindi")
    text, markup = await admins_view(repo, config)
    await call.message.edit_text(text, reply_markup=markup)
