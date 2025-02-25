from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from .base import Base


class User(Base):
    user_name: Mapped[str] = mapped_column(unique=True)
    chat_id: Mapped[bytes] = mapped_column(unique=True)
    tasks: Mapped[List["Task"]] = relationship(back_populates="user", uselist=True)
