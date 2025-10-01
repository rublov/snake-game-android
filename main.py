"""
Main entry point for Android version
This file is required by python-for-android/buildozer
"""

import sys
import os
import traceback

# Ensure the game directory is in the path
sys.path.insert(0, os.path.dirname(__file__))

# Инициализируем адаптер pygame для Android
try:
    from pygame_adapter import init_platform, ANDROID, get_platform_info
    
    # Инициализация pygame с учетом платформы
    pygame = init_platform()
    
    # Выводим информацию о платформе для отладки
    platform_info = get_platform_info()
    print(f"Информация о платформе: {platform_info}")
    
except Exception as e:
    print(f"Ошибка при инициализации адаптера pygame: {e}")
    traceback.print_exc()
    
    # Запасной вариант определения платформы
    ANDROID = False
    try:
        import android
        ANDROID = True
        print("Running on Android platform (fallback detection)")
    except ImportError:
        ANDROID = False
        print("Running on desktop platform (fallback detection)")

# Import and run the game
if __name__ == '__main__':
    try:
        # Import the main game
        import importlib.util
        
        # Load Snake Game.py
        snake_file = "Snake Game.py"
        print(f"Загрузка игры из файла: {snake_file}")
        
        spec = importlib.util.spec_from_file_location("snake_game", snake_file)
        snake_game = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(snake_game)
        print("Игра успешно запущена")
    except Exception as e:
        print(f"Ошибка при запуске игры: {e}")
        traceback.print_exc()
