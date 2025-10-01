"""
Модуль адаптера pygame/pygame_sdl2 для совместимости с Android
"""

# Пытаемся импортировать pygame_sdl2 для Android
try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
    USING_SDL2 = True
    print("Используется pygame_sdl2 для Android")
except ImportError:
    USING_SDL2 = False
    print("pygame_sdl2 не найден, используется стандартный pygame")

# Импортируем pygame (возможно уже замененный на pygame_sdl2)
import pygame

# Константы для проверки платформы
try:
    import android
    from android.permissions import request_permissions, Permission
    ANDROID = True
    print("Запущено на Android платформе")
except ImportError:
    ANDROID = False
    android = None
    print("Запущено на десктоп-платформе")

def init_platform():
    """
    Инициализирует специфичные для платформы настройки
    """
    if ANDROID:
        try:
            # Запрашиваем необходимые разрешения на Android
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
            print("Разрешения Android запрошены")
            
            # Настраиваем отображение окна на Android
            if hasattr(pygame, 'display'):
                pygame.display.init()
                print(f"Доступные разрешения: {pygame.display.list_modes()}")
        except Exception as e:
            print(f"Ошибка при настройке Android: {e}")
    
    # Общая инициализация pygame
    pygame.init()
    return pygame

def get_platform_info():
    """
    Возвращает информацию о текущей платформе и используемом pygame
    """
    info = {
        "android": ANDROID,
        "using_sdl2": USING_SDL2,
        "pygame_version": pygame.version.ver,
        "sdl_version": pygame.version.SDL,
    }
    return info