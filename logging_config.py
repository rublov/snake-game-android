"""Единая конфигурация логирования для проекта Snake Game."""

from __future__ import annotations

import logging
import logging.config
from logging.handlers import RotatingFileHandler
from pathlib import Path

_LOG_FILE = "snake_game.log"
_MAX_BYTES = 1 * 1024 * 1024  # 1 MB
_BACKUP_COUNT = 3
_CONFIGURED = False


def configure_logging(
    *,
    level: int = logging.INFO,
    log_file: Path | str | None = None,
    console: bool = True,
) -> None:
    """Настраивает глобальное логирование, избегая повторной конфигурации."""

    global _CONFIGURED
    if _CONFIGURED:
        return

    root = logging.getLogger()
    root.setLevel(level)

    # Удаляем ранее добавленные обработчики, если они есть
    for handler in list(root.handlers):
        root.removeHandler(handler)

    if log_file:
        log_path = Path(log_file)
    else:
        log_path = Path(__file__).resolve().with_name(_LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=_MAX_BYTES,
        backupCount=_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root.addHandler(console_handler)

    _CONFIGURED = True


__all__ = ["configure_logging"]
