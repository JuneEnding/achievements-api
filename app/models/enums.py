from enum import Enum


class Language(str, Enum):
    """
    Перечисление языков, которые может выбрать пользователь.
    Используется для локализации достижений.
    """

    RU = "ru"
    EN = "en"
