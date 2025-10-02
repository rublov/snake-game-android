"""Структуры данных для ядра игры."""

from __future__ import annotations

from dataclasses import dataclass

from .direction import Direction

Point = tuple[int, int]
SnakeBody = list[Point]


@dataclass(slots=True)
class SnakeGameConfig:
    """Конфигурация игрового поля и параметров сложности."""

    cols: int
    rows: int
    cell_size: int = 20
    initial_speed: float = 10.0
    speed_increment: float = 1.0
    speed_increase_interval: int = 5
    wrap_edges: bool = False
    rng_seed: int | None = None

    def with_board(self, cols: int, rows: int) -> SnakeGameConfig:
        return SnakeGameConfig(
            cols=cols,
            rows=rows,
            cell_size=self.cell_size,
            initial_speed=self.initial_speed,
            speed_increment=self.speed_increment,
            speed_increase_interval=self.speed_increase_interval,
            wrap_edges=self.wrap_edges,
            rng_seed=self.rng_seed,
        )


@dataclass(slots=True)
class SnakeGameState:
    """Текущее состояние игры."""

    cols: int
    rows: int
    cell_size: int
    snake: SnakeBody
    direction: Direction
    pending_direction: Direction
    food: Point
    score: int = 0
    speed: float = 10.0
    paused: bool = False
    game_over: bool = False
    steps: int = 0
    level_threshold: int = 5
    speed_multiplier: int = 1

    def head(self) -> Point:
        return self.snake[0]

    def copy(self) -> SnakeGameState:
        return SnakeGameState(
            cols=self.cols,
            rows=self.rows,
            cell_size=self.cell_size,
            snake=[(x, y) for (x, y) in self.snake],
            direction=self.direction,
            pending_direction=self.pending_direction,
            food=self.food,
            score=self.score,
            speed=self.speed,
            paused=self.paused,
            game_over=self.game_over,
            steps=self.steps,
            level_threshold=self.level_threshold,
            speed_multiplier=self.speed_multiplier,
        )
