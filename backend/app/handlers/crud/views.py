from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import create_model
from typing import Union
from .schemas import CreateReplay, CreateTask, CreateUser
from core import create, get_by_id, get_list, update, delete, db_helper, settings
from core.models import models, Base

router = APIRouter(prefix="/crud", tags=["crud"])


@router.get("/{model_name:str}/{id:int}")
async def get_model_by_id_view(
    model_name: str, id: int, session: AsyncSession = Depends(db_helper.session)
):
    """
    Получение экземпляра модели по имени и идентификатору.

    Этот метод предоставляет возможность получить объект определённой модели
    на основе её имени и идентификатора.

    Параметры:
    - `model_name` (str): Имя модели, например, "user" или "post".
    - `id` (int): Уникальный идентификатор объекта модели.
    - `session` (AsyncSession): Сессия для работы с базой данных (передаётся через Depends).

    Пример использования:
        GET /user/1

    Обработка ошибок:
    - Если модель с указанным именем не найдена в списке доступных моделей,
    возвращается ошибка с кодом 404 и сообщением из `settings.errors.defunct_model`.
    - Если объект с указанным идентификатором не найден, возвращается ошибка
    с кодом 404 и сообщением из `settings.errors.not_fount_by_id`.

    Возвращает:
    - Экземпляр модели, если он найден.
    """

    if not model_name in models.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=settings.errors.defunct_model
        )
    model: typing.Optional[Base] = await get_by_id(
        session=session, model=models.get(model_name), id=id
    )
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=settings.errors.not_fount_by_id.format(model=model_name, id=id),
        )
    return model


@router.get("/{model_name:str}/")
async def get_model_list_view(
    model_name: str, session: AsyncSession = Depends(db_helper.session)
):
    """
    Получение списка объектов модели.

    Этот метод позволяет получить список всех объектов указанной модели.

    Параметры:
    - `model_name` (str): Имя модели, для которой необходимо получить список объектов (например, "user" или "post").
    - `session` (AsyncSession): Сессия для работы с базой данных (передаётся через Depends).

    Пример использования:
        GET /user/

    Обработка ошибок:
    - Если модель с указанным именем не найдена в списке доступных моделей,
      возвращается ошибка с кодом 404 и сообщением из `settings.errors.defunct_model`.

    Возвращает:
    - Список объектов указанной модели.
    """

    if not model_name in models.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=settings.errors.defunct_model
        )
    return await get_list(session=session, model=models.get(model_name))


@router.post("/{model_name:str}")
async def create_model_view(
    model_name: str,
    data: Union[CreateTask, CreateReplay],
    session: AsyncSession = Depends(db_helper.session),
):
    """
    Создание нового объекта модели.

    Этот метод позволяет создать новый объект определённой модели с использованием предоставленных данных.

    Параметры:
    - `model_name` (str): Имя модели, для которой необходимо создать объект (например, "task", "replay").
    - `data` (Union[CreateUser, CreateTask, CreateReplay]): Данные для создания объекта модели.
      Ожидается экземпляр одной из предварительно определённых схем (например, `CreateUser`, `CreateTask`, `CreateReplay`).
    - `session` (AsyncSession): Сессия для работы с базой данных (передаётся через Depends).

    Пример использования:
        POST /user
        Тело запроса:
        {
            "user_name": "Jane Doe",
            "chat_id": "978465132"
        }

    Обработка ошибок:
    - Если модель с указанным именем не найдена в списке доступных моделей,
      возвращается ошибка с кодом 404 и сообщением из `settings.errors.defunct_model`.

    Возвращает:
    - Объект модели, созданный на основе переданных данных.

    !!! модель user создаёться в /auth/registration!!!
    """

    if not model_name in models.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=settings.errors.defunct_model
        )
    if model_name == "user":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user создаёться в auth/registration",
        )
    return await create(session=session, model=models.get(model_name), data=data)


@router.patch("/{model_name:str}/{id:int}")
async def patch_model_view(
    model_name: str,
    id: int,
    data: dict,
    session: AsyncSession = Depends(db_helper.session),
):
    """
    Обновление объекта модели по имени и идентификатору.

    Этот метод позволяет обновить указанные поля объекта определённой модели.

    Параметры:
    - `model_name` (str): Имя модели, объект которой необходимо обновить (например, "user" или "task").
    - `id` (int): Уникальный идентификатор объекта модели, который требуется обновить.
    - `data` (dict): Словарь с данными, которые нужно обновить (ключи — это имена полей, значения — новые значения для полей).
    - `session` (AsyncSession): Сессия для работы с базой данных (передаётся через Depends).

    Пример использования:
        PATCH /user/1
        Тело запроса:
        {
            "user_name": "John Doe",
            "cahat_id": "817287127498"
        }

    Обработка ошибок:
    - Если модель с указанным именем не найдена в списке доступных моделей,
      возвращается ошибка с кодом 404 и сообщением из `settings.errors.defunct_model`.
    - Если объект с указанным идентификатором не найден, возвращается ошибка
      с кодом 404 и сообщением из `settings.errors.not_fount_by_id`.

    Возвращает:
    - Обновлённый объект модели.

    Примечание:
    - Для создания валидационной модели (Pydantic) для входных данных используется динамическое создание класса `UpdateModel`.
    """

    if not model_name in models.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=settings.errors.defunct_model
        )
    UpdateModel = create_model(
        "UpdateModel", **{key: (type(value), ...) for key, value in data.items()}
    )
    model: typing.Optional[Base] = await update(
        session=session, id=id, data=UpdateModel(**data), model=models.get(model_name)
    )
    if model:
        return model
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=settings.errors.not_fount_by_id.format(model=model_name, id=id),
    )


@router.delete("/{model_name:str}/{id:int}", status_code=204)
async def delete_model_view(
    model_name: str, id: int, session: AsyncSession = Depends(db_helper.session)
):
    """
    Удаление объекта модели по имени и идентификатору.

    Этот метод позволяет удалить объект указанной модели по её имени и идентификатору.

    Параметры:
    - `model_name` (str): Имя модели, объект которой необходимо удалить (например, "user", "task", "replay").
    - `id` (int): Уникальный идентификатор объекта модели, который требуется удалить.
    - `session` (AsyncSession): Сессия для работы с базой данных (передаётся через Depends).

    Пример использования:
        DELETE /user/1

    Обработка ошибок:
    - Если модель с указанным именем не найдена в списке доступных моделей,
      возвращается ошибка с кодом 404 и сообщением из `settings.errors.defunct_model`.
    - Если объект с указанным идентификатором не найден, возвращается ошибка
      с кодом 404 и сообщением из `settings.errors.not_fount_by_id`.

    Возвращает:
    - Статус 204 (No Content), если объект успешно удалён.
    """

    if not model_name in models.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=settings.errors.defunct_model
        )
    model: bool = await delete(session=session, model=models.get(model_name), id=id)
    if model:
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=settings.errors.not_fount_by_id.format(model=model_name, id=id),
    )
