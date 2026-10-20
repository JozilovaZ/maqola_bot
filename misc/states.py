from aiogram.fsm.state import State, StatesGroup


class ScopusCheck(StatesGroup):
    query = State()


class CoauthSuggest(StatesGroup):
    keywords = State()


class EditValue(StatesGroup):
    """Admin: bitta qiymatni yozib yuborish. Nima tahrirlanayotgani FSM data'da: edit, id."""
    value = State()


class MediaUpload(StatesGroup):
    file = State()


class BroadcastState(StatesGroup):
    message = State()


class AddTopic(StatesGroup):
    base = State()
    title = State()
    prices = State()


class PlagiatCheck(StatesGroup):
    file = State()


class AddJournal(StatesGroup):
    title = State()
    base = State()
    url = State()


class EditJournal(StatesGroup):
    """Admin: jurnalning bitta qiymatini yozib yuborish. Nima tahrirlanayotgani FSM data'da: edit, edit_id."""
    value = State()


class ArticleSubmit(StatesGroup):
    """Hammualliflik uchun maqola: sarlavha → yo'nalish → baza → annotatsiya → o'rinlar → fayl → tasdiq."""
    title = State()
    annotation = State()
    file = State()


class ArticleReject(StatesGroup):
    """Admin: rad etish sababi. Maqola id'si FSM data'da: reject_id."""
    reason = State()


class Registration(StatesGroup):
    """Birinchi /start: ism-familiya → telefon → faoliyat yo'nalishi → yo'nalish."""
    full_name = State()
    phone = State()
    role = State()
    direction = State()
