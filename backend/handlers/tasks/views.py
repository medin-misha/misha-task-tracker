from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core import auth, db_helper, settings
from core.crud import create, delete
from core.models import Replay, Task, User
from .schemes import ReplayScheme, TaskScheme


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", status_code=201)
async def create_task_view(
    replay_data: ReplayScheme,
    task_data: TaskScheme,
    user: User = Depends(auth.login),
    session: AsyncSession = Depends(db_helper.session),
):
    replay = await create(model=Replay, data=replay_data, session=session)
    task_data.replay_id = replay.id
    task = await create(model=Task, data=task_data, session=session)
    return task


@router.delete("/{id:int}", status_code=204)
async def delete_task_view(
    id: int,
    user: User = Depends(auth.login),
    session: AsyncSession = Depends(db_helper.session),
):
    task: Task = get_by_id(session=session, model=Task, id=id)

    task_deleted: bool = delete(session=session, model=Task, id=id)
    replay_deleted: bool = delete(session=session, model=Task, id=task.replay_id)
    if task_deleted and replay_deleted:
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=settings.errors.not_fount_by_id.format(model=Task, id=id),
    )
