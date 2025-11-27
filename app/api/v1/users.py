from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.api.deps import UserServiceDep
from app.schemas.achievements import UserAchievementRead
from app.schemas.users import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    user_service: UserServiceDep,
) -> UserRead:
    user = await user_service.create_user(data)
    return UserRead.model_validate(user)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    user_service: UserServiceDep,
) -> UserRead:
    user = await user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.get("/{user_id}/achievements", response_model=list[UserAchievementRead])
async def get_user_achievements(
    user_id: int,
    user_service: UserServiceDep,
) -> list[UserAchievementRead]:
    user, achievements = await user_service.get_user_achievements(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return achievements
