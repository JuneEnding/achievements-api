from __future__ import annotations

from fastapi import status
from httpx import AsyncClient

from app.models.enums import Language


async def test_create_and_get_user(client: AsyncClient) -> None:
    """
    Проверяет, что пользователь создаётся и возвращается
    через API с корректными полями.
    """
    payload = {
        "username": "test_user",
        "language": Language.RU.value,
    }

    response = await client.post("/api/v1/users", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["id"] > 0
    assert data["username"] == "test_user"
    assert data["language"] == "ru"
    assert data["total_points"] == 0

    user_id: int = data["id"]

    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK

    data_get = response.json()
    assert data_get["id"] == user_id
    assert data_get["username"] == "test_user"
    assert data_get["language"] == "ru"
    assert data_get["total_points"] == 0


async def test_get_user_not_found(client: AsyncClient) -> None:
    """
    Проверяет, что API корректно возвращает 404 для несуществующего пользователя.
    """
    response = await client.get("/api/v1/users/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"
