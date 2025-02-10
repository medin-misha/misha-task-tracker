from datetime import datetime


class ElementDecoder:
    week_days: dict[str, int] = {
        "mo": 1,
        "tu": 2,
        "we": 3,
        "th": 4,
        "fr": 5,
        "sa": 6,
        "su": 7,
    }
    months: dict[str, int] = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }

    def e(self, *args, **kwargs) -> bool:
        return True

    def d(self, *args, **kwargs) -> bool:
        return True

    def w(self, arg: str, date_day: datetime.date) -> bool:
        valid_day: int | None = self.week_days.get(arg)
        if valid_day == date_day.weekday() + 1:
            return True
        return False

    def m(self, arg: str, date_day: datetime.date) -> bool:
        valid_month: int | None = self.months.get(arg)
        if valid_month == date_day.month:
            return True
        return False
