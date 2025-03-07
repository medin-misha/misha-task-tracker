from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from typing import List
from utils import tasks


router = Router(name="read_task")


@router.message(Command("tasks"))
async def days_tasks_view(msg: Message):
    msg_text: str = "Вот твои задачи на {date}:\n\n"
    task_template: str = (
        "Имя задачи: <b>{name}</b>\nОписание задачи: <i>{description}</i>\nId задачи: {id}\n--------------------\n"
    )
    tasks_data: List[dict] = await tasks(
        user_name=msg.from_user.username, user_id=msg.chat.id, how_many_days=1
    )
    days_tasks: dict = tasks_data[0]

    for task in days_tasks.get("tasks"):
        msg_text += task_template.format(
            name=task.get("name"),
            description=task.get("description"),
            id=task.get("id"),
        )
    date = days_tasks.get("date")
    await msg.reply(text=f"{msg_text.format(date=date)}")
