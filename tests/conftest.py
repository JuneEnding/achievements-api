from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterator, Generator

import pytest
from fastapi import status
from httpx import AsyncClient, ConnectError


@pytest.fixture(scope="function")
async def client() -> AsyncIterator[AsyncClient]:
    """
    Асинхронный HTTP-клиент для интеграционных тестов.

    - Создаётся один AsyncClient на всю тестовую сессию.
    - Перед запуском тестов ждём, пока тестовый сервер ответит 200 на /health.
    - Если сервер не поднялся за таймаут — падаем с понятной ошибкой.
    """
    base_url: str = os.getenv("TEST_API_URL", "http://localhost:8000")

    async with AsyncClient(base_url=base_url, timeout=10.0) as async_client:
        for _ in range(30):
            try:
                resp = await async_client.get("/health")
                if resp.status_code == status.HTTP_200_OK:
                    break
            except ConnectError:
                pass

            await asyncio.sleep(1)

        else:
            pytest.fail("API test server is not ready on /health after 30 seconds")

        yield async_client


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Фикстура заменяет event_loop из pytest.asyncio.
    Почему-то методы падают при попытке выполнить запрос в БД.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    yield loop

    loop.close()
