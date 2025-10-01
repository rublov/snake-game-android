# 🎯 APK - Краткая инструкция для PGS4A

## ✅ Что готово

- ✅ `.android.json` - настроен (разрешения интернета, иконка, splash)
- ✅ `icon.png` - создан (512x512)
- ✅ `splash.png` - создан (720x1280)
- ✅ Код игры адаптирован для Android
- ✅ Touch управление работает

## 🚀 Три способа получить APK

### 🥇 Вариант 1: Pydroid 3 (БЕЗ сборки APK)

**Самый простой - запуск на Android без компьютера!**

1. Скачайте **Pydroid 3** из Google Play
2. В Pydroid установите: `pip install pygame`
3. Скопируйте все файлы игры на телефон
4. Откройте `Snake Game.py` в Pydroid
5. Нажмите ▶ Play

**Время:** 5 минут
**Плюс:** Работает сразу
**Минус:** Это не APK, а запуск через Pydroid

---

### 🥈 Вариант 2: RAPT (настоящий APK)

**Для тех, кто хочет полноценное APK приложение**

#### Что нужно:
- Python 3.8+
- Java JDK 11
- Android SDK
- RAPT tool

#### Быстрая установка (Windows):

```powershell
# 1. Установите Java
# Скачайте: https://adoptium.net/temurin/releases/
# Выберите: JDK 11 (LTS)

# 2. Установите Android Studio (проще всего)
# Скачайте: https://developer.android.com/studio
# SDK установится автоматически

# 3. Настройте переменные окружения
setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-11.0.XX-hotspot"
setx ANDROID_HOME "%LOCALAPPDATA%\Android\Sdk"

# 4. Скачайте RAPT
git clone https://github.com/renpy/rapt.git
cd rapt

# 5. Настройте RAPT
python android.py installsdk

# 6. Соберите APK
cd "C:\Users\Зал Царства\papka\snake-pygame"
python "C:\путь\к\rapt\android.py" build "Snake Game" com.snakegame.pygame
```

**APK будет здесь:** `rapt\bin\SnakeGame-1.0-debug.apk`

**Время первой сборки:** 15-30 минут
**Размер APK:** ~15-20 MB

#### Установка APK на телефон:

```bash
# Через ADB (если телефон подключен по USB)
adb install rapt\bin\SnakeGame-1.0-debug.apk

# Или просто скопируйте APK на телефон и откройте
```

---

### 🥉 Вариант 3: Онлайн сборка (без установки)

**Если не хочется ничего устанавливать**

#### GitHub Actions (автоматическая сборка в облаке):

1. Загрузите проект на GitHub
2. GitHub Actions соберет APK автоматически
3. Скачайте готовый APK

Я могу создать готовый workflow файл, если нужно!

---

## 📱 Текущая конфигурация

### .android.json:
```json
{
    "package": "com.snakegame.pygame",
    "name": "Snake Game",
    "version": "1.0",
    "orientation": "portrait",
    "permissions": ["INTERNET", "ACCESS_NETWORK_STATE"],
    "icon": "icon.png",
    "presplash": "splash.png"
}
```

### Файлы для APK:
- ✅ `Snake Game.py` - основной код
- ✅ `leaderboard.py` - таблица лидеров
- ✅ `create_splash.py` - генератор заставки
- ✅ `icon.png` - иконка приложения (512x512)
- ✅ `splash.png` - заставка при загрузке (720x1280)
- ✅ `settings.json` - сохранения
- ✅ `assets/` - музыка и ресурсы
- ✅ `.android.json` - конфигурация Android

---

## 🔧 Быстрое решение проблем

### "Java not found"
```powershell
java -version
# Если не работает - переустановите Java и добавьте в PATH
```

### "Android SDK not found"
```powershell
echo %ANDROID_HOME%
# Должен показать путь к SDK
```

### "Permission denied" (Linux)
```bash
chmod +x rapt/android.py
```

### "Build failed"
```bash
# Очистите кэш и попробуйте снова
rm -rf .android/
rm -rf bin/
```

---

## 🎮 Что будет работать в APK

- ✅ Все игровые режимы (MVP, MVP2, Survival, Map)
- ✅ Touch управление (тап для смены направления)
- ✅ Музыка и звуки
- ✅ Сохранения настроек
- ✅ Splash screen при запуске
- ✅ Таблица лидеров (онлайн/оффлайн)
- ✅ Пауза при сворачивании приложения

---

## 📊 Ожидаемые характеристики APK

- **Размер:** ~15-20 MB
- **Минимальный Android:** 5.0+ (API 21+)
- **Целевой Android:** 12 (API 31)
- **Архитектуры:** armeabi-v7a, arm64-v8a
- **Разрешения:** INTERNET (для таблицы лидеров)

---

## 💡 Мои рекомендации

### Для тестирования:
👉 **Pydroid 3** - запустите игру за 5 минут без сборки

### Для распространения:
👉 **RAPT** - соберите настоящий APK

### Для публикации в Google Play:
👉 Нужен **release APK** с подписью (об этом отдельно)

---

## 📝 Следующие шаги

Выберите вариант:

**A. Хочу попробовать на телефоне прямо сейчас:**
→ Используйте Pydroid 3

**B. Хочу собрать APK для друзей:**
→ Установите RAPT и соберите debug APK

**C. Хочу опубликовать в Google Play:**
→ Нужен release APK с подписью (требуется дополнительная настройка)

**D. Не хочу возиться с установкой:**
→ Могу помочь настроить GitHub Actions для автоматической сборки

---

**Скажите, какой вариант вам подходит, и я помогу с деталями! 🚀**
