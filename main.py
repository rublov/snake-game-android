"""
Main entry point for Android version
This file is required by python-for-android/buildozer
"""

import sys
import os
import traceback
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Вывод логов в консоль
        logging.FileHandler('snake_game.log')  # Запись логов в файл
    ]
)

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
    logging.info("Запуск на платформе Android")
except ImportError:
    ANDROID = False
    logging.info("Запуск на десктоп-платформе")

# Import and run the game
if __name__ == '__main__':
    try:
        # Используем адаптер Kivy вместо Pygame
        from kivy_adapter import run_snake_game
        
        logging.info("Запуск игры Змейка через Kivy адаптер")
        run_snake_game()
        logging.info("Игра успешно запущена")
    except Exception as e:
        logging.error(f"Ошибка при запуске игры: {e}")
        traceback.print_exc()
        
        # В случае ошибки с Kivy, попробуем загрузить оригинальную игру
        try:
            logging.info("Попытка запустить оригинальную игру...")
            import importlib.util
            
            snake_file = "Snake Game.py"
            spec = importlib.util.spec_from_file_location(
                "snake_game", snake_file
            )
            snake_game = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(snake_game)
        except Exception as backup_error:
            logging.error(
                f"Не удалось запустить оригинальную игру: {backup_error}"
            )
            traceback.print_exc()
