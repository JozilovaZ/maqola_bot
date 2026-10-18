from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from infrastructure.database.models import Field
from keyboards.inline.callbacks import FieldPage, Nav


def coauth_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🎯 Individual tanlov", callback_data=Nav(to="coauth_individual"))
    keyboard.button(text="🎯 Dolzarb mavzalar tanlovini olish", callback_data=Nav(to="coauth_topics"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def coauth_topics_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Dolzarb mavzularni ko‘rish", callback_data=Nav(to="coauth_fields"))
    return keyboard.as_markup()


def fields_kb(fields: list[Field]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for field in fields:
        keyboard.button(text=field.title, callback_data=FieldPage(field_id=field.id))
    keyboard.adjust(1)
    return keyboard.as_markup()


def topics_page_kb(field_id: int, next_page: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Yana mavzularni olish", callback_data=FieldPage(field_id=field_id, page=next_page))
    keyboard.button(text="Hammualliflikka buyurtma berish", callback_data=Nav(to="coauth_order"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def coauth_final_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Hammualliflikka buyurtma berish", callback_data=Nav(to="coauth_order"))
    keyboard.button(text="Taklif qoldirish", callback_data=Nav(to="coauth_suggest"))
    keyboard.button(text="Bosh menyuga qaytish", callback_data=Nav(to="main"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def suggest_done_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Bosh menyuga qaytish", callback_data=Nav(to="main"))
    return keyboard.as_markup()
