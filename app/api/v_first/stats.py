from fastapi import APIRouter

from app.api.deps import StatsServiceDep
from app.schemas.stats import StatsSummary

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("", response_model=StatsSummary)
async def get_stats_summary(
    service: StatsServiceDep,
) -> StatsSummary:
    """
    Возвращает в одном ответе:
      * пользователя с максимальным количеством достижений;
      * пользователя с максимальным количеством очков;
      * пару пользователей с максимальной разностью очков;
      * пару пользователей с минимальной ненулевой разностью очков;
      * пользователей, получавших достижения 7 дней подряд.
    """

    max_achievements = await service.user_with_max_achievements()
    max_points = await service.user_with_max_points()
    max_diff, min_diff = await service.max_min_points_diff()
    streak_users = await service.users_with_7day_streak(min_days=7)

    return StatsSummary(
        max_achievements=max_achievements,
        max_points=max_points,
        max_points_diff=max_diff,
        min_points_diff=min_diff,
        streak_users=streak_users,
    )
