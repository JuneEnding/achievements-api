from __future__ import annotations

from pydantic import BaseModel

from app.schemas.users import Language


class UserWithCount(BaseModel):
    user_id: int
    username: str
    language: Language
    total_points: int
    achievements_count: int


class PointsDiffPair(BaseModel):
    user1_id: int
    user1_username: str
    user1_points: int
    user2_id: int
    user2_username: str
    user2_points: int
    diff: int


class UserWithStreak(BaseModel):
    user_id: int
    username: str
    language: Language
    total_points: int
    longest_streak: int
