from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import create_model
from typing import Union
from .schemas import CreateReplay, CreateTask, CreateUser
from core import create, get_by_id, get_list, update, delete, db_helper, settings
from core.models import models, Base

router = APIRouter(prefix="/crud", tags=["crud"])


@router.get("/{model:str}/{id:int}")
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
    data: Union[CreateUser, CreateTask, CreateReplay],
    session: AsyncSession = Depends(db_helper.session),
):
    if not model_name in models.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=settings.errors.defunct_model
        )

    return await create(session=session, model=models.get(model_name), data=data)


@router.patch("/{model:str}/{id:int}")
async def patch_model_view(
    model_name: str,
    id: int,
    data: dict,
    session: AsyncSession = Depends(db_helper.session),
):
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


@router.delete("/{model:str}/{id:int}", status_code=204)
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
