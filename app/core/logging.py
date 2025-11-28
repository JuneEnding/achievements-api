import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """
    Настраивает базовое логирование для всего приложения: вывод в stdout,
    формат с датой, уровнем, именем логгера и функцией. Если логирование
    уже настроено (есть обработчики у корневого логгера), повторная
    настройка не выполняется.

    :param level: Уровень логирования для корневого логгера.
    :return: None.
    """
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="[{asctime}] {levelname} {name}:{funcName}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
    )
    handler.setFormatter(formatter)

    root_logger.setLevel(level)
    root_logger.addHandler(handler)
