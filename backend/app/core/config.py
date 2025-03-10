from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseModel):
    url: str = f"postgresql+asyncpg://{os.getenv('postgres_user')}:{os.getenv('postgres_password')}@{os.getenv('postgres_host')}"


class SecuredSettings(BaseSettings):
    public_key: Path = BASE_DIR / "keys/public.pem"
    private_key: Path = BASE_DIR / "keys/private.pem"
    algrorithm: str = "RS256"


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
    secured: SecuredSettings = SecuredSettings()


settings: Settings = Settings()
