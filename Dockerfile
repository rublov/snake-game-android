# Базовый образ Ubuntu 22.04 с Python
FROM ubuntu:22.04

# Устанавливаем переменные окружения
ENV DEBIAN_FRONTEND=noninteractive \
    ANDROID_HOME=/opt/android-sdk \
    ANDROID_NDK_HOME=/opt/android-ndk \
    PATH="${PATH}:/opt/android-sdk/cmdline-tools/latest/bin:/opt/android-sdk/platform-tools"

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv \
    git zip unzip wget curl \
    openjdk-17-jdk \
    build-essential ccache \
    libffi-dev libssl-dev \
    zlib1g-dev libncurses5-dev libncursesw5-dev \
    libreadline-dev libsqlite3-dev libbz2-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Buildozer и Cython
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir buildozer==1.5.0 cython==0.29.33

# Рабочая директория
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости проекта
RUN pip3 install --no-cache-dir -r requirements-dev.txt || true

# Создаём каталоги для Buildozer
RUN mkdir -p /root/.buildozer/android/platform

# Запускаем сборку APK
CMD ["buildozer", "-v", "android", "debug"]
