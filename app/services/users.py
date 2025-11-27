from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.achievement import Achievement
from app.models.achievement_translation import AchievementTranslation
from app.models.user import User
from app.models.user_achievement import UserAchievement
from app.schemas.achievements import UserAchievementRead
from app.schemas.users import UserCreate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, data: UserCreate) -> User:
        user = User(
            username=data.username,
            language=data.language.value,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_achievements(self, user_id: int) -> tuple[User, list[UserAchievementRead]]:
        user = await self.get_user(user_id)
        if user is None:
            return None, []

        stmt = (
            select(
                UserAchievement.issued_at,
                Achievement.id,
                Achievement.code,
                Achievement.points,
                AchievementTranslation.name,
                AchievementTranslation.description,
            )
            .join(Achievement, UserAchievement.achievement_id == Achievement.id)
            .join(
                AchievementTranslation,
                (AchievementTranslation.achievement_id == Achievement.id)
                & (AchievementTranslation.language == user.language),
            )
            .where(UserAchievement.user_id == user.id)
            .order_by(UserAchievement.issued_at.desc())
        )

        result = await self.session.execute(stmt)
        rows = result.all()

        achievements = [
            UserAchievementRead(
                achievement_id=row.id,
                code=row.code,
                name=row.name,
                description=row.description,
                points=row.points,
                issued_at=row.issued_at.isoformat(),
            )
            for row in rows
        ]
        return user, achievements
