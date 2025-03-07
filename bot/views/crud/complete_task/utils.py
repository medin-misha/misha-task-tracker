from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils import complete_task
from keyboard import state_clear_reply_keyboard


async def set_complete(msg: Message, state: FSMContext, id: str) -> None:
    completed: bool = await complete_task(
        id=id, user_name=msg.from_user.username, user_id=msg.chat.id
    )
    if completed:
        await msg.answer(text="Задача помечена как выполненная.")
        await state.clear()
    else:
        await msg.answer(
            text="<b>Id</b> не корректен или такой задачи нет.",
            reply_markup=state_clear_reply_keyboard(),
        )
        await state.clear()
