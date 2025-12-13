from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy import String, Boolean, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.shared.database import Base
from src.tasks.models import Task

class UserRole(str, PyEnum):
    ADMIN = "Admin"
    MEMBER = "Member"
    MANAGER = "Manager"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Profile Data
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default=UserRole.MEMBER)
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
