from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, TelegramObject

from handlers.users.registration import start_registration
from misc.states import Registration


class RegistrationMiddleware(BaseMiddleware):
    """Ro'yxatdan o'tmagan foydalanuvchi botning birorta bo'limiga kira olmaydi: har qanday xabar yoki
    tugmada ro'yxatdan o'tish boshlanadi. Ro'yxatdan o'tish savollariga javoblar handlerga o'tkaziladi.

    DatabaseMiddleware'dan keyin ulanadi (data["user"] — bazadagi foydalanuvchi).
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, CallbackQuery):
            chat = event.message.chat if event.message else None
        else:
            chat = event.chat

        user = data.get("user")
        if chat is None or chat.type != ChatType.PRIVATE or user is None or user.registered_at:
            return await handler(event, data)

        state: FSMContext = data["state"]
        if await state.get_state() in Registration.__all_states_names__:
            return await handler(event, data)

        # Adminlar ro'yxatdan o'tmasdan ham admin buyruqlaridan foydalana oladi; /start da esa ro'yxatdan
        # o'tish ularga ham ko'rsatiladi (sinab ko'rish uchun)
        is_start = isinstance(event, Message) and (event.text or "").split(maxsplit=1)[:1] == ["/start"]
        if event.from_user.id in data["config"].tg_bot.admin_ids and not is_start:
            return await handler(event, data)

        if isinstance(event, CallbackQuery):
            await event.answer()
        await start_registration(data["bot"], event.from_user, state)
