"""Совместимый адаптер, использующий новое Kivy-приложение."""

from snake_game.ui import SnakeApp


def run_snake_game() -> None:
    """Запускает игру с помощью Kivy."""

    SnakeApp().run()


if __name__ == "__main__":
    run_snake_game()
