from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class UserDailyStat(Base):
    """
    Агрегированная статистика по количеству очков, набранных пользователем
    за конкретный календарный день. Используется для аналитики.

    Поля:
        id: Первичный ключ записи.
        user_id: Идентификатор пользователя.
        day: Календарная дата, за которую посчитана статистика.
        points: Количество очков за день.
        user: Объект пользователя.
    """

    __tablename__ = "user_daily_stats"
    __table_args__ = (UniqueConstraint("user_id", "day", name="uq_user_day"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    day: Mapped[date] = mapped_column(Date, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped[User] = relationship(back_populates="daily_stats")
