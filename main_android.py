"""
Android Entry Point - GUARANTEED APK BUILD
Этот файл является entry point для Android сборки через Buildozer.
Оптимизирован для стабильной сборки APK.
"""

import logging
import os
import sys

# Настройка логирования для Android
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Определяем платформу
ANDROID = False
try:
    import android  # noqa: F401
    ANDROID = True
    logger.info("🤖 Запуск на Android платформе")
except ImportError:
    ANDROID = False
    logger.info("💻 Запуск на Desktop платформе")

# Убеждаемся, что путь к игре в sys.path
game_dir = os.path.dirname(os.path.abspath(__file__))
if game_dir not in sys.path:
    sys.path.insert(0, game_dir)


def main():
    """Главная функция запуска игры"""
    try:
        logger.info("🎮 Загрузка Snake Game через Kivy...")
        
        # Импортируем Kivy-версию игры
        from snake_game.ui.kivy_app import SnakeApp
        
        logger.info("✅ Модули загружены успешно")
        
        # Запускаем Kivy приложение
        app = SnakeApp()
        logger.info("🚀 Запуск приложения...")
        app.run()
        
        logger.info("✅ Приложение завершено корректно")
        
    except ImportError as e:
        logger.error(f"❌ Ошибка импорта: {e}")
        logger.error(
            "💡 Проверьте установку зависимостей в buildozer.spec"
        )
        raise
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
