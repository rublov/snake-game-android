"""
Main entry point for Android version
This file is required by python-for-android/buildozer
"""

import logging
import os
import sys

from logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

# Ensure the game directory is in the path
sys.path.insert(0, os.path.dirname(__file__))

# Определяем, работаем ли на Android
ANDROID = False
try:
    # Пробуем импортировать android модуль
    # Питон-линтер показывает ошибку, но на андроиде он доступен
    # Поэтому приглушаем ошибку импорта следующей строкой
    import android  # noqa: F401
    ANDROID = True
    logger.info("Запуск на платформе Android")
except ImportError:
    ANDROID = False
    logger.info("Запуск на десктоп-платформе")

# Import and run the game
if __name__ == "__main__":
    try:
        # Используем адаптер Kivy вместо Pygame
        from kivy_adapter import run_snake_game

        logger.info("Запуск игры Змейка через Kivy адаптер")
        run_snake_game()
        logger.info("Игра успешно запущена")
    except Exception:  # pragma: no cover - зависит от окружения
        logger.exception("Ошибка при запуске Kivy-версии")

        # В случае ошибки с Kivy, попробуем загрузить оригинальную игру
        try:
            logger.info("Попытка запустить оригинальную игру...")
            import importlib.util

            snake_file = "Snake Game.py"
            spec = importlib.util.spec_from_file_location(
                "snake_game", snake_file
            )
            if spec and spec.loader:
                snake_game = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(snake_game)
                logger.info("Оригинальная игра запущена")
            else:  # pragma: no cover
                raise RuntimeError("Не удалось загрузить модуль Snake Game")
        except Exception:
            logger.exception("Не удалось запустить оригинальную игру")
            raise
