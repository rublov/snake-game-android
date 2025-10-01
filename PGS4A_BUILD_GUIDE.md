# 🎮 Сборка APK с помощью PGS4A (Pygame Subset for Android)

## 📋 Что такое PGS4A?

**PGS4A** (Pygame Subset for Android) - это самый простой способ портировать Pygame игры на Android. 
Мы уже добавили поддержку - ваша игра готова к сборке!

## ✅ Что уже готово

У вас есть файл `.android.json` с настройками:

```json
{
    "package": "com.snakegame.pygame",
    "name": "Snake Game",
    "version": "1.0",
    "orientation": "portrait"
}
```

✅ Код игры уже адаптирован (добавлены ~50 строк Android поддержки)
✅ Все функции работают: меню, музыка, сохранения, таблица лидеров
✅ Touch управление реализовано

## 🚀 Быстрый старт (3 варианта)

### Вариант 1: Использовать готовый сервис (самый простой) ⭐

**Pydroid 3** - приложение для запуска Python на Android:

1. **Скачайте Pydroid 3** с Google Play
2. **Установите Pygame** в Pydroid:
   ```
   pip install pygame
   ```
3. **Скопируйте файлы игры** на телефон
4. **Запустите** `Snake Game.py` в Pydroid

**Плюсы:** 
- ✅ Не нужен компьютер
- ✅ Работает сразу
- ✅ Все функции работают

**Минусы:**
- ❌ Не полноценное APK приложение
- ❌ Нужен Pydroid для запуска

---

### Вариант 2: RAPT (рекомендуется для PGS4A)

**RAPT** (Ren'Py Android Packaging Tool) - официальный инструмент для pgs4a.

#### Требования:
- Python 3.8+
- Java JDK 8 или 11
- Android SDK
- 5GB свободного места

#### Установка на Windows:

**Шаг 1:** Установите Java JDK
```powershell
# Скачайте с https://adoptium.net/
# Выберите: OpenJDK 11 (LTS)
# Установите в: C:\Program Files\Java\jdk-11
```

**Шаг 2:** Скачайте Android SDK
```powershell
# Вариант A: Через Android Studio
# Скачайте: https://developer.android.com/studio
# Установите, в настройках найдите SDK Manager

# Вариант B: Command Line Tools только
# Скачайте: https://developer.android.com/studio#command-tools
# Распакуйте в: C:\Android\cmdline-tools
```

**Шаг 3:** Настройте переменные окружения
```powershell
# Откройте PowerShell от администратора
[Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Java\jdk-11", "User")
[Environment]::SetEnvironmentVariable("ANDROID_HOME", "C:\Users\ВашеИмя\AppData\Local\Android\Sdk", "User")

# Добавьте в PATH
$oldPath = [Environment]::GetEnvironmentVariable("PATH", "User")
$newPath = "$oldPath;$env:JAVA_HOME\bin;$env:ANDROID_HOME\platform-tools"
[Environment]::SetEnvironmentVariable("PATH", $newPath, "User")

# Перезапустите PowerShell
```

**Шаг 4:** Скачайте RAPT
```powershell
# Клонируйте репозиторий
git clone https://github.com/renpy/rapt.git
cd rapt

# Или скачайте ZIP с GitHub
```

**Шаг 5:** Настройте RAPT
```bash
# В папке rapt запустите:
python android.py installsdk

# Выберите компоненты:
# - platform 31 (Android 12)
# - build-tools 31.0.0
# - platform-tools
```

**Шаг 6:** Соберите APK
```bash
# Вернитесь в папку с игрой
cd "C:\Users\Зал Царства\papka\snake-pygame"

# Запустите сборку
python "C:\путь\к\rapt\android.py" build "Snake Game" com.snakegame.pygame --launch

# Или используйте GUI
python "C:\путь\к\rapt\android.py" installsdk
```

**Время сборки:** 10-20 минут (первый раз)

**Где будет APK:**
```
rapt/bin/SnakeGame-1.0-debug.apk
```

---

### Вариант 3: Использовать Linux (проще чем на Windows)

Если у вас есть доступ к Linux компьютеру или виртуальной машине:

```bash
# Установите зависимости
sudo apt-get update
sudo apt-get install -y python3 python3-pip openjdk-11-jdk git

# Клонируйте RAPT
git clone https://github.com/renpy/rapt.git
cd rapt

# Установите SDK
python3 android.py installsdk

# Соберите APK
cd /path/to/snake-pygame
python3 /path/to/rapt/android.py build "Snake Game" com.snakegame.pygame
```

**Время:** 10-15 минут

---

## 📱 Настройка .android.json

Ваш текущий файл `.android.json`:

```json
{
    "package": "com.snakegame.pygame",
    "name": "Snake Game",
    "version": "1.0",
    "numeric_version": 1,
    "orientation": "portrait",
    "permissions": [],
    "include_pil": false,
    "include_sqlite": false,
    "layout": null,
    "icon": null,
    "presplash": null
}
```

### Улучшенная версия:

```json
{
    "package": "com.snakegame.pygame",
    "name": "Snake Game",
    "version": "1.0",
    "numeric_version": 1,
    "orientation": "portrait",
    "permissions": ["INTERNET", "ACCESS_NETWORK_STATE"],
    "include_pil": true,
    "include_sqlite": false,
    "layout": null,
    "icon": "icon.png",
    "presplash": "splash.png"
}
```

**Что изменилось:**
- ✅ Добавлены разрешения для интернета (для таблицы лидеров)
- ✅ Включен PIL (для обработки изображений)
- ✅ Указан presplash (ваш splash.png)

---

## 🎨 Подготовка ресурсов

### Иконка приложения (опционально)

Создайте `icon.png` (512x512 пикселей):

```python
# create_icon.py
from PIL import Image, ImageDraw, ImageFont

# Create 512x512 icon
img = Image.new('RGB', (512, 512), color=(34, 139, 34))
draw = ImageDraw.Draw(img)

# Draw snake emoji or shape
try:
    font = ImageFont.truetype("arial.ttf", 256)
except:
    font = ImageFont.load_default()

text = "🐍"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

x = (512 - text_width) // 2
y = (512 - text_height) // 2

draw.text((x, y), text, fill=(255, 255, 255), font=font)

img.save('icon.png')
print("✓ icon.png создан!")
```

---

## 🔧 Troubleshooting

### Проблема: "Java not found"
```powershell
# Проверьте установку Java
java -version

# Должно показать: openjdk version "11.0.x"
```

### Проблема: "Android SDK not found"
```powershell
# Проверьте ANDROID_HOME
echo $env:ANDROID_HOME

# Должно показать путь к SDK
```

### Проблема: "Permission denied" на Linux
```bash
chmod +x rapt/android.py
```

### Проблема: "Build failed"
```bash
# Очистите кэш
rm -rf .android/
rm -rf bin/

# Попробуйте снова
```

---

## 📊 Ограничения PGS4A

⚠️ **Важно знать:**

1. **Не все функции Pygame поддерживаются**
   - ✅ Работает: display, image, rect, sprite, font, mixer
   - ❌ Не работает: некоторые редкие модули

2. **Производительность**
   - На старых телефонах может быть медленнее
   - Рекомендуется Android 5.0+ (API 21+)

3. **Размер APK**
   - ~15-20 MB (включая Pygame runtime)

4. **Обновления**
   - PGS4A больше не активно развивается
   - Для новых проектов рекомендуется python-for-android

---

## 🎯 Альтернативы PGS4A

Если PGS4A не подходит:

### Python-for-Android (более современный)
```bash
pip install python-for-android
p4a apk --private . --package=com.snakegame.pygame --name="Snake Game" --version=1.0 --bootstrap=pygame --requirements=python3,pygame --permission INTERNET
```

### Buildozer (самый популярный)
```bash
pip install buildozer
buildozer android debug
```

---

## ✅ Итоговый чек-лист

Перед сборкой проверьте:

- [ ] Установлен Java JDK 11
- [ ] Установлен Android SDK
- [ ] Настроены переменные окружения
- [ ] Скачан RAPT
- [ ] Файл `.android.json` настроен
- [ ] Все файлы игры в одной папке
- [ ] Есть `splash.png` (для presplash)
- [ ] (Опционально) Есть `icon.png`

---

## 🚀 Команды для быстрой сборки

```powershell
# Перейдите в папку игры
cd "C:\Users\Зал Царства\papka\snake-pygame"

# Убедитесь что .android.json правильный
cat .android.json

# Запустите RAPT (замените путь на ваш)
python "C:\rapt\android.py" build "Snake Game" com.snakegame.pygame

# APK будет здесь:
# C:\rapt\bin\SnakeGame-1.0-debug.apk
```

---

## 📱 Установка на телефон

### Метод 1: ADB (через USB)
```bash
adb install C:\rapt\bin\SnakeGame-1.0-debug.apk
```

### Метод 2: Прямая установка
1. Скопируйте APK на телефон
2. Откройте файловый менеджер
3. Нажмите на APK
4. Разрешите установку из неизвестных источников
5. Установите!

---

## 🎮 Тестирование

После установки проверьте:

- [ ] Игра запускается
- [ ] Splash screen показывается
- [ ] Меню работает
- [ ] Touch управление работает
- [ ] Музыка играет
- [ ] Сохранения работают
- [ ] Таблица лидеров доступна (с интернетом)

---

## 💡 Советы

1. **Первая сборка долгая** - RAPT скачает SDK и все зависимости (~1-2 GB)
2. **Используйте debug APK** для тестирования
3. **Release APK** нужен только для публикации в Google Play
4. **Размер APK можно уменьшить** исключив неиспользуемую музыку

---

**Готовы начать сборку? Выбирайте вариант и действуйте! 🚀**

Если возникнут проблемы - пишите, помогу разобраться!
