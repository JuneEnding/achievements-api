from datetime import date
from itertools import combinations, pairwise

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.user_achievement import UserAchievement
from app.schemas.stats import PointsDiffPair, UserWithCount, UserWithStreak


class StatsService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def user_with_max_achievements(self) -> UserWithCount | None:
        """
        Вычисление пользователя, у которого выдано максимальное количество достижений.

        :return: Пользователь и количество его достижений или None, если данных нет.
        """
        stmt = (
            select(
                User.id,
                User.username,
                User.language,
                User.total_points,
                func.count(UserAchievement.id).label("achievements_count"),
            )
            .join(UserAchievement, User.id == UserAchievement.user_id)
            .group_by(User.id)
            .order_by(func.count(UserAchievement.id).desc())
            .limit(1)
        )

        row = (await self.session.execute(stmt)).one_or_none()
        if row is None:
            return None

        return UserWithCount(
            user_id=row.id,
            username=row.username,
            language=row.language,
            total_points=row.total_points,
            achievements_count=row.achievements_count,
        )

    async def user_with_max_points(self) -> UserWithCount | None:
        """
        Вычисление пользователя с максимальной суммой очков за достижения.

        :return: Пользователь и его суммарные очки или None, если данных нет.
        """
        stmt = (
            select(
                User.id,
                User.username,
                User.language,
                User.total_points,
                func.count(UserAchievement.id).label("achievements_count"),
            )
            .join(UserAchievement, User.id == UserAchievement.user_id, isouter=True)
            .group_by(User.id)
            .order_by(User.total_points.desc())
            .limit(1)
        )

        row = (await self.session.execute(stmt)).one_or_none()
        if row is None:
            return None

        return UserWithCount(
            user_id=row.id,
            username=row.username,
            language=row.language,
            total_points=row.total_points,
            achievements_count=row.achievements_count or 0,
        )

    async def max_min_points_diff(self) -> tuple[PointsDiffPair | None, PointsDiffPair | None]:
        """
        По всем пользователям вычисляется пара с максимальной и минимальной
        ненулевой разностью суммарных очков.

        :return: Кортеж из пары с максимальной разностью и пары с минимальной разностью.
        """
        stmt = select(User.id, User.username, User.total_points)
        rows = (await self.session.execute(stmt)).all()
        users = list(rows)
        if len(users) < 2:
            return None, None

        max_pair: PointsDiffPair | None = None
        min_pair: PointsDiffPair | None = None

        for u1, u2 in combinations(users, 2):
            diff = abs(u1.total_points - u2.total_points)
            if diff == 0:
                continue

            pair = PointsDiffPair(
                user1_id=u1.id,
                user1_username=u1.username,
                user1_points=u1.total_points,
                user2_id=u2.id,
                user2_username=u2.username,
                user2_points=u2.total_points,
                diff=diff,
            )

            if max_pair is None or diff > max_pair.diff:
                max_pair = pair
            if min_pair is None or diff < min_pair.diff:
                min_pair = pair

        return max_pair, min_pair

    async def users_with_7day_streak(self, min_days: int = 7) -> list[UserWithStreak]:
        """
        По датам выдачи достижений для каждого пользователя вычисляется
        длина максимального стрика - количества подряд идущих дней, в каждый
        из которых было выдано хотя бы одно достижение. Возвращаются
        пользователи, у которых длина стрика не меньше min_days.

        :param min_days: Минимальная длина стрика в днях.
        :return: Список пользователей с информацией о максимальном стрике.
        """

        day_expr = func.date_trunc("day", UserAchievement.issued_at).label("day")

        stmt = (
            select(
                User.id,
                User.username,
                User.language,
                User.total_points,
                day_expr,
            )
            .join(UserAchievement, User.id == UserAchievement.user_id)
            .group_by(
                User.id,
                User.username,
                User.language,
                User.total_points,
                day_expr,
            )
            .order_by(User.id, day_expr)
        )

        result = await self.session.execute(stmt)
        rows = result.all()

        users_days: dict[int, dict] = {}
        for row in rows:
            uid = row.id
            if uid not in users_days:
                users_days[uid] = {
                    "username": row.username,
                    "language": row.language,
                    "total_points": row.total_points,
                    "days": [],
                }
            day: date = row.day.date()
            users_days[uid]["days"].append(day)

        result_users: list[UserWithStreak] = []

        for uid, data in users_days.items():
            days = sorted(set(data["days"]))
            if not days:
                continue

            longest = 1
            current = 1

            for prev_day, curr_day in pairwise(days):
                delta = (curr_day - prev_day).days
                if delta == 1:
                    current += 1
                else:
                    current = 1
                longest = max(longest, current)

            if longest >= min_days:
                result_users.append(
                    UserWithStreak(
                        user_id=uid,
                        username=data["username"],
                        language=data["language"],
                        total_points=data["total_points"],
                        longest_streak=longest,
                    )
                )

        return result_users
