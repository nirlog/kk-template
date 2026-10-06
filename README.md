# KORSAC / kk-template

Документация бренда и продуктовой архитектуры KORSAC, а также статический
прототип сайта с визуальным языком v2.1 и Interactive Product Experience v3.1.

## Prototype

Прототип на HTML5, CSS и обычном JavaScript работает без установки пакетов,
сборки, Bitrix и внешних ресурсов. Откройте HTML-файл прямо в браузере:

- [prototype/index.html](prototype/index.html) — навигация для дизайнеров и разработчиков.
- [prototype/ui.html](prototype/ui.html) — компоненты, Identity/Interactive Product Primitives и motion-примеры.
- [prototype/product.html](prototype/product.html) — PLAY 1440, System Explorer, сцена конфигуратора и SYSTEM ID.

Для проверки через HTTP из корня репозитория:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory prototype
```

Откройте локальный порт 8000 в браузере. Сервер необязателен; файлы также
рассчитаны на открытие через `file://`: относительные ресурсы не требуют сервера.
Выбранные hardware-опции обновляют сцену, сводку и SYSTEM ID preview;
цены остаются статическими. Explorer синхронизирует сцену и пояснение
через context buttons, hotspots и Prev/Next, сохраняя обычную прокрутку.
Цены, статусы, паспорт и сервисные опции — примеры. Поиск, корзина, API
и расчёт цены не реализованы. Motion учитывает `prefers-reduced-motion`.

[Описание системы и план переноса в Bitrix](docs/frontend/KORSAC-STATIC-PROTOTYPE.md).
[Визуальное направление и motion v2](docs/frontend/KORSAC-VISUAL-MOTION-DIRECTION.md).
[Interactive Product Experience v3.1](docs/frontend/KORSAC-INTERACTIVE-PRODUCT-EXPERIENCE.md).
[Снимки и review-only MP4](docs/frontend/review/README.md).
