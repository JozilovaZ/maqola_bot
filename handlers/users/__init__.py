from handlers.users.about import about_router
from handlers.users.admin import admin_router
from handlers.users.admin_tools import admin_tools_router
from handlers.users.coauthor import coauthor_router
from handlers.users.contact import contact_router
from handlers.users.echo import echo_router
from handlers.users.registration import registration_router
from handlers.users.scopus_check import scopus_router
from handlers.users.services import services_router
from handlers.users.start import user_router

routers_list = [
    registration_router,
    admin_router,
    admin_tools_router,
    user_router,
    about_router,
    services_router,
    coauthor_router,
    scopus_router,
    contact_router,
    echo_router,
]

__all__ = [
    "routers_list",
]
