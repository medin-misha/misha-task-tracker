from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Date, Time, func
from datetime import datetime, date, time
from .base import Base

class Replay(Base):
    counter: Mapped[int]
    how_many: Mapped[int] = mapped_column(nullable=True)
    date: Mapped[str] = mapped_column(Date, nullable=True)
    time: Mapped[str] = mapped_column(Time, default=datetime.now().time, server_default=func.current_time())
    replay_mode: Mapped[str] = mapped_column(nullable=True)