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


class AlphabetConvert(StatesGroup):
    """Yangi alifboga o'girish: fayl yoki matn kutilmoqda (bir nechta ketma-ket yuborish mumkin)."""
    text = State()


class AddJournal(StatesGroup):
    title = State()
    base = State()
    url = State()
    description = State()


class EditJournal(StatesGroup):
    """Admin: jurnalning bitta qiymatini yozib yuborish. Nima tahrirlanayotgani FSM data'da: edit, edit_id."""
    value = State()


class EditDirection(StatesGroup):
    """Admin: yo'nalish nomi (yangi yoki o'zgartirilgan). FSM data'da: dir_edit (dir_add, dir_rename), dir_id."""
    value = State()


class AddAdmin(StatesGroup):
    """Admin: yangi adminning Telegram ID'si, @username'i yoki undan forward qilingan xabar."""
    user = State()


class ArticleSubmit(StatesGroup):
    """Hammualliflik uchun maqola: sarlavha → yo'nalish → baza → annotatsiya → o'rinlar narxi → fayl → tasdiq."""
    title = State()
    annotation = State()
    prices = State()
    file = State()


class ArticlePrices(StatesGroup):
    """Admin: maqola narxlarini o'zgartirish. Maqola id'si FSM data'da: prices_id."""
    value = State()


class ArticleReject(StatesGroup):
    """Admin: rad etish sababi. Maqola id'si FSM data'da: reject_id."""
    reason = State()


class Registration(StatesGroup):
    """Birinchi /start: ism-familiya → telefon → faoliyat yo'nalishi → yo'nalish."""
    full_name = State()
    phone = State()
    role = State()
    direction = State()
