"""
Адаптер для игры Змейка с использованием Kivy вместо Pygame
Этот файл служит для преобразования игровой логики с Pygame на Kivy
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Line
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

import os
import random
import logging

# Константы игры
CELL_SIZE = 20
SNAKE_COLOR = (0.2, 0.7, 0.2, 1)  # RGBA
FOOD_COLOR = (0.8, 0.2, 0.2, 1)
BG_COLOR = (0.1, 0.1, 0.1, 1)
GRID_COLOR = (0.3, 0.3, 0.3, 1)

# Направления движения
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)



class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = int(Window.width // CELL_SIZE)
        self.rows = int(Window.height // CELL_SIZE)
        self.score = 0
        self.speed = 10  # начальная скорость (количество обновлений в секунду)
        self.game_over = False
        self.paused = False

        # Инициализация змейки (список координат)
        x = self.cols // 2
        y = self.rows // 2
        self.snake = [(x, y), (x - 1, y), (x - 2, y)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        
        # Создаем первую еду
        self.spawn_food()
        
        # Загрузка звуков
        self.sound_eat = self.load_sound("eat.mp3")
        self.sound_death = self.load_sound("death.mp3")
        self.sound_level_up = self.load_sound("level_up.mp3")
        
        # Настройка обновления игры
        interval = 1.0 / self.speed
        self.update_event = Clock.schedule_interval(self.update, interval)

        # Настройка управления с клавиатуры
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
    
    def load_sound(self, filename):
        """Загружает звуковой файл"""
        try:
            sound_path = os.path.join(os.path.dirname(__file__), filename)
            if os.path.exists(sound_path):
                return SoundLoader.load(sound_path)
            return None
        except Exception as e:
            logging.error(f"Ошибка загрузки звука {filename}: {e}")
            return None
    
    def _keyboard_closed(self):
        """Обработчик закрытия клавиатуры"""
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """Обработчик нажатия клавиш"""
        key = keycode[1]  # keycode это кортеж (код, имя_клавиши)
        
        # Управление змейкой
        if key == 'up' and self.direction != DOWN:
            self.next_direction = UP
        elif key == 'down' and self.direction != UP:
            self.next_direction = DOWN
        elif key == 'left' and self.direction != RIGHT:
            self.next_direction = LEFT
        elif key == 'right' and self.direction != LEFT:
            self.next_direction = RIGHT
        
        # Пауза по клавише P или Space
        elif key in ('p', 'spacebar'):
            self.toggle_pause()
        
        # Перезапуск игры по R
        elif key == 'r' and self.game_over:
            self.restart_game()
        
        return True
    
    def spawn_food(self):
        """Создает новую еду на поле"""
        # Создаем список всех возможных позиций, не занятых змейкой
        all_positions = [
            (x, y) for x in range(self.cols) for y in range(self.rows)
            if (x, y) not in self.snake
        ]
        if all_positions:
            # Выбираем случайную позицию из доступных
            self.food = random.choice(all_positions)
    
    def toggle_pause(self):
        """Переключает паузу в игре"""
        if not self.game_over:
            self.paused = not self.paused
    
    def restart_game(self):
        """Перезапускает игру"""
        x = self.cols // 2
        y = self.rows // 2
        self.snake = [(x, y), (x - 1, y), (x - 2, y)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.speed = 10
        self.game_over = False
        self.spawn_food()
        
        # Перезапуск таймера обновлений
        Clock.unschedule(self.update_event)
        self.update_event = Clock.schedule_interval(self.update, 1.0 / self.speed)
    
    def update(self, dt):
        """Обновляет состояние игры"""
        if self.game_over or self.paused:
            return
        
        # Обновляем направление
        self.direction = self.next_direction
        
        # Получаем координаты головы
        head_x, head_y = self.snake[0]
        
        # Вычисляем новую позицию головы
        dx, dy = self.direction
        new_x = head_x + dx
        new_y = head_y + dy
        
        # Проверяем столкновение с границами
        if new_x < 0 or new_x >= self.cols or new_y < 0 or new_y >= self.rows:
            self.end_game()
            return
        
        # Проверяем столкновение с самим собой
        if (new_x, new_y) in self.snake:
            self.end_game()
            return
        
        # Добавляем новую голову
        self.snake.insert(0, (new_x, new_y))
        
        # Проверяем, съела ли змейка еду
        if (new_x, new_y) == self.food:
            self.score += 1
            if self.sound_eat:
                self.sound_eat.play()
            
            # Увеличиваем скорость каждые 5 очков
            if self.score % 5 == 0:
                self.speed += 1
                Clock.unschedule(self.update_event)
                interval = 1.0 / self.speed
                self.update_event = Clock.schedule_interval(
                    self.update, interval
                )
                if self.sound_level_up:
                    self.sound_level_up.play()
            
            # Создаем новую еду
            self.spawn_food()
        else:
            # Если еда не съедена, удаляем последний элемент хвоста
            self.snake.pop()
        
        # Перерисовываем игру
        self.canvas.clear()
        self.draw_game()
    
    def end_game(self):
        """Обработка окончания игры"""
        self.game_over = True
        if self.sound_death:
            self.sound_death.play()
        Clock.unschedule(self.update_event)
    
    def draw_game(self):
        """Отрисовка игрового поля"""
        # Рисуем фон
        with self.canvas:
            Color(*BG_COLOR)
            Rectangle(pos=self.pos, size=self.size)
            
            # Рисуем сетку
            Color(*GRID_COLOR)
            for x in range(0, self.cols + 1):
                points = [x * CELL_SIZE, 0, x * CELL_SIZE, self.height]
                Line(points=points, width=1)
            for y in range(0, self.rows + 1):
                points = [0, y * CELL_SIZE, self.width, y * CELL_SIZE]
                Line(points=points, width=1)
            
            # Рисуем змейку
            Color(*SNAKE_COLOR)
            for segment in self.snake:
                x, y = segment
                Rectangle(pos=(x * CELL_SIZE, y * CELL_SIZE),
                          size=(CELL_SIZE, CELL_SIZE))
            
            # Рисуем еду
            Color(*FOOD_COLOR)
            x, y = self.food
            Rectangle(pos=(x * CELL_SIZE, y * CELL_SIZE),
                      size=(CELL_SIZE, CELL_SIZE))



class SnakeApp(App):
    def build(self):
        # Создаем основной макет
        layout = BoxLayout(orientation='vertical')

        # Добавляем статусную строку
        self.status_label = Label(
            text="Score: 0",
            size_hint=(1, 0.1),
            halign='center'
        )

        # Создаем игровое поле
        self.game = SnakeGame()

        # Обновляем статус каждую секунду
        Clock.schedule_interval(self.update_status, 0.1)

        # Добавляем все в макет
        layout.add_widget(self.status_label)
        layout.add_widget(self.game)

        return layout
    
    def update_status(self, dt):
        """Обновляет статусную строку"""
        status = f"Score: {self.game.score}"

        if self.game.game_over:
            status += " | GAME OVER! Press R to restart"
        elif self.game.paused:
            status += " | PAUSED"

        self.status_label.text = status


def run_snake_game():
    """Запускает игру Змейка на Kivy"""
    SnakeApp().run()


if __name__ == "__main__":
    run_snake_game()
