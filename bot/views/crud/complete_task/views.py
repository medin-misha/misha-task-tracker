from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message

from typing import List
from .states import CompleteTask
from keyboard import state_clear_reply_keyboard
from .utils import set_complete

router = Router(name="complete_task")


@router.message(Command("complete"))
async def complete_task_view(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    msg_split: List[str] = msg.text.split()
    if len(msg_split) > 1 and msg_split[1].isdigit():
        await set_complete(msg=msg, state=state, id=msg_split[1])
    else:
        await msg.answer(text="Для выполнения задачи мне нужен <b>её ID</b>")
        await state.set_state(CompleteTask.get_id)


@router.message(CompleteTask.get_id, F.text)
async def get_task_id_view(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await set_complete(msg=msg, state=state, id=msg.text)


# errors views
@router.message(CompleteTask.get_id)
async def error_get_id_view(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await msg.reply(
        text="Слушай, когда ты мне отправляешь <i>подобную штуку</i> у меня в место текста высвечиваеться <code>None</code>. Я не вдупляю стикеры, смайлы, картинки и так далее. <b>Скинь текстом.</b>",
        reply_markup=state_clear_reply_keyboard(),
    )
