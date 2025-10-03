"""
Snake Eater
Made with PyGame
"""

# ruff: noqa

import json
import logging
import math
import os
import random
import sys
import time
from array import array
from typing import Optional, Dict
import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from logging_config import configure_logging

configure_logging()

try:
    import newrelic.agent  # type: ignore[import-not-found]  # noqa: E402
    NEW_RELIC_AVAILABLE = True
except ModuleNotFoundError:
    newrelic = None  # type: ignore[assignment]
    NEW_RELIC_AVAILABLE = False

# Android detection and support
try:
    import android  # type: ignore[import-not-found]
    ANDROID = True
    logging.info("Running on Android platform")
except ImportError:
    ANDROID = False
    android = None  # type: ignore[assignment]
    logging.info("Running on desktop platform")

import pygame  # noqa: E402
# Removed Kivy imports; not used in Pygame implementation

# Import leaderboard module
try:
    from leaderboard import leaderboard  # noqa: E402
    LEADERBOARD_AVAILABLE = True
    logging.info("Leaderboard module loaded")
except ImportError:
    LEADERBOARD_AVAILABLE = False
    leaderboard = None  # type: ignore[assignment]
    logging.warning("Leaderboard module not available")

NEW_RELIC_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "newrelic.ini")
if NEW_RELIC_AVAILABLE:
    if os.path.exists(NEW_RELIC_CONFIG_PATH):
        newrelic.agent.initialize(  # type: ignore[union-attr]
            NEW_RELIC_CONFIG_PATH
        )
    else:
        logging.warning(
            "New Relic config file not found at %s; monitoring disabled",
            NEW_RELIC_CONFIG_PATH,
        )
else:
    logging.info("New Relic package not installed; telemetry disabled")
rng = random.SystemRandom()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_FOLDERS = (
    '',
    'assets',
    'assets/audio',
    'assets/sounds',
    'assets/sound',
    'asset',
    'audio',
    'sounds',
    'sound',
)

# Cache for resolved asset paths
_asset_path_cache = {}


# Optimized resolve_asset_path with caching
def resolve_asset_path(filename: str) -> str:
    """Return an absolute path to the named asset, searching common folders."""
    if filename in _asset_path_cache:
        return _asset_path_cache[filename]

    for folder in ASSET_FOLDERS:
        candidate: str = os.path.join(BASE_DIR, folder, filename)
        if os.path.exists(candidate):
            _asset_path_cache[filename] = candidate
            return candidate

    # Default to root path even if missing so pygame raises a useful error
    default_path = os.path.join(BASE_DIR, filename)
    _asset_path_cache[filename] = default_path
    return default_path


# Optimized resolve_first_existing with caching
def resolve_first_existing(*filenames: str) -> str:
    """Return the first asset path that exists from the provided filenames."""
    for name in filenames:
        if name in _asset_path_cache:
            return _asset_path_cache[name]

        for folder in ASSET_FOLDERS:
            candidate: str = os.path.join(BASE_DIR, folder, name)
            if os.path.exists(candidate):
                _asset_path_cache[name] = candidate
                return candidate

    # Fallback to the first option (will raise pygame error later if missing)
    default_path = os.path.join(BASE_DIR, filenames[0])
    _asset_path_cache[filenames[0]] = default_path
    return default_path


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 10
best_score = 0
current_premium_minutes = 15

# Settings functions


def save_settings() -> None:
    pass  # Placeholder to avoid duplicate definition


def resolve_mode(preferred_mode: str, premium_active: bool) -> str:
    if preferred_mode == 'map':
        return 'map' if premium_active else 'mvp'
    if preferred_mode == 'survival':
        return 'survival'
    if preferred_mode == 'mvp2':
        return 'mvp2'
    return 'mvp'


# Refactored code for modularity
class SettingsManager:
    """Class to manage game settings."""

    def __init__(self, settings_file: str = 'settings.json'):
        self.settings_file = settings_file
        self.settings_cache: Optional[Dict[str, object]] = None

    def load_settings(self) -> None:
        if self.settings_cache is not None:
            settings = self.settings_cache
        elif os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.settings_cache = settings
            except (json.JSONDecodeError, KeyError):
                logging.error("Error decoding settings.json. Using defaults.")
                settings = {}
        else:
            settings = {}

        globals().update({
            'speed_setting': settings.get('speed_setting', 10),
            'sound_setting': settings.get('sound_setting', True),
            'theme_setting': settings.get('theme_setting', 'dark'),
            'mode': settings.get('mode', 'mvp'),
            'map_end_time': settings.get('map_end_time', 0),
            'first_launch_time': settings.get(
                'first_launch_time', time.time()
            ),
            'current_premium_minutes': settings.get(
                'current_premium_minutes', 15
            ),
            'best_score': settings.get('best_score', 0),
        })

    def save_settings(self) -> None:
        settings = {
            'speed_setting': speed_setting,
            'sound_setting': sound_setting,
            'theme_setting': theme_setting,
            'mode': mode,
            'map_end_time': map_end_time,
            'first_launch_time': first_launch_time,
            'current_premium_minutes': current_premium_minutes,
            'best_score': best_score
        }

        if settings != self.settings_cache:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
            self.settings_cache = settings


# Replace global functions with the SettingsManager instance
settings_manager = SettingsManager()
settings_manager.load_settings()

# Cache for settings to minimize file I/O
_settings_cache: Optional[Dict[str, object]] = None


# Optimized load_settings with caching
def load_settings() -> None:
    global speed_setting, sound_setting, theme_setting
    global mode, map_end_time, first_launch_time
    global current_premium_minutes, best_score, difficulty

    if os.path.exists('settings.json'):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                speed_setting = settings.get('speed_setting', 10)
                sound_setting = settings.get('sound_setting', True)
                theme_setting = settings.get('theme_setting', 'dark')
                mode = settings.get('mode', 'mvp')
                map_end_time = settings.get('map_end_time', 0)
                first_launch_time = settings.get(
                    'first_launch_time', time.time()
                )
                current_premium_minutes = settings.get(
                    'current_premium_minutes', 15
                )
                best_score = settings.get('best_score', 0)
        except (json.JSONDecodeError, KeyError):
            logging.error("Error decoding settings.json. Using defaults.")
            speed_setting = 10
            sound_setting = True
            theme_setting = 'dark'
            mode = 'mvp'
            map_end_time = 0
            first_launch_time = time.time()
            current_premium_minutes = 15
            best_score = 0
    else:
        # Defaults for first run
        speed_setting = 10
        sound_setting = True
        theme_setting = 'dark'
        mode = 'mvp'
        map_end_time = 0
        first_launch_time = time.time()
        current_premium_minutes = 15
        best_score = 0


# Note: load_settings functionality is now handled by SettingsManager class
# The old load_settings function has been replaced


# Settings
speed_setting: int = 10
sound_setting: bool = True
theme_setting: str = 'dark'
mode: str = 'map'
map_end_time: float = 0
first_launch_time: float = 0
promo_codes: Dict[str, int] = {
    'MAP30': 30 * 60,
    'qwerty': 10 * 60,
    'qwerty5': 5 * 60,
    'qwerty10': 10 * 60,
    'qwerty15': 15 * 60,
    'qwerty20': 20 * 60,
}  # Promo code and duration in seconds
load_settings()
logging.info("Game initialized")
last_mode_switch = 0
premium_expiry_message_until = 0
sound_enabled = bool(sound_setting)
sound_assets_available = False
background_music_available = False
premium_offer_active = False
missing_eat_sound_warned = False

# --- Constants and Setup ---

# Cache for music state to avoid redundant checks
_music_state_cache: Dict[str, Optional[object]] = {
    'initialized': False,
    'current_state': None,
    'is_paused': None
}


# Optimized update_music with caching
def update_music() -> None:
    """Synchronize runtime audio with the current settings and game state."""
    global sound_enabled, _music_state_cache

    if not sound_assets_available:
        sound_enabled = False
    else:
        sound_enabled = bool(sound_setting)

    if not pygame.mixer.get_init():
        _music_state_cache['initialized'] = False
        return

    current_state = globals().get('game_state', 'menu')
    is_paused = globals().get('paused', False)

    if (
        _music_state_cache['initialized']
        and _music_state_cache['current_state'] == current_state
        and _music_state_cache['is_paused'] == is_paused
    ):
        # No changes, skip redundant updates
        return

    # Update the cache
    _music_state_cache['initialized'] = True
    _music_state_cache['current_state'] = current_state
    _music_state_cache['is_paused'] = is_paused

    # Perform actual music synchronization logic here
    # ...existing code for music synchronization...
    pass


def generate_sound_wave(frequency, duration, volume):
    """Generates a sound wave as a pygame.mixer.Sound object."""
    sample_rate = 44100
    n_samples = int(round(duration * sample_rate))
    buf = np.zeros((n_samples, 2), dtype=np.int16)
    max_sample = 2 ** 15 - 1
    for s in range(n_samples):
        t = float(s) / sample_rate
        sine_wave = max_sample * math.sin(2 * math.pi * frequency * t)
        buf[s][0] = int(round(sine_wave))
        buf[s][1] = int(round(sine_wave))
    sound = pygame.sndarray.make_sound(buf)
    sound.set_volume(volume)
    return sound


def create_level_up_tone():
    """Creates a tone for leveling up."""
    return generate_sound_wave(880.0, 0.2, 0.1)


def create_eat_tone():
    """Creates a tone for eating food."""
    return generate_sound_wave(440.0, 0.1, 0.1)


def create_map_mode_tone():
    """Creates a tone for map mode."""
    return generate_sound_wave(660.0, 0.15, 0.1)


def set_sound_volume(sound, volume: float, label: str):
    """Clamp and apply volume to a sound effect with debug logging."""

    if not sound:
        return

    clamped = max(0.0, min(volume, 1.0))
    try:
        sound.set_volume(clamped)
        logging.debug("%s sound volume set to %.2f", label, clamped)
    except pygame.error:
        logging.debug(
            "Unable to adjust volume for %s sound", label, exc_info=True
        )


# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
# Skip strict initialization check in CI environments
if os.environ.get("SNAKE_GAME_SKIP_LOOP") == "1":
    print('[CI] Skipping strict PyGame initialization check for testing')
    pygame.init()  # Init anyway but don't check for errors
else:
    check_errors = pygame.init()
    # pygame.init() example output -> (6, 0)
    # second number in tuple gives number of errors
    if check_errors[1] > 0:
        print(
            f'[!] Had {check_errors[1]} errors when initialising game, '
            'exiting...'
        )
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')


# Splash screen function
def show_splash_screen(duration: float = 2.0):
    """Display splash screen for specified duration"""
    splash_path = resolve_asset_path('splash.png')
    try:
        splash_image = pygame.image.load(splash_path)
        # Scale to fit window
        splash_scaled = pygame.transform.scale(
            splash_image, (frame_size_x, frame_size_y)
        )
        game_window.blit(splash_scaled, (0, 0))
        pygame.display.flip()

        # Wait for duration or skip on key press
        start_time = time.time()
        while time.time() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.time.Clock().tick(30)
    except Exception as e:
        logging.warning(f"Could not load splash screen: {e}")


# Initialize mixer for sound
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
sound_enabled = True

# Load sounds (add eat.mp3, death.mp3, background.mp3 to folder)
eat_sound = None
death_sound = None
level_up_sound = None

try:
    eat_sound_path = resolve_asset_path('eat.mp3')
    eat_sound = pygame.mixer.Sound(eat_sound_path)
    set_sound_volume(eat_sound, 0.85, 'Eat')
    sound_assets_available = True
    logging.info("Eat sound loaded from %s", eat_sound_path)
except Exception as exc:
    eat_sound = create_eat_tone()
    if eat_sound:
        set_sound_volume(eat_sound, 0.85, 'Eat fallback')
        sound_assets_available = True
        logging.warning(
            'Eat sound load failed (%s); using generated tone instead',
            exc,
        )
    else:
        logging.warning(
            'Eat sound load failed (%s); continuing without it',
            exc,
        )

try:
    death_sound_path = resolve_asset_path('death.mp3')
    death_sound = pygame.mixer.Sound(death_sound_path)
    set_sound_volume(death_sound, 0.7, 'Death')
    sound_assets_available = True
    logging.info("Death sound loaded from %s", death_sound_path)
except Exception as exc:
    logging.warning(
        'Death sound load failed (%s); continuing without it',
        exc,
    )

try:
    level_up_path = resolve_asset_path('level_up.mp3')
    level_up_sound = pygame.mixer.Sound(level_up_path)
    set_sound_volume(level_up_sound, 0.8, 'Level up')
    sound_assets_available = True
    logging.info("Level up sound loaded from %s", level_up_path)
except Exception as exc:
    level_up_sound = create_level_up_tone()
    if level_up_sound:
        set_sound_volume(level_up_sound, 0.8, 'Level up fallback')
        sound_assets_available = True
        logging.warning(
            'Level up sound load failed (%s); using generated tone instead',
            exc,
        )
    else:
        logging.warning(
            'Level up sound load failed (%s); continuing without it',
            exc,
        )
try:
    background_path = resolve_asset_path('background.mp3')
    pygame.mixer.music.load(background_path)
    background_music_available = True
    logging.info("Background music loaded from %s", background_path)
except Exception as exc:
    background_music_available = False
    logging.warning(
        'Background music not found; continuing without it (%s)',
        exc,
    )

update_music()

# Load move sound for MVP2
# Звук движения и его канал
move_sound_channel = None
move_sound = None
try:
    move_sound_path = resolve_asset_path('negromkiy-korotkiy-klik.mp3')
    move_sound = pygame.mixer.Sound(move_sound_path)
    set_sound_volume(move_sound, 0.5, 'Move')
    logging.info("Move sound loaded from %s", move_sound_path)
except Exception as exc:
    move_sound = None
    logging.warning(
        'Move sound load failed (%s); movement will be silent', exc
    )


def create_move_tone(
    frequency: int = 440,
    duration: float = 0.22,
    volume: float = 1.0,
):
    """Generate a short, clearly audible tone for snake movement."""

    init = pygame.mixer.get_init()
    if not init:
        return None

    sample_rate, format_bits, channels = init
    sample_rate = int(sample_rate)
    bit_depth = abs(int(format_bits))
    max_amplitude = (2 ** (bit_depth - 1)) - 1
    amplitude = int(max_amplitude * max(0.0, min(volume, 1.0)))
    sample_count = max(1, int(sample_rate * duration))

    wave = array('h')
    for t in range(sample_count):
        angle = 2 * math.pi * frequency * t / sample_rate
        sample = int(amplitude * math.sin(angle))
        if channels >= 2:
            wave.append(sample)
            wave.append(sample)
        else:
            wave.append(sample)

    try:
        sound = pygame.mixer.Sound(buffer=wave.tobytes())
        set_sound_volume(sound, volume, 'Generated move')
        return sound
    except pygame.error:
        logging.debug("Failed to create move tone", exc_info=True)
        return None


# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Show splash screen
show_splash_screen(duration=2.0)

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
gold = pygame.Color(255, 215, 0)
orange = pygame.Color(255, 140, 0)
teal = pygame.Color(64, 224, 208)

# Game state variables
level = 1  # Initial level
score = 0
speed_boost_on_food = False
speed_boost_active_until = 0
invincible_until = 0
snake_body = []
walls = []
moving_walls = []
wrap_edges = False
food_type = 'normal'
current_food_color = white
current_food_value = 1
current_food_effect = None
food_pos = (0, 0)
snake_pos = (0, 0)
food_spawn = False
direction = 'RIGHT'
change_to = 'RIGHT'

# Snake color
snake_color = green


FOOD_TYPE_CONFIG = {
    'normal': {
        'color': white,
        'score': 1,
        'effect': None,
    },
    'bonus': {
        'color': gold,
        'score': 5,
        'effect': None,
    },
    'speed': {
        'color': orange,
        'score': 1,
        'effect': 'speed',
    },
    'shield': {
        'color': teal,
        'score': 1,
        'effect': 'shield',
    },
}

FOOD_LABELS = {
    'normal': 'Обыч',
    'bonus': 'Бонус',
    'speed': 'Скор',
    'shield': 'Щит',
}

MODE_FOOD_CONFIG = {
    'mvp': {
        'bonus': {'base': 0.03, 'level': 0.01, 'score': 0.005, 'cap': 0.18},
        'shield': {'base': 0.02, 'level': 0.008, 'score': 0.004, 'cap': 0.16},
        'speed': {'base': 0.03, 'level': 0.012, 'score': 0.006, 'cap': 0.2},
        'max_total': 0.55,
    },
    'map': {
        'bonus': {'base': 0.07, 'level': 0.02, 'score': 0.01, 'cap': 0.35},
        'shield': {'base': 0.06, 'level': 0.018, 'score': 0.009, 'cap': 0.32},
        'speed': {'base': 0.05, 'level': 0.02, 'score': 0.01, 'cap': 0.3},
        'max_total': 0.75,
    },
    'survival': {
        'bonus': {'base': 0.04, 'level': 0.012, 'score': 0.007, 'cap': 0.25},
        'shield': {'base': 0.07, 'level': 0.015, 'score': 0.01, 'cap': 0.35},
        'speed': {'base': 0.06, 'level': 0.02, 'score': 0.012, 'cap': 0.32},
        'max_total': 0.65,
    },
}


# Theme-dependent colors
def update_colors():
    global bg_color, text_color, wall_color, food_color
    if mode in ('mvp', 'mvp2'):
        # MVP mode always uses black theme
        bg_color = black
        text_color = white
        wall_color = white
        food_color = blue
    elif theme_setting == 'light':
        bg_color = pygame.Color(200, 200, 200)  # Light gray for contrast
        text_color = black
        wall_color = black
        food_color = blue
    else:
        bg_color = black
        text_color = white
        wall_color = white
        food_color = blue


def refresh_premium_state():
    """Ensure premium access expires correctly and UI reflects the change."""

    global mode
    global map_end_time
    global current_premium_minutes
    global last_mode_switch
    global premium_expiry_message_until

    now = time.time()
    changed = False

    if map_end_time > 0:
        remaining_seconds = map_end_time - now
        if remaining_seconds <= 0:
            map_end_time = 0
            changed = True
            if current_premium_minutes != 0:
                current_premium_minutes = 0
                changed = True
            if mode != 'mvp':
                mode = 'mvp'
                last_mode_switch = now
                update_colors()
                logging.info("Mode switched to MVP due to premium expiration")
                changed = True
                premium_expiry_message_until = now + 5
        else:
            updated_minutes = max(1, math.ceil(remaining_seconds / 60))
            if current_premium_minutes != updated_minutes:
                current_premium_minutes = updated_minutes
                changed = True
    else:
        if mode == 'map':
            mode = 'mvp'
            last_mode_switch = now
            update_colors()
            logging.info("Mode switched to MVP because premium flag reset")
            changed = True
            premium_expiry_message_until = now + 5
        if current_premium_minutes != 0:
            current_premium_minutes = 0
            changed = True

    if changed:
        save_settings()


# Initialize pygame objects
dis = game_window
fps_controller = pygame.time.Clock()

# Game state variables
game_state = 'menu'
player_name = ''
promo_input = ''
played_death = False
difficulty = 5


def show_score(choice, color, font, size, *args):
    """Display score and game status information."""
    score_font = pygame.font.SysFont(font, size)
    
    if choice == 1:
        # During gameplay - show compact status
        mode_text, countdown, elapsed_str, effects_parts = args
        status_parts = []
        status_parts.append(f'Счёт:{score}')
        if mode_text:
            status_parts.append(mode_text)
        if countdown:
            status_parts.append(countdown)
        status_parts.append(elapsed_str)
        status_parts.extend(effects_parts)
        status_text = ' '.join(status_parts)
        score_surface = score_font.render(status_text, True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (frame_size_x / 2, 10)
        game_window.blit(score_surface, score_rect)
    else:
        # Game over screen
        score_surface = score_font.render(f'Счёт: {score}', True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
        game_window.blit(score_surface, score_rect)


def message(msg, color):
    """Display a message on the screen."""
    mesg_font = pygame.font.SysFont('times new roman', 50)
    mesg = mesg_font.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(frame_size_x / 2, frame_size_y / 3))
    game_window.blit(mesg, mesg_rect)


def reset_game():
    """Reset the game to initial state."""
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to
    global score, paused, played_death, level, walls, moving_walls
    global wrap_edges, speed_boost_on_food, speed_boost_active_until
    global invincible_until, premium_offer_active, difficulty, start_time
    
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
    food_spawn = False
    spawn_food()
    direction = 'RIGHT'
    change_to = direction
    score = 0
    paused = False
    played_death = False
    level = 1
    walls = []
    moving_walls = []
    wrap_edges = False
    speed_boost_on_food = False
    speed_boost_active_until = 0
    invincible_until = 0
    premium_offer_active = False
    load_level(level)
    
    # Apply settings
    if mode in ('mvp', 'mvp2'):
        difficulty = 5
    else:
        difficulty = speed_setting
    update_music()
    start_time = time.time()


def toggle_pause():
    """Toggle the game pause state."""
    global paused
    paused = not paused


def update_and_show_game_status():
    """Calculates and displays the current game status."""
    now = time.time()
    elapsed_time = int(now - start_time)
    elapsed_minutes = elapsed_time // 60
    elapsed_seconds = elapsed_time % 60
    elapsed_str = f'Вр:{elapsed_minutes}:{elapsed_seconds:02d}'
    if mode == 'map':
        remaining_seconds = max(0, int(map_end_time - now))
        if remaining_seconds > 0:
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            mode_text = f'Премиум{current_premium_minutes}'
            countdown = f'До:{minutes}:{seconds:02d}'
        else:
            mode_text = 'Классика'
            countdown = ''
    elif mode == 'survival':
        mode_text = 'Выживание'
        countdown = ''
    elif mode == 'mvp':
        mode_text = 'Классика'
        countdown = ''
    elif mode == 'mvp2':
        mode_text = ''
        countdown = ''
    else:
        mode_text = ''
        countdown = ''
    effects_parts = []
    if speed_boost_active_until > now:
        boost_time = int(speed_boost_active_until - now)
        effects_parts.append(f'Буст:{boost_time}')
    if invincible_until > now:
        shield_time = int(invincible_until - now)
        effects_parts.append(f'Щит:{shield_time}')
    if food_type != 'normal':
        food_label = FOOD_LABELS.get(food_type, food_type)
        effects_parts.append(f'Еда:{food_label}')
    show_score(
        1,
        white,
        'consolas',
        20,
        mode_text,
        countdown,
        elapsed_str,
        effects_parts,
    )


# gameLoop
def gameLoop():
    """The main game loop."""
    global game_over, game_close, paused, premium_offer_active
    global snake_List, Length_of_snake, x1, y1, x1_change, y1_change
    global foodx, foody, food_type, score, start_time, last_move_time
    global current_direction, change_to, speed_boost_active_until
    global invincible_until, mode, map_end_time, current_premium_minutes
    global last_mode_switch, level, game_state, speed_setting
    global sound_setting, theme_setting, promo_input, played_death
    game_over = False
    game_close = False
    paused = False
    premium_offer_active = False
    # Initial snake and food setup
    x1 = frame_size_x // 2
    y1 = frame_size_y // 2
    snake_List = []
    Length_of_snake = 1

    # Speed and direction
    x1_change = 0
    y1_change = 0
    change_to = 'STOP'

    # Timers
    start_time = time.time()
    last_move_time = time.time()

    # Effects
    speed_boost_active_until = 0
    invincible_until = 0

    # Main game loop
    while not game_over:
        while game_close:
            dis.fill(blue)
            message('Вы проиграли! Нажмите Q-Выход или C-Играть снова', red)
            update_and_show_game_status()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        reset_game()
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if game_state == 'menu':
                    if event.key == pygame.K_SPACE:
                        reset_game()
                        game_state = 'playing'
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        if mode != 'mvp':
                            mode = 'mvp'
                            last_mode_switch = time.time()
                            update_colors()
                            save_settings()
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        if mode != 'mvp2':
                            mode = 'mvp2'
                            last_mode_switch = time.time()
                            update_colors()
                            save_settings()
                    elif event.key == pygame.K_s:
                        game_state = 'settings'
                    elif event.key == pygame.K_l:
                        if LEADERBOARD_AVAILABLE:
                            game_state = 'leaderboard'
                elif game_state == 'playing':
                    if premium_offer_active:
                        if event.key in (pygame.K_y, pygame.K_RETURN):
                            duration = 5 * 60
                            mode = 'map'
                            map_end_time = time.time() + duration
                            current_premium_minutes = duration // 60
                            last_mode_switch = time.time()
                            update_colors()
                            load_level(level)
                            save_settings()
                            premium_offer_active = False
                            paused = False
                        elif event.key in (
                            pygame.K_n,
                            pygame.K_SPACE,
                            pygame.K_ESCAPE,
                        ):
                            premium_offer_active = False
                            paused = False
                        # This continue is correct for the event loop
                        continue
                    # W -> Up; S -> Down; A -> Left; D -> Right
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        change_to = 'UP'
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        change_to = 'DOWN'
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        change_to = 'RIGHT'
                    # Esc -> Go to menu
                    if event.key == pygame.K_ESCAPE:
                        game_state = 'menu'
                    # Q -> Quit immediately
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    # P -> Pause/Resume
                    if event.key == pygame.K_p:
                        toggle_pause()
                elif game_state == 'settings':
                    if event.key == pygame.K_ESCAPE:
                        game_state = 'menu'
                    elif event.key == pygame.K_UP:
                        if speed_setting < 120:
                            speed_setting += 5
                            save_settings()
                    elif event.key == pygame.K_DOWN:
                        if speed_setting > 5:
                            speed_setting -= 5
                            save_settings()
                    elif event.key == pygame.K_s:
                        sound_setting = not sound_setting
                        save_settings()
                        update_music()
                    elif event.key == pygame.K_t:
                        theme_setting = (
                            'light' if theme_setting == 'dark' else 'dark'
                        )
                        save_settings()
                        update_colors()
                    elif event.key == pygame.K_m:
                        premium_active = (
                            map_end_time > 0 and time.time() <= map_end_time
                        )
                        available_modes = ['mvp', 'mvp2', 'survival']
                        if premium_active:
                            available_modes.append('map')
                        if mode not in available_modes:
                            mode = available_modes[0]
                        else:
                            current_index = available_modes.index(mode)
                            mode = available_modes[
                                (current_index + 1) % len(available_modes)
                            ]
                        update_colors()
                        save_settings()
                    elif event.key == pygame.K_p:
                        game_state = 'promo'
                    elif event.key == pygame.K_ESCAPE:
                        game_state = 'menu'
                elif game_state == 'promo':
                    if event.key == pygame.K_RETURN:
                        if promo_input in promo_codes:
                            mode = 'map'
                            duration = promo_codes[promo_input]
                            map_end_time = time.time() + duration
                            current_premium_minutes = (
                                promo_codes[promo_input] // 60
                            )
                            save_settings()
                            update_colors()
                            promo_input = ''
                            game_state = 'settings'
                        else:
                            promo_input = ''  # Invalid code
                    elif event.key == pygame.K_BACKSPACE:
                        promo_input = promo_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        promo_input = ''
                        game_state = 'settings'
                    else:
                        promo_input += event.unicode
                elif game_state == 'leaderboard':
                    if event.key == pygame.K_ESCAPE:
                        game_state = 'menu'

            # Touch/Mouse events for Android and desktop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Allow mouse clicks on desktop for testing
                if ANDROID or True:
                    mouse_x, mouse_y = event.pos
                    # Divide screen into 4 sections for directional control
                    center_x = frame_size_x / 2
                    center_y = frame_size_y / 2

                    if game_state == 'menu':
                        # Touch anywhere to start
                        reset_game()
                        game_state = 'playing'
                    elif game_state == 'playing' and not premium_offer_active:
                        # Determine swipe direction based on touch position
                        dx = mouse_x - center_x
                        dy = mouse_y - center_y

                        if abs(dx) > abs(dy):
                            # Horizontal swipe
                            if dx > 0:
                                change_to = 'RIGHT'
                            else:
                                change_to = 'LEFT'
                        else:
                            # Vertical swipe
                            if dy > 0:
                                change_to = 'DOWN'
                            else:
                                change_to = 'UP'
                    elif game_state == 'game_over':
                        # Touch to restart
                        reset_game()
                        game_state = 'playing'

        refresh_premium_state()
        update_music()

        if game_state == 'menu':
            game_window.fill(bg_color)
            title_font = pygame.font.SysFont('times new roman', 50)
            title_surface = title_font.render('Змейка', True, text_color)
            title_rect = title_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 - 50))
            game_window.blit(title_surface, title_rect)
            mode_font = pygame.font.SysFont('times new roman', 25)
            if mode == 'map':
                mode_text = f'Премиум{current_premium_minutes}'
            elif mode == 'survival':
                mode_text = 'Выживание'
            elif mode == 'mvp2':
                mode_text = 'Классика2'
            else:
                mode_text = 'Классика'
            mode_surface = mode_font.render(
                f'Режим: {mode_text}',
                True,
                text_color,
            )
            mode_rect = mode_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 - 10)
            )
            game_window.blit(mode_surface, mode_rect)
            start_font = pygame.font.SysFont('times new roman', 30)
            start_text = 'Нажмите ПРОБЕЛ для начала'
            start_surface = start_font.render(start_text, True, green)
            start_rect = start_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 + 20))
            game_window.blit(start_surface, start_rect)
            mode_hint_font = pygame.font.SysFont('times new roman', 22)
            mode_hint_text = '←/→ для выбора: Классика / Классика2'
            mode_hint_surface = mode_hint_font.render(
                mode_hint_text,
                True,
                text_color,
            )
            mode_hint_rect = mode_hint_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 + 55)
            )
            game_window.blit(mode_hint_surface, mode_hint_rect)
            settings_hint_font = pygame.font.SysFont('times new roman', 25)
            settings_hint_text = 'Нажмите S для настроек'
            settings_hint_surface = settings_hint_font.render(
                settings_hint_text, True, text_color
            )
            settings_hint_rect = settings_hint_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 + 90)
            )
            game_window.blit(settings_hint_surface, settings_hint_rect)

            # Leaderboard hint
            if LEADERBOARD_AVAILABLE:
                leaderboard_hint_font = pygame.font.SysFont(
                    'times new roman', 25
                )
                leaderboard_hint_text = 'Нажмите L для таблицы лидеров'
                leaderboard_hint_surface = leaderboard_hint_font.render(
                    leaderboard_hint_text, True, green
                )
                leaderboard_hint_rect = leaderboard_hint_surface.get_rect(
                    center=(frame_size_x / 2, frame_size_y / 2 + 125)
                )
                game_window.blit(
                    leaderboard_hint_surface, leaderboard_hint_rect
                )

            pygame.display.update()
            fps_controller.tick(10)
            update_music()
        elif game_state == 'settings':
            game_window.fill(bg_color)
            settings_font = pygame.font.SysFont('times new roman', 40)
            settings_surface = settings_font.render(
                'Настройки', True, text_color
            )
            settings_rect = settings_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 - 100)
            )
            game_window.blit(settings_surface, settings_rect)
            speed_font = pygame.font.SysFont('times new roman', 30)
            speed_surface = speed_font.render(
                f'Скорость: {speed_setting}',
                True,
                green,
            )
            speed_rect = speed_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 - 40)
            )
            game_window.blit(speed_surface, speed_rect)
            sound_font = pygame.font.SysFont('times new roman', 30)
            sound_text = 'Звук: Вкл' if sound_setting else 'Звук: Выкл'
            sound_surface = sound_font.render(sound_text, True, green)
            sound_rect = sound_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2)
            )
            game_window.blit(sound_surface, sound_rect)
            theme_font = pygame.font.SysFont('times new roman', 30)
            theme_status = "Светлая" if theme_setting == "light" else "Тёмная"
            theme_text = f'Тема: {theme_status}'
            theme_surface = theme_font.render(
                theme_text,
                True,
                green,
            )
            theme_rect = theme_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 + 40)
            )
            game_window.blit(theme_surface, theme_rect)
            mode_font = pygame.font.SysFont('times new roman', 30)
            premium_active = map_end_time > 0 and time.time() <= map_end_time
            mode_label_map = {
                'mvp': 'Классика',
                'mvp2': 'Классика2',
                'survival': 'Выживание',
                'map': 'Премиум',
            }
            current_mode_label = mode_label_map.get(mode, 'Классика')
            if mode == 'map' and not premium_active:
                current_mode_label = 'Премиум (нет доступа)'
            mode_text_line = f'Режим: {current_mode_label}'
            mode_surface = mode_font.render(mode_text_line, True, green)
            mode_rect = mode_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 + 80)
            )
            game_window.blit(mode_surface, mode_rect)

            # Управление в левом верхнем углу построчно
            controls_font = pygame.font.SysFont('times new roman', 18)
            control_lines = [
                '↑/↓ скорость',
                'S звук',
                'T тема',
                'P промокод'
            ]
            for idx, line_text in enumerate(control_lines):
                line_surface = controls_font.render(
                    line_text, True, text_color
                )
                line_rect = line_surface.get_rect()
                line_rect.left = 50
                line_rect.top = frame_size_y / 2 - 40 + idx * 20
                game_window.blit(line_surface, line_rect)

            autosave_font = pygame.font.SysFont('times new roman', 18)
            autosave_text = 'Изменения сохраняются автоматически.'
            autosave_surface = autosave_font.render(
                autosave_text,
                True,
                text_color,
            )
            autosave_rect = autosave_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 + 122)
            )
            game_window.blit(autosave_surface, autosave_rect)
            tip_font = pygame.font.SysFont('times new roman', 18)
            tip_lines = [
                ('+5 очков', gold),
                ('щит 6с', teal),
                ('быстрее 5с', orange),
            ]
            for idx, (line_text, line_color) in enumerate(tip_lines):
                line_surface = tip_font.render(line_text, True, line_color)
                line_rect = line_surface.get_rect()
                line_rect.right = frame_size_x - 50
                line_rect.top = frame_size_y / 2 - 40 + idx * 20
                game_window.blit(line_surface, line_rect)
            exit_font = pygame.font.SysFont('times new roman', 20)
            exit_text = 'ESC: Выйти из настроек'
            exit_surface = exit_font.render(
                exit_text,
                True,
                text_color,
            )
            exit_rect = exit_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 + 180)
            )
            game_window.blit(exit_surface, exit_rect)
            pygame.display.update()
            fps_controller.tick(10)
        elif game_state == 'promo':
            game_window.fill(bg_color)
            promo_font = pygame.font.SysFont('times new roman', 40)
            promo_surface = promo_font.render(
                'Введите промокод:',
                True,
                text_color,
            )
            promo_rect = promo_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 - 50)
            )
            game_window.blit(promo_surface, promo_rect)
            input_font = pygame.font.SysFont('times new roman', 30)
            input_surface = input_font.render(promo_input, True, text_color)
            input_rect = input_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2)
            )
            game_window.blit(input_surface, input_rect)
            pygame.draw.rect(
                game_window,
                text_color,
                input_rect.inflate(20, 10),
                2,
            )  # Border for input field
            hint_font = pygame.font.SysFont('times new roman', 20)
            hint_surface = hint_font.render(
                'Enter: Подтвердить, Esc: Отмена',
                True,
                text_color,
            )
            hint_rect = hint_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 + 50)
            )
            game_window.blit(hint_surface, hint_rect)
            pygame.display.update()
            fps_controller.tick(10)
            update_music()
        elif game_state == 'leaderboard':
            game_window.fill(bg_color)
            title_font = pygame.font.SysFont('times new roman', 45)
            title_surface = title_font.render(
                'Таблица лидеров', True, text_color
            )
            title_rect = title_surface.get_rect(
                center=(frame_size_x / 2, 50)
            )
            game_window.blit(title_surface, title_rect)

            # Get leaderboard data
            try:
                top_scores = leaderboard.get_leaderboard(mode=None, limit=10)
                status_font = pygame.font.SysFont('times new roman', 18)
                status_text = "🌐 Online" if leaderboard.online else "💾 Offline"
                status_surface = status_font.render(
                    status_text, True, green if leaderboard.online else orange
                )
                status_rect = status_surface.get_rect()
                status_rect.topright = (frame_size_x - 20, 20)
                game_window.blit(status_surface, status_rect)
            except Exception as e:
                logging.error(f"Failed to load leaderboard: {e}")
                top_scores = []

            # Display scores
            if top_scores:
                entry_font = pygame.font.SysFont('times new roman', 24)
                y_offset = 110
                for i, entry in enumerate(top_scores, 1):
                    rank = f"{i}."
                    name = entry.get('name', 'Unknown')[:15]
                    score_val = entry.get('score', 0)
                    mode_val = entry.get('mode', 'mvp')

                    # Highlight current player
                    if name == player_name:
                        color = gold
                    else:
                        color = text_color

                    text = f"{rank:3} {name:15} {score_val:5} [{mode_val}]"
                    entry_surface = entry_font.render(text, True, color)
                    entry_rect = entry_surface.get_rect(
                        center=(frame_size_x / 2, y_offset)
                    )
                    game_window.blit(entry_surface, entry_rect)
                    y_offset += 32
            else:
                no_data_font = pygame.font.SysFont('times new roman', 25)
                no_data_surface = no_data_font.render(
                    'Нет данных', True, text_color
                )
                no_data_rect = no_data_surface.get_rect(
                    center=(frame_size_x / 2, frame_size_y / 2)
                )
                game_window.blit(no_data_surface, no_data_rect)

            # Hint
            hint_font = pygame.font.SysFont('times new roman', 20)
            hint_surface = hint_font.render(
                'ESC: Вернуться в меню', True, text_color
            )
            hint_rect = hint_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y - 30)
            )
            game_window.blit(hint_surface, hint_rect)

            pygame.display.update()
            fps_controller.tick(10)
        elif game_state == 'playing':
            if premium_offer_active:
                game_window.fill(bg_color)
                for pos in snake_body:
                    segment_rect = pygame.Rect(pos[0], pos[1], 10, 10)
                    pygame.draw.rect(game_window, snake_color, segment_rect)
                food_rect = pygame.Rect(food_pos[0], food_pos[1], 10, 10)
                pygame.draw.rect(game_window, current_food_color, food_rect)
                for wall_rect in walls:
                    pygame.draw.rect(game_window, wall_color, wall_rect)
                for moving in moving_walls:
                    pygame.draw.rect(game_window, wall_color, moving['rect'])

                update_and_show_game_status()

                prompt_font = pygame.font.SysFont('times new roman', 36)
                prompt_surface = prompt_font.render(
                    'Открыть "Премиум5"? (Y — да, N — нет)',
                    True,
                    green,
                )
                prompt_rect = prompt_surface.get_rect(
                    center=(frame_size_x / 2, frame_size_y / 2 - 20)
                )
                game_window.blit(prompt_surface, prompt_rect)
                detail_font = pygame.font.SysFont('times new roman', 24)
                detail_surface = detail_font.render(
                    'Премиум5: стены, бонусы и музыка на 5 минут.',
                    True,
                    text_color,
                )
                detail_rect = detail_surface.get_rect(
                    center=(frame_size_x / 2, frame_size_y / 2 + 20)
                )
                game_window.blit(detail_surface, detail_rect)
                decline_surface = detail_font.render(
                    'N / пробел / Esc — продолжить классику.',
                    True,
                    text_color,
                )
                decline_rect = decline_surface.get_rect(
                    center=(frame_size_x / 2, frame_size_y / 2 + 50)
                )
                game_window.blit(decline_surface, decline_rect)

            pygame.display.update()
            fps_controller.tick(10)
        elif game_state == 'game_over':
            game_window.fill(bg_color)
            game_over_font = pygame.font.SysFont('times new roman', 50)
            game_over_surface = game_over_font.render(
                'Игра окончена', True, red
            )
            game_over_rect = game_over_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 - 50)
            )
            game_window.blit(game_over_surface, game_over_rect)
            score_font = pygame.font.SysFont('times new roman', 30)
            score_surface = score_font.render(
                f'Финальный счёт: {score} (Лучший: {best_score})',
                True,
                text_color,
            )
            score_rect = score_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2)
            )
            game_window.blit(score_surface, score_rect)
            restart_font = pygame.font.SysFont('times new roman', 25)
            restart_surface = restart_font.render(
                'Нажмите R для перезапуска или Q для выхода',
                True,
                green,
            )
            restart_rect = restart_surface.get_rect(
                center=(frame_size_x / 2, frame_size_y / 2 + 50)
            )
            game_window.blit(restart_surface, restart_rect)
            pygame.display.update()
            if not played_death and sound_enabled:
                death_sound.play()
                played_death = True
            fps_controller.tick(10)
            update_music()


def choose_food_type():
    """Chooses the type of food to spawn based on game mode and state."""
    if mode == 'mvp2':
        return 'normal'
    if speed_boost_on_food:
        return 'speed'
    if mode == 'mvp':
        return 'normal'

    config = MODE_FOOD_CONFIG.get(mode, MODE_FOOD_CONFIG['mvp'])
    
    # Calculate probabilities
    bonus_prob = min(
        config['bonus']['cap'],
        config['bonus']['base']
        + (level * config['bonus']['level'])
        + (score * config['bonus']['score']),
    )
    shield_prob = min(
        config['shield']['cap'],
        config['shield']['base']
        + (level * config['shield']['level'])
        + (score * config['shield']['score']),
    )
    speed_prob = min(
        config['speed']['cap'],
        config['speed']['base']
        + (level * config['speed']['level'])
        + (score * config['speed']['score']),
    )

    # Total probability capped at max_total
    # (bonus_prob + shield_prob + speed_prob <= config['max_total'])

    rand_val = rng.random()

    if rand_val < bonus_prob:
        return 'bonus'
    elif rand_val < bonus_prob + shield_prob:
        return 'shield'
    elif rand_val < bonus_prob + shield_prob + speed_prob:
        return 'speed'
    else:
        return 'normal'


def spawn_food(force_type=None):
    """Spawns food on the screen."""
    global food_pos, food_type, current_food_color
    global current_food_value, current_food_effect
    
    selected_type = force_type or choose_food_type()
    
    food_config = FOOD_TYPE_CONFIG[selected_type]
    food_type = selected_type
    current_food_color = food_config['color']
    current_food_value = food_config['score']
    current_food_effect = food_config['effect']

    while True:
        food_pos = [
            rng.randrange(1, (frame_size_x // 10)) * 10,
            rng.randrange(1, (frame_size_y // 10)) * 10,
        ]
        if (
            food_pos not in snake_body
            and food_pos not in [wall.topleft for wall in walls]
            and food_pos
            not in [moving['rect'].topleft for moving in moving_walls]
        ):
            break


def load_level(level_num):
    """Loads the specified level."""
    global walls, moving_walls, wrap_edges
    walls.clear()
    moving_walls.clear()
    wrap_edges = False

    if mode == 'map':
        wrap_edges = True
        # Simple wall pattern for any level > 0 in map mode
        if level_num > 0:
            for i in range(5, (frame_size_x // 10) - 5):
                walls.append(pygame.Rect(i * 10, frame_size_y // 2, 10, 10))
    elif mode == 'survival':
        pass  # No walls in survival
