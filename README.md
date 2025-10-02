# Snake Eater

![Quality Checks](https://github.com/rublov/snake-game-android/actions/workflows/quality.yml/badge.svg)
![Build Android APK](https://github.com/rublov/snake-game-android/actions/workflows/build-apk.yml/badge.svg)
[![CodeFactor](https://www.codefactor.io/repository/github/rublov/snake-game-android/badge)](https://www.codefactor.io/repository/github/rublov/snake-game-android)

A snake game written in Python using the Pygame library.

## Features

- Classic Snake gameplay
- Two modes: MAP (premium with obstacles) and MVP (free without obstacles)
- Themes: Light and Dark
- Sound effects and background music
- Settings persistence
- Promo codes for extending MAP mode
- Time tracking during gameplay
- Visual mode indicator on screen

## Modes

### MAP Mode (Premium)

- Includes obstacles (walls) for increased difficulty
- Activated via promo codes (e.g., "MAP30" for 30 minutes,
  "qwerty5" for 5 minutes, "qwerty10" for 10 minutes, etc.)
- Sound and music enabled
- Theme can be changed

### MVP Mode (Free)

- No obstacles, simpler gameplay
- Activated by default, no time limit
- Sound and music disabled
- Theme always black (forced)

## Installing

Download the Python 3 installer package from the official website
and install it, if not installed previously.

Run the following in the terminal to install the required dependencies

```bash
pip install -r requirements.txt
```

## Running the application

Download the source code from the repository and run the file
just as any other Python script (.py) file.

```bash
python3 Snake\ Game.py
```

## Example Usage

To start the game in MAP mode with a promo code:

```bash
python3 Snake\ Game.py --mode MAP --promo MAP30
```

To start the game in MVP mode:

```bash
python3 Snake\ Game.py --mode MVP
```

## Testing

### Visual Testing

The project includes a visual testing script (`visual_test.py`)
for detecting visual regressions in the game UI.

To run visual tests:

1. Start the game: `python "Snake Game.py"`
2. In another terminal, run: `python visual_test.py`

This will capture a screenshot and compare it with a baseline image.
If no baseline exists, it will create one.

### Security Testing

- Run `bandit "Snake Game.py"` for static security analysis.
- Run `safety check --file requirements.txt` for dependency
  vulnerability checks.

### Continuous Integration

This repository ships with three GitHub Actions workflows:

- `Quality Checks` — headless среда с запуском `ruff`, `mypy` и unit-тестов
   на каждый push/pull request.
- `Build Android APK` — сборка Android-пакета через Buildozer и загрузка
   артефакта.
- `CodeFactor` — статический анализ CodeFactor. Для работы требуется секрет
   `CODEFACTOR_TOKEN`, который можно получить в личном кабинете CodeFactor
   (Account → Integrations → GitHub Action token) и добавить в настройках
   репозитория GitHub (`Settings → Secrets and variables → Actions`).

Запустите их вручную на вкладке **Actions** или повторите локально:

```bash
ruff check .
mypy snake_game
pytest
```

## Changes for MVP/MAP Modes Implementation

To achieve the task of implementing two modes (MVP and MAP),
the following changes were made:

1. **Mode Variables**: Added `mode` variable ('map' or 'mvp')
   and `map_end_time` for timer management.
2. **First Launch Tracking**: Introduced `first_launch_time` to set
   a global 15-minute limit for MAP mode from the first app launch.
3. **Settings Persistence**: Updated `save_settings()` and `load_settings()`
   to store mode, timers, and first launch time.
4. **Theme Control**: Modified `update_colors()` to force black theme
   in MVP mode regardless of user setting.
5. **Sound Control**: Disabled sound in MVP mode by setting
   `sound_enabled = False` when mode is 'mvp'.
6. **Level Loading**: Updated `load_level()` to load walls only
   in MAP mode.
7. **Promo Codes**: Added promo code system with 'MAP30' and various
   'qwerty' codes (qwerty5, qwerty10, qwerty15, qwerty20) to extend MAP time.
8. **UI Notifications**: Added notification when switching
   from MAP to MVP.
9. **Timer Security**: Made MAP timer global to prevent abuse
   by closing/reopening the app.
10. **Time Display**: Added elapsed time counter in the top-right
    corner during gameplay.
11. **Mode Indicator**: Added visual indicator showing current mode
    (e.g., "Премиум15" for activated promo code duration, or "Классика")
    in the top-left corner during gameplay and pause, and in the start menu.
12. **Game Over Behavior**: Modified game_over() to not quit the application,
    allowing players to restart or return to menu without relaunching.

These changes ensure fair monetization with a free MVP mode
and a time-limited premium MAP mode.

The rest of the code is properly commented and self explanatory.
Tweaks can be made to change the play style or visuals of the game.

## Screenshots

![1](https://user-images.githubusercontent.com/32998741/33873439-27f635b2-df45-11e7-8fc1-f7812f17447a.png)
*Written using PyCharm*

![2](https://user-images.githubusercontent.com/32998741/33873437-2780ed2a-df45-11e7-9776-b1f151fa4e02.png)
*Active game screen*

![3](https://user-images.githubusercontent.com/32998741/33873440-28647360-df45-11e7-8291-b82d5646352f.png)
*Game over screen*

## Prerequisites

- [Python](https://www.python.org)
- [Pygame](https://www.pygame.org/wiki/GettingStarted),
  an open source Python library for making multimedia applications

## Authors

- **Rajat Dipta Biswas** - *Initial work*

See also the list of
[contributors](https://github.com/rajatdiptabiswas/snake-pygame/graphs/contributors)
who participated in this project.

## Dependency Management

This project uses [Dependabot](https://dependabot.com/) for automated
dependency updates. Dependabot automatically creates pull requests
to update dependencies to their latest versions, helping to keep
the project secure and up-to-date.

## Acknowledgements

- [Pygame Documentations](https://www.pygame.org/docs/)
- [Udemy: Python Game Development](<https://www.udemy.com/python-game-development-creating-a-snake-game-from-scratch/learn/v4/overview>)

## Android Adaptation

This project has been adapted to work with Kivy for Android development. Follow the steps below to build and run the application on Android devices:

### Prerequisites for Android

- Install [Kivy](https://kivy.org/doc/stable/gettingstarted/installation.html) in your Python environment.
- Install [Buildozer](https://github.com/kivy/buildozer) for building APKs.
- Ensure you have Java, Android SDK, and other dependencies required by Buildozer.

### Building the APK

1. Initialize Buildozer in the project directory:

   ```bash
   buildozer init
   ```

2. Edit the `buildozer.spec` file to configure your app (e.g., app name, package name, permissions).

3. Build the APK:

   ```bash
   buildozer -v android debug
   ```

4. Once the build is complete, the APK file will be located in the `bin/` directory.

### Installing the APK

Transfer the APK file to your Android device and install it manually. Ensure that "Install unknown apps" is enabled in your device settings.

### Running on Android

After installation, launch the app from your device's app drawer. The game will run with the same features as the desktop version, including MAP and MVP modes.
