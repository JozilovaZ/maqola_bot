import logging
from dataclasses import dataclass

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramAPIError


@dataclass
class RequiredChat:
    title: str
    url: str


# guruh nomi va havolasi kamdan-kam o'zgaradi, har safar so'ramaslik uchun xotirada saqlanadi
_chat_cache: dict[str, RequiredChat] = {}

MEMBER_STATUSES = (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER)


async def _is_member(bot: Bot, chat_id: str, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    except TelegramAPIError as e:
        # bot guruhda yo'q yoki admin emas — sozlama xatosi sababli hammani to'sib qo'ymaymiz
        logging.error(f"Majburiy obuna: {chat_id} ni tekshirib bo'lmadi ({e}). Bot guruhda admin ekanini tekshiring.")
        return True

    if member.status in MEMBER_STATUSES:
        return True
    # cheklangan (restricted) foydalanuvchi ham guruh a'zosi bo'lishi mumkin
    return member.status == ChatMemberStatus.RESTRICTED and getattr(member, "is_member", False)


async def _get_chat_info(bot: Bot, chat_id: str) -> RequiredChat | None:
    if chat_id in _chat_cache:
        return _chat_cache[chat_id]

    try:
        chat = await bot.get_chat(chat_id)
        if chat.username:
            url = f"https://t.me/{chat.username}"
        else:
            # yopiq guruh: taklif havolasi (bot admin bo'lishi va "Taklif qilish" huquqi kerak)
            url = chat.invite_link or await bot.export_chat_invite_link(chat_id)
    except TelegramAPIError as e:
        logging.error(f"Majburiy obuna: {chat_id} havolasini olib bo'lmadi ({e})")
        return None

    _chat_cache[chat_id] = RequiredChat(title=chat.title or "Guruh", url=url)
    return _chat_cache[chat_id]


async def get_missing_chats(bot: Bot, user_id: int, chat_ids: list[str]) -> list[RequiredChat]:
    """Foydalanuvchi hali a'zo bo'lmagan guruh/kanallar ro'yxati. Bo'sh bo'lsa — hammasiga a'zo."""
    missing = []
    for chat_id in chat_ids:
        if await _is_member(bot, chat_id, user_id):
            continue
        info = await _get_chat_info(bot, chat_id)
        if info:
            missing.append(info)
    return missing
