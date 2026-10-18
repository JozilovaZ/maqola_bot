from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.default.contact import share_contact_kb
from misc import texts


async def ask_contact(message: Message, state: FSMContext, text: str, reason: str, details: str | None = None):
    """Telefon raqamini so'rash: matn + alohida "⬇️" xabari "Kontaktni ulashish" tugmasi bilan.

    reason — raqam qaysi bo'limdan qoldirilgani (consult, order, ...), details — qo'shimcha ma'lumot
    (masalan, xizmat nomi). Ikkalasi FSM'da saqlanadi va raqam kelganda arizaga yoziladi.
    """
    await state.update_data(reason=reason, details=details)
    await message.answer(text)
    await message.answer(texts.CONTACT_ARROW, reply_markup=share_contact_kb())
