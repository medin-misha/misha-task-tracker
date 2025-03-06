from aiogram.fsm.state import State, StatesGroup

class DeleteTask(StatesGroup):
    get_id = State()