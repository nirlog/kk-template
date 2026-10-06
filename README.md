# KORSAC / kk-template

Документация бренда и продуктовой архитектуры KORSAC, а также статический
прототип сайта с визуальным языком инженерной системы и направлением motion v2.

## Prototype

Прототип на HTML5, CSS и обычном JavaScript работает без установки пакетов,
сборки, Bitrix и внешних ресурсов. Откройте HTML-файл прямо в браузере:

- [prototype/index.html](prototype/index.html) — навигация для дизайнеров и разработчиков.
- [prototype/ui.html](prototype/ui.html) — токены, компоненты, Identity Primitives и повторяемые motion-примеры.
- [prototype/product.html](prototype/product.html) — PLAY 1440, конфигуратор и SYSTEM ID.

Для проверки через HTTP из корня репозитория:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory prototype
```

Откройте локальный порт 8000 в браузере. Сервер необязателен; файлы также
рассчитаны на открытие через `file://`: относительные ресурсы не требуют сервера.
Выбранные подписи опций обновляют сводку, цены остаются статическими.
Цены, статусы, паспорт и сервисные опции — примеры. Поиск, корзина, API
и расчёт цены не реализованы. Motion учитывает `prefers-reduced-motion`.

[Описание системы и план переноса в Bitrix](docs/frontend/KORSAC-STATIC-PROTOTYPE.md).
[Визуальное направление и motion v2](docs/frontend/KORSAC-VISUAL-MOTION-DIRECTION.md).
[Сравнение снимков v1/v2](docs/frontend/review/README.md).
