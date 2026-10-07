# KORSAC — Homepage Experience v1

## Роль и путь

`prototype/index.html` — главная KORSAC. Прежний developer navigation hub
перенесён в `prototype/review.html`; каталог, продукт и UI Kit доступны через
него и соответствующие ссылки сайта. Публичная [оболочка](KORSAC-SITE-SHELL.md)
общая на homepage/catalog/product/UI Kit.

Путь: **что такое KORSAC → задача → подходящий PLAY → основания доверия →
изучение или настройка**. Главная редакционная; каталог отвечает за discovery
и сравнение, продукт — за inspection/configuration. Полная линейка карточек,
comparison dialog и шестисценарный Product Explorer на главной не повторяются.

Основа: [Brand Guide](../brand/KORSAC-BRAND-GUIDE.md),
[Visual/Motion](KORSAC-VISUAL-MOTION-DIRECTION.md),
[Product v3.1](KORSAC-INTERACTIVE-PRODUCT-EXPERIENCE.md),
[Catalog v1](KORSAC-CATALOG-EXPERIENCE.md). Рабочие GPU-классы и defaults
взяты из принятого каталога; PLAY 1440 сохраняет Ryzen 7 9700X, RTX 5070,
32 ГБ DDR5 и 1 ТБ NVMe TLC. Нет pricing arithmetic или новых бизнес-обещаний.

## Hero и media architecture

Основное сообщение: **«Компьютеры, точно собранные под задачу.»**. Короткое
описание объясняет продуманную конфигурацию, сборку и тестирование. Primary
«Выбрать компьютер» ведёт в каталог; «Настроить свой» — в существующий PLAY
1440 configurator. CTA доступны сразу и не зависят от окончания motion.

Desktop асимметричен: большая типографика слева, свободное продуктовое поле
справа. Wide layout ограничен 1360 px содержимого, full-width атмосферные
зоны связывают его с фоном. При 768 px hero складывается, а продуктовая схема
остаётся отдельным акцентом справа. На mobile сначала header/message/copy/CTA,
затем небольшая схема; giant image над текстом отсутствует.

Текущая схема — явно non-final 2D CSS representation. Она не выдаётся за
фотографию или физическую ревизию. Нет stock/competitor images, растрового
brand board, AI-generated PC, внешних шрифтов, видео-фона, WebGL или 3D.
Атмосфера — локальные умеренные graphite/blue gradients; copper завершает
небольшую линию. Основные заголовки используют системный sans, mono остаётся
у model identifiers и паспорта.

Утверждённый медный mark имеет ширину 320 px на 1280/1440/1920,
220 px на 1024, 210 px на tablet и 148 px на mobile; opacity .68.
Он смещён от схемы, глаза остаются видны, а продукт находится перед ним.
Blue ambient уменьшен до 6%, registration line до 18 px. Headline/CTA
и размер схемы сохраняются. Логотип уже финальный; схема продукта временная.

Слои figure:

1. `k-home-media-field` — декоративное поле.
2. `data-home-media` / `k-home-media-base` — заменяемая схема или `<picture>`.
3. `k-home-media-identity` — отдельные guide/copper layers, `aria-hidden`.
4. `k-home-brand-mark` — отдельный decorative ICON за product media, с известным aspect ratio.
5. `figcaption` — честная подпись изображения.

Base media занимает определённую область figure, не задаёт layout headline,
CTA или header. Будущая фотография вставляется как `picture/source/img`:
локальные responsive sources, реальные width/height и `alt`, `object-fit`
после согласования crop. Motion остаётся на wrapper. Layout probe с нейтральным
1200×1600 изображением сохранил высоту hero/header и отсутствие overflow на
320/768/1440/1920 px. Реальная фотография и финальный crop не утверждены.

## Motion

`assets/js/homepage.js` запускает однократную WAAPI последовательность с
существующими duration/easing tokens. Основная композиция — **940 ms**:

| Слой                             | Начало | Длительность |
| -------------------------------- | ------ | ------------ |
| Atmospheric field / guide        | 0 ms   | 420 ms       |
| Media settle, 16 px / scale .985 | 110 ms | 420 ms       |
| Headline resolve, 16 px          | 220 ms | 320 ms       |
| Support copy, 8 px               | 320 ms | 320 ms       |
| CTA, 8 px без скрытия            | 420 ms | 220 ms       |
| Copper registration              | 620 ms | 320 ms       |

В normal mode opacity используется только у декоративного поля. Смысловой текст/CTA
не скрываются; transform не блокирует native focus/click. Нет replay loop,
autoplay, mouse-follow, scroll-jacking и fade-up каждого раздела. Finished
promises освобождают эффекты; живое включение reduced motion отменяет active
animations. После завершения декоративная сцена неподвижна.

Reduced branch в `homepage.js`: headline, description, CTA и media получают
одновременно opacity **.75 → 1 за 180 ms**, без delay/translate/scale/clip.
Текст сразу читаем, controls сразу доступны; field/guide/copper — final state.
Это reduced-motion mode с коротким feedback, не global animation off.
Live preference change отменяет entry effects и возвращает final state;
обратный toggle не повторяет completed entry. Общие reduced tokens — 110/180 ms.
Compact discovery сохраняет такой же opacity-only confirmation, как Catalog.

Shared sticky header использует `data-shell-at-top`, sync `scrollY ≤ 16px`
и passive scroll listener с одним requestAnimationFrame. Hero intersection
не используется. Background становится opaque сразу после threshold;
transition — 140 ms normal / 110 ms reduced, без изменения высоты. Shell
не участвует в discovery/business state. В остальных разделах нет scroll
motion. Автоматический Hero Eye Flash удалён после live review; coupling
`korsac:hero-enter` больше нет. Hero totem — внешний static eyes-off
`korsac-mark.svg`. Замещающая hero animation не добавлена.

[Brand Intro](KORSAC-BRAND-ASSET-INTEGRATION.md) — отдельное общее shell
поведение при первом eligible входе на index/catalog/product: rolling 24h
per browser profile/origin. Он не принадлежит homepage, пропускается при
Reduced Motion и не требует backend/cookie/account sync. Intro не меняет
layout hero, scroll/focus и раннюю CTA; после его выхода страница доступна.

## Компактный discovery

Семейства: PLAY — текущий игровой путь; CREATE/WORK ясно в разработке.
Ссылка «Для бизнеса» ведёт к этому WORK обозначению, без ложной B2B-страницы.
PLAY использует принятую семантику **1080 → 1440 → 1440 PRO → 4K**, с одной
вложенной MINI-веткой от 1440: **«Тот же 1440p · Mini-ITX»**.

При выборе видны название, сценарий, форм-фактор, GPU-класс, базовые RAM/SSD
и одна CTA. PLAY 1440 открывает существующий продукт; другие модели ведут
к своим карточкам в каталоге. Ссылка «Посмотреть всю линейку PLAY» доступна
постоянно. Цены и сравнение на главной отсутствуют.

Используется **тот же** `catalog-experience.js`, отдельно для каждого root.
Compact variant не содержит recommendations/compare checkboxes; controller
принимает отсутствие этих optional частей. Model properties authored в HTML;
нет нового JS-массива SKU, fetch, singleton или отдельной discovery state
machine. Новый UI Kit compact fixture независим от Catalog/Product Primitives.

Preview клонируется из пяти компактных source articles. Неактивные панели
`hidden`/`inert` сохраняют intrinsic размеры grid slot, поэтому высота не
меняется при выборе. Selection обновляет `aria-pressed`, rail, MINI-parent,
identifier/status и CTA синхронно; 320 ms resolve — конечный feedback.
Контролы не изменяют URL/scroll/focus и не требуют hover/swipe.

Без JS видны пять сценарных anchors и пять кратких product summaries с CTA.
После успешного enhancement source list скрывается и остаётся один выбранный
preview. Основное сообщение, hero CTA и обычная навигация не исчезают.

## Остальные разделы

**Featured PLAY 1440** — отдельный редакционный акцент: большой 1440,
схема, сценарий и четырёхпольный baseline. Одна native `details` inspection
объясняет платформу/графику и выделяет GPU-зону; обзор остаётся читаемым.
CTA «Настроить» переводит в полный конфигуратор. Шестисценарный Explorer,
hotspots и live configuration на главную не перенесены.

**Почему KORSAC** — открытая типографическая композиция с четырьмя опорами:
архитектура, сборка, проверка, поддержка. Нет одинаковых rounded cards.
На узком экране статьи становятся одной колонкой, чтобы длинные русские
названия не создавали overflow.

**Сборка и проверка** — статические четыре шага: Сборка → Настройка →
Тестирование → Финальная проверка. Это описание процесса, не прогресс заказа,
не fake pending/confirmed и не численные тестовые результаты.

**SYSTEM ID / ownership** — структура будущего паспорта и native disclosure
его содержания. Configuration example подписан; идентификатор будет присвоен
при сборке, данные тестов появятся после проверки. Серийный номер, QR/barcode,
backend verification, реальные сервисные записи и гарантийные периоды не
выдуманы. Physical badge в схеме — только временный текстовый placeholder.

**Final CTA** — «Найдите свой KORSAC.» с переходом в каталог и настройку PLAY 1440. Просторный footer завершает бренд и содержит единственную тихую
prototype note.

## Future Bitrix mapping

| Область                   | Будущий источник                                   |
| ------------------------- | -------------------------------------------------- |
| Public shell              | `local/templates/korsac/header.php` / `footer.php` |
| Homepage hero / editorial | Site template и согласованные include areas        |
| Family/scenario discovery | Реальные catalog sections/properties               |
| Featured PLAY 1440        | Catalog/product data и реальный detail route       |
| SYSTEM ID story           | Static marketing сначала; реальные записи позже    |
| Search/account/cart       | Соответствующие site search / auth / sale adapters |

SSR может авторить тот же semantic HTML. Presentation keys не являются
XML_ID/API contract; цены, stock, совместимость и корзина принадлежат backend.
Bitrix, ConfiguratorCore и `kk.korsac` не изменены.

## Проверки, материалы и human acceptance

[Review assets](review/README.md) содержат desktop/mobile/wide homepage,
header/footer, scenario, feature/ownership, drawer, UIKit и оболочку
catalog/product. Review-only MP4 показывает normal motion и native действия;
он не используется runtime.

HTTP Chromium 151 проверен на 320/375/430/768/1024/1280/1440/1920 px,
с keyboard/native details/dialogs, touch320/375/430, no-JS320, обычной/reduced
motion и live отменой эффекта. На всех ширинах preview имеет стабильную
высоту. Мобильные hero CTA и часть media доступны в первом практическом
viewport. Проведены regressions исходного каталога и Product v3.1.

Self-review A–G:

- A: shell стал спокойнее: sans navigation, icon utilities, простор и большой footer wordmark.
- B: identity сохраняется через композицию, designation, copper и управляемый выбор без REV/DIRECTION chrome.
- C: hero/редакционная структура эмоциональнее scan catalog; aggressive gaming language отсутствует.
- D: precision остаётся в сценариях, базовых фактах и процессе, не в каждой рамке.
- E: утверждённые brand SVG интегрированы в прежние hooks; отдельный media slot остаётся готовым к фотографии.
- F: hero/discovery/feature/final CTA ведут в существующие Catalog и PLAY 1440.
- G: Homepage editorial, Catalog discovery/compare, Product inspection/configuration имеют разные роли.

Это self-review реализации, не результат пользовательского исследования.
Человек должен подтвердить premium feel header/footer, смысл hero с первого
экрана, простоту сценарного выбора, связь трёх страниц и normal/reduced motion
в живом браузере. Не сливать автоматически. PNG/MP4 не завершают acceptance.
Физические устройства, screen reader, Firefox/Safari не проверены; direct
`file://` заблокирован политикой среды.
