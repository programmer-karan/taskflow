from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy import DateTime, String, ForeignKey, func, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.shared.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.auth.models import User

class TaskStatus(str, PyEnum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    REVIEW = "Review"
    DONE = "Done"

class TaskPriority(str, PyEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(
        String(255), nullable=True) 
    
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), nullable=True)
    
    attachment_url: Mapped[str|None] = mapped_column(String(500), nullable=True)


    owner_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    
    # Task → User (many-to-one)
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="tasks"
    )
