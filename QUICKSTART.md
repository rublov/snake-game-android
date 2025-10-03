# 🚀 Быстрый Старт - Сборка APK

## ⚡ Запуск в 3 команды (Windows)

```powershell
# 1. Убедитесь, что Docker запущен
docker --version

# 2. Запустите сборку
.\build-apk.ps1

# 3. Установите APK
adb install bin\snakegame-*.apk
```

## ⚡ Запуск в 3 команды (Linux/Mac)

```bash
# 1. Убедитесь, что Docker запущен
docker --version

# 2. Запустите сборку
chmod +x build-apk.sh && ./build-apk.sh

# 3. Установите APK
adb install bin/snakegame-*.apk
```

---

## 📋 Что произойдет:

1. ✅ Создастся Docker контейнер с Android SDK/NDK
2. ✅ Установятся Python 3.10, Kivy 2.2.1, Buildozer
3. ✅ Соберется production APK (~20-30 минут)
4. ✅ APK появится в папке `bin/`

---

## ⏱️ Время выполнения:

- **Первый запуск**: 30-50 минут (скачивание ~2GB)
- **Повторные**: 10-20 минут (с кэшем)

---

## 🎯 Требования:

- [x] **Docker Desktop** установлен
- [x] **10+ GB** свободного места
- [x] **Интернет** для скачивания зависимостей

---

## 🆘 Проблемы?

Смотрите полную документацию: **[BUILD_APK_GUIDE.md](BUILD_APK_GUIDE.md)**

Или проверьте логи: `buildozer_full.log`
