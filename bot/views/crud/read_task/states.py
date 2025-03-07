from aiogram.fsm.state import State, StatesGroup


class GetNDaystasks(StatesGroup):
    get_days = State()
