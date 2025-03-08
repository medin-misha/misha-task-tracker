from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from datetime import datetime
from typing import List, Dict
from core import auth, db_helper, settings
from core.crud import create, delete, get_by_id
from core.models import Replay, Task, User
from .schemes import ReplayScheme, TaskScheme, ReturnTask, TaskCreateScheme
from .utils import is_complete, get_n_days_grafic, user_notification

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", status_code=201)
async def create_task_view(
    replay_data: ReplayScheme,
    task_data: TaskScheme,
    user: User = Depends(auth.login),
    session: AsyncSession = Depends(db_helper.session),
) -> ReturnTask:
    """
    Создание задачи для пользователя.

    Этот эндпоинт позволяет создать новую задачу для текущего авторизованного пользователя.
    Перед созданием задачи создаётся связанный объект ответа (`Replay`).

    Параметры:
    - `replay_data` (ReplayScheme): Данные для создания связанного объекта ответа.
    - `task_data` (TaskScheme): Данные для создания задачи.
    - `user` (User): Текущий авторизованный пользователь (определяется через Depends).
    - `session` (AsyncSession): Асинхронная сессия для работы с базой данных (передаётся через Depends).

    Пример использования:
        POST /

    Тело запроса (JSON):
    ```json
    {
        "replay_data": { ... },
        "task_data": { ... }
    }
    ```

    Возвращает:
    - Объект `ReturnTask`, представляющий созданную задачу.

    Обработка ошибок:
    - Если данные не прошли валидацию, возвращается ошибка 422.
    - Если пользователь не авторизован, будет возвращена ошибка аутентификации (401).
    """

    replay = await create(model=Replay, data=replay_data, session=session)
    task_data = TaskCreateScheme(
        **task_data.model_dump(), replay_id=replay.id, user_id=user.id
    )
    task = await create(model=Task, data=task_data, session=session)
    return task


@router.delete("/{id:int}", status_code=204)
async def delete_task_view(
    id: int,
    user: User = Depends(auth.login),
    session: AsyncSession = Depends(db_helper.session),
) -> None:
    """
    Удаление задачи пользователя.

    Этот эндпоинт позволяет удалить задачу по её идентификатору, если она принадлежит
    текущему авторизованному пользователю. Дополнительно удаляется связанный ответ,
    если он существует.

    Параметры:
    - `id` (int): Уникальный идентификатор задачи, которую необходимо удалить.
    - `user` (User): Текущий авторизованный пользователь (определяется через Depends).
    - `session` (AsyncSession): Асинхронная сессия для работы с базой данных (передаётся через Depends).

    Пример использования:
        DELETE /{id}

    Возвращает:
    - Статус 204 (No Content) в случае успешного удаления задачи и связанного ответа.

    Обработка ошибок:
    - Если задача с указанным идентификатором не найдена или не принадлежит пользователю,
      возвращается ошибка 404 с соответствующим сообщением.
    - Если пользователь не авторизован, будет возвращена ошибка аутентификации (401).
    """
    task: Task = await get_by_id(session=session, model=Task, id=id)
    reply: Reply = await get_by_id(session=session, model=Replay, id=task.replay_id)
    if not task is None and not reply is None and task.user_id == user.id:
        task_deleted: bool = await delete(session=session, model=Task, id=id)
        replay_deleted: bool = await delete(
            session=session, model=Replay, id=task.replay_id
        )
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=settings.errors.not_fount_by_id.format(model="task", id=id),
    )


@router.get("/complete/{id}", status_code=204)
async def task_complete_view(
    id: int,
    user: User = Depends(auth.login),
    session: AsyncSession = Depends(db_helper.session),
) -> None:
    """
    Пометка задачи как выполненной.

    Этот эндпоинт позволяет отметить задачу как выполненную по её идентификатору,
    если она принадлежит текущему авторизованному пользователю.

    Параметры:
    - `id` (int): Уникальный идентификатор задачи, которую необходимо пометить как выполненную.
    - `user` (User): Текущий авторизованный пользователь (определяется через Depends).
    - `session` (AsyncSession): Асинхронная сессия для работы с базой данных (передаётся через Depends).

    Пример использования:
        GET /complete/1

    Возвращает:
    - Статус 204 (No Content) в случае успешного выполнения операции.

    Обработка ошибок:
    - Если задача с указанным идентификатором не найдена или не принадлежит пользователю,
      возвращается ошибка 404 с соответствующим сообщением.
    - Если пользователь не авторизован, будет возвращена ошибка аутентификации (401).
    """

    task: Task = await get_by_id(session=session, model=Task, id=id)

    if not task is None and task.user_id == user.id:
        if task.replay.replay_mode == "":
            task.is_complete = True
        else:
            task.replay.counter += 1
        await session.commit()
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=settings.errors.not_fount_by_id.format(model="task", id=id),
    )


@router.get("/all", status_code=200)
async def get_my_all_tasks_view(
    user: User = Depends(auth.login), session: AsyncSession = Depends(db_helper.session)
) -> List[ReturnTask]:
    """
    Получение списка всех задач пользователя.

    Этот эндпоинт позволяет получить все задачи, которые когда-либо были созданы
    пользователем, независимо от их статуса выполнения.

    Параметры:
    - `user` (User): Текущий авторизованный пользователь (определяется через Depends).
    - `session` (AsyncSession): Асинхронная сессия для работы с базой данных (передаётся через Depends).

    Пример использования:
        GET /all

    Возвращает:
    - Список объектов `ReturnTask`, представляющих все задачи пользователя.

    Обработка ошибок:
    - В случае отсутствия задач возвращается пустой список.
    - Если пользователь не авторизован, будет возвращена ошибка аутентификации (401).
    """

    stmt = select(Task).where(Task.user_id == user.id)
    tasks: Result = await session.execute(stmt)
    return tasks.scalars().all()


@router.get("/completed", status_code=200)
async def get_my_completed_tasks_view(
    user: User = Depends(auth.login), session: AsyncSession = Depends(db_helper.session)
) -> List[ReturnTask]:
    """
    Получение списка выполненных задач пользователя.

    Этот эндпоинт позволяет получить все задачи, которые были помечены как выполненные
    для текущего авторизованного пользователя.

    Параметры:
    - `user` (User): Текущий авторизованный пользователь (определяется через Depends).
    - `session` (AsyncSession): Асинхронная сессия для работы с базой данных (передаётся через Depends).

    Пример использования:
        GET /completed

    Возвращает:
    - Список объектов `ReturnTask`, представляющих выполненные задачи пользователя.

    Обработка ошибок:
    - В случае отсутствия выполненных задач возвращается пустой список.
    - Если пользователь не авторизован, будет возвращена ошибка аутентификации (401).
    """

    stmt = select(Task).where(Task.user_id == user.id, Task.is_complete == True)
    tasks: Result = await session.execute(stmt)
    return tasks.scalars().all()


@router.get("/not/completed", status_code=200)
async def get_my_not_completed_tasks_view(
    user: User = Depends(auth.login), session: AsyncSession = Depends(db_helper.session)
) -> List[ReturnTask]:
    """
    Получение списка невыполненных задач пользователя.

    Этот метод позволяет получить все задачи, которые принадлежат текущему пользователю и ещё не были выполнены.

    Параметры:
    - `user` (User): Объект пользователя, передаваемый через Depends(auth.login).
    - `session` (AsyncSession): Асинхронная сессия для работы с базой данных (передаётся через Depends).

    Пример использования:
        GET /not/completed

    Возвращает:
    - Список объектов `ReturnTask`, содержащих информацию о невыполненных задачах пользователя.
    - Код состояния 200 при успешном выполнении запроса.
    """

    stmt = select(Task).where(Task.user_id == user.id, Task.is_complete == False)
    tasks: Result = await session.execute(stmt)
    return tasks.scalars().all()


@router.get("/is/complete/{id:int}")
async def is_complete_view(
    id: int,
    date=datetime.now().date(),
    user: User = Depends(auth.login),
    session: AsyncSession = Depends(db_helper.session),
) -> bool:
    """
    Проверка необходимости выполнения задачи на выбранную дату.

    Этот метод определяет, должна ли быть выполнена задача с указанным идентификатором на текущую дату.

    Параметры:
    - `id` (int): Идентификатор задачи.
    - `date` (date, optional): Дата для проверки (по умолчанию — текущая).
    - `user` (User): Объект пользователя, передаваемый через Depends(auth.login).
    - `session` (AsyncSession): Асинхронная сессия для работы с базой данных (передаётся через Depends).

    Пример использования:
        GET /is/complete/1

    Возвращает:
    - `bool`: `True`, если задачу нужно выполнить на указанную дату, иначе `False`.
    - Код состояния 200 при успешном выполнении запроса.
    """

    task: Task = await session.get(Task, id)
    replay: Replay = task.replay

    return is_complete(replay=replay, date_day=date)


@router.get("/get/{days_count:int}/calendar")
async def get_n_days_grafic_view(
    days_count: int,
    session: AsyncSession = Depends(db_helper.session),
    user: User = Depends(auth.login),
):
    return await get_n_days_grafic(days_count=days_count, session=session, user=user)


@router.get("/users/notifications/")
async def user_notification_view(session: AsyncSession = Depends(db_helper.session)):
    return await user_notification(session=session)