from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.achievements import AchievementService
from app.services.stats import StatsService
from app.services.users import UserService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)


def get_achievement_service(session: SessionDep) -> AchievementService:
    return AchievementService(session)


def get_stats_service(session: SessionDep) -> StatsService:
    return StatsService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AchievementServiceDep = Annotated[AchievementService, Depends(get_achievement_service)]
StatsServiceDep = Annotated[StatsService, Depends(get_stats_service)]
