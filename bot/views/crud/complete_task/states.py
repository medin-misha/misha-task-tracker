from aiogram.fsm.state import StatesGroup, State


class CompleteTask(StatesGroup):
    get_id = State()
