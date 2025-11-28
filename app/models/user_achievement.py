from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.achievement import Achievement
    from app.models.user import User


class UserAchievement(Base):
    """
    Связующая таблица между пользователями и достижениями. Хранит факт
    выдачи конкретного достижения конкретному пользователю и время выдачи.
    Одна и та же ачивка не может быть выдана одному пользователю дважды.

    Поля:
        id: Первичный ключ записи.
        user_id: Идентификатор пользователя.
        achievement_id: Идентификатор достижения.
        issued_at: Время выдачи достижения.
        user: Объект пользователя.
        achievement: Объект достижения.
    """

    __tablename__ = "user_achievements"
    __table_args__ = (UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    achievement_id: Mapped[int] = mapped_column(
        ForeignKey("achievements.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    issued_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates="achievements")
    achievement: Mapped[Achievement] = relationship(back_populates="user_achievements")
