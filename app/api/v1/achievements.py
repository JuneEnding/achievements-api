from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.api.deps import AchievementServiceDep
from app.schemas.achievements import AchievementCreate, AchievementRead

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("", response_model=list[AchievementRead])
async def list_achievements(
    service: AchievementServiceDep,
) -> list[AchievementRead]:
    achievements = await service.list_achievements()
    return [AchievementRead.model_validate(a) for a in achievements]


@router.post("", response_model=AchievementRead, status_code=status.HTTP_201_CREATED)
async def create_achievement(
    data: AchievementCreate,
    service: AchievementServiceDep,
) -> AchievementRead:
    ach = await service.create_achievement(data)
    return AchievementRead.model_validate(ach)


@router.post("/grant/{user_id}/{code}", status_code=status.HTTP_201_CREATED)
async def grant_achievement(
    user_id: int,
    code: str,
    service: AchievementServiceDep,
):
    ua = await service.grant_achievement_to_user(user_id, code)
    if ua is None:
        raise HTTPException(status_code=404, detail="User or achievement not found")
    return {"status": "ok", "user_id": ua.user_id, "achievement_id": ua.achievement_id}
