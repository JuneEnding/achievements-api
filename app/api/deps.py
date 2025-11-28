from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.achievements import AchievementService
from app.services.stats import StatsService
from app.services.users import UserService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_user_service(session: SessionDep) -> UserService:
    """
    Создаёт экземпляр сервиса работы с пользователями на основе переданной
    асинхронной сессии БД.

    :param session: Асинхронная сессия SQLAlchemy.
    :return: Экземпляр UserService.
    """
    return UserService(session)


def get_achievement_service(session: SessionDep) -> AchievementService:
    """
    Создаёт экземпляр сервиса работы с достижениями.

    :param session: Асинхронная сессия SQLAlchemy.
    :return: Экземпляр AchievementService.
    """
    return AchievementService(session)


def get_stats_service(session: SessionDep) -> StatsService:
    """
    Создаёт экземпляр сервиса статистики по пользователям и достижениям.

    :param session: Асинхронная сессия SQLAlchemy.
    :return: Экземпляр StatsService.
    """
    return StatsService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AchievementServiceDep = Annotated[AchievementService, Depends(get_achievement_service)]
StatsServiceDep = Annotated[StatsService, Depends(get_stats_service)]
