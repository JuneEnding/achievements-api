# Achievements API

Сервис для управления пользователями и их достижениями.

## Технологический стек
- Python 3.12
- FastAPI + async SQLAlchemy 2.0
- PostgreSQL
- Alembic (code-first миграции)
- uv для управления зависимостями и виртуальным окружением
- Docker + docker-compose
- nginx как reverse proxy перед API
- Ruff, pre-commit, pytest

## Архитектура

Сервис состоит из трёх компонентов:

- **PostgreSQL (db)** — хранилище данных с пользователями, их достижениями.
- **API (api)** — FastAPI-приложение c асинхронным доступом к БД.
- **nginx (nginx)** — reverse proxy, который принимает HTTP-запросы на порт `80` и проксирует их в контейнер `api:8000`.

Схема:

```text
Client (browser, curl)
        ↓
    nginx:80
        ↓
   api:8000 (FastAPI + uvicorn)
        ↓
     db:5432 (PostgreSQL)

## Основной функционал

Сервер хранит:
 1. Пользователей: 
    - имя пользователя
    - выбранный язык интерфейса ( ru / en );
 
 2. Достижения: 
    - код достижения;
    - имя и описание на двух языках ( ru / en );
    - количество очков за достижение (целое положительное число);

API для:
- получения информации о пользователе;
- получения списка всех достижений;
- добавления достижений;
- выдачи достижения пользователю (с сохранением времени выдачи);
- получения списка выданных достижений пользователя на выбранном им языке;
- статистики:
   - пользователь с максимальным количеством достижений;
   - пользователь с максимальной суммой очков;
   - пара пользователей с максимальной разностью очков;
   - пара пользователей с минимальной разностью очков;
   - пользователи, которые получали достижения 7 дней подряд.

## Запуск через Docker Compose
1. Создать .env (пример):
'''
POSTGRES_DB=achievements
POSTGRES_USER=app_user
POSTGRES_PASSWORD=app_password

APP_DEBUG=false
'''

2. Собрать и запустить:
'''
docker compose build
docker compose up
'''

3. Проверка:
API через nginx: http://localhost/
Swagger: http://localhost/docs
Пример: GET http://localhost/api/v1/users/1

При старте контейнера api автоматически:
- применяются миграции Alembic (alembic upgrade head);
- запускается скрипт seed_demo_data, который создаёт:
   - набор ачивок из app/data/achievements.json;
   - демонстрационных пользователей;
   - выдачи достижений, в том числе пользователей с 7-дневными стриками.

## Локальный запуск без Docker
Требования:
   - установлен uv
   - PostgreSQL локально или в контейнере

1. Установить зависимости:
'''
uv sync --all-groups
'''

2. Настроить переменные окружения (.env):
'''
DATABASE_URL=postgresql+asyncpg://app_user:app_password@localhost:5432/achievements
APP_DEBUG=true
'''

3. Применить миграции:
'''
uv run alembic upgrade head
'''

4. Запустить сервер разработки:
'''
uv run fastapi dev app/main.py
'''

API будет доступен по адресу: http://localhost:8000
Документация Swagger: http://localhost:8000/docs

## Качество кода
В проекте настроены:
- Ruff (линтер + форматер)
- pre-commit хуки

Запуск вручную:
'''
uv run ruff check .
uv run ruff format .
uv run pre-commit run --all-files
'''
## Тесты

Запуск:
'''
uv run pytest
'''

## Структура проекта
app/
  api/
    v1/             # роутеры FastAPI
  settings/
    config.py       # настройки (pydantic-settings)
    db.py           # async-engine и Session
    logging.py      # настройка логирования
  models/           # ORM-модели SQLAlchemy
  schemas/          # Pydantic-схемы
  services/         # бизнес-логика (users, achievements, stats)
  seed_demo_data.py # скрипт для генерации демо-данных
etc/
  migrations/       # Alembic миграции
nginx/
  nginx.conf        # конфигурация reverse proxy
docker-compose.yml
Dockerfile
README.md
