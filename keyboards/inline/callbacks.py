from aiogram.filters.callback_data import CallbackData


class Nav(CallbackData, prefix="nav"):
    """Bo'limlar orasida o'tish. to — bo'lim nomi: main, about, consult, scopus, services, coauth."""
    to: str


class Service(CallbackData, prefix="svc"):
    """key: scopus, wos, oak, diss, hirsh, conf"""
    key: str


class Order(CallbackData, prefix="ord"):
    """Xizmatga buyurtma. key — Service bilan bir xil."""
    key: str


class FieldPage(CallbackData, prefix="fld"):
    """Hammualliflik: soha mavzularining sahifasi (0 dan boshlanadi)."""
    field_id: int
    page: int = 0


class LeadStatus(CallbackData, prefix="adm_l"):
    """Ariza holatini o'zgartirish. status: contacted, closed, rejected"""
    id: int
    status: str


class MediaSlot(CallbackData, prefix="adm_m"):
    """/media: action — list, open, delete; key — misc.media dagi joy nomi (hero, about ...)."""
    action: str
    key: str = ""


class Broadcast(CallbackData, prefix="adm_b"):
    """Rassilkani tasdiqlash. action: send, cancel"""
    action: str


class AdminTopic(CallbackData, prefix="adm_t"):
    """Admin: mavzularni boshqarish.

    action: fields, field (id = field_id), topic (id = topic_id), slot (id = slot_id),
            delete / delete_yes / toggle_active / edit_base / edit_title / edit_prices (id = topic_id),
            add / field_rename / field_delete / field_delete_yes (id = field_id), field_add
    """
    action: str
    id: int = 0
