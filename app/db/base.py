from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Общий базовый класс для всех декларативных ORM-моделей SQLAlchemy.
    Наследование от него позволяет объявлять таблицы в виде Python-классов.
    """
