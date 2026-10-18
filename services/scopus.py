"""Jurnalni Elsevier Scopus Serial Title API orqali tekshirish.

Hujjat: https://dev.elsevier.com/documentation/SerialTitleAPI.wadl
ISSN bo'yicha: GET /content/serial/title/issn/{issn}
Nom bo'yicha:  GET /content/serial/title?title=...
"""
import datetime
import logging
import re
from dataclasses import dataclass
from typing import Optional

import aiohttp

API_URL = "https://api.elsevier.com/content/serial/title"
ISSN_RE = re.compile(r"^\d{4}-?\d{3}[\dXx]$")

# ASJC kodining birinchi ikki raqami → soha nomi
ASJC_AREAS = {
    "10": "Ko‘p tarmoqli",
    "11": "Qishloq xo‘jaligi va biologiya fanlari",
    "12": "San’at va gumanitar fanlar",
    "13": "Biokimyo, genetika va molekulyar biologiya",
    "14": "Biznes, menejment va buxgalteriya",
    "15": "Kimyoviy texnologiya",
    "16": "Kimyo",
    "17": "Kompyuter fanlari",
    "18": "Qaror qabul qilish fanlari",
    "19": "Yer va sayyoralar haqidagi fanlar",
    "20": "Iqtisodiyot, ekonometrika va moliya",
    "21": "Energetika",
    "22": "Muhandislik",
    "23": "Atrof-muhit fanlari",
    "24": "Immunologiya va mikrobiologiya",
    "25": "Materialshunoslik",
    "26": "Matematika",
    "27": "Tibbiyot",
    "28": "Nevrologiya",
    "29": "Hamshiralik ishi",
    "30": "Farmakologiya, toksikologiya va farmatsevtika",
    "31": "Fizika va astronomiya",
    "32": "Psixologiya",
    "33": "Ijtimoiy fanlar",
    "34": "Veterinariya",
    "35": "Stomatologiya",
    "36": "Sog‘liqni saqlash kasblari",
}


@dataclass
class Journal:
    title: str
    publisher: str
    issn: str          # "0028-0836" yoki "1932-6203 (E)"
    active: bool
    coverage: str      # "2006–2026"
    subjects: str      # "Ko‘p tarmoqli, Tibbiyot"


def _fmt_issn(value: str) -> str:
    value = re.sub(r"[^0-9Xx]", "", value or "").upper()
    return f"{value[:4]}-{value[4:]}" if len(value) == 8 else value


def _as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def parse_entry(entry: dict) -> Optional[Journal]:
    """Serial Title API javobidagi bitta "entry" ni Journal ga aylantiradi."""
    if not entry or "error" in entry or not entry.get("dc:title"):
        return None

    issn, eissn = entry.get("prism:issn"), entry.get("prism:eIssn")
    if issn:
        issn_label = _fmt_issn(issn)
    elif eissn:
        issn_label = f"{_fmt_issn(eissn)} (E)"
    else:
        issn_label = "—"

    codes = [str(area.get("@code", "")) for area in _as_list(entry.get("subject-area"))]
    subjects = dict.fromkeys(ASJC_AREAS[c[:2]] for c in codes if c[:2] in ASJC_AREAS)

    start, end = entry.get("coverageStartYear"), entry.get("coverageEndYear")
    coverage = f"{start}–{end}" if start and end and start != end else str(start or end or "—")
    # Qamrov o'tgan yildan oldin tugagan bo'lsa — jurnal endi indekslanmaydi
    active = not end or int(end) >= datetime.date.today().year - 1

    return Journal(
        title=entry["dc:title"],
        publisher=entry.get("dc:publisher") or "—",
        issn=issn_label,
        active=active,
        coverage=coverage,
        subjects=", ".join(subjects) or "—",
    )


def _pick(entries: list[dict], query: str) -> Optional[dict]:
    """Nom bo'yicha qidiruvda: aynan mos kelgan, bo'lmasa so'rov bilan boshlanadigan eng qisqa nom."""
    key = query.strip().casefold()
    titled = [e for e in entries if e.get("dc:title")]
    exact = [e for e in titled if e["dc:title"].casefold() == key]
    if exact:
        return exact[0]
    starts = [e for e in titled if e["dc:title"].casefold().startswith(key)]
    return min(starts, key=lambda e: len(e["dc:title"])) if starts else None


async def find_journal(query: str, api_key: str) -> Optional[Journal]:
    """ISSN yoki jurnal nomi bo'yicha qidiradi. Topilmasa yoki API xato bersa — None."""
    query = query.strip()
    if not api_key or not query:
        return None

    if ISSN_RE.match(query):
        url, params = f"{API_URL}/issn/{_fmt_issn(query)}", {}
    else:
        url, params = API_URL, {"title": query, "count": 25}
    headers = {"X-ELS-APIKey": api_key, "Accept": "application/json"}

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 404:
                    return None
                if response.status != 200:
                    logging.error(f"Scopus API xatosi {response.status}: {(await response.text())[:300]}")
                    return None
                data = await response.json()
    except Exception as e:
        logging.error(f"Scopus API'ga ulanib bo'lmadi: {e}")
        return None

    entries = _as_list(data.get("serial-metadata-response", {}).get("entry"))
    entry = entries[0] if url != API_URL else _pick(entries, query)
    return parse_entry(entry) if entry else None
