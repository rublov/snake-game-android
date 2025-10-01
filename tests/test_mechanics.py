import importlib.util
import os
from pathlib import Path
import unittest
from unittest import mock


os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ['SNAKE_GAME_SKIP_LOOP'] = '1'

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = PROJECT_ROOT / 'Snake Game.py'
SPEC = importlib.util.spec_from_file_location('snake_game', MODULE_PATH)
snake_game = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(snake_game)


class GameMechanicsTests(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        snake_game.pygame.quit()

    def setUp(self):
        self.game = snake_game
        self.state = {
            'mode': self.game.mode,
            'level': self.game.level,
            'score': self.game.score,
            'speed_boost_on_food': self.game.speed_boost_on_food,
            'speed_boost_active_until': self.game.speed_boost_active_until,
            'invincible_until': self.game.invincible_until,
            'snake_body': [segment[:] for segment in self.game.snake_body],
            'walls': list(self.game.walls),
            'moving_walls': [dict(item) for item in self.game.moving_walls],
            'wrap_edges': self.game.wrap_edges,
            'food_type': self.game.food_type,
            'current_food_color': self.game.current_food_color,
            'current_food_value': self.game.current_food_value,
            'current_food_effect': self.game.current_food_effect,
        }

    def tearDown(self):
        self.game.mode = self.state['mode']
        self.game.level = self.state['level']
        self.game.score = self.state['score']
        self.game.speed_boost_on_food = self.state['speed_boost_on_food']
        self.game.speed_boost_active_until = (
            self.state['speed_boost_active_until']
        )
        self.game.invincible_until = self.state['invincible_until']
        self.game.snake_body = [
            segment[:] for segment in self.state['snake_body']
        ]
        self.game.walls = list(self.state['walls'])
        self.game.moving_walls = [
            dict(item) for item in self.state['moving_walls']
        ]
        self.game.wrap_edges = self.state['wrap_edges']
        self.game.food_type = self.state['food_type']
        self.game.current_food_color = self.state['current_food_color']
        self.game.current_food_value = self.state['current_food_value']
        self.game.current_food_effect = self.state['current_food_effect']

    def test_choose_food_type_speed_boost_override(self):
        self.game.speed_boost_on_food = True
        self.game.mode = 'map'
        result = self.game.choose_food_type()
        self.assertEqual(result, 'speed')

    def test_choose_food_type_mvp_only_normal(self):
        self.game.speed_boost_on_food = False
        self.game.mode = 'mvp'
        self.game.level = 7
        self.game.score = 120
        with mock.patch.object(self.game.rng, 'random', return_value=0.0):
            result = self.game.choose_food_type()
        self.assertEqual(result, 'normal')

    def test_choose_food_type_mvp2_only_normal_even_with_boost(self):
        self.game.speed_boost_on_food = True
        self.game.mode = 'mvp2'
        self.game.level = 12
        self.game.score = 200
        result = self.game.choose_food_type()
        self.assertEqual(result, 'normal')

    def test_choose_food_type_map_bonus_preference(self):
        self.game.speed_boost_on_food = False
        self.game.mode = 'map'
        self.game.level = 6
        self.game.score = 90
        with mock.patch.object(self.game.rng, 'random', return_value=0.0):
            result = self.game.choose_food_type()
        self.assertEqual(result, 'bonus')

    def test_choose_food_type_survival_shield_priority(self):
        custom_config = {
            'bonus': {'base': 0.05, 'level': 0.0, 'score': 0.0, 'cap': 1.0},
            'shield': {'base': 0.5, 'level': 0.0, 'score': 0.0, 'cap': 1.0},
            'speed': {'base': 0.0, 'level': 0.0, 'score': 0.0, 'cap': 1.0},
            'max_total': 1.0,
        }
        with mock.patch.dict(
            self.game.MODE_FOOD_CONFIG,
            {'survival': custom_config},
            clear=False,
        ):
            self.game.speed_boost_on_food = False
            self.game.mode = 'survival'
            self.game.level = 1
            self.game.score = 0
            with mock.patch.object(self.game.rng, 'random', return_value=0.3):
                result = self.game.choose_food_type()
        self.assertEqual(result, 'shield')

    def test_spawn_food_force_type_applies_effect(self):
        self.game.speed_boost_on_food = False
        self.game.snake_body = []
        self.game.walls = []
        self.game.moving_walls = []
        with mock.patch.object(self.game.rng, 'randrange', side_effect=[5, 6]):
            self.game.spawn_food(force_type='shield')
        self.assertEqual(self.game.food_type, 'shield')
        self.assertEqual(self.game.current_food_effect, 'shield')
        self.assertEqual(
            self.game.current_food_color,
            self.game.FOOD_TYPE_CONFIG['shield']['color'],
        )
        self.assertEqual(self.game.food_pos, [50, 60])

    def test_load_level_map_features(self):
        self.game.mode = 'map'
        self.game.load_level(5)
        self.assertTrue(self.game.wrap_edges)
        self.assertGreater(len(self.game.walls), 0)

    def test_load_level_survival_clears_walls(self):
        self.game.mode = 'survival'
        self.game.load_level(2)
        self.assertFalse(self.game.walls)
        self.assertFalse(self.game.moving_walls)
        self.assertFalse(self.game.wrap_edges)


if __name__ == '__main__':
    unittest.main()
