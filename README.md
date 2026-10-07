# KORSAC / kk-template

Документация бренда и продуктовой архитектуры KORSAC, а также статический
прототип сайта с Premium Site Shell / Homepage v1, каталогом PLAY v1
и Interactive Product Experience v3.1 на визуальной основе v2.1.

## Prototype

Прототип на HTML5, CSS и обычном JavaScript работает без установки пакетов,
сборки, Bitrix и внешних ресурсов. Откройте HTML-файл прямо в браузере:

- [prototype/index.html](prototype/index.html) — главная KORSAC, редакционный путь к выбору системы.
- [prototype/review.html](prototype/review.html) — сохранённая навигация для дизайнеров и разработчиков.
- [prototype/ui.html](prototype/ui.html) — Premium Shell / Homepage / Identity / Interactive / Catalog Primitives и motion-примеры.
- [prototype/catalog.html](prototype/catalog.html) — выбор сценария PLAY, MINI-ветка, вся линейка и сравнение классов.
- [prototype/product.html](prototype/product.html) — PLAY 1440, System Explorer, сцена конфигуратора и SYSTEM ID.

Для проверки через HTTP из корня репозитория:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory prototype
```

Откройте локальный порт 8000 в браузере. Сервер необязателен; файлы также
рассчитаны на открытие через `file://`: относительные ресурсы не требуют сервера.
Главная использует компактный вариант того же HTML-driven catalog controller.
Публичная оболочка общая на homepage/catalog/product/UI Kit; developer rails
сохранены только в review hub. Утверждённые SVG используются в header/drawer,
responsive footer и hero; короткая вспышка глаз играет один раз. Фотография
продукта пока заменена нейтральной схемой.
Выбранные hardware-опции обновляют сцену, сводку и SYSTEM ID preview;
цены остаются статическими. Explorer синхронизирует сцену и пояснение
через context buttons, hotspots и Prev/Next, сохраняя обычную прокрутку.
Каталог читает данные из HTML-карточек: Navigator и сравнение 2–3 моделей
меняют только представление. MINI — компактное исполнение 1440p; PRO — более
высокий игровой класс. CREATE/WORK пока в разработке.
Цены, статусы, паспорт и сервисные опции — примеры. Поиск, корзина, API
и расчёт цены не реализованы. Motion учитывает `prefers-reduced-motion`.

[Brand Assets & Eye Flash](docs/frontend/KORSAC-BRAND-ASSET-INTEGRATION.md).
[Homepage Experience v1](docs/frontend/KORSAC-HOMEPAGE-EXPERIENCE.md).
[Premium Site Shell v1](docs/frontend/KORSAC-SITE-SHELL.md).
[Описание системы и план переноса в Bitrix](docs/frontend/KORSAC-STATIC-PROTOTYPE.md).
[Визуальное направление и motion v2](docs/frontend/KORSAC-VISUAL-MOTION-DIRECTION.md).
[Interactive Product Experience v3.1](docs/frontend/KORSAC-INTERACTIVE-PRODUCT-EXPERIENCE.md).
[Catalog & Product Family Experience v1](docs/frontend/KORSAC-CATALOG-EXPERIENCE.md).
[Снимки и review-only MP4](docs/frontend/review/README.md).
