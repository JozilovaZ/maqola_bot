# Botning barcha matnlari (dastlab @Mirzo_MA_bot asosida yozilgan). {name} — foydalanuvchining to'liq ismi.

GREETING = (
    "Assalomu alaykum, {name}! 👋\n\n"
    "Men — Oʻzbekiston tadqiqotchilari uchun Fihria Academic yordamchisiman.\n\n"
)

MAIN_MENU = GREETING + (
    "Xush kelibsiz! Menyuda siz:\n\n"
    "🏛 Fihria Academic haqida batafsil ma’lumot olishingiz\n"
    "💼 Xizmatlarimiz bilan tanishishingiz\n"
    "🔎 Jurnalning Scopus’dagi holatini tekshirishingiz\n"
    "💬 Bepul maslahat olishingiz\n"
    "📚 Yo‘nalishingiz bo‘yicha jurnallar ro‘yxatini ko‘rishingiz\n"
    "🧾 Maqolangizni plagiatga tekshirtirishingiz\n"
    "🤝 Scopus/Web of Science’da hammualliflik mavzularini ko‘rib chiqishingiz\n"
    "❓ Ko‘p beriladigan savollarga javob topishingiz mumkin\n\n"
    "Kerakli bo‘limni tanlang — men sizga mamnuniyat bilan yordam beraman."
)

# ---------- Fihria Academic haqida ----------

ABOUT = GREETING + (
    "Fihria Academic — tadqiqotchilarga ilmiy maqola tayyorlash, tahrirlash, tarjima qilish va ishonchli jurnal "
    "tanlashda yordam beradigan jamoa.\n\n"
    "Maqolani muallif bilan birga, uning o‘z tadqiqoti va ma’lumotlari asosida tayyorlaymiz. Har bir ish jurnal "
    "talablariga moslab, muallif bilan kelishilgan holda bajariladi.\n\n"
    "Quyidagi bo‘limni tanlang 👇"
)

ABOUT_WHY = (
    "⭐ Nega Fihria Academic?\n\n"
    "• mavzudan nashrga tayyor matngacha — maqola tayyorlash, plagiat tekshiruvi, tahrir va tarjima bir joyda;\n"
    "• o‘zbek, rus va ingliz tillarida ishlaymiz;\n"
    "• jurnal tanlashda yordam beramiz va soxta («o‘g‘irlangan») jurnallardan ogohlantiramiz;\n"
    "• narx va muddat ish hajmi ko‘rilgach oldindan kelishiladi;\n"
    "• oraliq variantlarni ko‘rsatib, izohlaringizni kiritamiz;\n"
    "• yo‘nalishlar bo‘yicha ishonchli jurnallar ro‘yxati — «📚 Jurnallar javoni» bo‘limida."
)

ABOUT_PROCESS = (
    "🤝 Qanday ishlaymiz\n\n"
    "1️⃣ <b>So‘rov yuborasiz</b> — xizmatni tanlab, mavzu va talablarni qisqacha yozasiz.\n"
    "2️⃣ <b>Kelishamiz</b> — hajm, narx va muddatni aniqlab, ish rejasini tasdiqlaymiz.\n"
    "3️⃣ <b>Birga ishlaymiz</b> — oraliq variantlarni ko‘rib, izohlaringizni kiritamiz.\n"
    "4️⃣ <b>Tayyor natija</b> — jurnalga yuborishga tayyor matn va hisobotni olasiz.\n\n"
    "Bizning tamoyillarimiz:\n\n"
    "• maqola muallifning o‘z tadqiqoti, ma’lumotlari va ishtirokida tayyorlanadi;\n"
    "• ilmiy halollik qoidalariga zid ishlar qabul qilinmaydi;\n"
    "• materiallaringiz uchinchi shaxslarga berilmaydi;\n"
    "• «3 kunda Scopus» yoki «100% kafolat» kabi va’dalar bermaymiz — nashr qarorini jurnal tahririyati va "
    "taqrizchilar qabul qiladi."
)

# ---------- Xizmatlar ----------

SERVICES = (
    "Assalomu alaykum, {name}! 👋\n\n"
    "Men — Fihria Academic yordamchisiman.\n\n"
    "Bu yerda maqola tayyorlash, nashrga tayyorlash va ilmiy faoliyatingiz uchun barcha xizmatlarimiz "
    "jamlangan.\n\n"
    "Menyudan kerakli xizmatni tanlang — batafsil ma’lumot va keyingi qadamlar bilan tanishing."
)

SERVICE_TEXTS = {
    "scopus": (
        "📚 Scopus’da maqola chop etish\n\n"
        "Scopus bazasidagi jurnalda maqola chop etishni rejalashtiryapsizmi? Fihria Academic maqolani tayyorlashdan "
        "tahririyatga yuborish va taqrizdan o‘tishgacha bo‘lgan jarayonda yoningizda bo‘ladi.\n\n"
        "Xizmat tarkibiga quyidagilar kiradi:\n\n"
        "• maqolani siz bilan birga tayyorlash yoki tayyor matnni professional auditdan o‘tkazish;\n"
        "• mavzu va kerakli kvartilga (Q1–Q4) mos jurnalni tanlash — indeksatsiya Scopus Sources ro‘yxatidan "
        "tekshiriladi;\n"
        "• plagiat va sun’iy intellektdan foydalanish bo‘yicha tekshiruv;\n"
        "• matnni jurnal shabloni va talablariga moslash;\n"
        "• tahririyatga yuborish, taqrizchi izohlariga javob xatini tayyorlash va tuzatishlar kiritish.\n\n"
        "Nashr qarorini jurnal tahririyati qabul qiladi, muddat esa jurnalning taqriz jarayoniga bog‘liq. Narx va "
        "muddatni ish hajmini ko‘rgach aniq aytamiz.\n\n"
        "Buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? Quyidagi kerakli tugmani tanlang 👇"
    ),
    "wos": (
        "🔬 Web of Science’da maqola chop etish\n\n"
        "Web of Science bazasidagi jurnalda maqola chop etishni rejalashtiryapsizmi? Fihria Academic maqolani "
        "tayyorlashdan tahririyatga yuborish va taqrizdan o‘tishgacha bo‘lgan jarayonda yoningizda bo‘ladi.\n\n"
        "Xizmat tarkibiga quyidagilar kiradi:\n\n"
        "• maqolani siz bilan birga tayyorlash yoki tayyor matnni professional auditdan o‘tkazish;\n"
        "• yo‘nalishingizga mos jurnalni tanlash — indeksatsiya Master Journal List’dan tekshiriladi;\n"
        "• plagiat va sun’iy intellektdan foydalanish bo‘yicha tekshiruv;\n"
        "• matnni jurnal shabloni va talablariga moslash;\n"
        "• har bir bosqichda matn va jurnalni siz bilan kelishish;\n"
        "• tahririyatga yuborish, taqrizchi izohlariga javob xatini tayyorlash va tuzatishlar kiritish.\n\n"
        "Nashr qarorini jurnal tahririyati qabul qiladi, muddat esa jurnalning taqriz jarayoniga bog‘liq. Narx va "
        "muddatni ish hajmini ko‘rgach aniq aytamiz.\n\n"
        "Buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? Quyidagi kerakli tugmani tanlang 👇"
    ),
    "oak": (
        "🎓 OAK jurnallarida maqola chop etish\n\n"
        "Oʻzbekiston Respublikasi OAK ro‘yxatidagi jurnalda maqola chop etishni rejalashtiryapsizmi? Fihria Academic "
        "maqolani tayyorlashdan nashrgacha bo‘lgan jarayonda yordam beradi.\n\n"
        "Xizmat tarkibiga quyidagilar kiradi:\n\n"
        "• maqolani siz bilan birga tayyorlash yoki tayyor matnni professional auditdan o‘tkazish;\n"
        "• OAKning amaldagi ro‘yxatidan yo‘nalishingizga mos jurnalni tanlash va uni siz bilan kelishish;\n"
        "• plagiat va sun’iy intellektdan foydalanish bo‘yicha tekshiruv;\n"
        "• matnni jurnal talablariga moslab rasmiylashtirish;\n"
        "• maqolani jurnalga yuborish va zarur tuzatishlarni kiritish.\n\n"
        "Jurnal OAK tomonidan tan olinishini doim OAK rasmiy ro‘yxatidan tekshiramiz. Narx va muddat yo‘nalish va "
        "tanlangan jurnalga qarab belgilanadi.\n\n"
        "Buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? Quyidagi kerakli tugmani tanlang 👇"
    ),
    "diss": (
        "🎓 Dissertatsiya bo‘yicha xizmatlar\n\n"
        "Himoyaga tayyorlanyapsizmi? Dissertatsiya ustida ishlashning turli bosqichlarida yordam beramiz.\n\n"
        "Ish yo‘nalishlari:\n\n"
        "• mavzu, reja va tuzilma bo‘yicha maslahat;\n"
        "• dissertatsiya mavzusi bo‘yicha ilmiy manbalar bazasini shakllantirish;\n"
        "• ilmiy bazalardan dissertatsiyalarni topib, yuklab (skachat qilib) berish;\n"
        "• boblarni ilmiy tahrirlash va korrektura;\n"
        "• bibliografiyani APA, GOST, IEEE va boshqa uslublarda rasmiylashtirish;\n"
        "• plagiat tekshiruvi va o‘xshashlikni kamaytirish bo‘yicha tavsiyalar;\n"
        "• himoya talablari bo‘yicha nashrlaringizni hisoblash va yetishmayotgan maqolalar uchun jurnal tanlash;\n"
        "• matnlarni o‘zbek, rus va ingliz tillari o‘rtasida tarjima qilish.\n\n"
        "Narx va muddat ish turi va hajmiga qarab kelishiladi.\n\n"
        "Buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? Quyidagi kerakli tugmani tanlang 👇"
    ),
    "hirsh": (
        "📈 Ilmiy profil va Hirsh indeksi\n\n"
        "Hirsh indeksi (h-indeks) nashrlaringiz va ularga qilingan iqtiboslar soniga qarab hisoblanadi. Profil "
        "tartibsiz bo‘lsa — nashrlar biriktirilmagan, ism turlicha yozilgan, bir nechta profil ochilgan — "
        "ko‘rsatkich haqiqiydan past chiqadi.\n\n"
        "Xizmat tarkibiga quyidagilar kiradi:\n\n"
        "• ORCID, Google Scholar va Scopus profillarini ochish yoki tartibga keltirish;\n"
        "• barcha nashrlaringizni profilga biriktirish;\n"
        "• takroriy profillarni birlashtirish va ism yozilishini bir xillashtirish;\n"
        "• attestatsiya va grantlar uchun profil ma’lumotlarini tayyorlash.\n\n"
        "Iqtibos sotib olish kabi sun’iy usullar bilan ishlamaymiz.\n\n"
        "Buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? Quyidagi kerakli tugmani tanlang 👇"
    ),
    "conf": (
        "🎤 Konferensiya tezislarini chop etish\n\n"
        "Ilmiy konferensiyada qatnashib, tezislarni chop ettirishingiz kerakmi? Materiallarni tayyorlash va ilmiy "
        "yo‘nalishingizga mos konferensiyani tanlashda yordam beramiz.\n\n"
        "Xizmat tarkibiga quyidagilar kiradi:\n\n"
        "• tezislarni siz bilan birga tayyorlash;\n"
        "• mos ilmiy konferensiyani tanlash;\n"
        "• materialni tashkiliy qo‘mita talablariga muvofiq rasmiylashtirish;\n"
        "• yuborish va tashkiliy qo‘mita bilan muloqot.\n\n"
        "Ko‘plab konferensiyalar ishtirokchi sertifikati va to‘plamning elektron nusxasini beradi, lekin bu har bir "
        "konferensiyaning o‘z qoidasiga bog‘liq — buyurtma vaqtida aniqlashtiramiz.\n\n"
        "Buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? Quyidagi kerakli tugmani tanlang 👇"
    ),
    "edit": (
        "✏️ Maqolani tahrirlash\n\n"
        "Maqolangiz tayyor, lekin jurnal talablariga to‘liq javob berishiga ishonchingiz komil emasmi? Fihria "
        "Academic mutaxassislari matnni ilmiy va texnik jihatdan tahrir qilib, jurnalga yuborishga tayyorlab beradi."
        "\n\n"
        "Xizmat tarkibiga quyidagilar kiradi:\n\n"
        "• ilmiy uslub, grammatika va mantiqiy izchillikni tuzatish;\n"
        "• ilmiy matn tuzilishini (IMRAD: kirish, usullar, natijalar, muhokama) takomillashtirish;\n"
        "• tanlangan jurnal shabloni va talablariga moslash;\n"
        "• annotatsiya, kalit so‘zlar va sarlavhani kuchaytirish;\n"
        "• adabiyotlar ro‘yxatini kerakli standartda (APA, IEEE, GOST va b.) formatlash;\n"
        "• taqrizchi izohlariga javob xatini tayyorlash.\n\n"
        "Narx va muddat matn hajmi hamda tahrir darajasiga qarab belgilanadi.\n\n"
        "Tahrirga buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? "
        "Quyidagi kerakli tugmani tanlang 👇"
    ),
    "translate": (
        "🌐 Maqolani tarjima qilish\n\n"
        "Maqolangizni xalqaro jurnalga yubormoqchimisiz? Fihria Academic ilmiy matnlarni soha terminologiyasini "
        "saqlagan holda tarjima qiladi.\n\n"
        "Xizmat tarkibiga quyidagilar kiradi:\n\n"
        "• o‘zbek, rus va ingliz tillari o‘rtasida ilmiy uslubda tarjima;\n"
        "• soha terminologiyasiga mos aniq tarjima;\n"
        "• annotatsiya va kalit so‘zlarni uch tilda tayyorlash;\n"
        "• xalqaro jurnal talablariga mos akademik ingliz tili;\n"
        "• tarjimadan keyin tahrir va korrektura.\n\n"
        "Narx va muddat matn hajmi va til juftligiga qarab belgilanadi.\n\n"
        "Tarjimaga buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? "
        "Quyidagi kerakli tugmani tanlang 👇"
    ),
    "board": (
        "🏅 Tahririyatga a’zolik\n\n"
        "Xalqaro jurnallar tahrir hay’ati yoki taqrizchilar safiga a’zo bo‘lishni xohlaysizmi? Arizangizni "
        "tayyorlash va yuborishda yordam beramiz.\n\n"
        "Xizmat tarkibiga quyidagilar kiradi:\n\n"
        "• ilmiy darajangiz va sohangizga mos jurnalni tanlash;\n"
        "• akademik CV va ORCID profilini tayyorlash;\n"
        "• tahririyat bilan muloqot va arizani yuborish;\n"
        "• ariza tasdiqlangach, a’zolik sertifikatini olish.\n\n"
        "A’zolik to‘g‘risidagi qarorni jurnal tahririyati qabul qiladi. Narx va muddat kelishiladi.\n\n"
        "Ariza bermoqchimisiz yoki bepul maslahat olmoqchimisiz? Quyidagi kerakli tugmani tanlang 👇"
    ),
    "isbn": (
        "📕 ISBN va DOI olish\n\n"
        "Monografiya, o‘quv qo‘llanma yoki maqolalar to‘plamini nashr qilyapsizmi? Rasmiy identifikatorlarni "
        "olishda yordam beramiz.\n\n"
        "Xizmat tarkibiga quyidagilar kiradi:\n\n"
        "• monografiya va o‘quv qo‘llanmalar uchun ISBN rasmiylashtirishga ko‘mak;\n"
        "• maqola va to‘plamlar uchun DOI rasmiylashtirishga ko‘mak;\n"
        "• kerakli hujjatlar va metama’lumotlarni tayyorlash.\n\n"
        "Narx va muddat nashr turiga qarab kelishiladi.\n\n"
        "Buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? Quyidagi kerakli tugmani tanlang 👇"
    ),
    "ehm": (
        "💾 EHM dasturi va ma’lumotlar bazasi guvohnomasi\n\n"
        "Kompyuter dasturi yoki ma’lumotlar bazasini yaratdingizmi? Uni rasmiy ro‘yxatdan o‘tkazish uchun "
        "hujjatlarni tayyorlashda yordam beramiz.\n\n"
        "Xizmat tarkibiga quyidagilar kiradi:\n\n"
        "• ariza va dastur tavsifini tayyorlash;\n"
        "• talab qilinadigan hujjatlar ro‘yxati bo‘yicha maslahat;\n"
        "• hujjatlarni topshirishga tayyorlash.\n\n"
        "Narx va muddat dastur hajmiga qarab kelishiladi.\n\n"
        "Buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? Quyidagi kerakli tugmani tanlang 👇"
    ),
}

ORDER = (
    "📝 Arizangiz uchun rahmat!\n\n"
    "Menejer siz bilan bog‘lanib, xizmat tafsilotlarini muhokama qilishi uchun quyidagi tugma orqali telefon "
    "raqamingizni qoldiring 👇\n\n"
    "Fihria Academic menejeri yaqin vaqt ichida sizga qo‘ng‘iroq qiladi."
)

CONSULT = (
    "Savolingiz bo‘yicha bepul maslahat olish uchun quyidagi tugma orqali telefon raqamingizni qoldiring 👇\n\n"
    "Fihria Academic menejeri yaqin vaqt ichida siz bilan bog‘lanadi va barcha savollaringizga javob "
    "beradi.\n\n"
    "📱 Telefon raqamini yuborish"
)

# Raqam so'ralganda matndan keyin alohida keladigan xabar ("Kontaktni ulashish" tugmasi shunga biriktiriladi).
# Oxiridagi ko'rinmas belgi (U+2063) emojini katta stiker emas, oddiy kichik matn qilib ko'rsatadi — originaldagidek.
CONTACT_ARROW = "⬇⁣"

# ---------- Hammualliflik ----------

COAUTH = GREETING + (
    "Hammualliflik variantlari mutaxassisligingiz, mavzuingiz va nashr maqsadingizni inobatga olgan holda "
    "individual tarzda tanlanadi.\n\n"
    "O‘zingizga qulay aloqa ma’lumotini qoldiring — Fihria Academic mutaxassisi siz bilan bog‘lanib, mos variantni "
    "tanlashga yordam beradi.\n\n"
    "Quyidagi qulay variantni tanlang 👇"
)

COAUTH_INDIVIDUAL = (
    "✅ Siz hammualliflik uchun bepul individual mavzular tanlovini tanladingiz.\n\n"
    "Telefon raqamingizni quyidagi tugma orqali qoldiring 👇\n\n"
    "Fihria Academic menejeri yaqin vaqt ichida siz bilan bog‘lanadi va hammualliflik uchun dolzarb "
    "mavzalarni taklif qiladi.\n\n"
    "⬇"
)

COAUTH_TOPICS_INTRO = (
    "Assalomu alaykum, {name}! 👋\n\n"
    "Ilmiy jurnallarda hammualliflik qilish imkoniyati Sizni qiziqtiradimi?\n\n"
    "Sizga mos va dolzarb mavzuni tanlashda yordam beraman.\n\n"
    "Davom etish uchun quyidagi tugmani bosing 👇"
)

COAUTH_FIELDS = "Sizni qaysi bilim sohasi qiziqtiradi?"

# Mavzu ko'rinishi: sarlavha + har bir muallif o'rni
TOPIC_HEADER = "📌 {base} | {title} ({free} ta bo‘sh joy)"
TOPIC_SLOT = "{position}-muallif o‘rni — {price}$"
TOPIC_SOLD = " (Sotilgan)"

COAUTH_FINAL = (
    "Bir yoki bir nechta mavzu Sizni qiziqtirdimi?\n\n"
    "Unda «Hammualliflikka buyurtma berish» tugmasini bosing.\n\n"
    "Sizga mos dolzarb mavzuni topmadingizmi?\n"
    "«Taklif qoldirish» tugmasini bosing va kalit so‘zlaringizni kiriting. Sizning yo‘nalishingiz bo‘yicha yangi "
    "mavzular tayyor bo‘lishi bilan darhol Siz bilan bog‘lanamiz."
)

COAUTH_ORDER = (
    "📝 So‘rovingiz uchun rahmat!\n\n"
    "Iltimos, quyidagi tugma orqali telefon raqamingizni qoldiring, shunda menejerimiz Siz bilan bog‘lanib, "
    "hammualliflik tafsilotlarini muhokama qilishi mumkin 👇"
)

COAUTH_SUGGEST = (
    "Kalit so‘zlaringizni kiriting. Sizning yo‘nalishingiz bo‘yicha mavzular yaratishimiz bilan darhol Siz bilan "
    "bog‘lanamiz."
)

COAUTH_SUGGEST_THANKS = (
    "Ma’lumot uchun rahmat! 😊\n\n"
    "Sizning yo‘nalishingiz bo‘yicha yangi mavzular paydo bo‘lishi bilan darhol Siz bilan bog‘lanamiz!"
)

# ---------- Scopus'da jurnalni tekshirish ----------

SCOPUS_INTRO = (
    "🔎 Scopus’da jurnalni tekshirish\n\n"
    "Jurnalda maqola chop etishni rejalashtiryapsizmi? Maqolani yuborishdan oldin nashr haqidagi dolzarb "
    "ma’lumotlarni Scopus’da tekshiring.\n\n"
    "Men sizga quyidagilarni aniqlashga yordam beraman:\n\n"
    "• jurnalning Scopus’dagi maqomi;\n"
    "• qamrov yillari;\n"
    "• nashriyotchi;\n"
    "• ilmiy sohalar.\n\n"
    "Tekshiruvni boshlash uchun quyidagi tugmani bosing 👇"
)

SCOPUS_ASK = "ISSN yoki jurnal nomini yuboring — Scopusda indekslashni tekshiraman.\n\nNamuna: 1932-6203 yoki PLOS ONE"

# Originalda "Manba: Scopus Source List, avgust 2026." — bizda ma'lumot API'dan jonli olinadi
SCOPUS_FOUND = (
    "<b>{title}</b>\n"
    "Nashriyot: {publisher} · ISSN: {issn}\n"
    "Holat: {status}\n"
    "Qamrov: {coverage}\n"
    "Sohalar: {subjects}\n"
    "Manba: Scopus, {date}.\n\n"
    "Jurnal bazada bor. Lekin Scopusda jurnal emas, maqola indekslanadi — ko‘pincha uni taqriz bosqichidayoq rad "
    "etishadi: mavzu nashr profiliga mos kelmaydi, rasmiylashtirish talabga zid, tuzilma zaif.\n"
    "Maqolangizni bepul ko‘rib chiqamiz va shu nashrga mos kelishini, topshirishdan oldin nimalarni tuzatish "
    "kerakligini aytamiz.\n"
    "Raqamingizni qoldiring — mutaxassis bog‘lanadi va maqolangiz bo‘yicha bepul maslahat beradi."
)

SCOPUS_STATUS_ACTIVE = "indekslanadi"
SCOPUS_STATUS_INACTIVE = "indekslanmaydi (qamrov to‘xtatilgan)"

SCOPUS_NOT_FOUND = (
    "Bu nashrni bazadan topa olmadik. Ko‘pincha sabab — Scopusdagi boshqa nom yoki yozilishdagi xato.\n\n"
    "Kontakt qoldiring — mutaxassis qo‘lda tekshiradi va aniq holatni aytadi: indekslanadimi, qamrov qaysi "
    "tomgacha amal qiladi va nashr chiqarilishga tayyorlanayotgani yo‘qmi."
)

SCOPUS_LEAVE_NUMBER = "Raqam qoldiring — mutaxassis qo‘lda tekshiradi va aniq holatni aytadi."

SCOPUS_AUDIT = "Raqamni pastdagi tugma orqali qoldiring — mutaxassis bog‘lanadi va maqola bo‘yicha maslahat beradi."

MONTHS = [
    "yanvar", "fevral", "mart", "aprel", "may", "iyun",
    "iyul", "avgust", "sentabr", "oktabr", "noyabr", "dekabr",
]

# ---------- Telefon raqami qabul qilinganda ----------

CONTACT_THANKS = "✅ Rahmat, {name}! Telefon raqamingiz qabul qilindi.\n\n{tail}"

# Ro'yxatdan o'tgan foydalanuvchi ariza qoldirganda (raqam qayta so'ralmaydi)
LEAD_THANKS = "✅ Rahmat, {name}! Arizangiz qabul qilindi.\n\n{tail}\n\n📱 Bog‘lanish uchun raqamingiz: {phone}"

# Javob oxiri raqam qaysi bo'limdan qoldirilganiga bog'liq (reason)
CONTACT_TAILS = {
    "consult": (
        "Fihria Academic menejeri yaqin vaqt ichida siz bilan bog‘lanadi va barcha savollaringizga "
        "javob beradi."
    ),
    "order": (
        "Fihria Academic menejeri yaqin vaqt ichida sizga qo‘ng‘iroq qiladi va xizmat tafsilotlarini "
        "muhokama qiladi."
    ),
    "coauth": (
        "Fihria Academic menejeri yaqin vaqt ichida siz bilan bog‘lanadi va hammualliflik uchun dolzarb "
        "mavzalarni taklif qiladi."
    ),
    "coauth_order": (
        "Fihria Academic menejeri yaqin vaqt ichida siz bilan bog‘lanadi va hammualliflik tafsilotlarini "
        "muhokama qiladi."
    ),
    "scopus": "Mutaxassis jurnalni qo‘lda tekshirib, yaqin vaqt ichida siz bilan bog‘lanadi.",
    "coauth_article": (
        "Fihria Academic menejeri yaqin vaqt ichida siz bilan bog‘lanadi va hammualliflik shartlarini "
        "muhokama qiladi."
    ),
    "audit": "Mutaxassis yaqin vaqt ichida bog‘lanadi va maqolangiz bo‘yicha bepul maslahat beradi.",
    "journal": (
        "Fihria Academic menejeri yaqin vaqt ichida siz bilan bog‘lanadi va jurnal talablari, muddatlari "
        "hamda narxini aytib beradi."
    ),
}

CONTACT_NOT_OWN = "Iltimos, pastdagi «Kontaktni ulashish» tugmasi orqali o‘zingizning raqamingizni yuboring."

# Bo'limlarga tegishli bo'lmagan har qanday xabarga javob
FALLBACK = "Rahmat; biz odatda bir necha soat ichida javob beramiz."

# ---------- Ro'yxatdan o'tish (birinchi /start) ----------

# Kalit bazada saqlanadi (users.role), qiymat — tugma matni
REG_ROLES = {
    "student": "🎓 Talabalar",
    "young_scientist": "🔬 Yosh tadqiqotchilar",
    "professor": "👨‍🏫 Professor-o‘qituvchilar va olimlar",
}

REG_START = GREETING + (
    "Botdan foydalanish uchun qisqa ro‘yxatdan o‘ting — bu 1 daqiqa vaqt oladi.\n\n"
    "✍️ <b>Ism va familiyangizni</b> yozing:\n"
    "<i>Namuna: Aliyev Vali</i>"
)
REG_NAME_INVALID = "Iltimos, ism va familiyangizni to‘liq yozing.\n<i>Namuna: Aliyev Vali</i>"

REG_PHONE = (
    "📱 <b>Telefon raqamingizni</b> yuboring.\n\n"
    "Pastdagi «Kontaktni ulashish» tugmasini bosing yoki raqamni yozing.\n"
    "<i>Namuna: +998901234567</i>"
)
REG_PHONE_INVALID = "Raqam noto‘g‘ri. «Kontaktni ulashish» tugmasini bosing yoki shunday yozing: +998901234567"

REG_ROLE = "👤 <b>Faoliyat yo‘nalishingizni tanlang:</b>"
REG_CHOOSE_BUTTON = "Iltimos, pastdagi tugmalardan birini tanlang 👇"

REG_DIRECTION = "📖 <b>Yo‘nalishingizni tanlang:</b>"

REG_TEXT_INVALID = "Iltimos, javobni matn ko‘rinishida qisqa yozing."
REG_TEXT_ONLY = "Iltimos, savolga javobni matn ko‘rinishida yozing."

REG_DONE = "✅ Rahmat, {name}! Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz."

# ---------- Jurnallar javoni ----------

JOURNALS = (
    "📚 <b>Jurnallar javoni</b>\n\n"
    "Bu yerda Fihria Academic mutaxassislari tanlagan ishonchli jurnallar yo‘nalishlar bo‘yicha jamlangan.\n\n"
    "Yo‘nalishni tanlang (qavs ichida — jurnallar soni) 👇"
)
JOURNALS_EMPTY = "Bu yo‘nalish bo‘yicha hozircha jurnal qo‘shilmagan. Tez orada to‘ldiriladi."
JOURNALS_HINT = (
    "\nJurnal haqida batafsil ma’lumot olish va zayavka qoldirish uchun uni pastdan tanlang.\n\n"
    "Mos jurnal tanlashda yordam kerakmi? Bepul maslahat oling 👇"
)
JOURNAL_NO_DESCRIPTION = "Bu jurnal haqida qisqacha ma’lumot hali kiritilmagan."
JOURNAL_CARD_HELP = (
    "✍️ <b>Muallifga</b>\n"
    "• Jurnal talablari, nashr muddatlari va narxi haqida menejerimiz batafsil ma’lumot beradi.\n"
    "• Maqolani jurnal shabloni va talablariga moslashtirishda yordam beramiz.\n"
    "• Tarjima, tahrir va plagiat tekshiruvi xizmatlaridan ham foydalanishingiz mumkin."
)
JOURNAL_CARD_HINT = "Shu jurnalda maqola chop etmoqchimisiz? Zayavka qoldiring 👇"
JOURNAL_APPLY = "📝 Jurnalga zayavka qoldirish uchun telefon raqamingizni qoldiring 👇"
JOURNAL_UNAVAILABLE = "Bu jurnal javondan olib tashlangan."
JOURNAL_SITE ="🔗 Kutish davomida jurnal sayti bilan tanishib chiqishingiz mumkin:"

# ---------- Matn bilan ishlash: tahrir, tarjima, yangi alifbo, Lotin ↔ Kirill ----------

TEXT_TOOLS = (
    "✍️ <b>Matn bilan ishlash</b>\n\n"
    "✏️ <b>Maqolani tahrirlash</b> — ilmiy uslub, grammatika va jurnal talablariga moslash (mutaxassis bajaradi).\n"
    "🌐 <b>Maqolani tarjima qilish</b> — o‘zbek, rus va ingliz tillari o‘rtasida (mutaxassis bajaradi).\n"
    "🔤 <b>Yangi alifboga o‘girish</b> — bepul, bir zumda.\n"
    "🔁 <b>Lotin ↔ Kirill</b> — bepul, bir zumda.\n"
    "📝 <b>Savodxon</b> — imlo xatolarini topib tuzatish, bepul.\n\n"
    "Kerakli xizmatni tanlang 👇"
)

FILE_HINT = (
    "📎 <b>Word (.docx)</b> yoki <b>.txt</b> fayl yuboring (20 MB gacha) yoki matnni shu yerga yozing. "
    "Word faylda shrift, jadval va rasmlar joyida qoladi."
)
ALPHABET = (
    "🔤 <b>Yangi alifboga o‘girish</b>\n\n"
    "Maqolangizni yangi o‘zbek lotin alifbosiga bepul o‘girib beramiz "
    "(2026-yil 21-oktyabrdagi OʻRQ–1184-son Qonun).\n\n"
    "Almashtiriladi: <b>oʻ → ö</b>, <b>gʻ → ğ</b>, <b>sh → ş</b>, <b>ch → ç</b>. "
    "Tutuq belgisi (maʼlumot, sanʼat) va «ng» o‘zgarmaydi. Kirill yozuvidagi matn ham to‘g‘ridan-to‘g‘ri "
    "yangi alifboga o‘giriladi.\n\n" + FILE_HINT
)
LATCYR = (
    "🔁 <b>Lotin ↔ Kirill</b>\n\n"
    "Matnni lotindan kirillga yoki kirilldan lotinga bepul o‘girib beramiz — yo‘nalish matnning o‘ziga qarab "
    "aniqlanadi. Yangi alifbodagi (ö, ğ, ş, ç) matn ham kirillga o‘giriladi.\n\n" + FILE_HINT
)
ALPHABET_WRONG = (
    "Iltimos, <b>Word (.docx)</b> yoki <b>.txt</b> fayl yuboring yoki matnni yozing.\n\n"
    "Eski <b>.doc</b> faylni Word’da ochib, «Saqlash» → <b>.docx</b> qilib saqlang. "
    "PDF’dan matnni formatlashsiz o‘girish uchun uni nusxalab shu yerga yozing."
)
ALPHABET_TOO_BIG = "Fayl 20 MB dan katta. Iltimos, kichikroq fayl yuboring."
ALPHABET_BROKEN = "Faylni ochib bo‘lmadi. U buzilmaganini tekshirib, qaytadan yuboring."
ALPHABET_DIRECTIONS = {
    "new": "yangi alifboga",
    "to_lat": "kirilldan lotinga",
    "to_cyr": "lotindan kirillga",
}
ALPHABET_DONE = (
    "✅ Tayyor: {direction} {changed} ta so‘z o‘girildi.\n\n"
    "⚠️ Inglizcha matn, havolalar va ISSN/DOI o‘zgartirilmaydi. Chet so‘zlar, ruscha o‘zlashmalar "
    "(masalan, litsey → лицей) va atoqli otlarni ko‘zdan kechiring.\n\n"
    "Yana fayl yoki matn yuborishingiz mumkin."
)
SAVODXON = (
    "📝 <b>Savodxon — imlo tekshiruvi</b>\n\n"
    "Matningizdagi imlo xatolarini sun’iy intellekt yordamida topib, tuzatib beramiz: harfi tushib qolgan "
    "so‘zlar, qo‘shib va ajratib yozish, tutuq belgisi va boshqalar. Lotin, yangi alifbo va kirill yozuvidagi "
    "matnlar tekshiriladi. Uslub va tinish belgilari tekshirilmaydi.\n\n"
    "Word faylda tuzatilgan so‘zlar <b>sariq rang</b> bilan belgilanadi.\n\n"
    "📎 <b>Word (.docx)</b> yoki <b>.txt</b> fayl yuboring (taxminan 25 betgacha) yoki matnni shu yerga yozing. "
    "Kuniga {limit} marta bepul."
)
SAVODXON_WAIT = "⏳ Matn tekshirilmoqda, bu bir-ikki daqiqa olishi mumkin…"
SAVODXON_BUSY = "⏳ Oldingi matn hali tekshirilmoqda. Tugashini kuting."
SAVODXON_DONE = (
    "✅ Tekshiruv tugadi: {total} joyda imlo xatosi tuzatildi.\n\n"
    "{items}\n\n"
    "⚠️ Sun’iy intellekt ham adashishi mumkin — tuzatishlarni ko‘zdan kechiring."
)
SAVODXON_MORE = "… va yana {count} ta"
SAVODXON_CLEAN = "✅ Imlo xatosi topilmadi."
SAVODXON_LIMIT = (
    "Bugungi bepul tekshiruvlar tugadi ({limit} ta). Ertaga yana urinib ko‘ring yoki "
    "«✏️ Maqolani tahrirlash» xizmatidan foydalaning — mutaxassis matnni to‘liq tahrir qiladi."
)
SAVODXON_TOO_LONG = "Matn juda uzun (taxminan 25 betdan ko‘p). Iltimos, uni qismlarga bo‘lib yuboring."
SAVODXON_OFF = "Imlo tekshiruvi vaqtincha ishlamayapti. Birozdan keyin urinib ko‘ring."

ALPHABET_NOTHING = (
    "Matnda o‘giradigan so‘z topilmadi.\n\n"
    "Matn allaqachon kerakli yozuvda yoki inglizcha bo‘lishi mumkin."
)

# ---------- Plagiatga tekshirish ----------

PLAGIAT = (
    "🧾 <b>Plagiatga tekshirish</b>\n\n"
    "Maqolangizni plagiat va sun’iy intellektdan foydalanish bo‘yicha tekshirib beramiz.\n\n"
    "📎 Faylni shu yerga yuboring — <b>Word (.doc, .docx)</b> yoki <b>PDF</b>, 20 MB gacha.\n\n"
    "Tekshiruv natijasi tayyor bo‘lgach, adminlarimiz siz bilan bog‘lanadi."
)
PLAGIAT_WRONG = "Iltimos, maqolani <b>Word (.doc, .docx)</b> yoki <b>PDF</b> fayl ko‘rinishida yuboring."
PLAGIAT_TOO_BIG = "Fayl 20 MB dan katta. Iltimos, kichikroq fayl yuboring."
PLAGIAT_DONE = (
    "✅ Rahmat, {name}! Faylingiz qabul qilindi.\n\n"
    "Natija tayyor bo‘lganida siz bilan adminlarimiz bog‘lanadi."
)

# ---------- Hammualliflik: foydalanuvchilar maqolalari ----------

ARTICLE_SUBMIT = (
    "📝 <b>Hammualliflik uchun maqola joylash</b>\n\n"
    "Maqolangizni yuboring — Fihria Academic mutaxassislari ko‘rib chiqadi va tasdiqlangach, u hammualliflik "
    "bo‘limiga joylanadi. Hammuallif bo‘lishni istaganlar bilan adminlarimiz bog‘lanadi.\n\n"
    "🔒 Boshqa foydalanuvchilarga faqat <b>sarlavha, annotatsiya, baza va o‘rinlar soni</b> ko‘rinadi. "
    "Maqola fayli va ismingiz faqat adminlarga ko‘rinadi.\n\n"
    "1️⃣ Maqola <b>sarlavhasini</b> yozing:"
)
ARTICLE_TITLE_INVALID = "Sarlavha 5 dan 300 belgigacha bo‘lsin. Qaytadan yozing:"
ARTICLE_DIRECTION = "2️⃣ Maqola qaysi <b>yo‘nalishga</b> tegishli?"
ARTICLE_BASE = "3️⃣ Maqola qaysi <b>bazadagi</b> jurnalga mo‘ljallangan?"
ARTICLE_ANNOTATION = (
    "4️⃣ Maqolaning qisqa <b>annotatsiyasini</b> yozing (30–1000 belgi).\n\n"
    "<i>Bu matn boshqa foydalanuvchilarga ko‘rinadi — unga ism, telefon va boshqa shaxsiy ma’lumotlarni "
    "yozmang.</i>"
)
ARTICLE_ANNOTATION_INVALID = "Annotatsiya 30 dan 1000 belgigacha bo‘lsin. Qaytadan yozing:"
ARTICLE_PRICES = (
    "5️⃣ Hammualliflar uchun <b>o‘rinlar narxini</b> ($) yozing — 1-o‘rindan boshlab, bo‘sh joy bilan. "
    "Nechta narx yozsangiz, shuncha hammuallif o‘rni bo‘ladi (10 tagacha).\n\n"
    "Masalan: <code>550 540 530</code> — 3 ta o‘rin: 1-o‘rin 550$, 2-o‘rin 540$, 3-o‘rin 530$.\n\n"
    "<i>Bu sizning taklifingiz — adminlar ko‘rib chiqib, kerak bo‘lsa siz bilan kelishadi.</i>"
)
ARTICLE_PRICES_INVALID = (
    "Narxlarni faqat raqam bilan, bo‘sh joy qo‘yib yozing (1 dan 10 tagacha o‘rin).\n"
    "Masalan: <code>550 540 530</code>"
)
ARTICLE_FILE = (
    "6️⃣ Maqola <b>faylini</b> yuboring — Word (.doc, .docx) yoki PDF, 20 MB gacha.\n\n"
    "<i>Fayl faqat adminlarga ko‘rinadi.</i>"
)
ARTICLE_CONFIRM = "Ma’lumotlarni tekshiring:\n\n{summary}\n\nAdminlarga ko‘rib chiqish uchun yuboraymi?"
ARTICLE_SENT = (
    "✅ Rahmat! Maqolangiz <b>#{id}</b> ko‘rib chiqish uchun adminlarga yuborildi.\n\n"
    "Tasdiqlangach yoki rad etilsa, shu bot orqali xabar beramiz. Holatini «🗂 Mening maqolalarim» bo‘limida "
    "ko‘rishingiz mumkin."
)
ARTICLE_CANCELLED = "❌ Maqola yuborish bekor qilindi."
ARTICLE_EXPIRED = "Ma’lumotlar topilmadi. Iltimos, maqola joylashni qaytadan boshlang."

ARTICLES = (
    "📖 <b>Hammualliflik uchun maqolalar</b>\n\n"
    "Bu yerda Fihria Academic tasdiqlagan, hammuallif izlayotgan maqolalar joylangan. Qiziqtirgan maqola ostidagi "
    "«🤝 Hammuallif bo‘lish» tugmasini bosing — adminlarimiz siz bilan bog‘lanadi.\n\n"
    "Yo‘nalishni tanlang (qavs ichida — maqolalar soni) 👇"
)
ARTICLES_EMPTY = "Bu yo‘nalish bo‘yicha hozircha maqola yo‘q. Tez orada yangilari qo‘shiladi."
ARTICLE_APPLY = "🤝 Hammuallif bo‘lish uchun telefon raqamingizni qoldiring 👇"
ARTICLE_OWN = "Bu o‘zingizning maqolangiz 🙂"
ARTICLE_UNAVAILABLE = "Bu maqola endi mavjud emas yoki o‘rinlar to‘lgan."

MY_ARTICLES_EMPTY = "Siz hali maqola joylamagansiz."

ARTICLE_APPROVED = (
    "✅ Maqolangiz <b>#{id}</b> tasdiqlandi va hammualliflik bo‘limiga joylandi!\n\n"
    "«{title}»\n\nHammuallif bo‘lishni istaganlar paydo bo‘lishi bilan adminlarimiz siz bilan bog‘lanadi."
)
ARTICLE_ANNOUNCE = (
    "🆕 <b>Yo‘nalishingizda hammualliflik uchun yangi maqola!</b>\n\n{card}\n\n"
    "Hammuallif bo‘lishni istasangiz, quyidagi tugmani bosing — adminlarimiz siz bilan bog‘lanadi 👇"
)
ARTICLE_REJECTED = "❌ Afsuski, maqolangiz <b>#{id}</b> tasdiqlanmadi.\n\n«{title}»{reason}"

# ---------- Ko'p beriladigan savollar ----------

FAQ = "❓ <b>Ko‘p beriladigan savollar</b>\n\nSavolni tanlang 👇 Javob topa olmasangiz, bepul maslahat oling."

# (tugma matni, javob)
FAQ_ITEMS = [
    (
        "Soxta jurnalni qanday aniqlash mumkin?",
        "• ISSN raqamini portal.issn.org saytida tekshiring — ro‘yxatda bo‘lmasa, ehtiyot bo‘ling.\n"
        "• Scopus indeksatsiyasini faqat Scopus Sources ro‘yxatidan, Web of Science’ni Master Journal List’dan "
        "tekshiring — jurnal saytidagi logotiplar dalil emas. Botdagi «🔎 Scopus’da jurnalni tekshirish» bo‘limidan "
        "ham foydalanishingiz mumkin.\n"
        "• Domen nomi taniqli jurnalnikiga juda o‘xshash, lekin biroz farq qilsa — bu «o‘g‘irlangan» (hijacked) "
        "jurnal belgisi bo‘lishi mumkin.\n"
        "• «3 kunda Scopus», «100% kafolat» kabi va’dalar va taqrizsiz nashr — jiddiy xavf belgisi.\n"
        "• OAK tan olishini doim OAK rasmiy ro‘yxati va talablaridan tekshiring.",
    ),
    (
        "Maqolani kim yozadi?",
        "Maqola muallifning o‘z tadqiqoti, ma’lumotlari va ishtirokida tayyorlanadi. Biz reja, adabiyotlar sharhi, "
        "tahlil, tahrir va rasmiylashtirishda yordam beramiz.",
    ),
    (
        "Nashr qancha vaqt oladi?",
        "Bu tanlangan jurnalning chiqish davriyligi va taqriz jarayoniga bog‘liq. Aniq muddatni buyurtma vaqtida "
        "jurnal talablariga qarab aytamiz.",
    ),
    (
        "Jurnallarni OAK tan oladimi?",
        "Faqat OAK ro‘yxatiga kiritilgan nashrlar tan olinadi — har doim OAK rasmiy ro‘yxatidan tekshiring. Xalqaro "
        "jurnallardan odatda Scopus va Web of Science bazalaridagilari hisobga olinadi.",
    ),
    (
        "Plagiat foizi qancha bo‘lishi kerak?",
        "Har bir jurnalning o‘z talabi bor. «🧾 Plagiatga tekshirish» xizmatimizda hisobot va o‘xshashlikni "
        "kamaytirish bo‘yicha tavsiyalar beramiz.",
    ),
    (
        "Sertifikat beriladimi?",
        "Ko‘plab jurnal va konferensiyalar elektron sertifikat beradi, lekin bu har bir nashrning o‘z qoidasiga "
        "bog‘liq. Buyurtma vaqtida aniqlashtiramiz.",
    ),
    (
        "To‘lov qanday amalga oshiriladi?",
        "Avval so‘rov qoldirasiz, menejer ish hajmi va narxni tasdiqlaydi, shundan keyin to‘lov tartibini "
        "kelishasiz.",
    ),
]
