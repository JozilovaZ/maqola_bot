"""O'zbek matnini bir yozuvdan boshqasiga o'girish.

Usullar (Mode):
- NEW     — yangi lotin alifbosiga (OʻRQ–1184, 2026-yil 21-oktyabr): oʻ → ö, gʻ → ğ, sh → ş, ch → ç.
            Kirill so'zlar ham to'g'ridan-to'g'ri yangi alifboga o'giriladi.
- TO_LAT  — kirill → amaldagi lotin (1995-yilgi qoidalar).
- TO_CYR  — lotin (amaldagi yoki yangi) → kirill.
Lotin ↔ Kirill bo'limida yo'nalish matnning qaysi yozuvi ko'pligiga qarab tanlanadi (detect_mode).

Maqolalarda inglizcha matn (adabiyotlar ro'yxati, annotatsiya) ko'p uchraydi, "research", "Chemistry" kabi
so'zlar buzilmasligi uchun: inglizcha deb topilgan xatboshining lotin so'zlari butunlay, inglizcha ko'rinishdagi
so'z esa alohida o'tkazib yuboriladi. Havolalar, email va ISSN/DOI kabi qisqartmalarga tegilmaydi.
Bu taxminiy usul — natijani ko'zdan kechirish kerak.
"""
import re
from dataclasses import dataclass
from enum import Enum
from io import BytesIO

from docx import Document


class Mode(str, Enum):
    NEW = "new"
    TO_LAT = "to_lat"
    TO_CYR = "to_cyr"


# Oʻ va gʻ dagi belgi turlicha yoziladi: ʻ ‘ ' ` ’ ʼ
APOSTROPHES = "ʻ‘'`’ʼ"
OKINA = "ʻ"   # oʻ, gʻ dagi rasmiy belgi
TUTUQ = "ʼ"   # maʼlumot, sanʼat
LATIN = "A-Za-zÖöĞğŞşÇç"
CYR = "Ѐ-ӿ"
TOKEN = re.compile(
    r"(?P<skip>https?://\S+|www\.\S+|\S+@\S+\.\w+)"
    rf"|(?P<lat>[{LATIN}][{LATIN}{APOSTROPHES}]*)"
    rf"|(?P<cyr>[{CYR}]+)"
)
LATIN_WORD = re.compile(rf"[{LATIN}][{LATIN}{APOSTROPHES}]*")
CYRILLIC_CHAR = re.compile(rf"[{CYR}]")
LATIN_CHAR = re.compile(rf"[{LATIN}]")

# O'zbek lotin yozuvida yo'q yoki juda kam uchraydigan harf birikmalari — bunday so'z inglizcha deb olinadi
FOREIGN = re.compile(r"w|c(?!h)|th|ph|ck|tion|ou|ear|[bcdfgklmnprstvz]y$|rch$")
ENGLISH_WORDS = {
    "the", "and", "of", "to", "for", "with", "is", "are", "was", "were", "by", "from", "this", "that", "which",
    "journal", "university", "research", "study", "analysis", "international", "science", "vol", "pp",
}
# Kirillga o'girilmaydigan xalqaro qisqartmalar
KEEP_LATIN = {"ISSN", "ISBN", "DOI", "URL", "PDF", "ORCID", "SCOPUS", "WOS", "IT", "AI", "SI", "UDK", "UDC"}


def is_english(text: str) -> bool:
    words = [w.lower() for w in LATIN_WORD.findall(text)]
    hits = sum(w in ENGLISH_WORDS for w in words)
    return hits >= 2 and hits >= len(words) * 0.08


def is_foreign(word: str) -> bool:
    return bool(FOREIGN.search(word.lower()))


# ---------- Lotin (amaldagi) → yangi alifbo ----------

O_G = re.compile(rf"([OoGg])[{APOSTROPHES}]")
SH_CH = re.compile(r"([SsCc])([Hh])")
NEW_O_G = {"O": "Ö", "o": "ö", "G": "Ğ", "g": "ğ"}
NEW_SH_CH = {"S": "Ş", "s": "ş", "C": "Ç", "c": "ç"}


def latin_to_new(word: str) -> str:
    word = O_G.sub(lambda m: NEW_O_G[m.group(1)], word)
    return SH_CH.sub(lambda m: NEW_SH_CH[m.group(1)], word)


# ---------- Kirill → lotin ----------

CYR_VOWELS = set("аеёиоуэюяў")
CYR_TO_LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ё": "yo", "ж": "j", "з": "z", "и": "i", "й": "y",
    "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "x", "ч": "ch", "ш": "sh", "щ": "sh", "ъ": TUTUQ, "ы": "i", "ь": "", "э": "e", "ю": "yu",
    "я": "ya", "ў": "o" + OKINA, "қ": "q", "ғ": "g" + OKINA, "ҳ": "h",
}
CYR_TO_NEW = {**CYR_TO_LAT, "ч": "ç", "ш": "ş", "щ": "ş", "ў": "ö", "ғ": "ğ"}


def cyrillic_to_latin(word: str, new: bool = False) -> str:
    table = CYR_TO_NEW if new else CYR_TO_LAT
    upper_word = len(word) > 1 and word.isupper()
    result = []
    for i, char in enumerate(word):
        lower = char.lower()
        prev = word[i - 1].lower() if i else ""
        if lower == "е":
            # So'z boshida va unli, ъ, ь dan keyin — ye (yer, oyeb), qolgan joyda — e
            latin = "ye" if not prev or prev in CYR_VOWELS or prev in "ъь" else "e"
        elif lower == "ц":
            # So'z boshida va undoshdan keyin — s (sex, konsert), unlidan keyin — ts (litsey)
            latin = "ts" if prev in CYR_VOWELS else "s"
        else:
            latin = table.get(lower, char)
        if char.isupper() and latin:
            latin = latin.upper() if upper_word or len(latin) == 1 else latin[0].upper() + latin[1:]
        result.append(latin)
    return "".join(result)


# ---------- Lotin → kirill ----------

LAT_DIGRAPHS = {"sh": "ш", "ch": "ч", "yo": "ё", "yu": "ю", "ya": "я", "ye": "е"}
LAT_TO_CYR = {
    "a": "а", "b": "б", "c": "ц", "d": "д", "e": "е", "f": "ф", "g": "г", "h": "ҳ", "i": "и", "j": "ж",
    "k": "к", "l": "л", "m": "м", "n": "н", "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с", "t": "т",
    "u": "у", "v": "в", "w": "в", "x": "х", "y": "й", "z": "з", "ö": "ў", "ğ": "ғ", "ş": "ш", "ç": "ч",
}


def latin_to_cyrillic(word: str) -> str:
    lower = word.lower()
    result = []
    i = 0
    while i < len(word):
        char, low = word[i], lower[i]
        nxt = lower[i + 1] if i + 1 < len(word) else ""
        if low in "og" and nxt and nxt in APOSTROPHES:
            cyr, size = ("ў" if low == "o" else "ғ"), 2
        elif low in APOSTROPHES:
            # s'h (Is'hoq) — harflarni ajratadi, o'zi yozilmaydi; boshqa joyda tutuq → ъ; oxirida — qo'shtirnoq
            if not nxt or not nxt.isalpha():
                cyr = char
            elif nxt == "h" and i and lower[i - 1] in "sc":
                cyr = ""
            else:
                cyr = "ъ"
            size = 1
        elif lower[i:i + 2] in LAT_DIGRAPHS:
            cyr, size = LAT_DIGRAPHS[lower[i:i + 2]], 2
        elif low == "e" and i == 0:
            cyr, size = "э", 1
        else:
            cyr, size = LAT_TO_CYR.get(low, char), 1
        if char.isupper():
            cyr = cyr.upper()
        result.append(cyr)
        i += size
    return "".join(result)


# ---------- Matn, xatboshi, fayl ----------

def convert_text(text: str, mode: Mode, english: bool = False) -> tuple[str, int]:
    """(yangi matn, o'zgargan so'zlar soni). english — xatboshi inglizcha: lotin so'zlarga tegilmaydi."""
    changed = 0

    def replace(match: re.Match) -> str:
        nonlocal changed
        word = match.group(0)
        if match.group("cyr"):
            new = word if mode == Mode.TO_CYR else cyrillic_to_latin(word, new=mode == Mode.NEW)
        elif match.group("lat") and not english and not is_foreign(word):
            if mode == Mode.NEW:
                new = latin_to_new(word)
            elif mode == Mode.TO_CYR and word.upper() not in KEEP_LATIN:
                new = latin_to_cyrillic(word)
            else:
                new = word
        else:
            new = word
        changed += new != word
        return new

    return TOKEN.sub(replace, text), changed


def detect_mode(paragraphs: list[str]) -> Mode:
    """Lotin ↔ Kirill: kirill harflari ko'p bo'lsa — lotinga, aks holda — kirillga. Inglizcha xatboshi va so'zlar
    (adabiyotlar ro'yxati, ISSN) hisobga olinmaydi — kirill maqoladagi inglizcha manbalar yo'nalishni buzmasin."""
    cyrillic = latin = 0
    for text in paragraphs:
        cyrillic += len(CYRILLIC_CHAR.findall(text))
        if not is_english(text):
            latin += sum(
                len(LATIN_CHAR.findall(word)) for word in LATIN_WORD.findall(text)
                if not is_foreign(word) and word.upper() not in KEEP_LATIN
            )
    return Mode.TO_LAT if cyrillic > latin else Mode.TO_CYR


@dataclass
class Result:
    mode: Mode
    changed: int  # nechta so'z o'zgardi


def convert_plain(text: str, mode: Mode | None = None) -> tuple[str, Result]:
    """mode=None — Lotin ↔ Kirill, yo'nalish matnga qarab tanlanadi."""
    mode = mode or detect_mode(text.split("\n"))
    changed = 0
    lines = []
    for line in text.split("\n"):
        new, count = convert_text(line, mode, english=is_english(line))
        changed += count
        lines.append(new)
    return "\n".join(lines), Result(mode, changed)


def iter_paragraphs(container):
    """Xatboshilar: matn, jadvallar (ichma-ich ham)."""
    yield from container.paragraphs
    for table in container.tables:
        for row in table.rows:
            for cell in row.cells:
                yield from iter_paragraphs(cell)


def convert_docx(data: bytes, mode: Mode | None = None) -> tuple[bytes, Result]:
    """Word fayl: har bir "run" (bir xil formatdagi matn bo'lagi) alohida o'giriladi — shrift, qalinlik,
    jadvallar va rasmlar joyida qoladi. mode=None — Lotin ↔ Kirill, yo'nalish fayl matniga qarab."""
    document = Document(BytesIO(data))
    containers = [document]
    for section in document.sections:
        containers += [section.header, section.footer]

    paragraphs = []
    # Birlashtirilgan jadval kataklari bir necha marta qaytadi. id() emas, elementning o'zi saqlanadi:
    # o'chgan obyektning id'si qayta ishlatilishi mumkin
    seen = set()
    for container in containers:
        for paragraph in iter_paragraphs(container):
            if paragraph._p not in seen:
                seen.add(paragraph._p)
                paragraphs.append(paragraph)

    mode = mode or detect_mode([p.text for p in paragraphs])
    changed = 0
    for paragraph in paragraphs:
        text = paragraph.text
        if not text.strip():
            continue
        english = is_english(text)
        for run in paragraph.runs:
            new, count = convert_text(run.text, mode, english)
            if count:
                changed += count
                run.text = new

    buffer = BytesIO()
    document.save(buffer)
    return buffer.getvalue(), Result(mode, changed)
