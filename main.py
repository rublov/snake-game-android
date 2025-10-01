"""
Main entry point for Android version
This file is required by python-for-android/buildozer
"""

import sys
import os

# Ensure the game directory is in the path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the game
if __name__ == '__main__':
    # Import the main game
    import importlib.util
    
    # Load Snake Game.py
    spec = importlib.util.spec_from_file_location("snake_game", "Snake Game.py")
    snake_game = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(snake_game)
