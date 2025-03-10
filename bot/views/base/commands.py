from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.enums.chat_action import ChatAction
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from settings import config
from utils import registration, login
from keyboard import menu_reply_keyboards, ButtonsText

router = Router()


@router.message(CommandStart())
async def start_view(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    log_code: int = await login(user_name=msg.from_user.username, user_id=msg.chat.id)
    if log_code == 401:
        await registration(user_name=msg.from_user.username, user_id=msg.from_user.id)

    await msg.bot.send_sticker(chat_id=msg.chat.id, sticker=config.msg.start_stiker)
    await msg.reply(
        text=f"{msg.from_user.first_name}, ты наконец то решил встать с дивана и начать действовать.\n\n"
        "минимальный пользовательский арсенал:\n- /create создать задачу\n- /tasks - список задач на сегодня\n- /delete - удалить задачу по id",
        parse_mode=ParseMode.HTML,
        reply_markup=menu_reply_keyboards(),
    )


@router.message(Command("help"))
async def help_view(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await msg.bot.send_sticker(chat_id=msg.chat.id, sticker=config.msg.help_stiker)
    await msg.answer(
        text="<code>/start</code> - начальная команда, она же используеться для аутентификации\n"
        + f"<code>/help</code> - команда на которую тыкнул <i>{msg.from_user.username}</i>, она отвечает за вывод всех понятных боту команд\n"
        + "<code>/helpReply</code> - команда которая расскажет тебе как более точно настраивать повтор сообщения"
        + "<code>/create</code> - создать задачу"
        + "<code>/delete</code> - удалить задачу по id"
        + "<code>/tasks</code> - список задач на день"
        + "<code>/complete</code> - пометить задачу как выполненную"
        + "<code>/tasksGet</code> - посмотреть задачи на n дней вперёд"
        + f"<i>{msg.from_user.username}</i>, пока всё.",  # last str
        parse_mode=ParseMode.HTML,
    )


@router.message(Command("helpReply"))
async def reply_help_view(msg: Message):
    await msg.reply(
        text="""
режимы недели, w
Частица w_ говорит системе что речь идёт о дне недели

w_mo → Понедельник
w_tu → Вторник
w_we → Среда
w_th → Четверг
w_fr → Пятница
w_sa → Суббота
w_su → Воскресенье Все комбинации с днём недели.
режимы месяца, m
Частица w_ говорит системе что речь идёт о дне недели

m_jan → Январь
m_feb → Февраль
m_mar → Март
m_apr → Апрель
m_may → Май
m_jun → Июнь
m_jul → Июль
m_aug → Август
m_sep → Сентябрь
m_oct → Октябрь
m_nev → Ноябрь
m_dec → Декабрь Все комбинации с днём неделиm
режимы года месяца дня y_ m_ d_
Частица y_ говорит системе о том что речь идёт про год Частица m_ говорит системе о том что речь идёт про месяц Частица d_ говорит системе о том что речь идёт про день

режимы цикла e_
Частица e_ говорит системе о том что следуйщее выражение нужно зациклить e_v - every day e_m - every month e_y - every year

&_
& говорит системе что нужно принять второе условие. Допустим e_w_su_&_e_w_mo повторять каждый день недели который равен sunday или повторять каждый день недели который равен monday."""
    )


@router.message(F.text == ButtonsText.state_clear)
async def clear_state_view(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await state.clear()
    await msg.answer(text="так, всё отменил")


@router.message(Command("myId"))
async def get_user_id_view(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await msg.answer(text=f"<code>{msg.chat.id}</code>")
