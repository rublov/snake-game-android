import pytest

from snake_game.core import (
    Direction,
    GameStepEvent,
    SnakeGameConfig,
    SnakeGameEngine,
)


@pytest.fixture()
def engine():
    config = SnakeGameConfig(cols=10, rows=10, cell_size=20)
    return SnakeGameEngine(config)


def test_step_moves_snake_forward(engine):
    start_head = engine.state.head()
    result = engine.step()

    assert engine.state.head() == (start_head[0] + 1, start_head[1])
    assert GameStepEvent.MOVED in result.events


def test_eating_food_increases_score_and_length(engine):
    head_x, head_y = engine.state.head()
    engine.state.food = (head_x + 1, head_y)

    previous_length = len(engine.state.snake)
    result = engine.step()

    assert engine.state.score == 1
    assert len(engine.state.snake) == previous_length + 1
    assert GameStepEvent.FOOD_EATEN in result.events


def test_collision_with_wall_triggers_game_over(engine):
    engine.state.snake = [(engine.state.cols - 1, engine.state.rows // 2)]
    engine.state.pending_direction = Direction.RIGHT
    engine.state.direction = Direction.RIGHT

    result = engine.step()

    assert engine.state.game_over is True
    assert GameStepEvent.GAME_OVER in result.events
