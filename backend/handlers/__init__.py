__all__ = ("crud_router", "auth_router", "tasks_router")

from .crud.views import router as crud_router
from .auth.views import router as auth_router
from .tasks.views import router as tasks_router