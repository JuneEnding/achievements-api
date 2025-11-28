from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import Language


class UserBase(BaseModel):
    """Базовая модель пользователя."""

    username: str = Field(..., description="Имя пользователя.")
    language: Language = Field(..., description="Предпочитаемый язык.")


class UserCreate(UserBase):
    """Модель для создания нового пользователя."""


class UserRead(UserBase):
    """Модель для возврата пользователя."""

    id: int = Field(..., description="Идентификатор пользователя.")
    total_points: int = Field(
        ..., description="Суммарное количество очков за все достижения пользователя."
    )
    created_at: datetime = Field(..., description="Дата и время создания пользователя.")

    class Config:
        from_attributes = True
