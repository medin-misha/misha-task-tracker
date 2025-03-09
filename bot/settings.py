from pydantic_settings import BaseSettings
import os


class ConfigMessages(BaseSettings):
    start_stiker: str = (
        "CAACAgIAAxkBAAMyZ72WppzmKXPGej9m9eYr0odwoOwAApMyAAIla8hKHRe9qJyjfek2BA"
    )
    help_stiker: str = (
        "CAACAgIAAxkBAAOdZ72xRoTCb57QIgusC3SYvM_QPTQAAiY4AAKDaclKThTMm9A1G0g2BA"
    )
    what_stiker: str = (
        "CAACAgIAAxkBAAIBDGfBlsJZr8FvdKlGbZ5XbOrKiM3wAAIDMgACAlLISkI46NLrk3R-NgQ"
    )
    star_eye_stiker: str = (
        "CAACAgIAAxkBAAMyZ72WppzmKXPGej9m9eYr0odwoOwAApMyAAIla8hKHRe9qJyjfek2BA"
    )
    tasks_list_header: str = "Вот твои задачи на {date}:\n\n"
    tasks_list_element: str = (
        "Имя задачи: <b>{name}</b>\nОписание задачи: <i>{description}</i>\nId задачи: {id}\n--------------------\n"
    )

class InlineButtonCallbacks(BaseSettings):
    task_complete: str = "complete"

class ConfigMain(BaseSettings):
    token: str = os.getenv("token")
    api_address: str = os.getenv("api_address")
    msg: ConfigMessages = ConfigMessages()
    inline_callbacks: InlineButtonCallbacks = InlineButtonCallbacks()

config: ConfigMain = ConfigMain()
