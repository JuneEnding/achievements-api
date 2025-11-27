from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import StatsServiceDep
from app.schemas.stats import PointsDiffPair, UserWithCount, UserWithStreak

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/max-achievements", response_model=UserWithCount | None)
async def max_achievements(
    service: StatsServiceDep,
) -> UserWithCount | None:
    return await service.user_with_max_achievements()


@router.get("/max-points", response_model=UserWithCount | None)
async def max_points(
    service: StatsServiceDep,
) -> UserWithCount | None:
    return await service.user_with_max_points()


@router.get("/points-diff", response_model=dict)
async def points_diff(
    service: StatsServiceDep,
) -> dict[str, PointsDiffPair | None]:
    max_pair, min_pair = await service.max_min_points_diff()
    return {
        "max_diff": max_pair,
        "min_diff": min_pair,
    }


@router.get("/7-days-streak", response_model=list[UserWithStreak])
async def seven_days_streak(
    service: StatsServiceDep,
) -> list[UserWithStreak]:
    return await service.users_with_7day_streak(min_days=7)
