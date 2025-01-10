from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base

class Task(Base):
    name: Mapped[str]
    description: Mapped[str]
    is_complete: Mapped[bool]
    
    
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")