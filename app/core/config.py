from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс настроек приложения. Загружает параметры из переменных окружения
    и файла .env.
    """

    database_url: str = Field(alias="DATABASE_URL", description="Строка подключения к базе данных.")
    debug: bool = Field(default=False, description="Флаг включения режима отладки.")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
