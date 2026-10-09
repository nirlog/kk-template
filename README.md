# KORSAC / kk-template

Документация бренда и продуктовой архитектуры KORSAC, а также статический
прототип сайта с Premium Site Shell / Homepage v1, каталогом PLAY v1
Interactive Product Experience v3.1, Cart & Checkout Experience v1, Contacts / Error Pages и SEO / IA Foundation на визуальной основе v2.1.

## Prototype

Прототип на HTML5, CSS и обычном JavaScript работает без установки пакетов,
сборки, Bitrix и внешних ресурсов. Откройте HTML-файл прямо в браузере:

- [prototype/index.html](prototype/index.html) — главная KORSAC, редакционный путь к выбору системы.
- [prototype/review.html](prototype/review.html) — сохранённая навигация для дизайнеров и разработчиков.
- [prototype/ui.html](prototype/ui.html) — Premium Shell / Homepage / Identity / Interactive / Catalog / Commerce Primitives и motion-примеры.
- [prototype/computers.html](prototype/computers.html) — выбор семейства PLAY / CREATE / WORK.
- [prototype/create.html](prototype/create.html) — рабочий процесс: 3D, CAD, видео и графика.
- [prototype/work.html](prototype/work.html) — рабочие задачи и operational priorities.
- [prototype/catalog.html](prototype/catalog.html) — выбор сценария PLAY, MINI-ветка, вся линейка и сравнение классов.
- [prototype/product.html](prototype/product.html) — PLAY 1440, System Explorer, сцена конфигуратора и SYSTEM ID.
- [prototype/cart.html](prototype/cart.html) — две конфигурации PLAY 1440, количество, demo totals и empty state.
- [prototype/checkout.html](prototype/checkout.html) — guest/company checkout, СДЭК placeholder, payment и validation.
- [prototype/order-success.html](prototype/order-success.html) — явно демонстрационный результат оформления.
- [prototype/contacts.html](prototype/contacts.html) — каналы связи без вымышленных реквизитов.
- [prototype/404.html](prototype/404.html), [500](prototype/500.html), [503](prototype/503.html) — визуальные error states; static files не задают HTTP error status.

Для проверки через HTTP из корня репозитория:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory prototype
```

Откройте локальный порт 8000 в браузере. Сервер необязателен; файлы также
рассчитаны на открытие через `file://`: относительные ресурсы не требуют сервера.
Главная использует компактный вариант того же HTML-driven catalog controller.
Публичная оболочка общая на homepage/catalog/product/UI Kit; developer rails
сохранены только в review hub. Утверждённые SVG используются в header/drawer,
responsive footer и статическом hero. Общий site-entry Brand Intro играет
не чаще раза за rolling 24h в browser profile; reduced motion пропускает его.
Computers/CREATE/WORK участвуют в этой же политике, без новых motion sequences.
Cart/Checkout/Success, Contacts и error pages исключены из Brand Intro и не меняют его timestamp.
Фотография продукта пока заменена нейтральной схемой.
Выбранные hardware-опции обновляют сцену, сводку и SYSTEM ID preview;
цены остаются статическими. Explorer синхронизирует сцену и пояснение
через context buttons, hotspots и Prev/Next, сохраняя обычную прокрутку.
Каталог читает данные из HTML-карточек: Navigator и сравнение 2–3 моделей
меняют только представление. MINI — компактное исполнение 1440p; PRO — более
высокий игровой класс. CREATE/WORK имеют разные family landing pages; их
модельные линейки ещё формируются, production publication не утверждена.
Цены, статусы, паспорт и сервисные опции — примеры. Cart читает авторские HTML
строки; quantity/remove/restore используют только prototype display arithmetic
в integer minor units. Checkout/Success имеют исходный demo order, без переноса
изменений между страницами, persistent basket или передачи контактов. Production
pricing/order остаются backend-authoritative. Поиск, аккаунт и API не реализованы.
Motion учитывает `prefers-reduced-motion`.

[Brand Assets & Eye Flash](docs/frontend/KORSAC-BRAND-ASSET-INTEGRATION.md).
[Homepage Experience v1](docs/frontend/KORSAC-HOMEPAGE-EXPERIENCE.md).
[Premium Site Shell v1](docs/frontend/KORSAC-SITE-SHELL.md).
[Описание системы и план переноса в Bitrix](docs/frontend/KORSAC-STATIC-PROTOTYPE.md).
[Визуальное направление и motion v2](docs/frontend/KORSAC-VISUAL-MOTION-DIRECTION.md).
[Interactive Product Experience v3.1](docs/frontend/KORSAC-INTERACTIVE-PRODUCT-EXPERIENCE.md).
[Catalog & Product Family Experience v1](docs/frontend/KORSAC-CATALOG-EXPERIENCE.md).
[Снимки и review-only MP4](docs/frontend/review/README.md).

[Cart & Checkout Experience v1](docs/frontend/KORSAC-CART-CHECKOUT-EXPERIENCE.md).

Все `prototype/*.html` имеют `noindex, nofollow, noarchive`; production policy
определена отдельно, canonical hostname и контактные данные не выдуманы.

[Information Architecture и production matrix](docs/frontend/KORSAC-INFORMATION-ARCHITECTURE.md).
[SEO Foundation и server-side Bitrix ownership](docs/frontend/KORSAC-SEO-FOUNDATION.md).
[Contacts / Error Pages и HTTP-контракт](docs/frontend/KORSAC-GENERIC-PAGES.md).
[SEO review result](docs/frontend/review/seo-foundation-v1.md).

Локальный аудит без зависимостей:

```sh
python3 tools/seo_audit.py
python3 -m unittest discover -s tools -p 'test_seo_audit.py'
```

[Computer Families Experience v1](docs/frontend/KORSAC-COMPUTER-FAMILIES-EXPERIENCE.md).
[Family review PNG / audit / QA](docs/frontend/review/computer-families-v1.md).
Projects реализованы в следующем stage ниже; Bitrix migration не начата.

### Projects Experience v1

- [Projects list](prototype/projects.html) — три реальные сборки из архива команды King-Komp.
- [Project detail](prototype/project.html) — белый игровой компьютер i5-14600KF / RTX 4070 SUPER, историческая конфигурация и provenance.
- [Content/source/SEO/Bitrix contract](docs/frontend/KORSAC-PROJECTS-EXPERIENCE.md).
- [Review screenshots и QA](docs/frontend/review/projects-v1.md).

Projects доступны через Homepage trust и footer; PLAY/family hierarchy сохранены. Факты сверены с оригиналами King-Komp; source фотографии сохранены локально: previews всех трёх проектов и gallery белой сборки. Equipment реализован в следующем stage ниже; System Passport реализован в следующем stage ниже; Bitrix не реализован.

### Equipment / Simple Product Experience v1

- [Оборудование](prototype/equipment.html) → [Мониторы](prototype/monitors.html).
- [MSI MAG 274QF X24](prototype/monitor.html) — ordinary Product, без PC Explorer/CONFIG.
- [Смешанная корзина](prototype/cart.html#cart-monitor) — две системы PLAY и отдельный монитор.
- [Content/media/cart/Bitrix contract](docs/frontend/KORSAC-EQUIPMENT-EXPERIENCE.md).
- [Review screenshots и QA](docs/frontend/review/equipment-v1.md).

10 уникальных реальных моделей MSI/LG (PLAY — 4, CREATE — 4, WORK — 5) сверены с карточками King-Komp и спецификациями
производителей. Фото локальные; цены явно обозначены как примеры. Production
price/availability/basket принадлежат Bitrix. Shared Media Viewer отложен;
Bitrix migration не начата; System Passport описан ниже. Human review требуется до merge.

### System Passport Experience v1

- [Активный паспорт](prototype/passport.html) и [ещё не активирован](prototype/passport-pending.html) — синтетические review states одной production route `/passport/{PUBLIC_ID}/`.
- [Internal workflow review / not public UI](prototype/system-workflow.html) — только review specimen, не публичная production route.
- [System / components / inquiry / D7 contract](docs/frontend/KORSAC-SYSTEM-PASSPORT.md).
- [Review evidence / QA](docs/frontend/review/system-passport-v1.md).

System — отдельный физический компьютер, не Product или Order. Одному заказу
соответствуют отдельные System на каждую единицу компьютера; обычному монитору
System не создаётся. Passport показывает подтверждённые компоненты и сохранённую
гарантию без S/N, заказа, клиента и внутренней сервисной истории. Product теперь
объясняет будущий паспорт без вымышленного SYSTEM ID. Глобального списка/поиска
паспортов нет. Формы не отправляют и не сохраняют данные; генераторы, автоматизация,
QR, расчёт гарантии и D7 — будущий backend. Human visual/architecture review required;
do not auto-merge.

Проверки: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_*.py'`,
`python3 tools/seo_audit.py`, `python3 tools/monitor_curation_audit.py`.
