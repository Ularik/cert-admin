from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, DateTime, func, ForeignKey
from src.database import Base
from datetime import datetime
from enum import Enum


class UserStatus(Enum):
    ADMIN = "ADMIN"
    HEAD = "HEAD"
    USER = "USER"


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    last_name: Mapped[str | None] = mapped_column(String(50))
    hashed_password: Mapped[bytes]
    tasks: Mapped[list["Tasks"]] = relationship(secondary="users_tasks", back_populates="executors")
    status: Mapped[UserStatus] = mapped_column(default=UserStatus.USER, server_default=UserStatus.USER.value)
    department: Mapped[int | None] = mapped_column(ForeignKey("departments.id", ondelete="SET NULL"), comment="Отдел")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.timezone('Asia/Bishkek', func.now()))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone('Asia/Bishkek', func.now()),
        onupdate=func.timezone('Asia/Bishkek', func.now())
    )


class UsersTasks(Base):
    __tablename__ = "users_tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    tasks_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.timezone('Asia/Bishkek', func.now()))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone('Asia/Bishkek', func.now()),
        onupdate=func.timezone('Asia/Bishkek', func.now())
    )