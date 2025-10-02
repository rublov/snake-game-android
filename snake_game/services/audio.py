"""Примитивный менеджер звуков с ленивой загрузкой."""

from __future__ import annotations

import logging
import os
from collections.abc import Callable
from typing import Protocol, runtime_checkable


@runtime_checkable
class SoundHandle(Protocol):
    def play(self) -> object:  # pragma: no cover - зависимость от движка
        ...

    def stop(self) -> object:  # pragma: no cover
        ...


SoundLoaderFunc = Callable[[str], SoundHandle | None]


class SoundManager:
    """Менеджер звуков, независимый от конкретного движка."""

    def __init__(self, loader: SoundLoaderFunc, base_path: str) -> None:
        self._loader = loader
        self._base_path = base_path
        self._cache: dict[str, SoundHandle | None] = {}
        self._aliases: dict[str, str] = {}

    def register(self, alias: str, filename: str) -> None:
        """Регистрирует читабельное имя для файла."""

        self._aliases[alias] = filename

    def play(self, alias: str) -> None:
        sound = self._load(alias)
        if sound is not None:
            try:
                sound.stop()
                sound.play()
            except Exception as exc:  # pragma: no cover - зависит от платформы
                logging.getLogger(__name__).warning(
                    "Не удалось воспроизвести звук %s: %s", alias, exc
                )

    def stop(self, alias: str) -> None:
        sound = self._cache.get(alias)
        if sound is not None:
            try:
                sound.stop()
            except Exception as exc:  # pragma: no cover
                logging.getLogger(__name__).warning(
                    "Не удалось остановить звук %s: %s", alias, exc
                )

    def _resolve_path(self, alias: str) -> str | None:
        filename = self._aliases.get(alias, alias)
        candidate = os.path.join(self._base_path, filename)
        if os.path.exists(candidate):
            return candidate
        return None

    def _load(self, alias: str) -> SoundHandle | None:
        if alias in self._cache:
            return self._cache[alias]
        path = self._resolve_path(alias)
        if not path:
            self._cache[alias] = None
            return None
        try:
            sound = self._loader(path)
        except Exception:  # pragma: no cover
            sound = None
        self._cache[alias] = sound
        return sound
