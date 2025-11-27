from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.models.enums import Language


class UserBase(BaseModel):
    username: str
    language: Language


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    total_points: int
    created_at: datetime

    class Config:
        from_attributes = True
