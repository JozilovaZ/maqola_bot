import asyncio
import logging
from typing import Any, Awaitable, Callable, Union
from aiogram import Bot, exceptions
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def send_message(
        bot: Bot,
        user_id: Union[int, str],
        text: str,
        disable_notification: bool = False,
        reply_markup: InlineKeyboardMarkup = None,
) -> bool:
    """
    Xavfsiz xabar yuboruvchi funksiya.

    :param bot: Bot obyekti.
    :param user_id: Foydalanuvchi ID si (int yoki str formatida, str bo‘lsa faqat raqamlardan iborat bo‘lishi kerak).
    :param text: Yuboriladigan xabar matni.
    :param disable_notification: Bildirishnoma ovozsiz yuboriladimi (False - ovozli, True - ovozsiz).
    :param reply_markup: Inline klaviatura (agar mavjud bo‘lsa).
    :return: Xabar muvaffaqiyatli yuborilgan bo‘lsa True, aks holda False.
    """
    try:
        # Xabarni chiroyli formatlash uchun Markdown ishlatamiz
        formatted_text = f"📬 *Yangilik!* \n{text}"
        await bot.send_message(
            user_id,
            formatted_text,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except exceptions.TelegramBadRequest as e:
        logging.error(f"Telegram server xatosi: Chat topilmadi [ID:{user_id}]")
        return False
    except exceptions.TelegramForbiddenError:
        logging.error(f"Foydalanuvchi [ID:{user_id}]: TelegramForbiddenError - bot bloklangan yoki chat mavjud emas")
        return False
    except exceptions.TelegramRetryAfter as e:
        logging.error(f"Foydalanuvchi [ID:{user_id}]: Flood limit oshdi. {e.retry_after} soniya kuting.")
        await asyncio.sleep(e.retry_after)
        # Qayta urinish
        return await send_message(bot, user_id, text, disable_notification, reply_markup)
    except exceptions.TelegramAPIError:
        logging.exception(f"Foydalanuvchi [ID:{user_id}]: Telegram API xatosi")
        return False
    else:
        logging.info(f"Foydalanuvchi [ID:{user_id}]: Xabar muvaffaqiyatli yuborildi")
        return True


async def broadcast(
        bot: Bot,
        users: list[Union[str, int]],
        text: str,
        disable_notification: bool = False,
        reply_markup: InlineKeyboardMarkup = None,
) -> int:
    """
    Ommaviy xabar yuboruvchi funksiya.

    :param bot: Bot obyekti.
    :param users: Foydalanuvchi ID lari ro‘yxati.
    :param text: Yuboriladigan xabar matni.
    :param disable_notification: Bildirishnoma ovozsiz yuboriladimi.
    :param reply_markup: Inline klaviatura (agar mavjud bo‘lsa).
    :return: Muvaffaqiyatli yuborilgan xabarlar soni.
    """
    count = 0
    try:
        for user_id in users:
            if await send_message(bot, user_id, text, disable_notification, reply_markup):
                count += 1
            await asyncio.sleep(0.05)  # Telegram cheklovi: soniyada 20 ta xabar
    finally:
        logging.info(f"{count} ta xabar muvaffaqiyatli yuborildi.")
    return count


async def deliver(
        user_ids: list[int],
        send: Callable[[int], Awaitable[Any]],
) -> tuple[int, list[int], int]:
    """
    send(user_id) ni har bir foydalanuvchi uchun chaqiradi: flood limitda kutadi, soniyada 20 tadan oshirmaydi.

    :return: (yuborilganlar soni, botni bloklaganlar ID lari, boshqa xatolar soni)
    """
    sent, blocked, failed = 0, [], 0
    for user_id in user_ids:
        try:
            await send(user_id)
            sent += 1
        except exceptions.TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            try:
                await send(user_id)
                sent += 1
            except exceptions.TelegramAPIError:
                failed += 1
        except exceptions.TelegramForbiddenError:
            blocked.append(user_id)
        except exceptions.TelegramAPIError as e:
            logging.error(f"Rassilka [ID:{user_id}]: {e}")
            failed += 1
        await asyncio.sleep(0.05)  # Telegram cheklovi: soniyada 20 ta xabar
    logging.info(f"Rassilka: {sent} yuborildi, {len(blocked)} bloklagan, {failed} xato")
    return sent, blocked, failed


async def copy_to_users(
        bot: Bot,
        user_ids: list[int],
        from_chat_id: int,
        message_id: int,
) -> tuple[int, list[int], int]:
    """Admin yuborgan xabarni (matn, rasm, video, fayl ...) o'zgarishsiz har bir foydalanuvchiga nusxalaydi."""
    return await deliver(user_ids, lambda user_id: bot.copy_message(user_id, from_chat_id, message_id))


async def send_to_users(
        bot: Bot,
        user_ids: list[int],
        text: str,
        reply_markup: InlineKeyboardMarkup = None,
) -> tuple[int, list[int], int]:
    """Bot o'zi tuzgan xabarni (masalan, yangi maqola haqida) tugmalari bilan har bir foydalanuvchiga yuboradi."""
    return await deliver(user_ids, lambda user_id: bot.send_message(user_id, text, reply_markup=reply_markup))


# Qo‘shimcha: Inline klaviatura yaratish uchun misol
def create_broadcast_keyboard():
    """Ommaviy xabar uchun inline klaviatura yaratadi."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="ℹ️ Batafsil ma'lumot", callback_data="more_info")
    keyboard.button(text="📞 Bog‘lanish", callback_data="contact")
    keyboard.adjust(2)
    return keyboard.as_markup()