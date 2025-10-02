"""Kivy-приложение, использующее чистое игровое ядро."""

from __future__ import annotations

import os

from kivy.app import App
from kivy.clock import Clock, ClockEvent
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from ..core import Direction, GameStepEvent, SnakeGameConfig
from ..services import SnakeSession, SoundManager

CELL_SIZE = 20
BG_COLOR = (0.1, 0.1, 0.1, 1)
GRID_COLOR = (0.3, 0.3, 0.3, 1)
SNAKE_COLOR = (0.2, 0.7, 0.2, 1)
FOOD_COLOR = (0.8, 0.2, 0.2, 1)
SOUND_FILES = {
    "eat": "eat.mp3",
    "death": "death.mp3",
    "level_up": "level_up.mp3",
}


class SnakeBoard(Widget):
    """Виджет игрового поля, отвечающий за отрисовку и ввод."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._cell_size = CELL_SIZE
        self._keyboard = None
        self._tick_event: ClockEvent | None = None

        sound_base = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..",
                "..",
                "assets",
            )
        )
        sound_manager = SoundManager(SoundLoader.load, sound_base)
        for alias, filename in SOUND_FILES.items():
            sound_manager.register(alias, filename)

        config = SnakeGameConfig(cols=10, rows=10, cell_size=self._cell_size)
        self.session = SnakeSession(config, sound_manager)

        self.bind(size=self._on_size_changed)
        self._bind_keyboard()
        self._schedule_tick()
        Clock.schedule_once(lambda *_: self._resize_to_widget(), 0)

    # ------------------------------------------------------------------
    # Системные хуки
    # ------------------------------------------------------------------
    def _bind_keyboard(self) -> None:
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        if self._keyboard:
            self._keyboard.bind(on_key_down=self._on_key_down)

    def _keyboard_closed(self) -> None:
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_key_down)
            self._keyboard = None

    def _on_key_down(self, _keyboard, keycode, _text, _modifiers) -> bool:
        key = keycode[1]
        mapping = {
            "up": Direction.UP,
            "down": Direction.DOWN,
            "left": Direction.LEFT,
            "right": Direction.RIGHT,
        }
        if key in mapping:
            self.session.set_direction(mapping[key])
            return True
        if key in ("p", "spacebar"):
            self.toggle_pause()
            return True
        if key == "r":
            self.restart()
            return True
        return False

    def _on_size_changed(self, *_args) -> None:
        self._resize_to_widget()

    # ------------------------------------------------------------------
    # Игровой цикл
    # ------------------------------------------------------------------
    def _schedule_tick(self) -> None:
        self._cancel_tick()
        interval = max(self.session.tick_interval, 1 / 60)
        self._tick_event = Clock.schedule_interval(self._on_tick, interval)

    def _cancel_tick(self) -> None:
        if self._tick_event is not None:
            self._tick_event.cancel()
            self._tick_event = None

    def _on_tick(self, _dt) -> None:
        result = self.session.step()
        if GameStepEvent.SPEED_CHANGED in result.events:
            self._schedule_tick()
        if GameStepEvent.GAME_OVER in result.events:
            self._cancel_tick()
        if result.needs_redraw or result.events:
            self._redraw()

    # ------------------------------------------------------------------
    # Управление состоянием
    # ------------------------------------------------------------------
    def toggle_pause(self) -> None:
        self.session.toggle_pause()
        if self.session.state.paused:
            self._cancel_tick()
        else:
            self._schedule_tick()
        self._redraw()

    def restart(self) -> None:
        self.session.restart()
        self._schedule_tick()
        self._redraw()

    def _resize_to_widget(self) -> None:
        if self.width <= 0 or self.height <= 0:
            return
        cols = max(int(self.width // self._cell_size), 5)
        rows = max(int(self.height // self._cell_size), 5)
        self.session.resize_board(cols, rows)
        self._redraw()

    # ------------------------------------------------------------------
    # Отрисовка
    # ------------------------------------------------------------------
    def _redraw(self) -> None:
        state = self.session.state
        self.canvas.clear()
        with self.canvas:
            Color(*BG_COLOR)
            Rectangle(pos=self.pos, size=self.size)

            Color(*GRID_COLOR)
            for x in range(0, state.cols + 1):
                x_pos = self.x + x * self._cell_size
                Line(
                    points=[
                        x_pos,
                        self.y,
                        x_pos,
                        self.y + state.rows * self._cell_size,
                    ],
                    width=1,
                )
            for y in range(0, state.rows + 1):
                y_pos = self.y + y * self._cell_size
                Line(
                    points=[
                        self.x,
                        y_pos,
                        self.x + state.cols * self._cell_size,
                        y_pos,
                    ],
                    width=1,
                )

            Color(*SNAKE_COLOR)
            for segment in state.snake:
                sx, sy = segment
                Rectangle(
                    pos=(
                        self.x + sx * self._cell_size,
                        self.y + sy * self._cell_size,
                    ),
                    size=(self._cell_size, self._cell_size),
                )

            Color(*FOOD_COLOR)
            fx, fy = state.food
            Rectangle(
                pos=(
                    self.x + fx * self._cell_size,
                    self.y + fy * self._cell_size,
                ),
                size=(self._cell_size, self._cell_size),
            )


class SnakeApp(App):
    """Основное Kivy-приложение."""

    def build(self):  # type: ignore[override]
        root = BoxLayout(orientation="vertical")
        self.status_label = Label(text="Score: 0", size_hint=(1, 0.1))
        self.board = SnakeBoard(size_hint=(1, 0.9))

        root.add_widget(self.status_label)
        root.add_widget(self.board)

        Clock.schedule_interval(self._update_status, 0.1)
        return root

    def _update_status(self, _dt) -> None:
        state = self.board.session.state
        status = f"Score: {state.score}"
        if state.game_over:
            status += " | GAME OVER (R to restart)"
        elif state.paused:
            status += " | PAUSED"
        self.status_label.text = status


def run_app() -> None:
    SnakeApp().run()


__all__ = ["SnakeApp", "SnakeBoard", "run_app"]
