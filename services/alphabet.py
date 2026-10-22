"""Amaldagi o'zbek lotin yozuvidagi matnni yangi alifboga o'girish (OʻRQ–1184, 2026-yil 21-oktyabr).

Almashtiriladi: oʻ → ö, gʻ → ğ, sh → ş, ch → ç (katta harflari ham). Tutuq belgisi (maʼlumot, sanʼat) va
"ng" o'zgarmaydi. Kirill yozuvidagi matnga tegilmaydi.

Maqolalarda inglizcha matn (adabiyotlar ro'yxati, annotatsiya) ko'p uchraydi, "research", "Chemistry" kabi
so'zlar buzilmasligi uchun: inglizcha deb topilgan xatboshi butunlay, inglizcha ko'rinishdagi so'z esa alohida
o'tkazib yuboriladi. Bu taxminiy usul — natijani ko'zdan kechirish kerak.
"""
import re
from dataclasses import dataclass
from io import BytesIO

from docx import Document

# Oʻ va gʻ dagi belgi turlicha yoziladi: ʻ ‘ ' ` ’ ʼ
APOSTROPHES = "ʻ‘'`’ʼ"
WORD = re.compile(rf"[A-Za-z][A-Za-z{APOSTROPHES}]*")
O_G = re.compile(rf"([OoGg])[{APOSTROPHES}]")
SH_CH = re.compile(r"([SsCc])([Hh])")
NEW_O_G = {"O": "Ö", "o": "ö", "G": "Ğ", "g": "ğ"}

# O'zbek lotin yozuvida yo'q yoki juda kam uchraydigan harf birikmalari — bunday so'z inglizcha deb olinadi
FOREIGN = re.compile(r"w|c(?!h)|th|ph|ck|tion|ou|ear|[bcdfgklmnprstvz]y$|rch$")
ENGLISH_WORDS = {
    "the", "and", "of", "to", "for", "with", "is", "are", "was", "were", "by", "from", "this", "that", "which",
    "journal", "university", "research", "study", "analysis", "international", "science", "vol", "pp",
}
CYRILLIC = re.compile(r"[Ѐ-ӿ]")


def is_english(text: str) -> bool:
    words = [w.lower() for w in WORD.findall(text)]
    hits = sum(w in ENGLISH_WORDS for w in words)
    return hits >= 2 and hits >= len(words) * 0.08


def convert_word(word: str) -> str:
    if FOREIGN.search(word.lower()):
        return word
    word = O_G.sub(lambda m: NEW_O_G[m.group(1)], word)
    return SH_CH.sub(lambda m: ("Ş" if m.group(1) == "S" else "ş") if m.group(1) in "Ss"
                     else ("Ç" if m.group(1) == "C" else "ç"), word)


def convert_text(text: str) -> str:
    """Bitta xatboshi (yoki xatboshi bo'lagi). Inglizcha xatboshilarni chaqiruvchi o'zi aniqlaydi."""
    return WORD.sub(lambda m: convert_word(m.group(0)), text)


@dataclass
class Result:
    changed: int    # nechta so'z o'zgardi
    cyrillic: bool  # matnda kirill harflari ko'p — ehtimol fayl kirill yozuvida


def convert_plain(text: str) -> tuple[str, Result]:
    changed = 0
    lines = []
    for line in text.split("\n"):
        new = line if is_english(line) else convert_text(line)
        changed += sum(a != b for a, b in zip(WORD.findall(line), WORD.findall(new)))
        lines.append(new)
    return "\n".join(lines), Result(changed, len(CYRILLIC.findall(text)) > len(text) * 0.3)


def iter_paragraphs(container):
    """Xatboshilar: matn, jadvallar (ichma-ich ham), sarlavha va pastki kolontitullar."""
    yield from container.paragraphs
    for table in container.tables:
        for row in table.rows:
            for cell in row.cells:
                yield from iter_paragraphs(cell)


def convert_docx(data: bytes) -> tuple[bytes, Result]:
    """Word fayl: har bir "run" (bir xil formatdagi matn bo'lagi) alohida o'giriladi — shrift, qalinlik,
    jadvallar va rasmlar joyida qoladi."""
    document = Document(BytesIO(data))
    containers = [document]
    for section in document.sections:
        containers += [section.header, section.footer]

    changed, total, cyrillic = 0, 0, 0
    seen = set()
    for container in containers:
        for paragraph in iter_paragraphs(container):
            # Birlashtirilgan jadval kataklari bir necha marta qaytadi. id() emas, elementning o'zi saqlanadi:
            # o'chgan obyektning id'si qayta ishlatilishi mumkin
            if paragraph._p in seen:
                continue
            seen.add(paragraph._p)
            text = paragraph.text
            total += len(text)
            cyrillic += len(CYRILLIC.findall(text))
            if not text.strip() or is_english(text):
                continue
            for run in paragraph.runs:
                new = convert_text(run.text)
                if new != run.text:
                    changed += sum(a != b for a, b in zip(WORD.findall(run.text), WORD.findall(new)))
                    run.text = new

    buffer = BytesIO()
    document.save(buffer)
    return buffer.getvalue(), Result(changed, cyrillic > total * 0.3)
