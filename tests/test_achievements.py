from __future__ import annotations

from fastapi import status
from httpx import AsyncClient

from app.models.enums import Language


async def test_create_and_list_achievements(client: AsyncClient) -> None:
    """
    Проверяет создание достижения и его появление в списке /achievements.
    """
    payload = {
        "code": "test_ach",
        "points": 10,
        "translations": [
            {
                "language": Language.RU.value,
                "name": "Тестовая ачивка",
                "description": "Описание на русском.",
            },
            {
                "language": Language.EN.value,
                "name": "Test achievement",
                "description": "Description in English.",
            },
        ],
    }

    response = await client.post("/api/v1/achievements", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    created = response.json()
    assert created["code"] == "test_ach"
    assert created["points"] == 10
    assert len(created["translations"]) == 2

    response = await client.get("/api/v1/achievements")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    codes = {item["code"] for item in data}
    assert "test_ach" in codes


async def test_grant_achievement_to_user(client: AsyncClient) -> None:
    """
    Проверяет, что достижение можно выдать пользователю и что при этом
    корректно возвращается статус и идентификаторы.
    """
    user_payload = {"username": "ach_user", "language": Language.EN.value}
    user_resp = await client.post("/api/v1/users", json=user_payload)
    assert user_resp.status_code == status.HTTP_201_CREATED
    user_id: int = user_resp.json()["id"]

    ach_payload = {
        "code": "grant_ach",
        "points": 20,
        "translations": [
            {
                "language": Language.EN.value,
                "name": "Grantable",
                "description": "Can be granted.",
            }
        ],
    }
    ach_resp = await client.post("/api/v1/achievements", json=ach_payload)
    assert ach_resp.status_code == status.HTTP_201_CREATED

    grant_resp = await client.post(
        f"/api/v1/achievements/grant/{user_id}/grant_ach",
    )
    assert grant_resp.status_code == status.HTTP_201_CREATED

    grant_data = grant_resp.json()
    assert grant_data["status"] == "ok"
    assert grant_data["user_id"] == user_id
    assert isinstance(grant_data["achievement_id"], int)
