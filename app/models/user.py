from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, func
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import Language

if TYPE_CHECKING:
    from app.models.user_achievement import UserAchievement
    from app.models.user_daily_stat import UserDailyStat


class User(Base):
    """
    Представляет пользователя, который может получать достижения. Хранит
    имя, язык, суммарные очки и дату создания
    учётной записи.

    Поля:
        id: Первичный ключ пользователя.
        username: Уникальный логин пользователя.
        language: Предпочитаемый язык интерфейса (ru/en).
        total_points: Суммарное количество очков за все достижения.
        created_at: Дата и время создания пользователя.
        achievements: Список выданных достижений (связанные UserAchievement).
        daily_stats: Ежедневная статистика по очкам пользователя.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
    )

    language: Mapped[Language] = mapped_column(
        PG_ENUM(Language, name="language_enum", create_type=False),
        nullable=False,
    )

    total_points: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    achievements: Mapped[list[UserAchievement]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    daily_stats: Mapped[list[UserDailyStat]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
