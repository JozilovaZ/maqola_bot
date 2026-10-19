from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.enums import ChatType
from aiogram.types import CallbackQuery, Message, TelegramObject

from keyboards.inline.callbacks import CheckSub
from keyboards.inline.subscription import subscription_kb
from misc import texts
from services.subscription import get_missing_chats


class SubscriptionMiddleware(BaseMiddleware):
    """Majburiy obuna: foydalanuvchi .env dagi REQUIRED_CHATS ga a'zo bo'lmaguncha botdan foydalana olmaydi.

    Faqat shaxsiy chatda ishlaydi, adminlar tekshirilmaydi. "✅ Tekshirish" tugmasi
    handlers/users/subscription.py da o'zi tekshiradi.
    """

    def __init__(self, chat_ids: list[str]) -> None:
        self.chat_ids = chat_ids

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not self.chat_ids:
            return await handler(event, data)

        if isinstance(event, CallbackQuery):
            chat = event.message.chat if event.message else None
            if event.data == CheckSub().pack():
                return await handler(event, data)
        else:
            chat = event.chat

        if chat is None or chat.type != ChatType.PRIVATE:
            return await handler(event, data)
        if event.from_user.id in data["config"].tg_bot.admin_ids:
            return await handler(event, data)

        bot: Bot = data["bot"]
        missing = await get_missing_chats(bot, event.from_user.id, self.chat_ids)
        if not missing:
            return await handler(event, data)

        # obuna bo'lmagan — handler chaqirilmaydi, o'rniga obuna xabari yuboriladi
        if isinstance(event, CallbackQuery):
            await event.answer()
        await bot.send_message(event.from_user.id, texts.SUBSCRIBE, reply_markup=subscription_kb(missing))
