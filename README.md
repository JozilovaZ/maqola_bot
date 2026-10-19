# Maqola bot

Ilmiy maqolalar bo'yicha Telegram bot: foydali materiallar, xizmatlar, Scopus'da jurnalni tekshirish,
hammualliflik mavzulari va arizalar (telefon raqamlar) yig'ish. @Mirzo_MA_bot asosida yaratilgan.

[aiogram_3_shablon](https://github.com/davronovuz/aiogram_3_shablon) shabloni asosida: aiogram 3, PostgreSQL,
SQLAlchemy 2, Alembic, Docker.

## Imkoniyatlar

**Foydalanuvchi uchun** — `/start` (`/hero`), `/guides`, `/about`, `/services`, `/help`, `/scopus_check`,
`/co_authorship`:
- Foydali materiallar: chek-listlar (PDF) va blog (Mini App)
- Akademiya haqida, 6 ta xizmat, buyurtma va bepul maslahat — telefon raqam "Kontaktni ulashish" orqali
- Scopus'da jurnalni ISSN yoki nom bo'yicha tekshirish (Elsevier API)
- Hammualliflik: sohalar → mavzular (narx, bo'sh o'rinlar) → buyurtma yoki mavzu taklifi
- Boshqa har qanday xabar adminlarga yuboriladi

**Admin uchun** (`.env` dagi `ADMINS`):

| Buyruq | Vazifasi |
|---|---|
| `/leads`, `/lead_N` | Ochiq arizalar; holat: 📞 Bog‘lanildi / ✅ Yopildi / ❌ Rad etildi |
| `/export` | Barcha arizalar Excel faylida |
| `/stat` | Foydalanuvchilar va arizalar statistikasi |
| `/broadcast` | Hammaga xabar yuborish (ko'rib chiqib, tasdiqlab) |
| `/topics` | Hammualliflik sohalari va mavzularini boshqarish |
| `/media` | Bo'limlar rasmlari va PDF chek-listlarni yuklash |
| reply | Arizaga yoki foydalanuvchi xabariga reply qilsangiz — javob bot nomidan unga boradi |

Matnlar: `misc/texts.py`. Yangi arizalar adminlarga holat tugmalari bilan keladi.

**Majburiy obuna** — `.env` dagi `REQUIRED_CHATS` ga guruh/kanal `@username` yoki ID sini (`-100...`) yozing
(bir nechtasi vergul bilan). Foydalanuvchi a'zo bo'lmaguncha bot faqat obuna xabarini ko'rsatadi; adminlar
tekshirilmaydi. Bot o'sha guruhda **admin** bo'lishi shart (yopiq guruh uchun "Taklif qilish" huquqi bilan).

## Kompyuterda ishga tushirish

```bash
python -m venv venv
venv\Scripts\pip install -r requirements.txt     # Linux/macOS: venv/bin/pip
copy .env.dist .env                               # BOT_TOKEN, ADMINS, POSTGRES_* ni to'ldiring
# PostgreSQL'da POSTGRES_DB nomli baza yarating
venv\Scripts\alembic upgrade head
venv\Scripts\python bot.py
```

## Serverga chiqarish (Docker)

Serverda (Ubuntu) Docker o'rnatilgan bo'lishi kerak: `curl -fsSL https://get.docker.com | sh`

```bash
git clone <repo-manzili> maqola_bot && cd maqola_bot
cp .env.dist .env
nano .env          # BOT_TOKEN, ADMINS, POSTGRES_PASSWORD (murakkab!), havolalar, SCOPUS_API_KEY
docker compose up -d --build
docker compose logs -f bot      # loglar
```

- Baza (`pg_database`) Docker ichida ishlaydi va tashqariga ochilmaydi; ma'lumotlar `pgdata` hajmida saqlanadi.
- Bot har ishga tushganda migratsiyalarni o'zi qo'llaydi (`alembic upgrade head`).
- Admin yuklagan rasm va PDF'lar serverdagi `media/` va `files/` papkalarida saqlanadi.

Yangilash: `git pull && docker compose up -d --build`

Baza nusxasi: `docker compose exec pg_database pg_dump -U postgres maqola_bot > backup.sql`
