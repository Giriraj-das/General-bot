__all__ = ('router',)

from aiogram import Router

from .base_commands import router as base_commands_router
from .callback_handlers import router as callback_handlers_router
from .user_commands import router as user_commands_router

router = Router(name=__name__)

router.include_routers(
    callback_handlers_router,
    base_commands_router,
    user_commands_router,
)
