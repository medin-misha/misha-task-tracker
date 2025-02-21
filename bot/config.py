from pydantic_settings import BaseSettings
import os


class ConfigMain(BaseSettings):
    token: str = os.getenv("token")
    api_address: str = os.getenv("api_address")


config: ConfigMain = ConfigMain()
