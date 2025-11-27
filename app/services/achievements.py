from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.achievement import Achievement
from app.models.achievement_translation import AchievementTranslation
from app.models.user import User
from app.models.user_achievement import UserAchievement
from app.schemas.achievements import (
    AchievementCreate,
)


class AchievementService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_achievements(self) -> list[Achievement]:
        stmt = (
            select(Achievement)
            .options(selectinload(Achievement.translations))
            .order_by(Achievement.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_achievement(self, data: AchievementCreate) -> Achievement:
        achievement = Achievement(
            code=data.code,
            points=data.points,
        )
        self.session.add(achievement)
        await self.session.flush()

        for t in data.translations:
            translation = AchievementTranslation(
                achievement_id=achievement.id,
                language=t.language.value,
                name=t.name,
                description=t.description,
            )
            self.session.add(translation)

        await self.session.commit()
        stmt = (
            select(Achievement)
            .options(selectinload(Achievement.translations))
            .where(Achievement.id == achievement.id)
        )
        result = await self.session.execute(stmt)
        achievement_with_translations = result.scalar_one()

        return achievement_with_translations

    async def grant_achievement_to_user(
        self,
        user_id: int,
        code: str,
    ) -> UserAchievement:
        user_stmt = select(User).where(User.id == user_id)
        ach_stmt = select(Achievement).where(Achievement.code == code)

        user = (await self.session.execute(user_stmt)).scalar_one_or_none()
        achievement = (await self.session.execute(ach_stmt)).scalar_one_or_none()

        if user is None or achievement is None:
            return None

        existing_stmt = select(UserAchievement).where(
            UserAchievement.user_id == user.id,
            UserAchievement.achievement_id == achievement.id,
        )
        existing = (await self.session.execute(existing_stmt)).scalar_one_or_none()
        if existing:
            return existing

        ua = UserAchievement(
            user_id=user.id,
            achievement_id=achievement.id,
        )
        self.session.add(ua)

        user.total_points += achievement.points

        await self.session.commit()
        await self.session.refresh(ua)
        await self.session.refresh(user)
        return ua
