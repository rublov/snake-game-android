# ==============================================================================
# СКРИПТ ДЛЯ ГАРАНТИРОВАННОЙ СБОРКИ APK ЧЕРЕЗ DOCKER
# ==============================================================================
# Использование:
#   .\build-apk.ps1              # Обычная сборка
#   .\build-apk.ps1 -Clean       # Сборка с очисткой предыдущих артефактов
#   .\build-apk.ps1 -NoBuild     # Только создать образ, не собирать APK
# ==============================================================================

param(
    [switch]$Clean,      # Очистить предыдущие сборки
    [switch]$NoBuild,    # Только создать Docker образ
    [switch]$UseCache    # Использовать кэш Docker (быстрее)
)

$ErrorActionPreference = "Stop"

# Цвета для вывода
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }
function Write-Error { Write-Host $args -ForegroundColor Red }

Write-Info "========================================="
Write-Info "🚀 Snake Game APK Builder"
Write-Info "========================================="
Write-Host ""

# Проверка Docker
Write-Info "🔍 Проверка Docker..."
try {
    $dockerVersion = docker --version
    Write-Success "✅ Docker найден: $dockerVersion"
} catch {
    Write-Error "❌ Docker не установлен или не запущен!"
    Write-Error "   Установите Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
}

Write-Host ""

# Определяем имя образа и контейнера
$IMAGE_NAME = "snakegame-builder"
$CONTAINER_NAME = "snakegame-build"

# Шаг 1: Сборка Docker образа
Write-Info "========================================="
Write-Info "📦 Шаг 1: Создание Docker образа"
Write-Info "========================================="

$dockerBuildArgs = @(
    "build",
    "-f", "Dockerfile.production",
    "-t", $IMAGE_NAME
)

if (-not $UseCache) {
    $dockerBuildArgs += "--no-cache"
    Write-Warning "⚠️  Кэш Docker отключен (сборка займет больше времени)"
}

$dockerBuildArgs += "."

Write-Info "Команда: docker $($dockerBuildArgs -join ' ')"
Write-Host ""

try {
    & docker $dockerBuildArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Docker build failed"
    }
    Write-Success "✅ Docker образ создан успешно"
} catch {
    Write-Error "❌ Ошибка при создании Docker образа"
    exit 1
}

Write-Host ""

# Если указан флаг NoBuild, останавливаемся здесь
if ($NoBuild) {
    Write-Success "✅ Docker образ создан. Сборка APK пропущена (флаг -NoBuild)"
    exit 0
}

# Шаг 2: Запуск сборки APK
Write-Info "========================================="
Write-Info "🔨 Шаг 2: Сборка APK"
Write-Info "========================================="

# Удаляем старый контейнер если существует
Write-Info "🧹 Очистка предыдущих контейнеров..."
docker rm -f $CONTAINER_NAME 2>$null | Out-Null

# Подготовка переменных окружения
$envVars = @()
if ($Clean) {
    $envVars += "-e", "CLEAN_BUILD=1"
    Write-Warning "⚠️  Режим CLEAN BUILD активирован"
}

# Запуск контейнера для сборки
Write-Info "🏗️  Запуск сборки в контейнере..."
Write-Host ""

try {
    $dockerRunArgs = @(
        "run",
        "--name", $CONTAINER_NAME,
        "-v", "${PWD}:/app"
    ) + $envVars + @($IMAGE_NAME)

    & docker $dockerRunArgs
    
    if ($LASTEXITCODE -ne 0) {
        throw "APK build failed"
    }
    
    Write-Host ""
    Write-Success "✅ APK собран успешно!"
    
} catch {
    Write-Error "❌ Ошибка при сборке APK"
    Write-Warning "💡 Проверьте логи: buildozer_full.log"
    
    # Копируем логи из контейнера
    Write-Info "📄 Копирование логов..."
    docker cp "${CONTAINER_NAME}:/app/buildozer_full.log" "./buildozer_full.log" 2>$null
    
    exit 1
}

# Шаг 3: Извлечение APK из контейнера
Write-Info ""
Write-Info "========================================="
Write-Info "📦 Шаг 3: Извлечение APK"
Write-Info "========================================="

try {
    # Копируем директорию bin с APK
    Write-Info "📥 Копирование файлов..."
    docker cp "${CONTAINER_NAME}:/app/bin" "./bin"
    
    # Проверяем наличие APK
    $apkFiles = Get-ChildItem -Path "./bin" -Filter "*.apk" -ErrorAction SilentlyContinue
    
    if ($apkFiles) {
        Write-Host ""
        Write-Success "========================================="
        Write-Success "🎉 УСПЕШНО! APK ГОТОВ!"
        Write-Success "========================================="
        Write-Host ""
        
        foreach ($apk in $apkFiles) {
            $sizeInMB = [math]::Round($apk.Length / 1MB, 2)
            Write-Info "📱 Файл: $($apk.Name)"
            Write-Info "   Размер: $sizeInMB MB"
            Write-Info "   Путь: $($apk.FullName)"
        }
        
        Write-Host ""
        Write-Success "✅ APK готов к установке на Android устройство!"
        Write-Info "💡 Для установки: adb install bin\*.apk"
        
    } else {
        Write-Warning "⚠️  APK файлы не найдены в директории bin/"
    }
    
} catch {
    Write-Error "❌ Ошибка при извлечении APK из контейнера"
    exit 1
}

# Очистка
Write-Host ""
Write-Info "🧹 Очистка контейнера..."
docker rm -f $CONTAINER_NAME 2>$null | Out-Null

Write-Host ""
Write-Success "========================================="
Write-Success "✅ Процесс завершен"
Write-Success "========================================="
