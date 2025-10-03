#!/bin/bash
# ==============================================================================
# СКРИПТ ДЛЯ ГАРАНТИРОВАННОЙ СБОРКИ APK ЧЕРЕЗ DOCKER (Linux/Mac)
# ==============================================================================
# Использование:
#   ./build-apk.sh              # Обычная сборка
#   ./build-apk.sh --clean      # Сборка с очисткой предыдущих артефактов
#   ./build-apk.sh --no-build   # Только создать образ, не собирать APK
#   ./build-apk.sh --use-cache  # Использовать кэш Docker (быстрее)
# ==============================================================================

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

function print_success() { echo -e "${GREEN}$1${NC}"; }
function print_info() { echo -e "${CYAN}$1${NC}"; }
function print_warning() { echo -e "${YELLOW}$1${NC}"; }
function print_error() { echo -e "${RED}$1${NC}"; }

# Параметры
CLEAN_BUILD=0
NO_BUILD=0
USE_CACHE=1

# Парсинг аргументов
while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN_BUILD=1
            shift
            ;;
        --no-build)
            NO_BUILD=1
            shift
            ;;
        --use-cache)
            USE_CACHE=0
            shift
            ;;
        *)
            print_error "❌ Неизвестный параметр: $1"
            echo "Использование: $0 [--clean] [--no-build] [--use-cache]"
            exit 1
            ;;
    esac
done

print_info "========================================="
print_info "🚀 Snake Game APK Builder"
print_info "========================================="
echo ""

# Проверка Docker
print_info "🔍 Проверка Docker..."
if ! command -v docker &> /dev/null; then
    print_error "❌ Docker не установлен!"
    print_error "   Установите Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

DOCKER_VERSION=$(docker --version)
print_success "✅ Docker найден: $DOCKER_VERSION"
echo ""

# Определяем имена
IMAGE_NAME="snakegame-builder"
CONTAINER_NAME="snakegame-build"

# Шаг 1: Сборка Docker образа
print_info "========================================="
print_info "📦 Шаг 1: Создание Docker образа"
print_info "========================================="

DOCKER_BUILD_ARGS="build -f Dockerfile.production -t $IMAGE_NAME"

if [ $USE_CACHE -eq 1 ]; then
    DOCKER_BUILD_ARGS="$DOCKER_BUILD_ARGS --no-cache"
    print_warning "⚠️  Кэш Docker отключен (сборка займет больше времени)"
fi

DOCKER_BUILD_ARGS="$DOCKER_BUILD_ARGS ."

print_info "Команда: docker $DOCKER_BUILD_ARGS"
echo ""

if ! docker $DOCKER_BUILD_ARGS; then
    print_error "❌ Ошибка при создании Docker образа"
    exit 1
fi

print_success "✅ Docker образ создан успешно"
echo ""

# Если указан флаг NO_BUILD, останавливаемся
if [ $NO_BUILD -eq 1 ]; then
    print_success "✅ Docker образ создан. Сборка APK пропущена (флаг --no-build)"
    exit 0
fi

# Шаг 2: Запуск сборки APK
print_info "========================================="
print_info "🔨 Шаг 2: Сборка APK"
print_info "========================================="

# Удаляем старый контейнер
print_info "🧹 Очистка предыдущих контейнеров..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

# Подготовка переменных окружения
ENV_VARS=""
if [ $CLEAN_BUILD -eq 1 ]; then
    ENV_VARS="-e CLEAN_BUILD=1"
    print_warning "⚠️  Режим CLEAN BUILD активирован"
fi

# Запуск сборки
print_info "🏗️  Запуск сборки в контейнере..."
echo ""

if ! docker run --name $CONTAINER_NAME -v "$(pwd):/app" $ENV_VARS $IMAGE_NAME; then
    print_error "❌ Ошибка при сборке APK"
    print_warning "💡 Проверьте логи: buildozer_full.log"
    
    # Копируем логи
    print_info "📄 Копирование логов..."
    docker cp "$CONTAINER_NAME:/app/buildozer_full.log" "./buildozer_full.log" 2>/dev/null || true
    
    exit 1
fi

echo ""
print_success "✅ APK собран успешно!"

# Шаг 3: Извлечение APK
print_info ""
print_info "========================================="
print_info "📦 Шаг 3: Извлечение APK"
print_info "========================================="

# Копируем bin директорию
print_info "📥 Копирование файлов..."
if ! docker cp "$CONTAINER_NAME:/app/bin" "./bin"; then
    print_error "❌ Ошибка при извлечении APK из контейнера"
    exit 1
fi

# Проверяем наличие APK
if ls ./bin/*.apk 1> /dev/null 2>&1; then
    echo ""
    print_success "========================================="
    print_success "🎉 УСПЕШНО! APK ГОТОВ!"
    print_success "========================================="
    echo ""
    
    for apk in ./bin/*.apk; do
        SIZE=$(du -h "$apk" | cut -f1)
        print_info "📱 Файл: $(basename "$apk")"
        print_info "   Размер: $SIZE"
        print_info "   Путь: $apk"
    done
    
    echo ""
    print_success "✅ APK готов к установке на Android устройство!"
    print_info "💡 Для установки: adb install bin/*.apk"
else
    print_warning "⚠️  APK файлы не найдены в директории bin/"
fi

# Очистка
echo ""
print_info "🧹 Очистка контейнера..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

echo ""
print_success "========================================="
print_success "✅ Процесс завершен"
print_success "========================================="
