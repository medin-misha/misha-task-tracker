from datetime import datetime
from core.models import Replay
from core.time_templating import check_schedule


def is_complete(replay: Replay, date_day: datetime.date) -> bool:
    print(replay.date, date_day)
    if replay.date == date_day:
        return True
    if not replay.replay_mode is "":
        return check_schedule(date_day=date_day, code=replay.replay_mode)
    return False