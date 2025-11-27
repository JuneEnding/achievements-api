from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.achievement import Achievement
    from app.models.user import User

from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserAchievement(Base):
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

    issused_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates="achievements")
    achievement: Mapped[Achievement] = relationship(back_populates="user_achievements")
