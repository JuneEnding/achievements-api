from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.users import Language


class AchievementTranslationBase(BaseModel):
    language: Language
    name: str
    description: str


class AchievementTranslationCreate(AchievementTranslationBase):
    pass


class AchievementTranslationRead(AchievementTranslationBase):
    id: int

    class Config:
        from_attributes = True


class AchievementBase(BaseModel):
    code: str = Field(..., max_length=64)
    points: int = Field(..., ge=0)


class AchievementCreate(AchievementBase):
    translations: list[AchievementTranslationCreate]


class AchievementRead(AchievementBase):
    id: int
    translations: list[AchievementTranslationRead]

    class Config:
        from_attributes = True


class UserAchievementRead(BaseModel):
    achievement_id: int
    code: str
    name: str
    description: str
    points: int
    issued_at: datetime

    class Config:
        from_attributes = False
