from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

# Buyruqlar menyusi
COMMANDS = [
    BotCommand(command="hero", description="🏠 Bosh sahifa"),
    BotCommand(command="scopus_check", description="🔎 Scopus’da jurnalni tekshirish"),
    BotCommand(command="about", description="🏛 Fihria Academic haqida"),
    BotCommand(command="services", description="💼 Fihria Academic xizmatlari"),
    BotCommand(command="help", description="💬 Bepul maslahat"),
    BotCommand(command="co_authorship", description="🤝 Scopus/WoS hammuallifligi"),
    BotCommand(command="journals", description="📚 Jurnallar javoni"),
    BotCommand(command="plagiat", description="🧾 Plagiatga tekshirish"),
]


# Faqat adminlarga ko'rinadigan qo'shimcha buyruqlar
ADMIN_COMMANDS = [
    BotCommand(command="leads", description="📋 Ochiq arizalar"),
    BotCommand(command="export", description="📥 Arizalar va foydalanuvchilar Excel faylda"),
    BotCommand(command="topics", description="🛠 Hammualliflik mavzularini boshqarish"),
    BotCommand(command="shelf", description="📚 Jurnallar javonini boshqarish"),
    BotCommand(command="articles", description="🤝 Hammualliflik maqolalarini ko‘rib chiqish"),
    BotCommand(command="media", description="🖼 Rasm va PDF'larni yuklash"),
    BotCommand(command="stat", description="📊 Statistika"),
    BotCommand(command="broadcast", description="📣 Hammaga xabar yuborish"),
]


async def set_default_commands(bot: Bot, admin_ids: list[int]) -> None:
    await bot.set_my_commands(COMMANDS, scope=BotCommandScopeDefault())
    for admin_id in admin_ids:
        try:
            await bot.set_my_commands(COMMANDS + ADMIN_COMMANDS, scope=BotCommandScopeChat(chat_id=admin_id))
        except Exception:
            # Admin botga hali /start bosmagan bo'lsa
            pass
