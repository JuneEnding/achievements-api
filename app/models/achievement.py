from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.achievement_translation import AchievementTranslation
    from app.models.user_achievement import UserAchievement


class Achievement(Base):
    """
    Базовое достижение без привязки к языку. Содержит уникальный код и
    количество очков. Тексты названия и описания хранятся в связанных
    записях `AchievementTranslation`.

    Поля:
        id: Первичный ключ достижения.
        code: Уникальный символьный код достижения.
        points: Количество очков за достижение.
        translations: Переводы названия и описания на разные языки.
        user_achievements: Связанные выдачи достижения пользователям.
    """

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
