import pytest
import random
from datetime import datetime, timedelta
from datetime import date

from main import check_schedule
from utils import get_weekdays_dates


def test_every_day():
    dates: list[date] = [
        date(
            year=random.randint(1, 3000),
            month=random.randint(1, 12),
            day=random.randint(1, 28),
        )
        for _ in range(30)
    ]

    template_element = "e_d"
    for date_ in dates:
        assert check_schedule(date_day=date_, code=template_element) is True


def test_every_week_day():
    successfull_date: list[date] = [
        date_ for date_ in get_weekdays_dates(day_num=0, dates_count=30)
    ]
    failure_date: list[date] = [
        date_
        for date_ in get_weekdays_dates(day_num=random.randint(1, 6), dates_count=30)
    ]

    template_element: str = "e_w_mo"
    for date_ in successfull_date:
        assert check_schedule(date_day=date_, code=template_element)
    for date_ in failure_date:
        assert not check_schedule(date_day=date_, code=template_element)


def test_and_week_day():
    successfull_date: list[date] = [
        date_
        for date_ in get_weekdays_dates(day_num=random.randint(0, 1), dates_count=60)
    ]
    template_element: str = "e_w_mo_&_e_w_tu"
    for date_ in successfull_date:
        assert check_schedule(date_day=date_, code=template_element)


def test_month_week_day():
    template_element: str = "e_m_jan_w_mo"
    dates: list[date] = [
        date(
            year=2025,
            month=1,
            day=day,
        )
        for day in range(1, 31)
    ]
    trues_list: list[bool] = [
        True for date_ in dates if check_schedule(date_day=date_, code=template_element)
    ]
    assert len(trues_list) == 4