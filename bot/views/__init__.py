__all__ = ("main_router",)

from aiogram import Router
from .base import base_router
from .view import view_router
from .crud import crud_router

main_router = Router(name="main_router")

main_router.include_routers(base_router, view_router, crud_router)
