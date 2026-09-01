from typing import Optional

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, DateTime, func, ForeignKey
from src.database import Base
from datetime import datetime
from enum import Enum


class UserStatus(Enum):
    ADMIN = "ADMIN"
    HEAD = "HEAD"
    DEPUTY = "DEPUTY"
    USER = "USER"

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    last_name: Mapped[str | None] = mapped_column(String(50))
    hashed_password: Mapped[bytes]
    tasks: Mapped[list["Tasks"]] = relationship(secondary="users_tasks", back_populates="executors")
    status: Mapped[UserStatus] = mapped_column(default=UserStatus.USER, server_default=UserStatus.USER.value)
    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id", ondelete="SET NULL"),
        comment="Отдел"
    )
    department: Mapped["Departments"] = relationship(back_populates="users")
    replies: Mapped[list["TaskReply"]] = relationship(back_populates="author")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.timezone('Asia/Bishkek', func.now()))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone('Asia/Bishkek', func.now()),
        onupdate=func.timezone('Asia/Bishkek', func.now())
    )
