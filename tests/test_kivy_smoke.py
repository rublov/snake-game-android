import os

import pytest

os.environ.setdefault("KIVY_WINDOW", "mock")
os.environ.setdefault("KIVY_AUDIO", "mock")

kivy = pytest.importorskip("kivy")  # noqa: F401 - ensures import

from kivy.base import EventLoop  # noqa: E402
from kivy.clock import Clock  # noqa: E402

from snake_game.ui.kivy_app import SnakeApp  # noqa: E402


def test_snake_app_builds_and_stops():
    app = SnakeApp()
    EventLoop.ensure_window()

    def _stop_app(*_args):
        app.stop()

    Clock.schedule_once(_stop_app, 0)
    app.run()
