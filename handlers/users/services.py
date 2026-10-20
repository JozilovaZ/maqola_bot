from html import escape

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, User

from config import Config
from infrastructure.database.models import User as DbUser
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.inline.callbacks import Nav, Order, Service
from keyboards.inline.services import SERVICE_BUTTONS, service_kb, services_kb
from misc import texts
from misc.contact import request_lead
from misc.media import send_photo

services_router = Router()


async def show_services(message: Message, user: User):
    await send_photo(message, "services")
    await message.answer(texts.SERVICES.format(name=escape(user.full_name)), reply_markup=services_kb())


@services_router.message(Command("services"))
async def cmd_services(message: Message):
    await show_services(message, message.from_user)


@services_router.callback_query(Nav.filter(F.to == "services"))
async def nav_services(call: CallbackQuery):
    await call.answer()
    await show_services(call.message, call.from_user)


@services_router.callback_query(Service.filter())
async def show_service(call: CallbackQuery, callback_data: Service, config: Config):
    await call.answer()
    key = callback_data.key
    await send_photo(call.message, f"svc_{key}")
    await call.message.answer(texts.SERVICE_TEXTS[key], reply_markup=service_kb(key, config.links.services[key]))


@services_router.callback_query(Order.filter())
async def order_service(call: CallbackQuery, callback_data: Order, state: FSMContext, user: DbUser, repo: RequestsRepo, bot: Bot, config: Config):
    await call.answer()
    await request_lead(
        call.message, state, user, repo, bot, config, texts.ORDER, reason="order", details=SERVICE_BUTTONS[callback_data.key]
    )


# ---------- Bepul maslahat ----------

@services_router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext, user: DbUser, repo: RequestsRepo, bot: Bot, config: Config):
    await request_lead(message, state, user, repo, bot, config, texts.CONSULT, reason="consult")


@services_router.callback_query(Nav.filter(F.to == "consult"))
async def nav_consult(call: CallbackQuery, state: FSMContext, user: DbUser, repo: RequestsRepo, bot: Bot, config: Config):
    await call.answer()
    await request_lead(call.message, state, user, repo, bot, config, texts.CONSULT, reason="consult")
