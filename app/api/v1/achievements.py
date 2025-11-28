from fastapi import APIRouter, HTTPException, status

from app.api.deps import AchievementServiceDep
from app.schemas.achievements import AchievementCreate, AchievementRead

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("", response_model=list[AchievementRead])
async def list_achievements(
    service: AchievementServiceDep,
) -> list[AchievementRead]:
    """
    Возвращает список всех доступных достижений.

    :param service: Сервис работы с достижениями.
    :return: Список достижений.
    """

    achievements = await service.list_achievements()
    return [AchievementRead.model_validate(a) for a in achievements]


@router.post("", response_model=AchievementRead, status_code=status.HTTP_201_CREATED)
async def create_achievement(
    data: AchievementCreate,
    service: AchievementServiceDep,
) -> AchievementRead:
    """
    Создаёт новое достижение и его переводы на указанных языках.

    :param data: Данные для создания достижения.
    :param service: Сервис работы с достижениями.
    :return: Созданное достижение.
    """

    achievement = await service.create_achievement(data)
    return AchievementRead.model_validate(achievement)


@router.post("/grant/{user_id}/{code}", status_code=status.HTTP_201_CREATED)
async def grant_achievement(
    user_id: int,
    code: str,
    service: AchievementServiceDep,
):
    """
    Выдаёт пользователю достижение по его коду. При повторной выдаче
    возвращается уже существующая запись. Если пользователь или достижение
    не найдены, возвращается ошибка 404.

    :param user_id: Идентификатор пользователя.
    :param code: Код достижения.
    :param service: Сервис работы с достижениями.
    :return: Статус операции и идентификаторы пользователя и достижения.
    """

    user_achievement = await service.grant_achievement_to_user(user_id, code)
    if user_achievement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User or achievement not found"
        )
    return {
        "status": "ok",
        "user_id": user_achievement.user_id,
        "achievement_id": user_achievement.achievement_id,
    }
