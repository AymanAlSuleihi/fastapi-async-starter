from src.core.config import settings
from src.modules.items.router import router as items_router
from src.users.router import router as users_router


def register_routers(app):
    app.include_router(users_router, prefix=settings.API_V1_PREFIX)
    app.include_router(items_router, prefix=settings.API_V1_PREFIX)
