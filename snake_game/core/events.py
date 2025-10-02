"""Определения игровых событий, возникающих при обновлении состояния."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class GameStepEvent(Enum):
    """События, которые может породить одно обновление игры."""

    MOVED = auto()
    FOOD_EATEN = auto()
    SPEED_CHANGED = auto()
    GAME_OVER = auto()
    RESIZED = auto()


@dataclass(frozen=True, slots=True)
class GameStepResult:
    """Результат выполнения одного шага игрового движка."""

    events: frozenset[GameStepEvent] = field(default_factory=frozenset)
    needs_redraw: bool = True
