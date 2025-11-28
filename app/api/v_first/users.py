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
    """
    Создание нового пользователя и возврат его данных.

    :param data: Тело запроса с данными пользователя.
    :param user_service: Сервис работы с пользователями.
    :return: Данные созданного пользователя.
    """

    user = await user_service.create_user(data)
    return UserRead.model_validate(user)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    user_service: UserServiceDep,
) -> UserRead:
    """
    Возвращает данные пользователя по его идентификатору. Если пользователь
    не найден, возвращается ошибка 404.

    :param user_id: Идентификатор пользователя.
    :param user_service: Сервис работы с пользователями.
    :return: Данные найденного пользователя.
    """

    user = await user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead.model_validate(user)


@router.get("/{user_id}/achievements", response_model=list[UserAchievementRead])
async def get_user_achievements(
    user_id: int,
    user_service: UserServiceDep,
) -> list[UserAchievementRead]:
    """
    Возвращает список выданных пользователю достижений с учётом выбранного им языка.

    :param user_id: Идентификатор пользователя.
    :param user_service: Сервис работы с пользователями.
    :return: Список достижений пользователя.
    """

    user, achievements = await user_service.get_user_achievements(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return achievements
