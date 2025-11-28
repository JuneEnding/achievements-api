from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import Language

if TYPE_CHECKING:
    from app.models.achievement import Achievement


class AchievementTranslation(Base):
    """
    Хранит локализованные название и описание достижения на конкретном языке.
    Для каждой пары (achievement_id, language) допускается только одна запись.

    Поля:
        id: Первичный ключ записи.
        achievement_id: Идентификатор базового достижения.
        language: Язык перевода (ru/en).
        name: Название достижения на указанном языке.
        description: Описание достижения на указанном языке.
    """

    __tablename__ = "achievement_translations"
    __table_args__ = (
        UniqueConstraint(
            "achievement_id",
            "language",
            name="uq_achievement_language",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    achievement_id: Mapped[int] = mapped_column(
        ForeignKey("achievements.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    language: Mapped[Language] = mapped_column(
        PG_ENUM(Language, name="language_enum", create_type=True),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    achievement: Mapped[Achievement] = relationship(
        back_populates="translations",
    )
