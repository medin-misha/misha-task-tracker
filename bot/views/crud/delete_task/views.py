from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ChatAction
from .states import DeleteTask
from utils import delete_task
from keyboard import state_clear_reply_keyboard

router = Router(name="delete_task")


@router.message(Command("delete"))
async def delete_task_view(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await msg.answer(text="Для удаления задачи мне нужен <b>её ID</b>")
    await state.set_state(DeleteTask.get_id)


@router.message(DeleteTask.get_id, F.text)
async def get_id_and_delete_task_view(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    deleted: bool = await delete_task(
        id=msg.text, user_name=msg.from_user.username, user_id=msg.chat.id
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


# erros views
@router.message(DeleteTask.get_id)
async def error_get_id_view(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await msg.reply(
        text="Слушай, когда ты мне отправляешь <i>подобную штуку</i> у меня в место текста высвечиваеться <code>None</code>. Я не вдупляю стикеры, смайлы, картинки и так далее. <b>Скинь текстом.</b>",
        reply_markup=state_clear_reply_keyboard(),
    )
