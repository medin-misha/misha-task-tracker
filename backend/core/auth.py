from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
import secrets
from core.models import User
from core import db_helper

security = HTTPBasic()

async def login(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    session: AsyncSession = Depends(db_helper.session)
) -> None:
    """
    Функция авторизации пользователя.

    Ожидает следующие данные:
    - `credentials` (объект с username и password, полученный через `HTTPBasic` аутентификацию)
    - `session` (асинхронная сессия базы данных)

    Выполняет проверку существования пользователя в базе данных по полю `user_name`.
    Затем сравнивает хэшированный `chat_id` пользователя с паролем, переданным в запросе.

    При успешной проверке ничего не возвращает. Если проверка не пройдена, 
    выбрасывает исключение HTTP 401 Unauthorized с соответствующим сообщением.
    """
    stmt = select(User).where(User.user_name == credentials.username)
    stmt_result: Result = await session.execute(stmt)
    user: User = stmt_result.scalar()

    if secrets.compare_digest(
        user.chat_id.encode("utf-8"), credentials.password.encode("utf-8")
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=settings.errors.auth_error
    )

