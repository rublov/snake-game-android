"""Игровое ядро без привязки к графическому движку."""

from __future__ import annotations

import random
from dataclasses import dataclass

from .direction import Direction
from .events import GameStepEvent, GameStepResult
from .state import Point, SnakeGameConfig, SnakeGameState


@dataclass(slots=True)
class StepContext:
    """Вспомогательная структура для передачи параметров шага."""

    direction: Direction
    next_head: Point
    wrapped: bool = False


class SnakeGameEngine:
    """Движок змейки, управляющий состоянием и игровыми событиями."""

    def __init__(self, config: SnakeGameConfig) -> None:
        if config.cols <= 0 or config.rows <= 0:
            raise ValueError("Размер игрового поля должен быть положительным")
        self.config = config
        self._rng = random.Random(config.rng_seed)  # noqa: B311,S311  # nosec
        self.state = self._create_initial_state(config)

    # ------------------------------------------------------------------
    # Свойства и удобные геттеры
    # ------------------------------------------------------------------
    @property
    def tick_interval(self) -> float:
        """Интервал между обновлениями в секундах."""

        return 1.0 / self.state.speed if self.state.speed > 0 else 0.1

    @property
    def is_running(self) -> bool:
        return not self.state.paused and not self.state.game_over

    # ------------------------------------------------------------------
    # Управление игрой
    # ------------------------------------------------------------------
    def reset(
        self, *, cols: int | None = None, rows: int | None = None
    ) -> None:
        """Полностью перезапускает игру, опционально меняя размеры поля."""

        if cols is not None and rows is not None:
            self.config = self.config.with_board(cols, rows)
        self.state = self._create_initial_state(self.config)

    def resize(
        self, cols: int, rows: int, *, preserve_state: bool = False
    ) -> None:
        """Изменяет размеры поля. Можно сохранить текущее состояние."""

        if cols <= 0 or rows <= 0:
            raise ValueError("Размер поля должен быть положительным")

        self.config = self.config.with_board(cols, rows)
        if not preserve_state:
            self.state = self._create_initial_state(self.config)
            return

        # Обновляем текущее состояние, сохраняя змейку и счёт
        state = self.state
        state.cols = cols
        state.rows = rows
        state.cell_size = self.config.cell_size

        # Обрезаем сегменты, выходящие за границы
        clamped_snake: list[Point] = []
        for segment in state.snake:
            x = min(max(segment[0], 0), cols - 1)
            y = min(max(segment[1], 0), rows - 1)
            point = (x, y)
            if point not in clamped_snake:
                clamped_snake.append(point)
        if not clamped_snake:
            clamped_snake = self._initial_snake(cols, rows)
            state.score = 0
        state.snake = clamped_snake

        # Корректируем еду
        fx, fy = state.food
        if (
            not (0 <= fx < cols and 0 <= fy < rows)
            or state.food in state.snake
        ):
            self._spawn_food(state)

    def set_direction(self, direction: Direction) -> None:
        """Меняет направление движения, если оно допустимо."""

        state = self.state
        if direction == state.pending_direction:
            return
        if direction.is_opposite(state.direction) and len(state.snake) > 1:
            return
        state.pending_direction = direction

    def toggle_pause(self) -> None:
        self.state.paused = not self.state.paused

    def pause(self) -> None:
        self.state.paused = True

    def resume(self) -> None:
        if not self.state.game_over:
            self.state.paused = False

    # ------------------------------------------------------------------
    # Основной игровой цикл
    # ------------------------------------------------------------------
    def step(self) -> GameStepResult:
        """Делает один шаг игры и возвращает возникшие события."""

        state = self.state
        if state.game_over:
            return GameStepResult(frozenset(), needs_redraw=False)
        if state.paused:
            return GameStepResult(frozenset(), needs_redraw=False)

        state.direction = state.pending_direction
        ctx = self._build_step_context(state)
        events: set[GameStepEvent] = {GameStepEvent.MOVED}

        # Столкновение со стеной
        if not ctx.wrapped and not self._within_bounds(ctx.next_head, state):
            self._apply_game_over()
            events.add(GameStepEvent.GAME_OVER)
            return GameStepResult(frozenset(events))

        # Столкновение с собой
        if ctx.next_head in state.snake:
            self._apply_game_over()
            events.add(GameStepEvent.GAME_OVER)
            return GameStepResult(frozenset(events))

        state.snake.insert(0, ctx.next_head)

        if ctx.next_head == state.food:
            state.score += 1
            events.add(GameStepEvent.FOOD_EATEN)
            self._maybe_increase_speed(events)
            self._spawn_food(state)
        else:
            state.snake.pop()

        state.steps += 1
        return GameStepResult(frozenset(events))

    # ------------------------------------------------------------------
    # Внутренняя логика
    # ------------------------------------------------------------------
    def _create_initial_state(self, config: SnakeGameConfig) -> SnakeGameState:
        snake = self._initial_snake(config.cols, config.rows)
        direction = Direction.RIGHT
        food = self._random_empty_cell(config.cols, config.rows, snake)
        if food is None:
            msg = "Не удалось разместить еду на стартовом поле"
            raise RuntimeError(msg)
        return SnakeGameState(
            cols=config.cols,
            rows=config.rows,
            cell_size=config.cell_size,
            snake=snake,
            direction=direction,
            pending_direction=direction,
            food=food,
            score=0,
            speed=config.initial_speed,
            paused=False,
            game_over=False,
            steps=0,
            level_threshold=config.speed_increase_interval,
            speed_multiplier=1,
        )

    def _initial_snake(self, cols: int, rows: int) -> list[Point]:
        cx = max(cols // 2, 1)
        cy = max(rows // 2, 1)
        return [(cx, cy), (cx - 1, cy), (cx - 2, cy)]

    def _build_step_context(self, state: SnakeGameState) -> StepContext:
        head_x, head_y = state.head()
        dx = state.direction.dx
        dy = state.direction.dy
        next_x = head_x + dx
        next_y = head_y + dy
        wrapped = False

        if self.config.wrap_edges:
            next_x %= state.cols
            next_y %= state.rows
            wrapped = True

        return StepContext(
            direction=state.direction,
            next_head=(next_x, next_y),
            wrapped=wrapped,
        )

    def _within_bounds(self, point: Point, state: SnakeGameState) -> bool:
        x, y = point
        return 0 <= x < state.cols and 0 <= y < state.rows

    def _apply_game_over(self) -> None:
        self.state.game_over = True
        self.state.paused = False

    def _maybe_increase_speed(self, events: set[GameStepEvent]) -> None:
        state = self.state
        if state.score <= 0:
            return
        if state.score % self.config.speed_increase_interval != 0:
            return
        state.speed += self.config.speed_increment
        events.add(GameStepEvent.SPEED_CHANGED)
        state.speed_multiplier += 1

    def _spawn_food(self, state: SnakeGameState) -> None:
        food = self._random_empty_cell(state.cols, state.rows, state.snake)
        if food is None:
            self._apply_game_over()
            return
        state.food = food

    def _random_empty_cell(
        self, cols: int, rows: int, snake: list[Point]
    ) -> Point | None:
        free_cells = [
            (x, y)
            for x in range(cols)
            for y in range(rows)
            if (x, y) not in snake
        ]
        if not free_cells:
            return None
        return self._rng.choice(free_cells)
