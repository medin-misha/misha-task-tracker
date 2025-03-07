from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message

from .states import CompleteTask
from keyboard import state_clear_reply_keyboard
from utils import complete_task

router = Router(name="complete_task")


@router.message(Command("complete"))
async def complete_task_view(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await msg.answer(text="Для выполнения задачи мне нужен <b>её ID</b>")
    await state.set_state(CompleteTask.get_id)


@router.message(CompleteTask.get_id, F.text)
async def get_task_id_view(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    completed: bool = await complete_task(
        id=msg.text, user_name=msg.from_user.username, user_id=msg.chat.id
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


# errors views
@router.message(CompleteTask.get_id)
async def error_get_id_view(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await msg.reply(
        text="Слушай, когда ты мне отправляешь <i>подобную штуку</i> у меня в место текста высвечиваеться <code>None</code>. Я не вдупляю стикеры, смайлы, картинки и так далее. <b>Скинь текстом.</b>",
        reply_markup=state_clear_reply_keyboard(),
    )
