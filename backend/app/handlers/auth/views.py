from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import Annotated
import secrets
from core import auth, db_helper, settings, auth
from core.models import User
from .schemes import RegistrationUser, UserReturn

security = HTTPBasic()
router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login", status_code=200)
async def login_view(login: User = Depends(auth.login)):
    """
    Обработчик для входа пользователя в систему.

    Данная функция выполняет роль обёртки для вызова функции `auth.login`.
    Самостоятельно она не содержит никакой логики, а используется исключительно
    как представление (view) для маршрута.

    Возвращает статус 200 и User-а при успешной авторизации пользователя.
    """
    return UserReturn(id=login.id, user_name=login.user_name)


@router.post("/registration", status_code=201)
async def registration_view(
    user: RegistrationUser, session: AsyncSession = Depends(db_helper.session)
) -> None:
    """
    Обработчик регистрации нового пользователя.

    Ожидает объект `user` в теле запроса с данными:
    - `user_name` (имя пользователя)
    - `chat_id` (идентификатор чата)

    Функция создаёт нового пользователя в базе данных.
    При успешном выполнении возвращает статус 201 без тела ответа.

    В случае конфликта, например, если пользователь с такими данными уже существует,
    возвращается ошибка 400 с соответствующим сообщением.
    """
    hashed_chat_id: bytes = auth.hash_password(password=user.chat_id)
    user.chat_id = hashed_chat_id
    user_model = User(**user.model_dump())
    session.add(user_model)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=settings.errors.registration_error,
        )
    return
