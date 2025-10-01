# 🤖 GitHub Actions - Автоматическая сборка APK

## 🎯 Что это?

GitHub Actions автоматически соберет ваш APK в облаке каждый раз, когда вы загружаете код на GitHub.

**Преимущества:**
- ✅ Не нужно ничего устанавливать на компьютер
- ✅ Сборка происходит автоматически
- ✅ Бесплатно для публичных репозиториев
- ✅ APK доступен для скачивания из GitHub

## 📋 Пошаговая инструкция

### Шаг 1: Создайте репозиторий на GitHub

1. Откройте https://github.com
2. Нажмите **New repository** (зеленая кнопка)
3. Заполните:
   - Repository name: `snake-game`
   - Description: `Classic Snake Game for Android`
   - Visibility: **Public** (для бесплатной сборки)
4. Нажмите **Create repository**

### Шаг 2: Загрузите код на GitHub

#### Вариант A: Через Git командную строку

```bash
cd "C:\Users\Зал Царства\papka\snake-pygame"

# Инициализируйте git (если еще не сделано)
git init

# Добавьте remote
git remote add origin https://github.com/ВАШ_USERNAME/snake-game.git

# Добавьте все файлы
git add .

# Сделайте commit
git commit -m "Initial commit with GitHub Actions workflow"

# Отправьте на GitHub
git push -u origin master
```

#### Вариант B: Через GitHub Desktop

1. Скачайте GitHub Desktop: https://desktop.github.com/
2. Откройте программу
3. File → Add Local Repository
4. Выберите папку: `C:\Users\Зал Царства\papka\snake-pygame`
5. Нажмите **Publish repository**
6. Выберите созданный репозиторий

#### Вариант C: Через веб-интерфейс GitHub

1. На странице репозитория нажмите **uploading an existing file**
2. Перетащите все файлы из папки `snake-pygame`
3. Нажмите **Commit changes**

### Шаг 3: Активируйте GitHub Actions

GitHub Actions автоматически обнаружит файл `.github/workflows/build-apk.yml` и запустит сборку!

### Шаг 4: Следите за сборкой

1. Откройте ваш репозиторий на GitHub
2. Перейдите на вкладку **Actions**
3. Вы увидите процесс сборки "Build Android APK"
4. Кликните на него, чтобы посмотреть прогресс

**Время сборки:** 15-30 минут (первый раз)

### Шаг 5: Скачайте APK

После успешной сборки:

1. На странице workflow нажмите на завершенную сборку
2. Прокрутите вниз до раздела **Artifacts**
3. Скачайте `snake-game-apk.zip`
4. Распакуйте - внутри будет APK файл!

## 🔄 Автоматические сборки

Теперь каждый раз когда вы делаете `git push`, GitHub автоматически:
- ✅ Соберет новый APK
- ✅ Сохранит его в Artifacts
- ✅ (Опционально) Создаст Release с APK

## 📱 Установка APK на телефон

1. Скачайте APK файл на телефон
2. Откройте через файловый менеджер
3. Разрешите установку из неизвестных источников
4. Установите!

Или через ADB:
```bash
adb install путь/к/snake-game.apk
```

## ⚙️ Настройка workflow

Файл `.github/workflows/build-apk.yml` уже создан и настроен!

### Что он делает:

1. **Запускается когда:**
   - Вы делаете push в ветку master/main
   - Вы создаете Pull Request
   - Вы запускаете вручную (кнопка "Run workflow")

2. **Устанавливает:**
   - Python 3.10
   - Java 11 (для Android SDK)
   - Buildozer (инструмент сборки)
   - Все необходимые зависимости

3. **Собирает:**
   - Debug APK (для тестирования)
   - Размер: ~15-20 MB

4. **Сохраняет:**
   - APK в Artifacts (доступен 30 дней)
   - (Опционально) Создает Release

## 🎮 Запуск сборки вручную

Не хотите делать commit? Запустите сборку вручную!

1. Откройте репозиторий на GitHub
2. Вкладка **Actions**
3. Выберите "Build Android APK"
4. Нажмите **Run workflow**
5. Выберите ветку (master)
6. Нажмите зеленую кнопку **Run workflow**

## 🔍 Проверка статуса

### Индикатор в README

Добавьте badge в ваш README.md:

```markdown
![Build Status](https://github.com/ВАШ_USERNAME/snake-game/workflows/Build%20Android%20APK/badge.svg)
```

Будет показывать: ✅ зеленый = сборка успешна, ❌ красный = ошибка

## 🐛 Решение проблем

### Ошибка: "Buildozer failed"

**Причина:** Не хватает памяти или timeout

**Решение:** В файле `build-apk.yml` добавьте:
```yaml
timeout-minutes: 60  # Увеличьте время
```

### Ошибка: "SDK not found"

**Причина:** Android SDK не установился

**Решение:** Уже исправлено в workflow - используется buildozer

### Ошибка: "Permission denied"

**Причина:** GitHub не может создать Release

**Решение:** 
1. Settings → Actions → General
2. Workflow permissions → выберите "Read and write permissions"
3. Сохраните

## 📊 Лимиты GitHub Actions

### Бесплатные лимиты (Public репозиторий):

- ✅ **Неограниченные минуты** для публичных репозиториев
- ✅ Хранилище: 500 MB
- ✅ Artifacts: хранятся 90 дней (настроено 30)

### Платные лимиты (Private репозиторий):

- 2,000 минут в месяц (бесплатно)
- Затем $0.008 за минуту

**Рекомендация:** Используйте публичный репозиторий!

## 🚀 Оптимизация

### Ускорение сборки:

Добавьте кэширование в `build-apk.yml`:

```yaml
- name: Cache Buildozer dependencies
  uses: actions/cache@v3
  with:
    path: .buildozer
    key: ${{ runner.os }}-buildozer-${{ hashFiles('buildozer.spec') }}
```

Это сократит время сборки с 20 минут до 5 минут!

## 📦 Альтернативные сервисы

Не нравится GitHub Actions? Попробуйте:

### 1. **Travis CI**
- Бесплатно для Open Source
- https://travis-ci.org/

### 2. **CircleCI**
- 2,500 минут бесплатно
- https://circleci.com/

### 3. **AppCenter** (Microsoft)
- Специально для мобильных приложений
- https://appcenter.ms/

## 🎯 Release на GitHub

Workflow автоматически создаст Release с APK!

**Как это работает:**
1. Вы делаете push в master
2. GitHub собирает APK
3. Создается новый Release с номером сборки
4. APK прикрепляется к Release
5. Пользователи могут скачать из вкладки "Releases"

### Отключить автоматические Releases:

Удалите эту секцию из `build-apk.yml`:

```yaml
- name: Create Release (optional)
  ...
```

## ✅ Итоговый чек-лист

Перед загрузкой на GitHub проверьте:

- [ ] Все файлы на месте
- [ ] `.github/workflows/build-apk.yml` создан
- [ ] `buildozer.spec` настроен
- [ ] `.android.json` настроен
- [ ] `icon.png` создан (512x512)
- [ ] `splash.png` создан (720x1280)
- [ ] Репозиторий создан на GitHub
- [ ] Код загружен на GitHub
- [ ] Workflow запущен

## 📖 Полезные ссылки

- **GitHub Actions документация:** https://docs.github.com/actions
- **Buildozer документация:** https://buildozer.readthedocs.io/
- **Python-for-Android:** https://python-for-android.readthedocs.io/

---

## 🎮 Готово!

Теперь при каждом обновлении игры просто делайте:

```bash
git add .
git commit -m "Updated game features"
git push
```

И GitHub автоматически соберет новый APK! 🚀

**Вопросы? Смотрите логи в разделе Actions на GitHub!**
