from datetime import datetime, timedelta
from datetime import date
from typing import Callable
from .classes import ElementDecoder


def infinite_is_execution_time(
    date_day: datetime.date, elements: list[str], decoder: ElementDecoder
) -> list[bool]:
    decode_result: list[bool] = []

    for index, element in enumerate(elements):

        if len(element) > 1:
            continue
        method: Callable | None = getattr(decoder, element)

        element_slice = elements[index + 1 : index + 2]
        arg = element_slice[0] if len(element_slice) > 0 else None

        decode_result.append(method(arg=arg, date_day=date_day))

    return all(decode_result)


def is_execution_time(date_day: datetime.date, component: str) -> bool:
    elements: list[str] = component.split("_")
    decoder = ElementDecoder()
    if elements[0] == "e":
        return infinite_is_execution_time(
            date_day=date_day, elements=elements, decoder=decoder
        )
    else:
        pass


def get_weekdays_dates(day_num: int, dates_count: int) -> list[date]:
    """функция генератор которая получает
    day_num - это номер дня недели 0 - 6 и dates_cound - сколько нужно получить дат"""
    now = datetime.now()
    now_weekday = now.weekday()
    required_weekday = now - timedelta(days=now_weekday - day_num)
    for i in range(dates_count):
        required_week_day = required_weekday.date() + timedelta(days=7 * i)
        yield required_week_day
