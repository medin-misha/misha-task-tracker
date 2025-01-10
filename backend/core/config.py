from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DBSettings(BaseModel):
    url: str = (
        "postgresql+asyncpg://postgres_user:postgres_password@localhost/postgres_db"
    )


class Settings(BaseSettings):
    db: DBSettings = DBSettings()


settings: Settings = Settings()
