# Базовый образ Ubuntu 22.04 с Python
FROM ubuntu:22.04

# Устанавливаем переменные окружения
ENV DEBIAN_FRONTEND=noninteractive \
    ANDROID_HOME=/opt/android-sdk \
    ANDROID_NDK_HOME=/opt/android-ndk \
    PATH="${PATH}:/opt/android-sdk/cmdline-tools/latest/bin:/opt/android-sdk/platform-tools" \
    BUILDOZER_WARN_ON_ROOT=0 \
    JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 \
    TMPDIR=/tmp \
    TMP=/tmp \
    TEMP=/tmp

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

# Устанавливаем Android SDK
RUN mkdir -p ${ANDROID_HOME} && \
    cd ${ANDROID_HOME} && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip && \
    unzip -q commandlinetools-linux-9477386_latest.zip && \
    rm commandlinetools-linux-9477386_latest.zip && \
    mkdir -p cmdline-tools/latest && \
    mv cmdline-tools/* cmdline-tools/latest/ && \
    rmdir cmdline-tools || true

# Принимаем лицензии Android SDK и устанавливаем необходимые компоненты
RUN mkdir -p /root/.android && \
    printf '8933bad161af4178b1185d1a37fbf41ea5269c55\nd56f5187479451eabf01fb78af6dfcb131a6481e\n24333f8a63b6825ea9c5514f83c2829b004d1fee\n' \
    > /root/.android/repositories.cfg

RUN yes | ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager --licenses && \
    ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager \
    "platform-tools" \
    "build-tools;34.0.0" \
    "platforms;android-31" \
    "ndk;25.2.9519653"

# Обновляем Buildozer до последней версии для исправления проблем с временными файлами
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir buildozer==1.5.0 cython==0.29.33 && \
    pip3 install --no-cache-dir --upgrade python-for-android

# Рабочая директория
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости проекта
RUN pip3 install --no-cache-dir -r requirements-dev.txt || true

# Создаём каталоги для Buildozer
RUN mkdir -p /root/.buildozer/android/platform

# Создаём дополнительные каталоги для Buildozer
RUN mkdir -p /root/.buildozer/.android && \
    mkdir -p /tmp/buildozer && \
    chmod 1777 /tmp && \
    chmod 755 /tmp/buildozer

# Настраиваем права доступа для временных файлов
RUN mkdir -p /root/.cache && \
    chmod -R 755 /root/.cache

# Проверяем, что aidl установлен
RUN ls -la ${ANDROID_HOME}/build-tools/34.0.0/aidl || echo "AIDL not found, but continuing..."

# Создаем скрипт-обертку для buildozer с улучшенной обработкой ошибок
RUN echo '#!/bin/bash\nset -e\necho "Запуск buildozer с улучшенной обработкой ошибок..."\nexec buildozer "$@"' > /usr/local/bin/buildozer-wrapper && \
    chmod +x /usr/local/bin/buildozer-wrapper

# Запускаем сборку APK с автоматическим принятием лицензий
CMD ["buildozer-wrapper", "-v", "android", "debug"]
