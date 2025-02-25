from pydantic import BaseModel, PositiveInt


class RegistrationUser(BaseModel):
    user_name: str
    chat_id: str


class UserReturn(BaseModel):
    id: PositiveInt
    user_name: str
