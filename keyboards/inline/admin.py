from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from infrastructure.database.models import Direction, Field, Topic
from keyboards.inline.callbacks import AdminTopic, Broadcast, BroadcastTarget, LeadStatus, MediaSlot
from misc import media
from misc.media import PDF_SLOTS, PHOTO_SLOTS


def media_list_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for key, label in {**PHOTO_SLOTS, **PDF_SLOTS}.items():
        mark = "✅" if media.uploaded(key) else "🖼" if media.default(key) else "➖"
        keyboard.button(text=f"{mark} {label}", callback_data=MediaSlot(action="open", key=key))
    keyboard.adjust(1)
    return keyboard.as_markup()


def media_slot_kb(key: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    if media.uploaded(key):
        text = "🗑 O‘chirish (standart rasm qaytadi)" if media.default(key) else "🗑 O‘chirish"
        keyboard.button(text=text, callback_data=MediaSlot(action="delete", key=key))
    keyboard.button(text="⬅️ Ro‘yxat", callback_data=MediaSlot(action="list"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def lead_status_kb(lead_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📞 Bog‘lanildi", callback_data=LeadStatus(id=lead_id, status="contacted"))
    keyboard.button(text="✅ Yopildi", callback_data=LeadStatus(id=lead_id, status="closed"))
    keyboard.button(text="❌ Rad etildi", callback_data=LeadStatus(id=lead_id, status="rejected"))
    keyboard.adjust(3)
    return keyboard.as_markup()


def admin_fields_kb(fields: list[Field], counts: dict[int, int]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for field in fields:
        keyboard.button(
            text=f"{field.title} ({counts.get(field.id, 0)})",
            callback_data=AdminTopic(action="field", id=field.id),
        )
    keyboard.adjust(2)
    keyboard.row(InlineKeyboardButton(
        text="➕ Soha qo‘shish", callback_data=AdminTopic(action="field_add").pack()
    ))
    return keyboard.as_markup()


def admin_field_kb(field_id: int, topics: list[Topic]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for topic in topics:
        hidden = "" if topic.active else "🙈 "
        keyboard.button(
            text=f"{hidden}#{topic.id} {topic.title[:40]}", callback_data=AdminTopic(action="topic", id=topic.id)
        )
    keyboard.button(text="➕ Mavzu qo‘shish", callback_data=AdminTopic(action="add", id=field_id))
    keyboard.button(text="✏️ Soha nomini o‘zgartirish", callback_data=AdminTopic(action="field_rename", id=field_id))
    keyboard.button(text="🗑 Sohani o‘chirish", callback_data=AdminTopic(action="field_delete", id=field_id))
    keyboard.button(text="⬅️ Sohalar", callback_data=AdminTopic(action="fields"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def admin_topic_kb(topic: Topic) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for slot in topic.slots:
        status = "❌ sotilgan" if slot.sold else "✅ bo‘sh"
        keyboard.button(
            text=f"{slot.position}-o‘rin — {slot.price}$: {status}",
            callback_data=AdminTopic(action="slot", id=slot.id),
        )
    keyboard.adjust(1)
    keyboard.row(
        InlineKeyboardButton(text="🏷 Baza", callback_data=AdminTopic(action="edit_base", id=topic.id).pack()),
        InlineKeyboardButton(text="✏️ Nomi", callback_data=AdminTopic(action="edit_title", id=topic.id).pack()),
        InlineKeyboardButton(text="💲 Narxlar", callback_data=AdminTopic(action="edit_prices", id=topic.id).pack()),
    )
    keyboard.row(InlineKeyboardButton(
        text="👁 Ko‘rsatish" if not topic.active else "🙈 Yashirish",
        callback_data=AdminTopic(action="toggle_active", id=topic.id).pack(),
    ))
    keyboard.row(InlineKeyboardButton(
        text="🗑 Mavzuni o‘chirish", callback_data=AdminTopic(action="delete", id=topic.id).pack()
    ))
    keyboard.row(InlineKeyboardButton(
        text="⬅️ Orqaga", callback_data=AdminTopic(action="field", id=topic.field_id).pack()
    ))
    return keyboard.as_markup()


def broadcast_target_kb(directions: list[Direction], counts: dict[int, int], total: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=f"👥 Hammaga ({total})", callback_data=BroadcastTarget(direction_id=0))
    for direction in directions:
        keyboard.button(
            text=f"{direction.title} ({counts.get(direction.id, 0)})",
            callback_data=BroadcastTarget(direction_id=direction.id),
        )
    keyboard.button(text="❌ Bekor qilish", callback_data=Broadcast(action="cancel"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def broadcast_confirm_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✅ Yuborish", callback_data=Broadcast(action="send"))
    keyboard.button(text="❌ Bekor qilish", callback_data=Broadcast(action="cancel"))
    keyboard.adjust(2)
    return keyboard.as_markup()


def admin_delete_kb(topic: Topic) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Ha, o‘chirish", callback_data=AdminTopic(action="delete_yes", id=topic.id))
    keyboard.button(text="Yo‘q", callback_data=AdminTopic(action="topic", id=topic.id))
    keyboard.adjust(2)
    return keyboard.as_markup()


def field_delete_kb(field_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Ha, o‘chirish", callback_data=AdminTopic(action="field_delete_yes", id=field_id))
    keyboard.button(text="Yo‘q", callback_data=AdminTopic(action="field", id=field_id))
    keyboard.adjust(2)
    return keyboard.as_markup()
