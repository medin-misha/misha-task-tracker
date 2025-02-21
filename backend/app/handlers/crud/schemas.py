from pydantic import BaseModel, PositiveInt
from typing import Any
from core.models import schemas


class Returned(BaseModel):
    id: PositiveInt


class CreateUser(schemas.BaseUser):
    pass


class CreateTask(schemas.BaseTask):
    pass


class CreateReplay(schemas.BaseReplay):
    pass
