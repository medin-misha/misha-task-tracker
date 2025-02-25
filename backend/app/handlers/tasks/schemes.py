from pydantic import BaseModel, PositiveInt
from datetime import datetime
from datetime import date as Date, time as Time


class TaskScheme(BaseModel):
    name: str = ""
    description: str = ""
    is_complete: bool = False


class TaskCreateScheme(TaskScheme):
    replay_id: PositiveInt = 10**10
    user_id: PositiveInt


class ReplayScheme(BaseModel):
    counter: int | None = 0
    date: Date = datetime.now().date()
    time: Time = datetime.now().time()
    replay_mode: str = ""


class ReturnReplay(BaseModel):
    id: PositiveInt
    time: Time
    counter: int
    replay_mode: str
    date: Date


class ReturnTask(BaseModel):
    id: PositiveInt
    is_complete: bool = False
    name: str
    description: str
    user_id: PositiveInt
    replay_id: PositiveInt
    replay: ReturnReplay
