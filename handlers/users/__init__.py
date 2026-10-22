from handlers.users.about import about_router
from handlers.users.admin_admins import admin_admins_router
from handlers.users.text_tools import text_tools_router
from handlers.users.admin_articles import admin_articles_router
from handlers.users.articles import articles_router
from handlers.users.admin import admin_router
from handlers.users.admin_journals import admin_journals_router
from handlers.users.admin_tools import admin_tools_router
from handlers.users.coauthor import coauthor_router
from handlers.users.contact import contact_router
from handlers.users.echo import echo_router
from handlers.users.faq import faq_router
from handlers.users.journals import journals_router
from handlers.users.plagiat import plagiat_router
from handlers.users.registration import registration_router
from handlers.users.scopus_check import scopus_router
from handlers.users.services import services_router
from handlers.users.start import user_router

routers_list = [
    registration_router,
    admin_router,
    admin_tools_router,
    admin_admins_router,
    admin_journals_router,
    admin_articles_router,
    user_router,
    about_router,
    services_router,
    coauthor_router,
    articles_router,
    scopus_router,
    journals_router,
    plagiat_router,
    text_tools_router,
    faq_router,
    contact_router,
    echo_router,
]

__all__ = [
    "routers_list",
]
