# Fihria Academic bot — ish rejasi

Bot: @maqola_2026_bot ("Fihria Academic"). Dastlab @Mirzo_MA_bot asosida qurilgan
(tahlil: `research/MIRZO_BOT_TAHLIL.md`), keyin Fihria Academic uchun qayta ishlangan.

## Texnologiya

- Shablon: [davronovuz/aiogram_3_shablon](https://github.com/davronovuz/aiogram_3_shablon) — ishga tushirish: `python bot.py`
- Python 3.11, aiogram 3, proyekt ichidagi `venv`
- PostgreSQL 16 + SQLAlchemy + Alembic (Docker'da har ishga tushishda `alembic upgrade head`)
- Scopus: Elsevier Serial Title API (`SCOPUS_API_KEY`)
- `.env` — token, adminlar, baza, havolalar, Scopus kaliti (namuna: `.env.dist`)

## Serverga chiqarish

```
cd ~/maqola_bot && git pull && docker compose up -d --build
```

`.env` o'zgarsa ham `up -d` kerak (`restart` yangi `.env` ni o'qimaydi).
`media/` va `files/` git'ga kirmaydi — rasmlarni faqat admin `/media` orqali yuklaydi (yuklanmagan bo'limda rasm chiqmaydi).

## Hozirgi holat

### Foydalanuvchi uchun

- **Ro'yxatdan o'tish** (birinchi /start): ism → telefon → faoliyat yo'nalishi → yo'nalish (`directions` jadvali, 7 ta).
- **Bosh menyu:** Fihria Academic haqida · Xizmatlar · Bepul maslahat · Scopus'da jurnalni tekshirish ·
  Jurnallar javoni · Plagiatga tekshirish · Hammualliflik · Savollar.
- **Fihria Academic haqida:** "Nega Fihria Academic" · "Qanday ishlaymiz" (4 bosqich + tamoyillar) · Savollar.
- **Xizmatlar (11 ta):** Scopus · Web of Science · OAK · Dissertatsiya · Ilmiy profil va Hirsh indeksi ·
  Konferensiya · ✍️ Matn bilan ishlash (Tahrirlash · Tarjima · Yangi alifbo · Lotin ↔ Kirill) ·
  Tahririyatga a'zolik · ISBN va DOI · EHM guvohnomasi.
  Buyurtma va bepul maslahatda telefon qayta so'ralmaydi (ro'yxatdagi raqam ishlatiladi).
- **Scopus tekshiruvi:** ISSN yoki nom bo'yicha, API orqali jonli.
- **Jurnallar javoni** (/journals): yo'nalishlar bo'yicha jurnallar. Jurnal tanlansa — kartochka (qisqa ma'lumot)
  va «Zayavka qoldirish»; sayt havolasi zayavka qabul qilingandan keyin beriladi. Ma'lumot /shelf orqali yoziladi.
  Boshlang'ich 200 ta nashr "Ilmiy nashrlar javoni" katalogidan (migratsiya `b9e2f4a6c8d1`).
- **Plagiatga tekshirish** (/plagiat): .doc/.docx/.pdf fayl adminlarga to'liq profil bilan boradi.
- **✍️ Matn bilan ishlash** (/matn; bosh menyuda ham, Xizmatlar ichida ham): tahrir va tarjima (pullik, buyurtma)
  hamda ikkita bepul vosita (ariza yaratmaydi; .docx — formatlash saqlanadi, .txt yoki matn):
  - /alifbo — yangi alifbo: oʻ→ö, gʻ→ğ, sh→ş, ch→ç (OʻRQ–1184); kirill matn ham to'g'ridan-to'g'ri yangi alifboga.
  - /kirill — Lotin ↔ Kirill, yo'nalish matnning qaysi yozuvi ko'pligiga qarab.
  Inglizcha xatboshi/so'zlar, havolalar, email, ISSN/DOI o'tkazib yuboriladi (services/alphabet.py, taxminiy).
- **Hammualliflik** (/co_authorship): foydalanuvchi maqola joylaydi (sarlavha → yo'nalish → baza → annotatsiya →
  o'rinlar narxi → fayl), admin tasdiqlaydi; boshqalar yo'nalish bo'yicha ko'rib "Hammuallif bo'lish"ni bosadi.
  Tasdiqlangan maqola haqida shu yo'nalishdagilarga xabar yuboriladi. Eski mavzular tizimi (/topics) ham turibdi.
- **Savollar** (/faq): 7 ta ko'p beriladigan savol.
- **Fallback:** boshqa xabarlarga javob + adminga forward.

### Admin uchun

- /leads, /lead_N — arizalar; har birida [📞 Bog‘lanildi] [✅ Yopildi] [❌ Rad etildi].
- /export — arizalar va foydalanuvchilar (har yo'nalish alohida varaq) Excel faylda.
- /stat — statistika; /broadcast — hammaga yoki bitta yo'nalishga xabar.
- /shelf — jurnallar javoni: jurnallar (nomi, baza, havola, qisqa ma'lumot, yo'nalishi; qo'shish, o'chirish) va
  yo'nalishlar (qo'shish, nomini o'zgartirish, o'chirish — ro'yxatdan o'tishda ham shu yo'nalishlar); /articles, /article_N — hammualliflik maqolalari (tasdiqlash, rad etish,
  yopish, narxlarni o'zgartirish); /topics — eski hammualliflik mavzulari.
- /media — rasm va PDF'larni yuklash (17 ta rasm joyi).
- /admins — adminlar: qo'shish (kontakt tanlash, ID, @username yoki forward), adminlikdan olish. `.env` dagi
  ADMINS — asosiy adminlar, ularni bot orqali o'chirib bo'lmaydi; qo'shilganlar `admins` jadvalida saqlanadi.
- Admin "✉️ Foydalanuvchidan xabar" yoki "🆕 Yangi ariza" xabariga reply qilsa, javob foydalanuvchiga boradi.

## Ochiq masalalar

- [ ] **Scopus API kaliti** → serverdagi `.env` dagi `SCOPUS_API_KEY`
- [ ] **Rasmlar** (ixtiyoriy) — kerak bo'lsa admin `/media` orqali yuklaydi
- [ ] **Bot tokenini yangilash** (BotFather → /revoke), agar token biror joyda ko'ringan bo'lsa
- [ ] **Hammualliflik:** eski mavzular tizimi (/topics) kerakmi; pullik o'rinlar "ilmiy halollik" tamoyiliga mosmi
- [ ] **Xizmat havolalari** (ixtiyoriy, https) → `.env`: URL_SCOPUS, URL_WOS, ... (bo'sh bo'lsa tugma chiqmaydi)
- [ ] Haqiqiy mijozlar fikrlari to'plansa — "Biz haqimizda"ga qaytarish
