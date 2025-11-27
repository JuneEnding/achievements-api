from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_achievement import UserAchievement
    from app.models.user_daily_stat import UserDailyStat

from datetime import datetime

from sqlalchemy import Integer, String, func
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import Language


class User(Base):
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
