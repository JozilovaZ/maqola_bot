"""Rasm va fayllarni yuborish hamda admin yuklagan fayllarni saqlash.

Rasmlar media/ papkasida, PDF'lar files/ papkasida nomi bo'yicha qidiriladi (hero.jpg, hero.png —
kengaytmasi farqi yo'q). Fayl bo'lmasa, hech narsa yuborilmaydi.
PDF admin yuklagan asl nomi bilan saqlanadi: <joy>__<asl nom>.pdf — foydalanuvchi asl nomni ko'radi.
Telegram qaytargan file_id keshlanadi, fayl qayta yuklanmaydi.
"""
from pathlib import Path
from typing import Optional

from aiogram import Bot
from aiogram.types import FSInputFile, Message

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"
FILES_DIR = BASE_DIR / "files"

# /media da ko'rinadigan joylar: nom → admin uchun tavsif
PHOTO_SLOTS = {
    "hero": "🏠 Bosh sahifa",
    "about": "🏛 Fihria Academic haqida",
    "services": "💼 Xizmatlar",
    "svc_scopus": "📝 Xizmat: Scopus",
    "svc_wos": "📝 Xizmat: Web of Science",
    "svc_oak": "🎓 Xizmat: OAK",
    "svc_diss": "📚 Xizmat: Dissertatsiya",
    "svc_hirsh": "📈 Xizmat: Hirsh indeksi",
    "svc_conf": "🎤 Xizmat: Konferensiya",
    "svc_edit": "✏️ Xizmat: Tahrirlash",
    "svc_translate": "🌐 Xizmat: Tarjima",
    "coauth": "🤝 Hammualliflik",
    "coauth_topics": "🎯 Dolzarb mavzular",
    "coauth_field": "📌 Soha mavzulari",
}
# PDF joylari (files/ papkasi): hozircha yo'q, kerak bo'lsa shu yerga qo'shiladi
PDF_SLOTS: dict[str, str] = {}

_file_ids: dict[Path, str] = {}


def _directory(name: str) -> Path:
    return FILES_DIR if name in PDF_SLOTS else MEDIA_DIR


def _all_files(name: str) -> list[Path]:
    directory = _directory(name)
    found = list(directory.glob(f"{name}.*")) + list(directory.glob(f"{name}__*"))
    return sorted(p for p in found if p.is_file())


def find(name: str) -> Optional[Path]:
    files = _all_files(name)
    return files[0] if files else None


def _display_name(path: Path) -> str:
    return path.name.split("__", 1)[1] if "__" in path.name else path.name


async def send_photo(message: Message, name: str) -> None:
    path = find(name)
    if path is None:
        return
    sent = await message.answer_photo(_file_ids.get(path) or FSInputFile(path))
    _file_ids[path] = sent.photo[-1].file_id


async def send_document(message: Message, name: str) -> None:
    path = find(name)
    if path is None:
        return
    sent = await message.answer_document(_file_ids.get(path) or FSInputFile(path, filename=_display_name(path)))
    _file_ids[path] = sent.document.file_id


def delete(name: str) -> None:
    for path in _all_files(name):
        path.unlink()
        _file_ids.pop(path, None)


async def save_upload(
    bot: Bot, name: str, file_id: str, original_name: Optional[str], extension: str, reuse_file_id: bool = True
) -> Path:
    """Admin yuborgan faylni joyiga saqlaydi (eskisini o'chirib).

    reuse_file_id — file_id ni keshga yozish (qayta yuklamaslik uchun). Rasm "fayl" sifatida yuborilgan
    bo'lsa False: hujjatning file_id si bilan rasm yuborib bo'lmaydi.
    """
    delete(name)
    directory = _directory(name)
    directory.mkdir(parents=True, exist_ok=True)
    if name in PDF_SLOTS and original_name:
        safe = "".join(c for c in original_name if c not in '\\/:*?"<>|').strip() or f"{name}{extension}"
        path = directory / f"{name}__{safe}"
    else:
        path = directory / f"{name}{extension}"
    await bot.download(file_id, destination=path)
    if reuse_file_id:
        _file_ids[path] = file_id
    return path
