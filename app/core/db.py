from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость FastAPI, которая предоставляет асинхронную сессию SQLAlchemy
    для работы с базой данных. Сессия автоматически закрывается после
    завершения обработки запроса.

    :yield: Асинхронная сессия SQLAlchemy.
    """
    async with AsyncSessionFactory() as session:
        yield session
