# @Mirzo_MA_bot — to'liq tahlil

Sana: 2026-10-18. Bot: **Mirzo | Maqolalar Akademiyasi** (@Mirzo_MA_bot).
Tavsif (bio): "🤖 Mirzo — Maqolalar akademiyasi yordamchisi. Scopus, Web of Science va OAK bo‘yicha yordam."

Har bir xabarning aynan matni `mirzo_bot_dump/` papkasida (01–38 fayllar). Matnlar `texts.py` ga ham ko'chirilgan.

## Umumiy ishlash uslubi

- Har bir bo'lim **yangi xabar** bilan ochiladi (eski xabar tahrirlanmaydi).
- Ko'p bo'limlarda avval **rasm** (alohida xabar, captionsiz), keyin **matn + inline tugmalar** keladi.
- Telefon raqam so'ralganda: matn xabari, keyin alohida **"⬇️"** xabari keladi. Unda reply-klaviatura bor, tugmasi **"Kontaktni ulashish"** (request_contact).
- Raqam yuborilgach: "✅ Rahmat, {Ism Familiya}! Telefon raqamingiz qabul qilindi." + qaysi bo'limdan kelganiga qarab boshqa oxirgi gap.
- Salomlashuvda foydalanuvchining to'liq ismi ishlatiladi: "Assalomu alaykum, {full_name}! 👋".
- Boshqa holatda yozilgan har qanday matnga javob: "Rahmat; biz odatda bir necha soat ichida javob beramiz." (aftidan, xabar adminga yuboriladi).
- Ba'zi xabarlarga bot ❤️ reaksiya qo'yadi (muhim emas).

## Buyruqlar menyusi (Menu tugmasi)

| Buyruq | Tavsif |
|---|---|
| /hero | 🏠 Bosh sahifa |
| /guides | 🎁 Foydali materiallar |
| /scopus_check | 🔎 Scopus’da jurnalni tekshirish |
| /about | 🏛 Maqolalar akademiyasi haqida |
| /services | 💼 Maqolalar akademiyasi xizmatlari |
| /help | 💬 Bepul maslahat |
| /co_authorship | 🤝 Scopus/WoS hammuallifligi |

/start = /hero.

## Bo'limlar daraxti

```
/start, /hero  →  [rasm] + Bosh menyu matni
├── 🎁 Foydali materiallar (/guides)        → matn + [rasm keyin keladi]
│   ├── ✅ Chek-listlar                      → matn + 4 tugma
│   │   ├── 📁 PhD himoyasi uchun hujjatlar checklisti   → matn + PDF
│   │   ├── 📘 Maqola rad etilgandan keyingi 5 qadam     → matn + PDF
│   │   ├── 📝 Taqrizchi izohlariga javob xati checklisti → matn + PDF
│   │   └── 🔎 Scopus jurnalini tanlash: 7 ta xavf belgisi → matn + PDF
│   └── 📝 Blog maqolalari                   → matn
│       ├── 📚 Maqolalar katalogini ochish   (WEB APP → sayt blogi)
│       └── 🏠 Bosh menyuga qaytish
├── 🏛 Maqolalar akademiyasi haqida (/about) → [rasm] + matn
│   ├── 🌟 Nega aynan bizni tanlashadi       → matn (oxiri "bo‘y" deb kesilgan — originaldagi xato)
│   │   ├── 💼 Xizmatni tanlash  → Xizmatlar
│   │   ├── 🤝 Hammualliflik uchun mavzularni tanlash → Hammualliflik
│   │   └── 💬 Bepul maslahat olish → Bepul maslahat
│   ├── 🛡 Bizning kafolatlarimiz            → ❌ JAVOB BERMAYDI (originalda ishlamaydi)
│   └── 💬 Mijozlarimiz fikrlari             → ❌ JAVOB BERMAYDI
├── 💬 Bepul maslahat (/help)                → matn + "⬇️" + Kontaktni ulashish
├── 🔎 Scopus’da jurnalni tekshirish (/scopus_check) → matn + 1 tugma
│   └── 🔎 Scopus’da jurnalni tekshirish     → "ISSN yoki jurnal nomini yuboring..." + "⬇️" (kontakt klaviatura)
│       ├── topildi    → jurnal kartochkasi + [Maqola auditi] [Boshqa jurnalni tekshirish]
│       │   └── Maqola auditi → "Raqamni pastdagi tugma orqali qoldiring..." + "⬇️"
│       └── topilmadi  → matn + [Raqam qoldirish] [Boshqa jurnalni tekshirish]
│           └── Raqam qoldirish → "Raqam qoldiring — mutaxassis qo‘lda tekshiradi..." + "⬇️"
├── 💼 Xizmatlar (/services)                 → [rasm] + matn + 7 tugma
│   ├── 📝 Scopus’da maqola chop etish
│   ├── 📝 Web of Science’da maqola chop etish
│   ├── 🎓 OAK jurnallarida maqola chop etish
│   ├── 📚 Dissertatsiyalar bo‘yicha xizmatlar
│   ├── 📈 Hirsh indeksini oshirish
│   ├── 🎤 Konferensiya tezislarini chop etish
│   │     (har biri: [rasm] + matn + 3 tugma)
│   │     ├── 🛒 Xizmatga buyurtma berish → "📝 Arizangiz uchun rahmat!..." + "⬇️"
│   │     ├── 💬 Bepul maslahat olish     → Bepul maslahat
│   │     └── ℹ️ Xizmat haqida batafsil    (WEB APP → saytdagi xizmat sahifasi)
│   └── 🤝 Scopus / Web of Science’da hammualliflik → Hammualliflik
└── 🤝 Hammualliflik (/co_authorship)        → [rasm] + matn
    ├── 🎯 Individual tanlov                 → "✅ Siz ... individual mavzular tanlovini tanladingiz..." + "⬇️"
    └── 🎯 Dolzarb mavzalar tanlovini olish  → [rasm] + matn + [Dolzarb mavzularni ko‘rish]
        └── "Sizni qaysi bilim sohasi qiziqtiradi?" + 10 soha tugmasi:
            Energetika va qurilish, Agronomiya, Tibbiyot, Ta’lim, Biologiya,
            Iqtisodiyot, Biznes va menejment, Kiberxavfsizlik, Moliya va bank ishi, Boshqa soha
            └── soha → [rasm] + mavzular ro'yxati (5 tadan) + [Yana mavzularni olish] [Hammualliflikka buyurtma berish]
                └── oxirgi sahifa → mavzular + yakuniy xabar:
                    [Hammualliflikka buyurtma berish] → "📝 So‘rovingiz uchun rahmat!..." + "⬇️"
                    [Taklif qoldirish] → "Kalit so‘zlaringizni kiriting..." → foydalanuvchi matn yozadi →
                                         "Ma’lumot uchun rahmat! 😊 ..." + [Bosh menyuga qaytish]
                    [Bosh menyuga qaytish]
```

## Hammualliflik mavzusi formati

```
📌 Scopus Q3 | <Mavzu nomi> (5 ta bo‘sh joy)
1-muallif o‘rni — 550$
2-muallif o‘rni — 540$
3-muallif o‘rni — 530$
4-muallif o‘rni — 510$ (Sotilgan)
5-muallif o‘rni — 490$
```
"Bo‘sh joy" soni = sotilmagan o'rinlar soni. Baza: Scopus Q1–Q4 / Web of Science Q1–Q4.

## Scopus tekshiruvi natijasi formati

```
PLOS One
Nashriyot: Public Library of Science · ISSN: 1932-6203 (E)
Holat: indekslanadi
Qamrov: 2006–2026
Sohalar: Ko‘p tarmoqli
Manba: Scopus Source List, avgust 2026.

Jurnal bazada bor. Lekin Scopusda jurnal emas, maqola indekslanadi — ...
Maqolangizni bepul ko‘rib chiqamiz ...
Raqamingizni qoldiring — mutaxassis bog‘lanadi ...
```
- ISSN bo'yicha ham, aniq nom bo'yicha ham qidiradi ("Nature", "1932-6203").
- Faqat elektron ISSN bo'lsa "(E)" qo'shiladi.
- Ma'lumot manbai — Elsevier'ning **Scopus Source List** fayli (xlsx), oyma-oy yangilanadi.
- Natijadan keyin holat tugaydi: yana matn yozilsa, umumiy "Rahmat; biz odatda..." javobi keladi.

## Tashqi resurslar (foydalanuvchi o'zi beradi)

- PDF chek-listlar (4 ta).
- Rasmlar: bosh sahifa, foydali materiallar, akademiya haqida, xizmatlar, har bir xizmat (6), hammualliflik, mavzular, soha.
- Web App havolalari: blog katalogi va 6 ta xizmatning "batafsil" sahifasi (originalda a-articles.uz saytiga ochiladi).
