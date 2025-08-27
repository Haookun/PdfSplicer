
<div align="center">
   <img width="100" height="100" alt="app_icon" src="https://github.com/user-attachments/assets/a3f9089a-cf94-43be-b485-f682a43492c6" />
</div>

# PdfSplicer

Вы сталкивались с проблемой объединения лицевой и оборотной сторон сканированных документов в один PDF?

PdfSplicer решает эту задачу! Умный инструмент для macOS с графическим интерфейсом, автоматически определяет порядок страниц и объединяет их в единый PDF.

## Особенности
- Простой графический интерфейс
- Выбор PDF лицевой и оборотной сторон
- Автоматическое определение и объединение порядка страниц
- Выбор папки для сохранения и быстрый доступ
- Одно нажатие — готовый PDF

## Использование

<div align="center">
   <img width="400" alt="Скриншот" src="https://github.com/user-attachments/assets/e22dde23-d568-4592-9f83-bb71a0ec1290" />
</div>

1. Перейдите на [страницу релизов](https://github.com/Haookun/PdfSplicer/releases) и скачайте последний установщик `PdfSplicer.dmg`.
2. Откройте DMG-файл, перетащите `PdfSplicer.app` в папку Приложения.
3. Запустите PdfSplicer, выберите PDF лицевой/оборотной сторон и путь сохранения, нажмите "Начать объединение".

## Упаковка и распространение
1. Установите зависимости:
   ```bash
   pip install pyinstaller dmgbuild
   ```
2. Подготовьте прозрачную иконку `.icns` с именем `app_icon.icns` в корне проекта.
3. Упакуйте с помощью PyInstaller:
   ```bash
   pyinstaller --windowed --name PdfSplicer --icon=app_icon.icns main.py
   ```
   - Результат в `dist/PdfSplicer.app`.
4. Проверьте или отредактируйте `dmg_settings.py` для конфигурации DMG.
5. Создайте DMG:
   ```bash
   dmgbuild -s dmg_settings.py "PdfSplicer" PdfSplicer.dmg
   ```
   - DMG будет в корне проекта или указанном пути.
6. Переместите DMG в папку `release` для распространения.
7. Пользователь просто перетаскивает `PdfSplicer.app` в Приложения для установки.

## Лицензия
MIT License

## Репозиторий
https://github.com/Haookun/PdfSplicer
