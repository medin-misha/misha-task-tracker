from datetime import date
from .utils import is_execution_time


def check_schedule(date_day: date, code: str) -> bool:
    code_components: list[str] = code.split("_&_")
    need_todo: list[bool] = []
    for component in code_components:
        need_todo.append(is_execution_time(date_day=date_day, component=component))
    return True if True in need_todo else False


if __name__ == "__main__":
    now_date = date(year=2024, month=1, day=1)
    component = "e_w_mo_&_e_w_tu"
    print(check_schedule(date_day=now_date, code=component))
