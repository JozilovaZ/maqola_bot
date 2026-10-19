# Botning barcha matnlari (original @Mirzo_MA_bot dan aynan). {name} — foydalanuvchining to'liq ismi.

GREETING = (
    "Assalomu alaykum, {name}! 👋\n\n"
    "Men — Oʻzbekiston tadqiqotchilari uchun Maqolalar akademiyasi yordamchisi Mirzoman.\n\n"
)

MAIN_MENU = GREETING + (
    "Xush kelibsiz! Menyuda siz:\n\n"
    "📝 Foydali maqola va materiallarni o‘qishingiz\n\n"
    "🏛 Maqolalar akademiyasi haqida batafsil ma’lumot olishingiz mumkin\n\n"
    "🔎 Jurnalning Scopus’dagi holatini tekshirishingiz\n\n"
    "📌 Akademiyaning dolzarb xizmatlari bilan tanishishingiz\n\n"
    "🤝 Scopus/Web of Science tizimlarida hammualliflik bo‘yicha dolzarb mavzularni ko‘rib chiqish\n\n"
    "Kerakli bo‘limni tanlang — men sizga mamnuniyat bilan yordam beraman."
)

# ---------- Foydali materiallar ----------

GUIDES = (
    "📚 Foydali materiallar\n\n"
    "Bu yerda Maqolalar akademiyasining maqolalari va chek-listlari jamlangan — nashr qilish, jurnal tanlash, "
    "dissertatsiyalar va ilmiy rivojlanish bo‘yicha sodda tushuntirishlar.\n\n"
    "Sizni qiziqtirgan bo‘limni tanlang 👇"
)

CHECKLISTS = (
    "Maqola tayyorlash, jurnal tanlash, dissertatsiya ustida ishlash yoki ilmiy profilingizni rivojlantirish "
    "jarayonida hech narsani e’tibordan chetda qoldirmaslikka yordam beradigan bosqichma-bosqich "
    "chek-listlarni jamladik.\n\n"
    "Quyidagi kerakli chek-listni tanlang 👇"
)

CHECKLIST_TEXTS = {
    "phd": (
        "Xush kelibsiz! PhD himoyasiga chiqish uchun hujjatlar checklisti allaqachon shu yerda 📁\n\n"
        "Instagram'da va'da berganimizdek — OAK nizomining 2893-sonli 2-ilovasiga muvofiq rasmiy to'plamni "
        "yubormoqdamiz.\n\n"
        "Doktorantlarning ko'pchiligi 6 dan 12 oygacha vaqtni ilmiy qism tufayli emas, balki rasmiy xatolar "
        "tufayli yo'qotishadi: noto'g'ri tasdiqlangan joriy etish dalolatnomasi, ishlar ro'yxatining eskirgan "
        "shakli yoki hammualliflarning yozma roziligi yo'qligi.\n\n"
        "Hozir nima qilish kerak:\n\n"
        "Quyidagi faylni yuklab ol ⬇️\n"
        "Ilmiy kotibga tashrifdan oldin papkangni band-band tekshirib chiq.\n"
        "Agar kamida bitta hujjat yetishmasa — bu masalani oldindan hal qilib qo'y."
    ),
    "rejected": (
        "📘 Maqolangiz rad etildimi? Keyingi qadamni to‘g‘ri tanlang\n"
        "Rad javobi — tadqiqotning yakuni emas. Muhimi, muharrir va taqrizchi izohlarini to‘g‘ri tahlil qilib, "
        "maqolani qayta topshirishga tayyorlash.\n"
        "Siz uchun «Maqolangiz rad etildimi? 5 qadamli harakat rejasi» chek-listini tayyorladik.\n"
        "Unda siz:\n"
        "✅ muharrir qarorining turini aniqlaysiz;\n"
        "✅ taqrizchi izohlarini tizimlashtirasiz;\n"
        "✅ har bir izohga to‘g‘ri javob tayyorlaysiz;\n"
        "✅ shu jurnalda qolish yoki boshqasini tanlashni hal qilasiz;\n"
        "✅ maqolani qayta yuborishdan oldin tekshirasiz.\n"
        "Chek-listni saqlab qo‘ying va qayta topshirishdan oldin barcha bosqichlarni tekshiring 👇"
    ),
    "reply": (
        "🤖 Salom! Men Mirzo — Maqolalar akademiyasi yordamchi botiman.\n"
        "Maqolangizga taqrizchilar izoh berdimi?\n\n"
        "Javob xatini qanday tuzishni bilmasangiz, siz uchun tayyor chek-list bor.\n\n"
        "Unda:\n"
        "✅ har bir izohga qanday javob berish\n"
        "✅ o‘zgarishlarni qanday ko‘rsatish\n"
        "✅ rozi bo‘lmaganda qanday muloyim argument qilish\n"
        "✅ javob xatini yuborishdan oldin nimalarni tekshirish\n\n"
        "📌 Chek-listni saqlab qo‘ying — retsenziya kelganda tayyor qo‘llanma bo‘ladi."
    ),
    "redflags": (
        "🤖 Salom! Men Mirzo — Maqolalar akademiyasi yordamchi botiman.\n\n"
        "Maqolangizni Scopus jurnaliga yubormoqchimisiz? Avval jurnalni tekshirib oling.\n\n"
        "Siz uchun «Scopus jurnalini tanlash: 7 ta xavf belgisi» chek-listini tayyorladik.\n"
        "Unda:\n\n"
        "✅ nashrlar sonining shubhali o‘sishini aniqlash\n"
        "✅ maqolalarning jurnal yo‘nalishi va sifatiga e’tibor berish\n"
        "✅ haddan tashqari tez nashr va’dalari va tinimsiz taklif xatlarini baholash\n"
        "✅ aniqlangan belgilar asosida xavf darajasini tekshirish\n\n"
        "📌 Chek-listni saqlab qo‘ying — maqolangizni yuborishdan oldin jurnalni tekshirishda yordam beradi."
    ),
}

BLOG = (
    "Blogimizda olimlar uchun dolzarb va amaliy materiallar jamlangan:\n\n"
    "• Oʻzbekiston Respublikasi OAKdagi yangilanishlar hamda dissertatsiya himoyasi yoki ilmiy unvon olish "
    "uchun nashr talablari;\n"
    "• Scopus, Web of Science va OAK jurnallarida maqola chop etish xususiyatlari;\n"
    "• maqolani yuborish bo‘yicha tavsiyalar, odatiy xatolar va jurnal tanlashdagi muhim jihatlar;\n"
    "• Hirsh indeksi, ORCID va ilmiy rivojlanish uchun boshqa vositalar.\n\n"
    "Quyidagi sizni qiziqtirgan maqolani tanlang 👇"
)

# ---------- Akademiya haqida ----------

ABOUT = GREETING + (
    "Xizmatni tanlashdan oldin Maqolalar akademiyasi — jamoamiz, ish yondashuvimiz va mijozlar uchun "
    "kafolatlarimiz bilan yaqindan tanishib chiqishni taklif qilaman.\n\n"
    "Ilmiy maqolangizni, dissertatsiyangizni yoki boshqa muhim loyihangizni kimga ishonib topshirayotganingizni "
    "yaxshi tushunishingiz biz uchun muhim.\n\n"
    "Quyidagi bo‘limni tanlang — olimlar nima uchun Maqolalar akademiyasini tanlashlarini bilib oling 👇"
)

# Originalda matn "bo‘y" so'zida kesilib qolgan — oxiri to'ldirildi
ABOUT_WHY = (
    "⭐ Nega olimlar Maqolalar akademiyasini tanlashadi?\n\n"
    "Biz shaffof ishlaymiz, mijozlarni har bir bosqichda qo‘llab-quvvatlaymiz va hatto noodatiy ilmiy "
    "vazifalar uchun ham yechim topishga yordam beramiz.\n\n"
    "Bizning afzalliklarimiz:\n\n"
    "• menejerlar doimo aloqada;\n"
    "• halol va ochiq muloqot;\n"
    "• shaffof narxlar va to‘lovni bosqichma-bosqich amalga oshirish imkoniyati;\n"
    "• barcha jurnallar va materiallar yuborishdan oldin mijoz bilan kelishiladi;\n"
    "• professional tahririy nazorat, plagiat va sun’iy intellektdan foydalanish bo‘yicha tekshiruv;\n"
    "• ishonchli jurnallarni tanlashda yordam va xavfli nashrlar haqida ogohlantirish;\n"
    "• individual va noodatiy so‘rovlar bo‘yicha yordam."
)

# Originalda bu ikki tugma javob bermaydi — NAMUNA matn, o'zingiznikiga almashtiring
ABOUT_GUARANTEES = (
    "🛡 Bizning kafolatlarimiz\n\n"
    "• hamkorlik rasmiy shartnoma asosida amalga oshiriladi;\n"
    "• to‘lovni bosqichma-bosqich amalga oshirish mumkin;\n"
    "• shartnoma shartlari bajarilmagan taqdirda mablag‘ qaytariladi;\n"
    "• barcha materiallar maxfiy saqlanadi."
)

ABOUT_REVIEWS = (
    "💬 Mijozlarimiz fikrlari\n\n"
    "Bu yerga mijozlaringiz fikrlarini yozing."
)

# ---------- Xizmatlar ----------

SERVICES = (
    "Assalomu alaykum, {name}! 👋\n\n"
    "Men — Maqolalar akademiyasi yordamchisi Mirzoman.\n\n"
    "Bu yerda nashr qilishni rejalashtirayotgan, hammualliflik izlayotgan yoki professional yordamga muhtoj "
    "bo‘lganlar uchun barcha xizmatlarimiz jamlangan.\n\n"
    "Menyudan kerakli xizmatni tanlang — batafsil ma’lumot, shartlar va keyingi qadamlar bilan tanishing."
)

SERVICE_TEXTS = {
    "scopus": (
        "📚 Scopus’da maqola chop etish\n\n"
        "Scopus bazasida indekslanadigan jurnalda maqola chop etishni rejalashtiryapsizmi? Maqolalar akademiyasi "
        "maqola yozilishidan boshlab, uning Scopus bazasida indekslanishigacha bo‘lgan butun jarayonni kuzatib "
        "boradi.\n\n"
        "Xizmat tarkibiga quyidagilar kiradi:\n\n"
        "• ilmiy maqolani yozish yoki professional auditdan o‘tkazish;\n"
        "• mavzuingiz, mutaxassisligingiz va talab etiladigan percentilni inobatga olgan holda Scopus Q1–Q4 "
        "jurnalini tanlash;\n"
        "• matnni Turnitin orqali plagiat va sun’iy intellektdan foydalanish bo‘yicha tekshirish;\n"
        "• maqolani topshirishdan oldin siz bilan kelishish;\n"
        "• tahririyatga yuborish, taqriz jarayonini kuzatish va tuzatishlar kiritish;\n"
        "• nashrni nazorat qilish hamda Scopus bazasida indekslanishini kafolatlash.\n\n"
        "Hamkorlik rasmiy shartnoma asosida amalga oshiriladi. To‘lovni bosqichma-bosqich amalga oshirish mumkin; "
        "shartnoma shartlari bajarilmagan taqdirda mablag‘ qaytarilishi nazarda tutiladi.\n\n"
        "Nashrning taxminiy muddati soha va jurnal siyosatiga qarab 4 oydan 12 oygacha.\n\n"
        "Maqola chop etishga buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? "
        "Quyidagi kerakli tugmani tanlang 👇"
    ),
    "wos": (
        "🔬 Web of Science’da maqola chop etish\n\n"
        "Web of Science bazasida indekslanadigan jurnalda maqola chop etishni rejalashtiryapsizmi? Maqolalar "
        "akademiyasi maqola yozilishidan boshlab, uning Web of Science bazasida indekslanishigacha bo‘lgan butun "
        "jarayonni kuzatib boradi.\n\n"
        "Xizmat quyidagilarni o‘z ichiga oladi:\n\n"
        "• nashr talablarini hisobga olgan holda maqolani yozish yoki auditdan o‘tkazish;\n"
        "• yo‘nalishingizga mos Web of Science jurnalini tanlash;\n"
        "• matnni Turnitin orqali plagiat va sun’iy intellektdan foydalanish bo‘yicha tekshirish;\n"
        "• yo‘nalishingiz bo‘yicha mutaxassis-muallifni tanlash;\n"
        "• har bir bosqichda matn va jurnalni siz bilan kelishish;\n"
        "• maqolani yuborish, tahririyat bilan muloqot qilish va taqrizdan keyingi tuzatishlarni kiritish;\n"
        "• nashr va indekslanishgacha bo‘lgan jarayonni kuzatib borish.\n\n"
        "Ish rasmiy shartnoma asosida olib boriladi. To‘lov ikki bosqichda — 50/50 shaklida amalga oshiriladi, "
        "jurnal tanlashdan tortib matnning yakuniy versiyasigacha bo‘lgan barcha muhim qarorlar siz bilan "
        "kelishiladi.\n\n"
        "Maqola chop etishga buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? "
        "Quyidagi kerakli tugmani tanlang 👇"
    ),
    "oak": (
        "🎓 OAK jurnallarida maqola chop etish\n\n"
        "Oʻzbekiston Respublikasi OAKning amaldagi roʻyxatidagi jurnalda maqola chop etishni rejalashtiryapsizmi? "
        "Maqolalar akademiyasi material tayyorlashdan boshlab, maqolaning rasmiy nashr qilinishigacha bo‘lgan "
        "butun jarayonni kuzatib boradi.\n\n"
        "Xizmat tarkibiga quyidagilar kiradi:\n\n"
        "• mavzuingiz bo‘yicha sifatli ilmiy maqola yozish yoki tayyor matnni professional auditdan o‘tkazish;\n"
        "• OAKning amaldagi ro‘yxatidan yo‘nalishingizga mos jurnalni tanlash va uni siz bilan kelishish;\n"
        "• maqolani plagiat va sun’iy intellektdan foydalanish bo‘yicha tekshirish;\n"
        "• faqat barqaror obro‘ga ega, sinovdan o‘tgan nashrlar bilan ishlash;\n"
        "• mavzu, muddat va narx belgilangan rasmiy shartnoma tuzish;\n"
        "• maqolani jurnalga yuborish, taqriz jarayonini kuzatish va zarur tuzatishlarni kiritish;\n"
        "• maqola OAK ro‘yxatidagi nashrda chop etilgungacha bo‘lgan jarayonni nazorat qilish.\n\n"
        "Xizmat narxi — 2 400 000 UZSdan boshlanadi. Yakuniy narx mutaxassislik va tanlangan jurnalga bog‘liq.\n\n"
        "Hamkorlik rasmiy shartnoma asosida amalga oshiriladi. To‘lovni 50/50 yoki 25/25/50 shaklida "
        "bosqichma-bosqich amalga oshirish mumkin. Shartnoma shartlari bajarilmagan taqdirda mablag‘ qaytarilishi "
        "nazarda tutiladi.\n\n"
        "Maqola chop etishga buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? "
        "Quyidagi kerakli tugmani tanlang 👇"
    ),
    "diss": (
        "🎓 Dissertatsiya bo‘yicha xizmatlar\n\n"
        "Dissertatsiya bo‘yicha yordam kerakmi? Alohida bobga ham, mavzu tanlashdan himoyaga tayyorgarlikkacha "
        "bo‘lgan kompleks yordamga ham buyurtma berishingiz mumkin.\n\n"
        "Ish yo‘nalishlari:\n\n"
        "• dissertatsiya mavzusini tanlash va asoslash;\n"
        "• reja va tuzilmani ishlab chiqish;\n"
        "• alohida boblarni yoki dissertatsiyani to‘liq tayyorlash;\n"
        "• ilmiy tahrirlash va korrektura;\n"
        "• bibliografiyani APA, GOST, MLA va boshqa uslublarda rasmiylashtirish;\n"
        "• StrikePlagiarism / Turnitin orqali plagiat va sun’iy intellektdan foydalanish bo‘yicha tekshirish;\n"
        "• matnning originalligini oshirish;\n"
        "• avtoreferatga taqriz hamda retsenziyalarni tayyorlash;\n"
        "• himoyagacha bo‘lgan tuzatishlarni kuzatib borish.\n\n"
        "Ishlar maxfiy tarzda va shartnoma asosida olib boriladi. To‘lovni 50/50 yoki 25/25/50 shaklida "
        "bosqichma-bosqich amalga oshirish mumkin.\n\n"
        "Bir bobni tayyorlashning taxminiy muddati uning turi va hajmiga bog‘liq.\n\n"
        "Dissertatsiya bo‘yicha xizmatga buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? "
        "Quyidagi kerakli tugmani tanlang 👇"
    ),
    "hirsh": (
        "📈 Hirsh indeksini oshirish\n\n"
        "Hirsh indeksi yoki h-indeks olimning ilmiy nufuzini uning nashrlari va iqtiboslari soni orqali "
        "ko‘rsatadi.\n\n"
        "Xizmat PhD darajasiga ega mutaxassislar, doktorantlar, tadqiqotchilar, grant tanlovlari ishtirokchilari "
        "hamda ilmiy profilini mustahkamlashni istaganlar uchun mos.\n\n"
        "Ish bosqichlari:\n\n"
        "• Scopus, Web of Science yoki Google Scholar’dagi profilingizni tahlil qilish;\n"
        "• maqsadli ko‘rsatkichni hisoblash;\n"
        "• zarur iqtiboslar sonini aniqlash;\n"
        "• mavzuga mos ilmiy nashrlarni tanlash;\n"
        "• akademik iqtiboslarni sohangizga oid tadqiqotlarga integratsiya qilish;\n"
        "• bajarilgan ishlar bo‘yicha oylik hisobotlarni taqdim etish.\n\n"
        "Ko‘rsatkich oshishining taxminiy muddati — 4 oydan 16 oygacha.\n\n"
        "Hirsh indeksingizni oshirmoqchimisiz yoki bepul maslahat olmoqchimisiz? "
        "Quyidagi kerakli tugmani tanlang 👇"
    ),
    "conf": (
        "🎤 Konferensiya tezislarini chop etish\n\n"
        "Ilmiy konferensiyada qatnashib, tezislarni chop ettirishingiz kerakmi? Materiallarni tayyorlash va ilmiy "
        "yo‘nalishingizga mos konferensiyani tanlashda yordam beramiz.\n\n"
        "Siz quyidagilarga ega bo‘lasiz:\n\n"
        "• sifatli konferensiya tezislarini yozish;\n"
        "• mos ilmiy konferensiyani tanlash;\n"
        "• materialni tashkiliy qo‘mita talablariga muvofiq rasmiylashtirish;\n"
        "• konferensiya ishtirokchisi sertifikati;\n"
        "• konferensiya materiallari to‘plamining PDF formatidagi nusxasi.\n\n"
        "Tezislar — tadqiqot natijalarining qisqacha bayoni bo‘lib, odatda 1 dan 5 sahifagacha bo‘ladi va ilmiy "
        "faolligingizni tasdiqlaydi.\n\n"
        "Tezislarni chop etishga buyurtma bermoqchimisiz yoki bepul maslahat olmoqchimisiz? "
        "Quyidagi kerakli tugmani tanlang 👇"
    ),
}

ORDER = (
    "📝 Arizangiz uchun rahmat!\n\n"
    "Menejer siz bilan bog‘lanib, xizmat tafsilotlarini muhokama qilishi uchun quyidagi tugma orqali telefon "
    "raqamingizni qoldiring 👇\n\n"
    "Maqolalar akademiyasi menejeri yaqin vaqt ichida sizga qo‘ng‘iroq qiladi."
)

CONSULT = (
    "Savolingiz bo‘yicha bepul maslahat olish uchun quyidagi tugma orqali telefon raqamingizni qoldiring 👇\n\n"
    "Maqolalar akademiyasi menejeri yaqin vaqt ichida siz bilan bog‘lanadi va barcha savollaringizga javob "
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
    "O‘zingizga qulay aloqa ma’lumotini qoldiring — Akademiya mutaxassisi siz bilan bog‘lanib, mos variantni "
    "tanlashga yordam beradi.\n\n"
    "Quyidagi qulay variantni tanlang 👇"
)

COAUTH_INDIVIDUAL = (
    "✅ Siz hammualliflik uchun bepul individual mavzular tanlovini tanladingiz.\n\n"
    "Telefon raqamingizni quyidagi tugma orqali qoldiring 👇\n\n"
    "Maqolalar akademiyasi menejeri yaqin vaqt ichida siz bilan bog‘lanadi va hammualliflik uchun dolzarb "
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
    "Mirzo sizga quyidagilarni aniqlashga yordam beradi:\n\n"
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

# Javob oxiri raqam qaysi bo'limdan qoldirilganiga bog'liq (reason)
CONTACT_TAILS = {
    "consult": (
        "Maqolalar akademiyasi menejeri yaqin vaqt ichida siz bilan bog‘lanadi va barcha savollaringizga "
        "javob beradi."
    ),
    "order": (
        "Maqolalar akademiyasi menejeri yaqin vaqt ichida sizga qo‘ng‘iroq qiladi va xizmat tafsilotlarini "
        "muhokama qiladi."
    ),
    "coauth": (
        "Maqolalar akademiyasi menejeri yaqin vaqt ichida siz bilan bog‘lanadi va hammualliflik uchun dolzarb "
        "mavzalarni taklif qiladi."
    ),
    "coauth_order": (
        "Maqolalar akademiyasi menejeri yaqin vaqt ichida siz bilan bog‘lanadi va hammualliflik tafsilotlarini "
        "muhokama qiladi."
    ),
    "scopus": "Mutaxassis jurnalni qo‘lda tekshirib, yaqin vaqt ichida siz bilan bog‘lanadi.",
    "audit": "Mutaxassis yaqin vaqt ichida bog‘lanadi va maqolangiz bo‘yicha bepul maslahat beradi.",
}

CONTACT_NOT_OWN = "Iltimos, pastdagi «Kontaktni ulashish» tugmasi orqali o‘zingizning raqamingizni yuboring."

# Bo'limlarga tegishli bo'lmagan har qanday xabarga javob
FALLBACK = "Rahmat; biz odatda bir necha soat ichida javob beramiz."

# ---------- Majburiy obuna ----------

SUBSCRIBE = (
    "Botdan foydalanish uchun quyidagi guruhga a’zo bo‘ling 👇\n\n"
    "A’zo bo‘lgach, <b>✅ Tekshirish</b> tugmasini bosing."
)
SUBSCRIBE_NOT_YET = "❌ Siz hali guruhga a’zo bo‘lmadingiz. Avval a’zo bo‘ling, so‘ng «Tekshirish»ni bosing."
SUBSCRIBE_DONE = "✅ Rahmat! Obuna tasdiqlandi."
