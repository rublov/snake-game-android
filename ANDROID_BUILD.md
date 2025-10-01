# Сборка APK для Android с использованием Pygame Subset for Android (pgs4a)

## 📱 Подготовка к сборке

### Шаг 1: Установка требуемых инструментов

#### На Windows:
1. **Установите Python 3.8+** (если еще не установлен)
2. **Установите Java Development Kit (JDK)**
   - Скачайте OpenJDK 8 или 11: https://adoptopenjdk.net/
   - Добавьте в PATH: `C:\Program Files\Java\jdk-11\bin`

3. **Установите Android SDK**
   - Скачайте Android Studio: https://developer.android.com/studio
   - Или используйте command line tools: https://developer.android.com/studio#command-tools
   - Установите SDK Platform 29 (Android 10) или выше
   - Установите build-tools версии 29.0.2 или выше

4. **Настройте переменные окружения:**
   ```powershell
   $env:JAVA_HOME = "C:\Program Files\Java\jdk-11"
   $env:ANDROID_HOME = "C:\Users\ВашеИмя\AppData\Local\Android\Sdk"
   $env:PATH += ";$env:ANDROID_HOME\platform-tools;$env:ANDROID_HOME\tools"
   ```

#### На Linux:
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip openjdk-11-jdk
sudo apt-get install -y android-sdk
```

### Шаг 2: Установка Pygame Subset for Android

```bash
# Клонируйте репозиторий pgs4a
git clone https://github.com/pygame/pygame_sdl2
cd pygame_sdl2
python setup.py install

# Клонируйте rapt (Renpy Android Packaging Tool)
cd ..
git clone https://github.com/renpy/rapt
cd rapt
```

Или используйте готовую версию:
```bash
pip install python-for-android
```

## 🔨 Процесс сборки

### Вариант A: Использование rapt (рекомендуется)

1. **Настройте rapt:**
   ```bash
   cd rapt
   ./android.py installsdk
   ```

2. **Создайте проект:**
   ```bash
   ./android.py configure "Snake Game" com.snakegame.pygame
   ```

3. **Скопируйте файлы игры:**
   ```bash
   # Скопируйте ваш Snake Game.py в rapt/game/
   cp "path/to/Snake Game.py" game/main.py
   
   # Скопируйте все ресурсы (звуки, изображения)
   cp -r assets game/
   cp settings.json game/
   ```

4. **Соберите APK:**
   ```bash
   # Debug версия (для тестирования)
   ./android.py build "Snake Game" debug
   
   # Release версия (для публикации)
   ./android.py build "Snake Game" release
   ```

5. **Найдите APK:**
   - Debug: `rapt/bin/SnakeGame-debug.apk`
   - Release: `rapt/bin/SnakeGame-release-unsigned.apk`

### Вариант B: Использование python-for-android

1. **Установите зависимости:**
   ```bash
   pip install python-for-android
   pip install buildozer
   ```

2. **Создайте buildozer.spec:**
   ```bash
   buildozer init
   ```

3. **Отредактируйте buildozer.spec:**
   ```ini
   [app]
   title = Snake Game
   package.name = snakegame
   package.domain = com.pygame
   source.dir = .
   source.include_exts = py,png,jpg,mp3,wav,json
   version = 1.0
   requirements = python3,pygame
   orientation = portrait
   android.permissions = 
   android.api = 29
   android.minapi = 21
   ```

4. **Соберите APK:**
   ```bash
   buildozer -v android debug
   ```

## 📲 Установка на устройство

### Через USB:
```bash
# Включите режим разработчика на Android
# Включите отладку по USB

# Установите APK
adb install bin/SnakeGame-debug.apk

# Или напрямую через buildozer
buildozer android deploy run
```

### Ручная установка:
1. Скопируйте APK на устройство
2. Откройте файл на Android
3. Разрешите установку из неизвестных источников
4. Установите приложение

## 🧪 Тестирование на ПК

Вы можете протестировать сенсорное управление на ПК с помощью мыши:

```bash
python "Snake Game.py"
```

Кликайте мышью в разные части экрана:
- **Верх экрана** → змейка идет вверх
- **Низ экрана** → змейка идет вниз
- **Лево** → змейка идет влево
- **Право** → змейка идет вправо

## ⚙️ Настройка конфигурации

Файл `.android.json` содержит настройки приложения:

```json
{
    "package": "com.snakegame.pygame",
    "name": "Snake Game",
    "version": "1.0",
    "numeric_version": 1,
    "orientation": "portrait",
    "permissions": [],
    "include_pil": false,
    "include_sqlite": false
}
```

## 🐛 Решение проблем

### Ошибка: "android module not found"
- **Решение:** Это нормально на ПК. Игра автоматически определит платформу.

### Ошибка: "SDK not found"
- **Решение:** Установите ANDROID_HOME:
  ```bash
  export ANDROID_HOME=/path/to/android/sdk
  ```

### APK не устанавливается
- **Решение:** 
  1. Включите "Неизвестные источники" в настройках Android
  2. Проверьте подпись APK
  3. Используйте debug версию для тестирования

### Игра тормозит на Android
- **Решение:**
  1. Уменьшите размер окна
  2. Уменьшите сложность
  3. Отключите звук в настройках

## 📝 Примечания

1. **Размер APK:** ~15-25 МБ (зависит от ресурсов)
2. **Минимальная версия Android:** 5.0 (API 21)
3. **Рекомендуемая версия Android:** 10+ (API 29)
4. **Производительность:** Отлично на всех современных устройствах

## 🚀 Публикация в Google Play

1. Создайте release версию
2. Подпишите APK своим ключом
3. Создайте аккаунт разработчика Google Play ($25)
4. Загрузите APK в консоль
5. Заполните описание и скриншоты
6. Отправьте на модерацию

## 📞 Поддержка

Если возникли проблемы:
- Проверьте логи: `adb logcat | grep python`
- Создайте issue в репозитории
- Проверьте документацию pygame_sdl2

---

**Удачи в разработке! 🎮🐍**
