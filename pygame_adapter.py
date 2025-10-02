"""Модуль адаптера pygame/pygame_sdl2 для совместимости с Android."""

from __future__ import annotations

import logging
from collections.abc import Sequence

logger = logging.getLogger(__name__)

try:  # noqa: SIM105 - привязка для платформенных зависимостей
    import android  # type: ignore[import-not-found]
    from android.permissions import (  # type: ignore[import-not-found]
        Permission,
        request_permissions,
    )
except ImportError:  # pragma: no cover - выполняется вне Android
    android = None
    Permission = None  # type: ignore[assignment]
    request_permissions = None  # type: ignore[assignment]

ANDROID = android is not None

try:
    import pygame_sdl2
except ImportError:
    pygame_sdl2 = None


if pygame_sdl2 is not None:
    pygame_sdl2.import_as_pygame()
    USING_SDL2 = True
    logger.info("Используется pygame_sdl2 для Android")
else:
    USING_SDL2 = False
    logger.info("pygame_sdl2 не найден, используется стандартный pygame")

import pygame  # noqa: E402


def _request_android_permissions(permissions: Sequence[object]) -> None:
    if request_permissions is None:
        logger.debug("Пропуск запроса прав: функция недоступна")

        return

    try:
        request_permissions(list(permissions))
        logger.info("Разрешения Android запрошены")
    except Exception as exc:  # noqa: BLE001 - логируем любые ошибки платформы
        logger.exception("Ошибка при запросе Android-разрешений: %s", exc)


def init_platform() -> pygame.module:
    """Инициализирует специфичные для платформы настройки."""
    if ANDROID:
        _request_android_permissions(
            [
                Permission.WRITE_EXTERNAL_STORAGE if Permission else None,
                Permission.READ_EXTERNAL_STORAGE if Permission else None,
            ]
        )

        if hasattr(pygame, "display"):
            pygame.display.init()

            logger.debug(
                "Доступные разрешения: %s",
                pygame.display.list_modes(),
            )

    pygame.init()
    return pygame


def get_platform_info() -> dict[str, object]:
    """Возвращает информацию о текущей платформе и используемом pygame."""
    return {
        "android": ANDROID,
        "using_sdl2": USING_SDL2,
        "pygame_version": pygame.version.ver,
        "sdl_version": pygame.version.SDL,
    }
