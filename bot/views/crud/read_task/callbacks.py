from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils import complete_task
from settings import config


router = Router(name="read_tasks_callbacks")


@router.callback_query(F.data.regexp(f"^{config.inline_callbacks.task_complete}(\d+)$"))
async def complete_task_callback(query: CallbackQuery):
    if query.data is not None:
        id: int = query.data.split()[1]
        completed: bool = await complete_task(
            id=id, user_name=query.from_user.username, user_id=query.from_user.id
        )
        if completed:
            await query.answer(text=f"задание {id} выполнено")
        else:
            await query.answer(text="error")
    else:
        await query.answer(text="error")
