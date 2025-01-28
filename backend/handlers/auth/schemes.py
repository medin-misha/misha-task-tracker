from pydantic import BaseModel


class RegistrationUser(BaseModel):
    user_name: str
    chat_id: str
