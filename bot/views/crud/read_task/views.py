from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from typing import List
from keyboard import state_clear_reply_keyboard
from .states import GetNDaystasks
from .utils import get_day_tasks, get_n_days_tasks

router = Router(name="read_task")


@router.message(Command("tasks"))
async def days_tasks_view(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    text: str = await get_day_tasks(msg=msg)
    await msg.reply(text=text)


@router.message(Command("tasksGet"))
async def get_n_days_tasks_view(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    msg_split: List[str] = msg.text.split()
    if len(msg.text) > 1 and msg_split[1]:
        messages_texts: List[str] = await get_n_days_tasks(
            msg=msg, state=state, days=msg_split[1]
        )
        for text in messages_texts:
            await msg.reply(text=text)
    else:
        await msg.reply(
            text="Скинь мне то, на какое кол-во дней вперёд тебе показать задачи"
        )
        await state.set_state(GetNDaystasks.get_days)


@router.message(GetNDaystasks.get_days)
async def get_days_views(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    messages_texts: List[str] = await get_n_days_tasks(
        msg=msg, state=state, days=msg.text
    )
    for text in messages_texts:
        await msg.reply(text=text)


# erros views
@router.message(GetNDaystasks.get_days)
async def error_get_id_view(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await msg.reply(
        text="Слушай, когда ты мне отправляешь <i>подобную штуку</i> у меня в место текста высвечиваеться <code>None</code>. Я не вдупляю стикеры, смайлы, картинки и так далее. <b>Скинь текстом.</b>",
        reply_markup=state_clear_reply_keyboard(),
    )
