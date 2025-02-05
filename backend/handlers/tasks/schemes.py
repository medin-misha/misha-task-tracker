from pydantic import BaseModel, PositiveInt
from datetime import datetime
from datetime import date as Date, time as Time


class TaskScheme(BaseModel):
    name: str = ""
    description: str = ""
    is_complete: bool = False
    user_id: PositiveInt
    replay_id: PositiveInt = 10**10

class ReplayScheme(BaseModel):
    counter: int | None = 0
    date: Date = datetime.now().date()
    time: Time = datetime.now().time()
    replay_mode: str = ""

