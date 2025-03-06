__all__ = ("crud_router",)

from aiogram import Router
from .create_task.views import router as create_router
from .read_task.views import router as read_router

crud_router = Router(name="crud_router")

crud_router.include_router(create_router)
crud_router.include_router(read_router)
