"""
Main entry point for Android version
This file is required by python-for-android/buildozer
"""

import sys
import os

# Ensure the game directory is in the path
sys.path.insert(0, os.path.dirname(__file__))

# Определяем, работаем ли на Android
ANDROID = False
try:
    import android
    from android_utils import setup_android
    ANDROID = True
    print("Running on Android platform")
except ImportError:
    ANDROID = False
    android = None
    print("Running on desktop platform")

# Import and run the game
if __name__ == '__main__':
    # Настраиваем Android, если нужно
    if ANDROID:
        try:
            setup_android()
            print("Android setup completed")
        except Exception as e:
            print(f"Android setup error: {e}")
    
    # Import the main game
    import importlib.util
    
    # Load Snake Game.py
    spec = importlib.util.spec_from_file_location("snake_game", "Snake Game.py")
    snake_game = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(snake_game)
