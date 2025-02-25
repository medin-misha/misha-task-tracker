__all__ = ("base_router",)

from aiogram import Router
from .commands import router

base_router = Router(name="base_router")

base_router.include_router(router=router)
