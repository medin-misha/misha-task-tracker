from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload, lazyload
from datetime import datetime, timedelta
from typing import List, Dict
from core.models import Replay, User, Task
from core.time_templating import check_schedule


def is_complete(replay: Replay, date_day: datetime.date) -> bool:
    if replay.date.strftime("%Y-%m-%d") == date_day:
        return True
    if not replay.replay_mode == "":
        return check_schedule(date_day=date_day, code=replay.replay_mode)
    return False


# эта функция очень зависит от is_complete!!!
async def get_n_days_grafic(
    days_count: int, session: AsyncSession, user: User
) -> List[dict]:
    days: list[datetime.date] = [
        datetime.now() + timedelta(days=i) for i in range(days_count)
    ]
    stmt = (
        select(Task)
        .where(Task.user_id == user.id, Task.is_complete == False)
        .options(selectinload(Task.replay))
    )

    tasks = await session.execute(stmt)
    tasks = tasks.scalars().all()
    n_day_calendar: list[dict] = []
    for day in days:
        day_tasks: Dict[str, datetime.date | list] = {
            "date": day.strftime("%Y-%m-%d"),
            "tasks": [],
        }
        for task in tasks:
            if is_complete(replay=task.replay, date_day=day.strftime("%Y-%m-%d")):
                day_tasks["tasks"].append(task)
        n_day_calendar.append(day_tasks)
    return n_day_calendar

async def user_notification(session: AsyncSession):
    all_users_stmt = select(User).options().where(User.tasks.any())
    all_users = await session.execute(all_users_stmt)
    users: list = all_users.scalars().all()
    # todo доделай уведомительную функцию
