from pydantic import BaseModel, Field

from app.schemas.users import Language


class UserWithCount(BaseModel):
    """Пользователь и количество его достижений."""

    user_id: int = Field(..., description="Идентификатор пользователя.")
    username: str = Field(..., description="Имя пользователя.")
    language: Language = Field(..., description="Предпочитаемый язык интерфейса пользователя.")
    total_points: int = Field(
        ..., description="Суммарное количество очков за все достижения пользователя."
    )
    achievements_count: int = Field(..., description="Количество выданных пользователю достижений.")


class PointsDiffPair(BaseModel):
    """Пара пользователей и разность их очков."""

    user1_id: int = Field(..., description="Идентификатор первого пользователя.")
    user1_username: str = Field(..., description="Имя первого пользователя.")
    user1_points: int = Field(..., description="Суммарное количество очков первого пользователя.")
    user2_id: int = Field(..., description="Идентификатор второго пользователя.")
    user2_username: str = Field(..., description="Имя второго пользователя.")
    user2_points: int = Field(..., description="Суммарное количество очков второго пользователя.")
    diff: int = Field(..., description="Абсолютная разность очков между пользователями.")


class UserWithStreak(BaseModel):
    """Пользователь и его максимальный стрик по дням."""

    user_id: int = Field(..., description="Идентификатор пользователя.")
    username: str = Field(..., description="Имя пользователя.")
    language: Language = Field(..., description="Предпочитаемый язык интерфейса пользователя.")
    total_points: int = Field(
        ..., description="Суммарное количество очков за все достижения пользователя."
    )
    longest_streak: int = Field(..., description="Длина максимального стрика.")


class StatsSummary(BaseModel):
    """Сводная статичтика по пользователям и достижениям."""

    max_achievements: UserWithCount | None = Field(
        None, description="Пользователь с максимальным количеством достижений."
    )
    max_points: UserWithCount | None = Field(
        None, description="Пользователь с максимальной суммой очков за достижения."
    )
    max_points_diff: PointsDiffPair | None = Field(
        None, description="Пара пользователей с максимальной разностью очков."
    )
    min_points_diff: PointsDiffPair | None = Field(
        None, description="Пара пользователей с минимальной ненулевой разностью очков."
    )
    streak_users: list[UserWithStreak] = Field(
        default_factory=list,
        description="Список пользователей, которые получали достижения не менее 7 дней подряд.",
    )
