"""Определения направлений движения змейки."""

from __future__ import annotations

from enum import Enum


class Direction(Enum):
    """Кардинальные направления движения змейки."""

    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]

    def is_opposite(self, other: Direction) -> bool:
        """Возвращает True, если направление противоположно другому."""

        return self.dx + other.dx == 0 and self.dy + other.dy == 0

    @classmethod
    def from_tuple(cls, value: tuple[int, int]) -> Direction:
        """Создаёт направление из вектора (dx, dy)."""

        for direction in cls:
            if direction.value == value:
                return direction
        raise ValueError(f"Неизвестное направление: {value}")
