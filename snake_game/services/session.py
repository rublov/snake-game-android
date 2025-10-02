"""Высокоуровневое управление игровой сессией."""

from __future__ import annotations

from dataclasses import replace

from ..core import (
    Direction,
    GameStepEvent,
    GameStepResult,
    SnakeGameConfig,
    SnakeGameEngine,
    SnakeGameState,
)
from .audio import SoundManager


class SnakeSession:
    """Обёртка над игровым движком с учетом внешних сервисов."""

    def __init__(
        self,
        config: SnakeGameConfig,
        sound_manager: SoundManager | None = None,
    ) -> None:
        self._config = config
        self._engine = SnakeGameEngine(config)
        self._sound_manager = sound_manager

    # ------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------
    @property
    def engine(self) -> SnakeGameEngine:
        return self._engine

    @property
    def state(self) -> SnakeGameState:
        return self._engine.state

    @property
    def tick_interval(self) -> float:
        return self._engine.tick_interval

    # ------------------------------------------------------------------
    # Игровой цикл
    # ------------------------------------------------------------------
    def step(self) -> GameStepResult:
        result = self._engine.step()
        self._handle_events(result)
        return result

    # ------------------------------------------------------------------
    # Управление состоянием
    # ------------------------------------------------------------------
    def set_direction(self, direction: Direction) -> None:
        self._engine.set_direction(direction)

    def toggle_pause(self) -> None:
        self._engine.toggle_pause()

    def restart(self) -> None:
        self._engine.reset()

    def resize_board(self, cols: int, rows: int) -> None:
        previous_state = replace(self.state)
        self._engine.resize(cols, rows, preserve_state=True)
        if (
            previous_state.cols != self.state.cols
            or previous_state.rows != self.state.rows
        ):
            self._engine.state.steps = 0

    # ------------------------------------------------------------------
    # События
    # ------------------------------------------------------------------
    def _handle_events(self, result: GameStepResult) -> None:
        if not self._sound_manager:
            return
        if GameStepEvent.FOOD_EATEN in result.events:
            self._sound_manager.play("eat")
        if GameStepEvent.SPEED_CHANGED in result.events:
            self._sound_manager.play("level_up")
        if GameStepEvent.GAME_OVER in result.events:
            self._sound_manager.play("death")


__all__ = ["SnakeSession"]
