from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.users import Language


class AchievementTranslationBase(BaseModel):
    """Базовые поля локализации достижений."""

    language: Language = Field(..., description="Язык локализации.")
    name: str = Field(..., description="Название достижения на указанном языке.")
    description: str = Field(..., description="Описание достижения на указанном языке.")


class AchievementTranslationCreate(AchievementTranslationBase):
    """Модель для создания перевода достижения."""


class AchievementTranslationRead(AchievementTranslationBase):
    """Модель для чтения перевода достижения из БД."""

    id: int = Field(..., description="Идентификатор записи.")

    class Config:
        from_attributes = True


class AchievementBase(BaseModel):
    """Базовые поля достижения"""

    code: str = Field(..., max_length=64, description="Уникальный символьный код достижения.")
    points: int = Field(..., ge=0, description="Количество очков за достижения.")


class AchievementCreate(AchievementBase):
    """Модель для создания достижения с локализацией."""

    translations: list[AchievementTranslationCreate] = Field(
        ..., description="Список переводов названия и описания достижения."
    )


class AchievementRead(AchievementBase):
    """Модель для возврата достижения."""

    id: int = Field(..., description="Идентификатор достижения.")
    translations: list[AchievementTranslationRead] = Field(
        ..., description="Переводы названия и описания достижения."
    )

    class Config:
        from_attributes = True


class UserAchievementRead(BaseModel):
    """Информация о выданном пользователю достижении."""

    achievement_id: int = Field(..., description="Идентификатор достижения.")
    code: str = Field(..., description="Код достижения.")
    name: str = Field(..., description="Локализованное название достижения.")
    description: str = Field(..., description="Локализованное описание достижения.")
    points: int = Field(..., description="Количество очков, которое даёт достижения.")
    issued_at: datetime = Field(..., description="Дата и время выдачи достижэения пользователю.")

    class Config:
        from_attributes = False
