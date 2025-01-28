__all__ = ("crud_router", "auth_router")

from .crud.views import router as crud_router
from .auth.views import router as auth_router