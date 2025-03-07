from aiogram import Router, F
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from datetime import datetime
from .states import CreateTask
from keyboard import (
    ButtonsText,
    edit_task_data_reply_keyboards,
    menu_reply_keyboards,
    send_data_reply_keyboards,
    send_reply_mode_reply_keyboards,
)
from settings import config
from utils import create_task, validate_date

router = Router(name="create_task")


@router.message(Command("create") or F.text == ButtonsText.create_new_task)
async def create_task_view(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await msg.answer(text="Имя создаваемой <b>задачи</b>: ")
    await state.set_state(CreateTask.name)


@router.message(CreateTask.name, F.text)
async def get_task_name_view(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await state.update_data(name=msg.text)
    await msg.answer(text="задачу нужно описать <b>описать</b>:")
    await state.set_state(CreateTask.description)


@router.message(CreateTask.description, F.text)
async def get_task_description_view(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await state.update_data(description=msg.text)
    await msg.answer(
        text=f"На какое число поставить твою задачу? (число должно быть в формате: {datetime.now().strftime("%Y-%m-%d")})",
        reply_markup=send_data_reply_keyboards(),
    )
    await state.set_state(CreateTask.date)


@router.message(CreateTask.date, F.text)
async def get_task_date_view(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    if validate_date(text=msg.text):
        await state.update_data(date=msg.text)
        await msg.answer(
            text="Нужно ли зациклить задачу или она чисто на один раз? (/helpReply - узнать больше)",
            reply_markup=send_reply_mode_reply_keyboards(),
        )
        await state.set_state(CreateTask.replay_mode)
    else:
        await msg.reply(
            text=f"<b>{msg.text}</b> - это не корректный формат времени. Чесно говоря я вооще хз чё ты мне скинул.\n\nбудь так добр скидывай дату в фомрате <b>{datetime.now().strftime("%Y-%m-%d")}</b>. Просто попробуй скинуть ещё раз.",
            reply_markup=send_data_reply_keyboards(),
        )
        await state.set_state(CreateTask.date)


@router.message(CreateTask.replay_mode, F.text)
async def get_edits_or_ok(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    replay_mode: str = (
        ""
        if ButtonsText.reply_mode.get(msg.text) is None
        else ButtonsText.reply_mode.get(msg.text)
    )
    await state.update_data(replay_mode=replay_mode)
    task_data: dict = await create_task(
        state=state, user_name=msg.from_user.username, user_id=msg.chat.id
    )
    print(task_data)
    await msg.bot.send_sticker(chat_id=msg.chat.id, sticker=config.msg.star_eye_stiker)
    await msg.answer(
        text="Создал. Удачи в работе.", reply_markup=menu_reply_keyboards()
    )
    await state.clear()


# value errors views
@router.message(
    CreateTask.name
    or CreateTask.description
    or CreateTask.replay_mode
    or CreateTask.date
    or CreateTask.edit
)
async def get_error_view(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await msg.bot.send_sticker(chat_id=msg.chat.id, sticker=config.msg.what_stiker)
    await msg.reply(
        text="Слушай, когда ты мне отправляешь <i>подобную штуку</i> у меня в место текста высвечиваеться <code>None</code>. Я не вдупляю стикеры, смайлы, картинки и так далее. <b>Скинь текстом.</b>",
        reply_markup=state_clear_reply_keyboard(),
    )
