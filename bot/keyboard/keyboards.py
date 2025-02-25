from aiogram import types


class ButtonsText:
    my_today_tasks: str = "мои задачи на сегодня"
    create_new_task: str = "создать новую задачу"


def menu_reply_keyboards() -> types.ReplyKeyboardMarkup:
    buttons_line: list[types.KeyboardButton] = [
        types.KeyboardButton(text=btn_text)
        for btn_text in [ButtonsText.create_new_task, ButtonsText.my_today_tasks]
    ]
    keyboard: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(keyboard=[buttons_line])
    return keyboard
