# 🚀 Быстрый старт: GitHub Actions

## ✅ Что готово

✅ Workflow файл создан: `.github/workflows/build-apk.yml`
✅ Buildozer.spec настроен
✅ Android конфигурация готова
✅ Иконка и splash screen созданы

## 📋 3 простых шага

### Шаг 1: Создайте репозиторий на GitHub

Откройте: https://github.com/new

Заполните:
- **Repository name:** `snake-game`
- **Description:** `Snake Game for Android`
- **Visibility:** Public ✅ (для бесплатной сборки)
- Нажмите **Create repository**

### Шаг 2: Загрузите код

```bash
cd "C:\Users\Зал Царства\papka\snake-pygame"

# Если git не инициализирован:
git init

# Добавьте remote (замените YOUR_USERNAME):
git remote add origin https://github.com/YOUR_USERNAME/snake-game.git

# Добавьте файлы:
git add .

# Commit:
git commit -m "Add GitHub Actions workflow for APK build"

# Push:
git push -u origin master
```

Если спросит логин/пароль:
- **Username:** ваш GitHub username
- **Password:** используйте Personal Access Token (не пароль!)
  - Создать токен: https://github.com/settings/tokens

### Шаг 3: Дождитесь сборки

1. Откройте ваш репозиторий на GitHub
2. Вкладка **Actions** (вверху)
3. Увидите "Build Android APK" - кликните
4. Наблюдайте за процессом (15-30 минут)

### Шаг 4: Скачайте APK

После завершения:
1. Прокрутите вниз до **Artifacts**
2. Скачайте `snake-game-apk`
3. Распакуйте ZIP
4. Внутри будет APK файл!

## 🎮 Готово!

Установите APK на Android телефон и играйте! 🐍

---

## 🔄 Следующие обновления

Просто делайте:
```bash
git add .
git commit -m "Updated game"
git push
```

GitHub автоматически соберет новый APK!

---

## 📖 Подробности

Смотрите `GITHUB_ACTIONS_GUIDE.md` для полной инструкции.

---

## ❓ Проблемы?

### "Permission denied"
Settings → Actions → General → Workflow permissions → "Read and write" ✅

### "Build failed"
Проверьте логи в Actions → кликните на failed build → смотрите красные шаги

### Нужна помощь?
Создайте Issue в репозитории или пишите мне!

**Удачи! 🚀**
