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


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    errors: ErrorsMassages = ErrorsMassages()


settings: Settings = Settings()
