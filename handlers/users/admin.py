from html import escape
from typing import Optional

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from filters.admin import AdminFilter
from infrastructure.database.models import Topic
from infrastructure.database.repo.requests import RequestsRepo
from keyboards.inline.admin import (
    admin_delete_kb, admin_field_kb, admin_fields_kb, admin_topic_kb, field_delete_kb,
)
from keyboards.inline.callbacks import AdminTopic
from misc.states import AddJournal, AddTopic, BroadcastState, EditJournal, EditValue, MediaUpload
from misc.topics import render_topic

admin_router = Router()
admin_router.message.filter(AdminFilter())
admin_router.callback_query.filter(AdminFilter())

PRICES_EXAMPLE = "Masalan: <code>550 540 530 510 490</code>"


def parse_prices(text: str) -> Optional[list[int]]:
    parts = text.replace(",", " ").split()
    return [int(p) for p in parts] if parts and all(p.isdigit() for p in parts) else None


# ---------- Hammualliflik mavzularini boshqarish (/topics) ----------

async def fields_view(repo: RequestsRepo):
    fields = await repo.topics.list_fields()
    counts = await repo.topics.count_by_field()
    return "📋 <b>Hammualliflik mavzulari</b>\n\nSohani tanlang (qavsda — ko‘rinadigan mavzular soni):", \
        admin_fields_kb(fields, counts)


async def field_view(repo: RequestsRepo, field_id: int):
    field = await repo.topics.get_field(field_id)
    topics = await repo.topics.field_topics(field_id, include_hidden=True)
    lines = [f"📂 <b>{escape(field.title)}</b>\n"]
    lines += [
        f"{'' if t.active else '🙈 '}#{t.id} {escape(t.base)} | {escape(t.title[:60])} — {t.free_slots} ta bo‘sh joy"
        for t in topics
    ] or ["Hozircha mavzu yo‘q."]
    if any(not t.active for t in topics):
        lines.append("\n🙈 — yashirilgan, foydalanuvchilarga ko‘rinmaydi")
    return "\n".join(lines), admin_field_kb(field_id, topics)


def topic_view(topic: Topic) -> str:
    text = render_topic(topic)
    if not topic.active:
        text += "\n\n🙈 <b>Yashirilgan</b> — foydalanuvchilarga ko‘rinmaydi."
    return text


@admin_router.message(Command("topics"))
async def cmd_topics(message: Message, state: FSMContext, repo: RequestsRepo):
    await state.set_state(None)
    text, markup = await fields_view(repo)
    await message.answer(text, reply_markup=markup)


@admin_router.callback_query(AdminTopic.filter(F.action == "fields"))
async def admin_fields(call: CallbackQuery, repo: RequestsRepo):
    await call.answer()
    text, markup = await fields_view(repo)
    await call.message.edit_text(text, reply_markup=markup)


@admin_router.callback_query(AdminTopic.filter(F.action == "field"))
async def admin_field(call: CallbackQuery, callback_data: AdminTopic, repo: RequestsRepo):
    await call.answer()
    if await repo.topics.get_field(callback_data.id) is None:
        return
    text, markup = await field_view(repo, callback_data.id)
    await call.message.edit_text(text, reply_markup=markup)


@admin_router.callback_query(AdminTopic.filter(F.action == "topic"))
async def admin_topic(call: CallbackQuery, callback_data: AdminTopic, repo: RequestsRepo):
    await call.answer()
    topic = await repo.topics.get_topic(callback_data.id)
    if topic is None:
        return
    await call.message.edit_text(topic_view(topic), reply_markup=admin_topic_kb(topic))


@admin_router.callback_query(AdminTopic.filter(F.action == "slot"))
async def admin_toggle_slot(call: CallbackQuery, callback_data: AdminTopic, repo: RequestsRepo):
    slot = await repo.topics.toggle_slot(callback_data.id)
    if slot is None:
        await call.answer()
        return
    await call.answer("Sotilgan deb belgilandi" if slot.sold else "Bo‘sh deb belgilandi")
    topic = await repo.topics.get_topic(slot.topic_id)
    await repo.session.refresh(topic, ["slots"])
    await call.message.edit_text(topic_view(topic), reply_markup=admin_topic_kb(topic))


@admin_router.callback_query(AdminTopic.filter(F.action == "toggle_active"))
async def admin_toggle_active(call: CallbackQuery, callback_data: AdminTopic, repo: RequestsRepo):
    topic = await repo.topics.get_topic(callback_data.id)
    if topic is None:
        await call.answer()
        return
    await repo.topics.update_topic(topic.id, active=not topic.active)
    await repo.session.refresh(topic)
    await call.answer("Mavzu ko‘rsatiladi" if topic.active else "Mavzu yashirildi")
    await call.message.edit_text(topic_view(topic), reply_markup=admin_topic_kb(topic))


@admin_router.callback_query(AdminTopic.filter(F.action == "delete"))
async def admin_delete(call: CallbackQuery, callback_data: AdminTopic, repo: RequestsRepo):
    await call.answer()
    topic = await repo.topics.get_topic(callback_data.id)
    if topic is None:
        return
    await call.message.edit_text(
        render_topic(topic) + "\n\n<b>Shu mavzuni o‘chirasizmi?</b>",
        reply_markup=admin_delete_kb(topic),
    )


@admin_router.callback_query(AdminTopic.filter(F.action == "delete_yes"))
async def admin_delete_yes(call: CallbackQuery, callback_data: AdminTopic, repo: RequestsRepo):
    topic = await repo.topics.get_topic(callback_data.id)
    if topic is None:
        await call.answer()
        return
    field_id = topic.field_id
    await repo.topics.delete_topic(topic.id)
    await call.answer("Mavzu o‘chirildi")
    text, markup = await field_view(repo, field_id)
    await call.message.edit_text(text, reply_markup=markup)


# ---------- Sohani o'chirish ----------

@admin_router.callback_query(AdminTopic.filter(F.action == "field_delete"))
async def admin_field_delete(call: CallbackQuery, callback_data: AdminTopic, repo: RequestsRepo):
    await call.answer()
    field = await repo.topics.get_field(callback_data.id)
    if field is None:
        return
    count = len(await repo.topics.field_topics(field.id, include_hidden=True))
    warning = f"\nUndagi <b>{count} ta mavzu</b> ham o‘chadi." if count else ""
    await call.message.edit_text(
        f"«{escape(field.title)}» sohasini o‘chirasizmi?{warning}", reply_markup=field_delete_kb(field.id)
    )


@admin_router.callback_query(AdminTopic.filter(F.action == "field_delete_yes"))
async def admin_field_delete_yes(call: CallbackQuery, callback_data: AdminTopic, repo: RequestsRepo):
    await repo.topics.delete_field(callback_data.id)
    await call.answer("Soha o‘chirildi")
    text, markup = await fields_view(repo)
    await call.message.edit_text(text, reply_markup=markup)


# ---------- Bitta qiymatni tahrirlash: mavzu bazasi / nomi / narxlari, soha nomi ----------

EDIT_PROMPTS = {
    "edit_base": "Yangi baza va kvartilni yozing.\nMasalan: <code>Scopus Q3</code> yoki <code>Web of Science Q4</code>",
    "edit_title": "Mavzuning yangi nomini yozing.",
    "edit_prices": "Yangi narxlarni ($) 1-o‘rindan boshlab bo‘sh joy bilan yozing.\n" + PRICES_EXAMPLE
                   + "\nO‘rinlar soni o‘zgarishi mumkin; mavjud o‘rinlarning «sotilgan» belgisi saqlanadi.",
    "field_add": "Yangi soha nomini yozing.",
    "field_rename": "Sohaning yangi nomini yozing.",
}


@admin_router.callback_query(AdminTopic.filter(F.action.in_(EDIT_PROMPTS)))
async def admin_edit_start(call: CallbackQuery, callback_data: AdminTopic, state: FSMContext, repo: RequestsRepo):
    await call.answer()
    current = ""
    if callback_data.action in ("edit_base", "edit_title", "edit_prices"):
        topic = await repo.topics.get_topic(callback_data.id)
        if topic is None:
            return
        value = {
            "edit_base": topic.base,
            "edit_title": topic.title,
            "edit_prices": " ".join(str(s.price) for s in topic.slots),
        }[callback_data.action]
        current = f"\n\nHozirgisi: <code>{escape(value)}</code>"
    elif callback_data.action == "field_rename":
        field = await repo.topics.get_field(callback_data.id)
        current = f"\n\nHozirgisi: <code>{escape(field.title)}</code>" if field else ""
    await state.set_state(EditValue.value)
    await state.update_data(edit=callback_data.action, edit_id=callback_data.id)
    await call.message.answer(EDIT_PROMPTS[callback_data.action] + current + "\n\nBekor qilish: /cancel")


@admin_router.message(Command("cancel"), StateFilter(AddJournal, AddTopic, BroadcastState, EditJournal, EditValue, MediaUpload))
async def admin_cancel(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.answer("Bekor qilindi.")


@admin_router.message(EditValue.value, F.text)
async def admin_edit_value(message: Message, state: FSMContext, repo: RequestsRepo):
    data = await state.get_data()
    action, item_id, value = data.get("edit"), data.get("edit_id"), message.text.strip()

    if action == "edit_prices":
        prices = parse_prices(value)
        if prices is None:
            await message.answer("Faqat raqamlar bo‘lsin. " + PRICES_EXAMPLE)
            return
        await repo.topics.set_prices(item_id, prices)
    elif action == "edit_base":
        await repo.topics.update_topic(item_id, base=value)
    elif action == "edit_title":
        await repo.topics.update_topic(item_id, title=value)
    elif action == "field_add":
        field = await repo.topics.add_field(value)
        item_id = field.id
    elif action == "field_rename":
        await repo.topics.rename_field(item_id, value)
    await state.set_state(None)

    if action.startswith("field_"):
        text, markup = await field_view(repo, item_id)
    else:
        topic = await repo.topics.get_topic(item_id)
        await repo.session.refresh(topic)
        await repo.session.refresh(topic, ["slots"])
        text, markup = topic_view(topic), admin_topic_kb(topic)
    await message.answer("✅ Saqlandi\n\n" + text, reply_markup=markup)


# ---------- Yangi mavzu qo'shish ----------

@admin_router.callback_query(AdminTopic.filter(F.action == "add"))
async def admin_add(call: CallbackQuery, callback_data: AdminTopic, state: FSMContext):
    await call.answer()
    await state.set_state(AddTopic.base)
    await state.update_data(field_id=callback_data.id)
    await call.message.answer(
        "Baza va kvartilni yozing.\nMasalan: <code>Scopus Q3</code> yoki <code>Web of Science Q4</code>\n\n"
        "Bekor qilish: /cancel"
    )


@admin_router.message(AddTopic.base, F.text)
async def admin_add_base(message: Message, state: FSMContext):
    await state.update_data(base=message.text.strip())
    await state.set_state(AddTopic.title)
    await message.answer("Mavzu nomini yozing.")


@admin_router.message(AddTopic.title, F.text)
async def admin_add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddTopic.prices)
    await message.answer("Muallif o‘rinlari narxlarini ($) 1-o‘rindan boshlab bo‘sh joy bilan yozing.\n" + PRICES_EXAMPLE)


@admin_router.message(AddTopic.prices, F.text)
async def admin_add_prices(message: Message, state: FSMContext, repo: RequestsRepo):
    prices = parse_prices(message.text)
    if prices is None:
        await message.answer("Faqat raqamlar bo‘lsin. " + PRICES_EXAMPLE)
        return
    data = await state.get_data()
    await state.set_state(None)
    topic = await repo.topics.add_topic(data["field_id"], data["base"], data["title"], prices)
    await message.answer("✅ Mavzu qo‘shildi:\n\n" + render_topic(topic), reply_markup=admin_topic_kb(topic))
