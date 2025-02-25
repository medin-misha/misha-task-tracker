from aiogram import Router, F
from aiogram.types import Message, URLInputFile
from aiogram.filters import Command, CommandStart
from aiogram.enums.chat_action import ChatAction
from aiogram.enums import ParseMode
from settings import config
from utils import registration, login
from keyboard import menu_reply_keyboards

router = Router()


@router.message(CommandStart())
async def start_view(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    log_code: int = await login(user_name=msg.from_user.username, user_id=msg.chat.id)
    if log_code == 401:
        reg_code: int = await registration(
            user_name=msg.from_user.username, user_id=msg.from_user.id
        )

    await msg.bot.send_sticker(chat_id=msg.chat.id, sticker=config.msg.start_stiker)
    await msg.reply(
        text=f"{msg.from_user.first_name}, ты наконец то решил встать с дивана и начать действовать.",
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
        
        + f"<i>{msg.from_user.username}</i>, пока всё.", # last str
        parse_mode=ParseMode.HTML
    )


@router.message()
async def get_stiker(msg: Message):
    print(msg.sticker.file_id)
    await msg.bot.copy_message(
        chat_id=msg.chat.id, from_chat_id=msg.chat.id, message_id=msg.message_id
    )
