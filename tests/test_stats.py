from __future__ import annotations

from fastapi import status
from httpx import AsyncClient

from app.models.enums import Language


async def test_stats_summary(client: AsyncClient) -> None:
    """
    Создаёт несколько пользователей и достижений, выдаёт ачивки и проверяет,
    что эндпоинт /stats возвращает корректную структуру данных.
    """
    u1_resp = await client.post(
        "/api/v1/users",
        json={"username": "u1", "language": Language.RU.value},
    )
    assert u1_resp.status_code == status.HTTP_201_CREATED
    u1 = u1_resp.json()

    u2_resp = await client.post(
        "/api/v1/users",
        json={"username": "u2", "language": Language.EN.value},
    )
    assert u2_resp.status_code == status.HTTP_201_CREATED
    u2 = u2_resp.json()

    a1_resp = await client.post(
        "/api/v1/achievements",
        json={
            "code": "s1",
            "points": 10,
            "translations": [
                {
                    "language": Language.RU.value,
                    "name": "S1",
                    "description": "S1 desc",
                }
            ],
        },
    )
    assert a1_resp.status_code == status.HTTP_201_CREATED

    a2_resp = await client.post(
        "/api/v1/achievements",
        json={
            "code": "s2",
            "points": 30,
            "translations": [
                {
                    "language": Language.RU.value,
                    "name": "S2",
                    "description": "S2 desc",
                }
            ],
        },
    )
    assert a2_resp.status_code == status.HTTP_201_CREATED

    await client.post(f"/api/v1/achievements/grant/{u1['id']}/s1")
    await client.post(f"/api/v1/achievements/grant/{u1['id']}/s2")
    await client.post(f"/api/v1/achievements/grant/{u2['id']}/s2")

    resp = await client.get("/api/v1/stats")
    assert resp.status_code == status.HTTP_200_OK

    stats = resp.json()

    assert "max_achievements" in stats
    assert "max_points" in stats
    assert "max_points_diff" in stats
    assert "min_points_diff" in stats
    assert "streak_users" in stats

    assert stats["max_points"] is not None
    assert "user_id" in stats["max_points"]
    assert "total_points" in stats["max_points"]
