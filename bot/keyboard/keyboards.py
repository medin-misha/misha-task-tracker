from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from datetime import datetime
from typing import List, Dict
from settings import config


class ButtonsText:
    my_today_tasks: str = "/tasks"
    create_new_task: str = "/create"
    edit_task: Dict[str, str] = {
        "изменить имя": "name",
        "изменить описание": "description",
        "изменить дату": "date",
        "изменить режим повтора": "reply",
    }
    no_edit_task: str = "всё норм"
    reply_mode: Dict[str, str] = {
        "один раз": "",
        "каждый день": "e_d",
        "каждую неделю": "e_w",
        "каждый месяц": "e_m",
    }
    state_clear: str = "ОТМЕНИТЬ"


def menu_reply_keyboards() -> types.ReplyKeyboardMarkup:
    buttons_line: List[types.KeyboardButton] = [
        types.KeyboardButton(text=btn_text)
        for btn_text in [ButtonsText.create_new_task, ButtonsText.my_today_tasks]
    ]
    keyboard: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
        keyboard=[buttons_line]
    )
    return keyboard


def edit_task_data_reply_keyboards() -> types.ReplyKeyboardMarkup:
    edit_line: List[types.KeyboardButton] = [
        types.KeyboardButton(text=text) for text in ButtonsText.edit_task.keys()
    ]
    no_edit_line: List[types.KeyboardButton] = [
        types.KeyboardButton(text=ButtonsText.no_edit_task)
    ]
    keyboard: List[List[types.KeyboardButton]] = [
        no_edit_line,
        edit_line[0:2],
        edit_line[2:4],
    ]
    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def send_data_reply_keyboards() -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=f"{datetime.now().strftime('%Y-%m-%d')}")
    return builder.as_markup(resize_keyboard=True)


def send_reply_mode_reply_keyboards() -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for text in ButtonsText.reply_mode.keys():
        builder.button(text=text)

    return builder.as_markup(resize_keyboard=True)


def state_clear_reply_keyboard() -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=ButtonsText.state_clear)
    return builder.as_markup(resize_keyboard=True)


def task_complete_inline_keyboard(ids: List[int]) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for id in ids:
        builder.button(
            text=f"{id} - выполнил",
            callback_data=config.inline_callbacks.task_complete + str(id),
        )
    return builder.as_markup()
