from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from utils import delete_task
from keyboard import state_clear_reply_keyboard


async def delete_task_func(msg: Message, state: FSMContext, id: str):
    deleted: bool = await delete_task(
        id=id, user_name=msg.from_user.username, user_id=msg.chat.id
    )
    if deleted:
        await msg.answer(text="Всё, удалил.")
        await state.clear()
    else:
        await msg.answer(
            text="<b>Id</b> не корректен или такой задачи нет.",
            reply_markup=state_clear_reply_keyboard(),
        )
        await state.clear()
