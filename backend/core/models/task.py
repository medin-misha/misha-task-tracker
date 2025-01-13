from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base


class Task(Base):
    name: Mapped[str]
    description: Mapped[str]
    is_complete: Mapped[bool]

    replay_id: Mapped[int] = mapped_column(
        ForeignKey("replay.id"), unique=True, nullable=True
    )
    replay: Mapped["Replay"] = relationship(back_populates="task", lazy="selectin")

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")
