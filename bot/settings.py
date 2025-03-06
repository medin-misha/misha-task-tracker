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


class ConfigMain(BaseSettings):
    token: str = os.getenv("token")
    api_address: str = os.getenv("api_address")
    msg: ConfigMessages = ConfigMessages()


config: ConfigMain = ConfigMain()
