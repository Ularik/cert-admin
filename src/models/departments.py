from typing import Optional

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, DateTime, func, ForeignKey, CheckConstraint
from datetime import datetime
from src.database import Base


class Departments(Base):
    __tablename__ = "departments"
    __table_args__ = (
        CheckConstraint(
            "head_id IS NULL OR deputy_head_id IS NULL OR head_id <> deputy_head_id",
            name="check_head_and_deputy_different"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None]
    # Внешние ключи на пользователей
    head_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
            use_alter=True,
            name="fk_departments_head_id_users"
        ),
        unique=True,
        nullable=True,
        comment="Начальник отдела"
    )
    deputy_head_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
            use_alter=True,
            name="fk_departments_deputy_head_id_users"
        ),
        unique=True,
        nullable=True,
        comment="Заместитель начальника отдела"
    )

    # Relationship для обратного обращения
    head: Mapped[Optional["Users"]] = relationship(
        foreign_keys=[head_id],
        back_populates="managed_department"
    )
    deputy_head: Mapped[Optional["Users"]] = relationship(
        foreign_keys=[deputy_head_id],
        back_populates="deputy_managed_department"
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.timezone('Asia/Bishkek', func.now()))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone('Asia/Bishkek', func.now()),
        onupdate=func.timezone('Asia/Bishkek', func.now())
    )