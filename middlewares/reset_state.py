from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, TelegramObject


class ResetStateMiddleware(BaseMiddleware):
    """Tugma bosilganda yoki buyruq yuborilganda kutish holatini (masalan, kalit so'zlar) bekor qiladi.

    Aks holda foydalanuvchi "Taklif qoldirish"dan keyin boshqa bo'limga o'tib matn yozsa, u kalit so'z
    deb qabul qilinardi. Holat kerak bo'lgan handlerlar uni o'zi qayta o'rnatadi; FSM ma'lumotlari saqlanadi.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        is_command = isinstance(event, Message) and (event.text or "").startswith("/")
        state: FSMContext = data.get("state")
        if state and (is_command or not isinstance(event, Message)):
            # /cancel o'zi holatga qarab ishlaydi
            if not (is_command and event.text.startswith("/cancel")):
                await state.set_state(None)
        return await handler(event, data)
