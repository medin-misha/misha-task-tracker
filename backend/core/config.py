from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DBSettings(BaseModel):
    url: str = (
        "postgresql+asyncpg://postgres_user:postgres_password@localhost/postgres_db"
    )


class ErrorsMassages(BaseModel):
    defunct_model: str = (
        "Эта модель не существует. Попробуйте одну из этих: user, task, replay"
    )
    not_fount_by_id: str = "{model} не был найден по id = {id}"
    auth_error: str = "плохое имя или chat_id"
    registration_error: str = "У вас не может быть такого chat_id."

class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    errors: ErrorsMassages = ErrorsMassages()


settings: Settings = Settings()
