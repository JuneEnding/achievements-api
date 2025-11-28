import asyncio
import json
import random
from collections import defaultdict
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import AsyncSessionFactory
from app.models import (
    Achievement,
    AchievementTranslation,
    Language,
    User,
    UserAchievement,
)

BASE_DIR = Path(__file__).resolve().parent
ACHIEVEMENTS_JSON_PATH = BASE_DIR / "data" / "achievements.json"


async def is_already_seeded(session: AsyncSession) -> bool:
    """
    Проверка, содержит ли база данных уже записи пользователей, достижений
    или выданных достижений.

    :param session: Асинхронная сессия SQLAlchemy.
    :return: True, если данные уже есть, иначе False.
    """
    ach_count = await session.scalar(select(func.count(Achievement.id)))
    user_count = await session.scalar(select(func.count(User.id)))
    ua_count = await session.scalar(select(func.count(UserAchievement.id)))
    return bool(ach_count or user_count or ua_count)


async def seed_achievements(session: AsyncSession) -> dict[str, Achievement]:
    """
    Создание или обновление достижений и их переводов на основе JSON-файла.

    :param session: Асинхронная сессия SQLAlchemy.
    :return: Словарь код достижения → объект достижения.
    """
    if not ACHIEVEMENTS_JSON_PATH.exists():
        raise FileNotFoundError(f"JSON file not found: {ACHIEVEMENTS_JSON_PATH}")

    with ACHIEVEMENTS_JSON_PATH.open("r", encoding="utf-8") as f:
        data: list[dict[str, Any]] = json.load(f)

    achievements_by_code: dict[str, Achievement] = {}

    for item in data:
        code = item["id"]
        points = int(item["points"])

        stmt = select(Achievement).where(Achievement.code == code)
        result = await session.execute(stmt)
        achievement = result.scalar_one_or_none()

        if achievement is None:
            achievement = Achievement(code=code, points=points)
            session.add(achievement)
            await session.flush()
        else:
            achievement.points = points

        achievements_by_code[code] = achievement

        for lang, name_key, desc_key in [
            (Language.EN, "name_en", "description_en"),
            (Language.RU, "name_ru", "description_ru"),
        ]:
            stmt_tr = select(AchievementTranslation).where(
                AchievementTranslation.achievement_id == achievement.id,
                AchievementTranslation.language == lang,
            )
            tr_result = await session.execute(stmt_tr)
            translation = tr_result.scalar_one_or_none()

            if translation is None:
                translation = AchievementTranslation(
                    achievement_id=achievement.id,
                    language=lang,
                    name=item[name_key],
                    description=item[desc_key],
                )
                session.add(translation)
            else:
                translation.name = item[name_key]
                translation.description = item[desc_key]

    await session.commit()
    return achievements_by_code


async def seed_users(session: AsyncSession) -> list[User]:
    """
    Создание набора демонстрационных пользователей с разными языками интерфейса.
    Уже существующие пользователи с тем же именем переиспользуются.

    :param session: Асинхронная сессия SQLAlchemy.
    :return: Список созданных или найденных пользователей.
    """
    demo_users = [
        ("streak_ru", Language.RU),
        ("streak_en", Language.EN),
        ("alice", Language.EN),
        ("bob", Language.EN),
        ("ivan", Language.RU),
        ("olga", Language.RU),
        ("devops_ru", Language.RU),
        ("backend_en", Language.EN),
    ]

    users: list[User] = []

    for username, lang in demo_users:
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                username=username,
                language=lang,
            )
            session.add(user)
            await session.flush()

        users.append(user)

    await session.commit()
    return users


async def seed_user_achievements(
    session: AsyncSession,
    users: list[User],
    achievements_by_code: dict[str, Achievement],
) -> None:
    """
    Выдача достижений пользователям для заполнения базы демонстрационными данными.
    Для части пользователей создаются стрики из нескольких подряд идущих дней.

    :param session: Асинхронная сессия SQLAlchemy.
    :param users: Пользователи, которым выдаются достижения.
    :param achievements_by_code: Словарь код достижения → объект достижения.
    :return: None.
    """
    if not users or not achievements_by_code:
        return

    random.seed(42)

    all_achievements = list(achievements_by_code.values())
    today = date.today()

    user_to_achievement_ids: dict[int, set[int]] = defaultdict(set)
    user_points: dict[int, int] = defaultdict(int)

    streak_users = users[:2]
    streak_length = 7
    streak_start = today - timedelta(days=streak_length - 1)

    for user in streak_users:
        available_for_user = all_achievements.copy()
        random.shuffle(available_for_user)

        for i in range(streak_length):
            if not available_for_user:
                break
            ach = available_for_user.pop()
            issued_day = streak_start + timedelta(days=i)
            issued_at = datetime.combine(issued_day, time(hour=10, minute=0))

            ua = UserAchievement(
                user_id=user.id,
                achievement_id=ach.id,
                issued_at=issued_at,
            )
            session.add(ua)

            user_to_achievement_ids[user.id].add(ach.id)
            user_points[user.id] += ach.points

    other_users = users[2:]

    for user in other_users:
        available = all_achievements.copy()
        random.shuffle(available)
        count = random.randint(5, min(12, len(available)))  # noqa: S311
        selected = available[:count]

        for ach in selected:
            days_ago = random.randint(0, 29)  # noqa: S311
            issued_day = today - timedelta(days=days_ago)
            issued_at = datetime.combine(issued_day, time(hour=random.randint(9, 20)))  # noqa: S311

            ua = UserAchievement(
                user_id=user.id,
                achievement_id=ach.id,
                issued_at=issued_at,
            )
            session.add(ua)

            user_to_achievement_ids[user.id].add(ach.id)
            user_points[user.id] += ach.points

    for user in users:
        user.total_points = user_points.get(user.id, 0)

    await session.commit()


async def main() -> None:
    """
    Точка входа скрипта заполнения базы демонстрационными данными:
    открывает сессию, проверяет наличие данных и при необходимости
    создаёт достижения, пользователей и выданные достижения.

    :return: None.
    """
    async with AsyncSessionFactory() as session:
        if await is_already_seeded(session):
            print("Database already contains data. Skipping seeding.")
            return

        print(f"Seeding achievements from {ACHIEVEMENTS_JSON_PATH}...")
        achievements_by_code = await seed_achievements(session)
        print(f"Created/updated {len(achievements_by_code)} achievements.")

        print("Seeding users...")
        users = await seed_users(session)
        print(f"Created/loaded {len(users)} users.")

        print("Seeding user achievements (including 7-day streaks)...")
        await seed_user_achievements(session, users, achievements_by_code)

        print("Done. Demo data has been inserted.")


if __name__ == "__main__":
    asyncio.run(main())
