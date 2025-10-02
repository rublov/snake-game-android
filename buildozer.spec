[app]

# Название приложения
title = Snake Game

# Имя пакета (используется в Java/Android)
package.name = snakegame

# Домен (можно указать любой обратный домен)
package.domain = com.pygame

# Папка с исходниками (текущая директория)
source.dir = .

# Какие файлы включать в сборку
source.include_exts = py,png,jpg,kv,atlas,json,mp3,wav

# Версия приложения
version = 1.0

# Зависимости (Kivy, Python и прочее)
requirements = python3,kivy==2.2.1,pyjnius,requests

# Модули Kivy Garden, если нужны (оставим пустым — нет)
garden_requirements =

# Ветка p4a (используется "develop", можно сменить на "master")
p4a.branch = develop

# Сплэш-экран
presplash.filename = %(source.dir)s/splash.png

# Иконка (если нужно, раскомментируй)
# icon.filename = %(source.dir)s/icon.png

# Ориентация экрана
orientation = portrait

# Полноэкранный режим
fullscreen = 1

# Разрешения Android
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Целевая версия API Android
android.api = 31

# Минимальная поддерживаемая версия API
android.minapi = 21

# Версия NDK
android.ndk = 25b

# Версия Build-tools
android.build_tools_version = 34.0.0

# Использовать приватное хранилище приложения
android.private_storage = True

# Фильтры logcat
android.logcat_filters = *:S python:D

# Копировать библиотеки внутрь APK
android.copy_libs = 1

# Архитектура Android (64-бит ARM)
android.archs = arm64-v8a

# Требуемая версия Kivy
kivy.require = 2.2.1

# Отключаем SVG (опционально)
kivy.graphics.svg = 0

# Настройки Kivy (оптимизация)
kivy.skip_gl_redirect = 0
kivy.no_config = 1
kivy.no_use_deprecation = 1


[buildozer]

# Уровень логов (0 = только ошибки, 1 = инфо, 2 = отладка)
log_level = 2

# Показывать предупреждение при запуске от root
warn_on_root = 1
