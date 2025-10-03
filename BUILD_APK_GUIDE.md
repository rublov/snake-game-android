# 📱 Гарантированная Сборка APK для Snake Game

## 🎯 Обзор

Этот проект содержит **production-ready конфигурацию** для сборки Android APK через Docker + Buildozer с **гарантией успешной сборки**.

### ✨ Ключевые особенности:

- ✅ **Изолированная сборка** в Docker контейнере
- ✅ **Воспроизводимые результаты** (фиксированные версии всех зависимостей)
- ✅ **Простой запуск** одной командой
- ✅ **Подробные логи** для отладки
- ✅ **Kivy-based** приложение (нативная поддержка Android)
- ✅ **Поддержка Windows, Linux, Mac**

---

## 🚀 Быстрый Старт

### Предварительные требования:

1. **Docker Desktop** установлен и запущен
   - Windows/Mac: https://www.docker.com/products/docker-desktop
   - Linux: `sudo apt install docker.io`

2. **Минимум 10 GB** свободного места на диске

3. **Стабильное интернет-соединение** (первая сборка скачает ~2GB зависимостей)

---

## 📋 Пошаговая Инструкция

### Windows:

```powershell
# 1. Открыть PowerShell в директории проекта
cd "C:\Users\Зал Царства\papka\snake-pygame"

# 2. Запустить сборку
.\build-apk.ps1

# 3. Дождаться завершения (20-40 минут при первом запуске)

# 4. Найти готовый APK в папке bin/
```

### Linux/Mac:

```bash
# 1. Открыть терминал в директории проекта
cd ~/snake-pygame

# 2. Дать права на выполнение скрипта
chmod +x build-apk.sh

# 3. Запустить сборку
./build-apk.sh

# 4. Дождаться завершения

# 5. Найти готовый APK в папке bin/
```

---

## 🛠️ Параметры Сборки

### PowerShell (Windows):

```powershell
# Обычная сборка
.\build-apk.ps1

# Сборка с очисткой предыдущих артефактов
.\build-apk.ps1 -Clean

# Только создать Docker образ (без сборки APK)
.\build-apk.ps1 -NoBuild

# Использовать кэш Docker (быстрее)
.\build-apk.ps1 -UseCache
```

### Bash (Linux/Mac):

```bash
# Обычная сборка
./build-apk.sh

# Сборка с очисткой
./build-apk.sh --clean

# Только Docker образ
./build-apk.sh --no-build

# С кэшем
./build-apk.sh --use-cache
```

---

## 📦 Структура Проекта

```
snake-pygame/
├── main_android.py              # ✨ Entry point для Android
├── buildozer_production.spec    # ✨ Production конфигурация
├── Dockerfile.production        # ✨ Docker образ для сборки
├── build-apk.ps1               # ✨ Скрипт сборки (Windows)
├── build-apk.sh                # ✨ Скрипт сборки (Linux/Mac)
├── snake_game/                 # Исходный код игры
│   ├── ui/
│   │   └── kivy_app.py        # Kivy UI для Android
│   ├── core/
│   │   └── game.py            # Игровая логика
│   └── services/
│       ├── session.py         # Сессия игры
│       └── audio.py           # Звуковой менеджер
└── bin/                        # ✨ Готовые APK файлы (после сборки)
```

---

## 🔧 Техническая Информация

### Используемые технологии:

- **Python**: 3.10
- **Kivy**: 2.2.1 (UI framework для Android)
- **Buildozer**: 1.5.0 (инструмент сборки APK)
- **Python-for-Android**: latest
- **Android API**: 31 (Android 12)
- **NDK**: 25.2.9519653
- **Архитектуры**: arm64-v8a, armeabi-v7a

### Размер APK:

- **Debug APK**: ~20-30 MB
- **Release APK**: ~15-25 MB (после оптимизации)

### Время сборки:

- **Первый запуск**: 30-50 минут (скачивание зависимостей)
- **Последующие**: 10-20 минут (с кэшем)

---

## 🐛 Решение Проблем

### 1. Docker не запускается

**Проблема**: Ошибка "Docker not found"

**Решение**:
```powershell
# Проверить установлен ли Docker
docker --version

# Если не установлен - установить Docker Desktop
```

### 2. Недостаточно места на диске

**Проблема**: "No space left on device"

**Решение**:
```powershell
# Очистить Docker кэш
docker system prune -a

# Освободить минимум 10GB места
```

### 3. Ошибка при сборке APK

**Проблема**: Buildozer завершается с ошибкой

**Решение**:
```powershell
# Посмотреть полный лог
type buildozer_full.log

# Попробовать чистую сборку
.\build-apk.ps1 -Clean
```

### 4. APK не устанавливается на устройство

**Проблема**: "App not installed" при установке

**Решение**:
- Включить "Неизвестные источники" в настройках Android
- Проверить подпись APK
- Использовать `adb install -r bin/snakegame-*.apk`

---

## 📱 Установка APK на Android

### Метод 1: ADB (Android Debug Bridge)

```bash
# 1. Установить ADB (если еще не установлен)
# Windows: scoop install adb
# Linux: sudo apt install adb
# Mac: brew install android-platform-tools

# 2. Включить USB-отладку на Android устройстве

# 3. Подключить устройство через USB

# 4. Установить APK
adb install bin/snakegame-*.apk
```

### Метод 2: Прямая Передача

1. Скопировать APK файл на устройство (через USB, email, облако)
2. Открыть APK через файловый менеджер
3. Разрешить установку из неизвестных источников
4. Установить приложение

---

## 🎮 Управление в Игре

- **Стрелки** или **Свайп**: Управление змейкой
- **P / Пауза**: Пауза игры
- **R**: Перезапуск игры

---

## 📝 Логи и Отладка

### Просмотр логов сборки:

```powershell
# Полный лог Buildozer
type buildozer_full.log

# Последние 100 строк
Get-Content buildozer_full.log -Tail 100
```

### Просмотр логов приложения на Android:

```bash
# Подключиться к logcat
adb logcat -s python

# Сохранить логи в файл
adb logcat -s python > android_logs.txt
```

---

## 🔄 Обновление Конфигурации

### Изменить название приложения:

Отредактировать `buildozer_production.spec`:

```ini
[app]
title = Ваше Название
package.name = yourpackagename
package.domain = com.yourcompany
```

### Изменить иконку и сплэш:

```ini
[app]
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/splash.png
```

### Добавить разрешения Android:

```ini
[app]
android.permissions = INTERNET,ACCESS_NETWORK_STATE,CAMERA,VIBRATE
```

---

## 🚀 Production Release

Для выпуска в Google Play:

```bash
# 1. Создать keystore
keytool -genkey -v -keystore my-release-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000

# 2. Изменить buildozer.spec для release
[app]
android.release_artifact = apk

# 3. Собрать release APK
buildozer android release

# 4. Подписать APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore bin/*.apk my-key-alias

# 5. Выровнять APK
zipalign -v 4 bin/snakegame-*.apk bin/snakegame-release-aligned.apk
```

---

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `buildozer_full.log`
2. Убедитесь, что Docker запущен
3. Попробуйте чистую сборку: `.\build-apk.ps1 -Clean`
4. Проверьте наличие свободного места (минимум 10GB)

---

## 📄 Лицензия

Этот проект использует лицензию MIT.

---

## ✅ Чек-лист Готовности

Перед сборкой убедитесь:

- [ ] Docker установлен и запущен
- [ ] Минимум 10GB свободного места
- [ ] Стабильное интернет-соединение
- [ ] Все файлы проекта на месте
- [ ] PowerShell/Bash имеет права на выполнение

**После этого просто запустите скрипт сборки и дождитесь результата!** 🎉
