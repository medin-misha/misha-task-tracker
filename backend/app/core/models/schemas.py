from pydantic import BaseModel
from typing import Optional


class BaseUser(BaseModel):
    user_name: str
    chat_id: str


class BaseTask(BaseModel):
    is_complete: bool
    replay_id: Optional[int] = None
    user_id: int
    description: Optional[str] = None
    name: str


class BaseReplay(BaseModel):
    how_many: int
    date: str
    time: str
    counter: int
    replay_mode: Optional[str] = ""
