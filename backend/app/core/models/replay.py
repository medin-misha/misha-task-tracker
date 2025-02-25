from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date, Time, func
from datetime import datetime, date, time
from .base import Base


class Replay(Base):
    counter: Mapped[int] = mapped_column(default=0, server_default="0")
    date: Mapped[str] = mapped_column(Date, nullable=True)
    time: Mapped[str] = mapped_column(
        Time, default=datetime.now().time, server_default=func.current_time()
    )
    replay_mode: Mapped[str] = mapped_column(nullable=True)
    task: Mapped["Task"] = relationship(back_populates="replay")
