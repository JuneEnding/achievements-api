from __future__ import annotations

from fastapi import FastAPI

from app.api.v1 import achievements as achievements_router
from app.api.v1 import stats as stats_router
from app.api.v1 import users as users_router


def create_app() -> FastAPI:
    app = FastAPI(title="Achievements API", version="1.0.0")

    app.include_router(users_router.router, prefix="/api/v1")
    app.include_router(achievements_router.router, prefix="/api/v1")
    app.include_router(stats_router.router, prefix="/api/v1")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
