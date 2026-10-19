# Fihria Academic bot — ish rejasi

Maqsad: @Mirzo_MA_bot ning barcha bo'limlari va funksiyalarini birga-bir takrorlash.
Tahlil: `research/MIRZO_BOT_TAHLIL.md`, xabarlarning aynan matnlari: `research/mirzo_bot_dump/`.

## Texnologiya

- Shablon: [davronovuz/aiogram_3_shablon](https://github.com/davronovuz/aiogram_3_shablon) — ishga tushirish: `python bot.py`
- Python 3.11, aiogram 3, proyekt ichidagi `venv`
- PostgreSQL 16 (kompyuterda o'rnatilgan, baza `maqola_bot`) + SQLAlchemy + Alembic
- Scopus: Elsevier Serial Title API (`SCOPUS_API_KEY`)
- `.env` — token, adminlar, baza, havolalar, Scopus kaliti

## Bosqichlar

1. ✅ **Asos** — baza, middleware, buyruqlar menyusi.
2. ✅ **Bosh menyu** — rasm + salomlashuv (to'liq ism bilan) + 6 tugma.
3. ❌ **Foydali materiallar** — chek-listlar va blog; keyinchalik bo'lim olib tashlandi.
4. ✅ **Fihria Academic haqida** — 3 bo'lim.
5. ✅ **Xizmatlar** — 6 xizmat sahifasi (Buyurtma / Bepul maslahat / Batafsil Web App).
6. ✅ **Kontakt oqimi** — raqam → bazaga (`leads`) + adminga ariza.
7. ✅ **Hammualliflik** — mavzular bazada; admin uchun /topics.
8. ✅ **Scopus tekshiruvi** — API orqali; kalit kelganda sinaladi.
9. ✅ **Fallback** — boshqa xabarlarga javob + adminga forward.
10. ✅ **Sinov** — matnlar original bilan harfma-harf solishtirildi.
11. ✅ **Admin funksiyalari**
    - /stat — foydalanuvchilar (jami, bugun, 7 kun, bloklaganlar), arizalar (jami, bugun), bo'limlar bo'yicha.
    - /broadcast — istalgan xabarni (matn, rasm, video, fayl) ko'rib chiqib tasdiqlagach hammaga yuborish;
      botni bloklaganlar `users.active = false` qilinadi; oxirida hisobot.
    - Javob yozish — admin "✉️ Foydalanuvchidan xabar" yoki "🆕 Yangi ariza" xabariga reply qilsa,
      javob bot nomidan o'sha foydalanuvchiga boradi.

12. ✅ **Admin funksiyalari (2-qism)**
    - **Arizalar bilan ishlash:** har bir arizada [📞 Bog‘lanildi] [✅ Yopildi] [❌ Rad etildi] tugmalari
      (kim va qachon o'zgartirgani yoziladi); /leads — ochiq arizalar ro'yxati, /lead_N — bitta ariza;
      /export — barcha arizalar Excel (.xlsx) faylida.
    - **Rasm va PDF'larni bot orqali yuklash:** /media — 13 ta rasm va 4 ta PDF ro'yxati (bor/yo'q),
      tanlab yangisini yuborish yoki o'chirish.
    - **Mavzularni tahrirlash:** mavzuning bazasi, nomi, narxlarini o'zgartirish, yashirish/ko'rsatish;
      soha qo'shish, nomini o'zgartirish, o'chirish.

## Originaldan farqlar

- "Kafolatlar" va "Mijozlar fikrlari" tugmalari ishlaydi (originalda javob bermaydi).
- "Nega aynan bizni" matnining kesilib qolgan oxiri to'ldirilgan.
- Scopus kartochkasida "Manba: Scopus, {oy yil}" (ma'lumot API'dan jonli olinadi).
- Admin funksiyalari: /topics, /stat, /broadcast, javob yozish.

## Sizdan kerak bo'ladigan narsalar

- [ ] **Scopus API kaliti** → `.env` dagi `SCOPUS_API_KEY`
- [ ] **Rasmlar** (12 ta) → `media/`: hero, about, services, svc_scopus, svc_wos, svc_oak, svc_diss,
      svc_hirsh, svc_conf, coauth, coauth_topics, coauth_field
- [ ] **Havolalar** (https) → `.env`: URL_SCOPUS, URL_WOS, URL_OAK, URL_DISS, URL_HIRSH, URL_CONF
- [ ] "Kafolatlar" va "Mijozlar fikrlari" matnlari
- [ ] Hammualliflik mavzulari (/topics orqali)
- [ ] Bot tokenini yangilash (BotFather → /revoke), serverga chiqarish
