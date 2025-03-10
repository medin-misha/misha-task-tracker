from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from typing import List, Dict, Any, Tuple
import copy
from settings import config
from utils import tasks


async def get_day_tasks(msg: Message) -> Tuple[str, List[int]]:

    msg_text: str = copy.copy(config.msg.tasks_list_header)
    task_template: str = copy.copy(config.msg.tasks_list_element)

    tasks_data: List[dict] = await tasks(
        user_name=msg.from_user.username, user_id=msg.chat.id, how_many_days=1
    )
    days_tasks: dict = tasks_data[0]
    ids: List[int] = []
    for task in days_tasks.get("tasks"):
        msg_text += task_template.format(
            name=task.get("name"),
            description=task.get("description"),
            id=task.get("id"),
        )
        ids.append(task.get('id'))
    date = days_tasks.get("date")

    return f"{msg_text.format(date=date)}", ids


async def get_n_days_tasks(msg: Message, state: FSMContext, days: str) -> List[str]:
    msg_text: str = copy.copy(config.msg.tasks_list_header)
    task_template: str = copy.copy(config.msg.tasks_list_element)

    tasks_data: List[dict] = await tasks(
        user_name=msg.from_user.username, user_id=msg.chat.id, how_many_days=days
    )
    messages_texts: List[str] = []
    for days_tasks in tasks_data:
        for task in days_tasks.get("tasks"):
            msg_text += task_template.format(
                name=task.get("name"),
                description=task.get("description"),
                id=task.get("id"),
            )
        date = days_tasks.get("date")
        messages_texts.append(msg_text.format(date=date))
    await state.clear()
    return messages_texts
