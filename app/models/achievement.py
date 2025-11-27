from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.achievement_translation import AchievementTranslation
    from app.models.user_achievement import UserAchievement

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
    )

    points: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    translations: Mapped[list[AchievementTranslation]] = relationship(
        back_populates="achievement",
        cascade="all, delete-orphan",
    )

    user_achievements: Mapped[list[UserAchievement]] = relationship(
        back_populates="achievement",
        cascade="all, delete-orphan",
    )
