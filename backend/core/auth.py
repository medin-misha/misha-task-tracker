from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt
from typing import Annotated
import secrets
from core.models import User
from core import db_helper, settings


security = HTTPBasic()


def validate_password(password: str, hashed_password: bytes) -> bool:
    """
    Функция сравнения хешированного пароля с паролем.
    """
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)


async def login(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    session: AsyncSession = Depends(db_helper.session),
) -> User:
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

    if validate_password(
        password=credentials.password, hashed_password=user.chat_id
    ):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=settings.errors.auth_error
    )


def hash_password(password: str) -> bytes:
    """
    Функция хеширования пароля
    """
    salt = bcrypt.gensalt()
    password_bytes: bytes = password.encode()
    return bcrypt.hashpw(password=password_bytes, salt=salt)
