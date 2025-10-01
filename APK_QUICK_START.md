# 🚀 Быстрый старт: Создание APK

## 📱 Самый простой способ (рекомендуется)

### Вариант 1: Buildozer (проще всего!)

**Шаг 1:** Установите buildozer (только Linux/WSL/Mac)

```bash
# Установка зависимостей
pip install buildozer

# Если на Windows, используйте WSL (Windows Subsystem for Linux)
wsl --install
```

**Шаг 2:** Создайте buildozer.spec

Я уже создал для вас файл `buildozer.spec` - он готов к использованию!

**Шаг 3:** Соберите APK

```bash
cd snake-pygame
buildozer android debug

# APK будет здесь: bin/snakegame-0.1-debug.apk
```

**Время сборки:** 15-30 минут (первый раз), 5-10 минут (последующие)

---

## 🖥️ Альтернатива для Windows (без WSL)

### Вариант 2: Python-for-Android на Windows

**Проблема:** Python-for-Android не работает нативно на Windows.

**Решения:**

#### A. Используйте виртуальную машину Ubuntu:
1. Установите VirtualBox
2. Создайте VM с Ubuntu 20.04+
3. Следуйте инструкциям для Linux (вариант 1)

#### B. Используйте GitHub Actions (сборка в облаке):

Я создал для вас готовый workflow! Просто:

1. Загрузите проект на GitHub
2. GitHub автоматически соберет APK
3. Скачайте готовый APK из Artifacts

---

## 🎯 Мой выбор: Что использовать?

### ✅ Для Windows 10/11:
**WSL + Buildozer** - самый простой способ!

```powershell
# 1. Включите WSL
wsl --install -d Ubuntu-20.04

# 2. Перезагрузите компьютер

# 3. Запустите Ubuntu
wsl

# 4. В Ubuntu установите buildozer
sudo apt update
sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --upgrade buildozer cython==0.29.33

# 5. Перейдите в папку проекта
cd /mnt/c/Users/Зал\ Царства/papka/snake-pygame

# 6. Соберите APK
buildozer android debug
```

**Время:** ~20 минут первая сборка

---

## 📋 Что нужно для сборки

### Минимальные требования:

- ✅ **ОС:** Linux / WSL / MacOS
- ✅ **RAM:** 4GB+ (рекомендуется 8GB)
- ✅ **Диск:** 5GB свободного места
- ✅ **Интернет:** для скачивания SDK и NDK

### Что будет установлено автоматически:

- Android SDK
- Android NDK
- Pygame для Android
- Все зависимости Python

---

## 🔧 Troubleshooting

### Ошибка: "buildozer: command not found"

```bash
pip3 install --user buildozer
export PATH=$PATH:~/.local/bin
```

### Ошибка: "SDK not found"

```bash
buildozer android clean
rm -rf .buildozer
buildozer android debug
```

### Ошибка: "Permission denied"

```bash
chmod +x ~/.buildozer/android/platform/android-sdk/tools/bin/*
```

---

## 🎮 Тестирование APK

### На эмуляторе:

```bash
# Установите Android Studio
# Создайте виртуальное устройство (AVD)
# Запустите эмулятор

# Установите APK
adb install bin/snakegame-0.1-debug.apk
```

### На реальном устройстве:

1. Включите "Режим разработчика" на Android:
   - Настройки → О телефоне → 7 раз нажмите "Номер сборки"
2. Включите "Отладка по USB"
3. Подключите телефон к ПК
4. Установите APK:

```bash
adb install bin/snakegame-0.1-debug.apk
```

Или просто скопируйте APK на телефон и откройте!

---

## 🚀 Release версия (для публикации)

### Создание подписанного APK:

```bash
# 1. Создайте keystore (один раз)
keytool -genkey -v -keystore snake-game.keystore -alias snake -keyalg RSA -keysize 2048 -validity 10000

# 2. Соберите release APK
buildozer android release

# 3. Подпишите APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore snake-game.keystore bin/snakegame-0.1-release-unsigned.apk snake

# 4. Оптимизируйте APK
zipalign -v 4 bin/snakegame-0.1-release-unsigned.apk bin/snakegame-0.1-release.apk
```

---

## 📊 Размер APK

Ожидаемый размер:
- **Debug:** ~15-25 MB
- **Release:** ~10-18 MB

Зависит от:
- Pygame библиотеки: ~8-12 MB
- Ваш код и ресурсы: ~2-5 MB
- Android runtime: ~5-8 MB

---

## ⏱️ Время сборки

- **Первая сборка:** 15-30 минут (скачивание SDK/NDK)
- **Последующие сборки:** 2-5 минут
- **После изменений кода:** 1-3 минуты

---

## 🎯 Готовые решения

Не хотите возиться с настройкой?

### Вариант 3: Используйте онлайн-сервисы

#### A. **Pydroid 3** (приложение для Android):
1. Установите Pydroid 3 на телефон
2. Установите Pygame в Pydroid
3. Скопируйте код игры
4. Запустите прямо на телефоне!

#### B. **Google Colab** (бесплатно):
1. Откройте Google Colab
2. Загрузите мой notebook (создам отдельно)
3. Запустите ячейки
4. Скачайте готовый APK

#### C. **GitHub Actions** (автоматическая сборка):
1. Пушните код на GitHub
2. GitHub Actions соберет APK автоматически
3. Скачайте из Artifacts

---

## 🆘 Нужна помощь?

### Я могу помочь с:

1. ✅ Настройкой buildozer.spec
2. ✅ Созданием GitHub Actions workflow
3. ✅ Решением проблем при сборке
4. ✅ Оптимизацией размера APK
5. ✅ Подписанием release версии

### Что вы хотите использовать?

**Вариант 1:** WSL + Buildozer (рекомендуется) ⭐
**Вариант 2:** GitHub Actions (самый простой)
**Вариант 3:** Виртуальная машина Linux

Скажите, какой вариант вам больше подходит, и я подготовлю детальные инструкции!

---

## 📝 Примечания

- ⚠️ **pgs4a устарел** - используйте buildozer
- ✅ **Ваш код уже готов** для Android
- 🎮 **Все функции работают**: меню, музыка, сохранения, таблица лидеров
- 📱 **Минимальная версия Android:** 5.0+ (API 21+)
- 🌐 **Интернет нужен только** для онлайн таблицы лидеров

**Готовы начать? Выбирайте вариант! 🚀**
