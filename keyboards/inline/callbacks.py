from aiogram.filters.callback_data import CallbackData


class Nav(CallbackData, prefix="nav"):
    """Bo'limlar orasida o'tish. to — bo'lim nomi: main, about, consult, scopus, services, coauth."""
    to: str


class Service(CallbackData, prefix="svc"):
    """key: keyboards.inline.services.SERVICE_BUTTONS dagi kalit (scopus, wos, oak ...)"""
    key: str


class Faq(CallbackData, prefix="faq"):
    """Ko'p beriladigan savollar: index — texts.FAQ_ITEMS dagi tartib raqami."""
    index: int


class Order(CallbackData, prefix="ord"):
    """Xizmatga buyurtma. key — Service bilan bir xil."""
    key: str


class FieldPage(CallbackData, prefix="fld"):
    """Hammualliflik: soha mavzularining sahifasi (0 dan boshlanadi)."""
    field_id: int
    page: int = 0


class JournalPage(CallbackData, prefix="jrn"):
    """Jurnallar javoni: yo'nalishdagi jurnallar sahifasi (0 dan boshlanadi)."""
    direction_id: int
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


class BroadcastTarget(CallbackData, prefix="adm_bt"):
    """Rassilka kimga: direction_id — yo'nalish, 0 — hammaga."""
    direction_id: int


class AdminTopic(CallbackData, prefix="adm_t"):
    """Admin: mavzularni boshqarish.

    action: fields, field (id = field_id), topic (id = topic_id), slot (id = slot_id),
            delete / delete_yes / toggle_active / edit_base / edit_title / edit_prices (id = topic_id),
            add / field_rename / field_delete / field_delete_yes (id = field_id), field_add
    """
    action: str
    id: int = 0


class AdminJournal(CallbackData, prefix="adm_j"):
    """Admin: jurnallar javonini boshqarish.

    action: directions, direction (id = direction_id), add (id = direction_id), journal (id = journal_id),
            edit_title / edit_base / edit_url / delete / delete_yes (id = journal_id)
    """
    action: str
    id: int = 0


class ArticleForm(CallbackData, prefix="art_f"):
    """Hammualliflik uchun maqola yuborish: tugma bilan tanlanadigan qadamlar.

    field: direction (value = direction_id), base (value = misc.articles.BASES indeksi), send, cancel
    """
    field: str
    value: int = 0


class ArticleBrowse(CallbackData, prefix="art_b"):
    """Hammualliflik uchun maqolalar: yo'nalishdagi sahifa (0 dan boshlanadi)."""
    direction_id: int
    page: int = 0


class ArticleApply(CallbackData, prefix="art_a"):
    """Foydalanuvchi maqolaga hammuallif bo'lmoqchi."""
    id: int


class AdminArticle(CallbackData, prefix="adm_a"):
    """Admin: maqola holati va narxlari. action: approve (qayta joylash ham), reject, close, prices"""
    action: str
    id: int
