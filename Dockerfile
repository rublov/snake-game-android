# Используем проверенный образ с Buildozer и всеми зависимостями
FROM kivy/buildozer:1.5.0

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements-dev.txt

# Создаём каталоги для кеша Buildozer
RUN mkdir -p /root/.buildozer/android/platform

# Запускаем сборку APK
CMD ["buildozer", "-v", "android", "debug"]
