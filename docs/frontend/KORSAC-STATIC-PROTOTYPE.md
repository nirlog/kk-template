# KORSAC — Static UI Prototype / Homepage & Shell v1 / Product v3.1 / Catalog v1

## Назначение

Прототип на HTML/CSS/vanilla JS развивает KORSAC как инженерную систему:
индексированные разделы, точные направляющие, асимметричная композиция,
паспорт продукта и короткое движение, связанное с действием. Техническая
основа v1 сохраняется: семантический HTML, нативные контролы, адаптивность,
видимый фокус, CSS-токены и запуск без сборки.

`index.html` — редакционная главная KORSAC; прежний навигационный хаб
сохранён в `review.html`. `ui.html` показывает Shell/Homepage/Identity/Catalog
Primitives и motion; `product.html` демонстрирует PLAY 1440.
`catalog.html` показывает сценарный выбор PLAY и сравнение продуктовых классов.
Подробные решения и будущие точки интеграции описаны в
[Visual & Motion Direction](KORSAC-VISUAL-MOTION-DIRECTION.md).
Product Stage, synchronized Explorer и связь сцены с опциями добавлены в
[Interactive Product Experience v3.1](KORSAC-INTERACTIVE-PRODUCT-EXPERIENCE.md).
[Catalog Experience v1](KORSAC-CATALOG-EXPERIENCE.md) описывает PLAY ladder,
MINI-ветку, scoped controller и future Bitrix mapping.
[Homepage v1](KORSAC-HOMEPAGE-EXPERIENCE.md) и [Premium Shell](KORSAC-SITE-SHELL.md)
описывают новую публичную оболочку, editorial journey и будущие assets.

Источники продуктового содержания:

- [Бренд](../brand/KORSAC-BRAND-GUIDE.md).
- [PLAY 1440 baseline](../product/KORSAC-PLAY-1440-SPEC-v0.1.md).
- [Архитектура PLAY](../product/KORSAC-PLAY-ARCHITECTURE.md).
- [Архитектура MINI](../product/KORSAC-MINI-ARCHITECTURE.md).

## Файлы и запуск

```text
prototype/
├── index.html
├── review.html
├── ui.html
├── product.html
├── catalog.html
└── assets/
    ├── css/
    │   ├── tokens.css
    │   ├── base.css
    │   ├── layout.css
    │   ├── components.css
    │   ├── pages.css
    │   ├── product-stage.css
    │   ├── catalog.css
    │   ├── shell.css
    │   └── homepage.css
    ├── js/
    │   ├── prototype.js
    │   ├── product-experience.js
    │   ├── catalog-experience.js
    │   ├── shell.js
    │   └── homepage.js
    └── images/README.md
```

Откройте `prototype/index.html` в браузере. Относительные CSS/JS рассчитаны
на `file://`; нет `fetch`, ES-модулей и внешних ресурсов. Для HTTP-проверки
из корня репозитория:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory prototype
```

Откройте `/index.html`, `/ui.html`, `/product.html`, `/catalog.html`, `/review.html` на локальном порту 8000.
Установка пакетов, сборка и Bitrix не требуются. Архитектура рассчитана
на актуальные Chrome, Edge, Firefox и Safari; фактический список проверенных
браузеров и ограничения проверки нужно фиксировать в PR.

## Visual Direction v2

KORSAC узнаётся по повторяемой структуре: технический индекс у раздела,
направляющая линия, рамка с прерыванием угла, медная метка ревизии или
регистрации и синий сигнал взаимодействия. Рамка `k-frame` выделяет stage,
важные технические блоки и паспорт; обычные поля сохраняют понятную форму
и полную область нажатия. Общие поверхности и открытые полосы уменьшают
количество отдельных округлых карточек.

Desktop hero даёт продуктовой сцене большую долю ширины; рядом доминирует
PLAY 1440 и его сценарий 1440p. Stage оставляет место для будущей фотографии:
индексы, ревизия и направляющие располагаются по краям. На mobile порядок
идёт от media к сценарию, имени, короткому описанию, цене и CTA; компактные
характеристики следуют после действия. Высота media ограничена, чтобы CTA
появлялся раньше.

Страница чередует плотность: process rail, конфигуратор, открытая narrative
полоса, технические характеристики, зона измерений, связанная линия сборки,
паспорт SYSTEM ID и FAQ. Product/catalog content сохраняет эти примитивы;
public header/drawer/footer теперь использует более спокойный Shell v1.
Прежние development rails остаются в review hub.

## Токены и CSS

`tokens.css` содержит рабочую палитру `--korsac-*`, семантические роли `--k-*`,
типографику, интервалы, геометрию и централизованные motion-токены.
Electric Blue — сигнал выбора, фокуса и действия. Copper связывает
индексы, ревизии и серийную идентичность; его роль не распространяется
на основные CTA.

Для primary CTA сохранена заливка `#245DDD` с белым текстом. UI Kit сравнивает
её с `#397BFF` и тёмным текстом `#0B0E13`; сравнение не меняет рабочий токен.
Обоснование и расчёт контраста — в документе визуального направления.

Основной шрифт использует `system-ui`, системные fallback и `sans-serif`;
технические подписи — `SFMono-Regular`, `Consolas`, `Liberation Mono`,
`monospace`. Удалённые шрифты не загружаются. Монопространственный набор
применяется к индексам, ревизиям и техническим значениям, а основной текст
остаётся обычным и читабельным.

Префикс классов — `k-`; модификаторы — `--secondary`, `--image` и аналогичные.
`k-state-*` используется для статических примеров UI Kit. Реальные
`:hover`, `:active`, `:focus-visible`, `:checked` работают отдельно.

| Файл                | Ответственность                                                  |
| ------------------- | ---------------------------------------------------------------- |
| `tokens.css`        | Значения, семантические роли, duration/easing                    |
| `base.css`          | Reset, текст, ссылки, focus, reduced motion                      |
| `layout.css`        | Контейнер, grid, stack, cluster, прежняя review shell            |
| `components.css`    | Контролы, рамки, направляющие, паспорт, motion-примитивы         |
| `pages.css`         | Компоновка UI Kit, hero и разделов продукта                      |
| `product-stage.css` | Product Stage, контексты, Explorer, interactive fixture          |
| `catalog.css`       | Family navigation, scenario rail, карточки, preview и comparison |
| `shell.css`         | Общие public header, icons, native mobile navigation и footer    |
| `homepage.css`      | Editorial hero/discovery/feature/trust/ownership                 |

## Identity Primitives и Motion System

UI Kit содержит отдельные примеры индекса, section rail, угловой рамки,
selected-state, copper registration, validation rail и устройства SYSTEM ID.
В разделе Motion кнопки повторяют hero, выбор, validation sweep, паспорт
и появление индекса. Демонстрации не открывают корзину и не запускают расчёт.

Motion имеет три уровня: короткий сигнал контроля, раскрытие ключевого
элемента бренда и несколько последовательностей для hero и паспорта.
Спокойная страница движется после значимого события; постоянного scanning,
typing и декоративного прогресса нет. Основные анимации используют
`transform`/`opacity`; направляющие — `scaleX`.

`data-motion` задаёт тип последовательности, `k-motion-run` — её запуск,
`data-motion-replay` — ID повторяемого примера. Hero проходит от рамки
и media к маркеру модели, названию, фактам и CTA. Контролы доступны с первого
момента: последовательность не задерживает действие и не перемещает фокус.
Наблюдение за viewport ограничено несколькими важными якорями; обычный текст
не получает массовую scroll-анимацию.

### Reduced Motion

При `prefers-reduced-motion: reduce` значимое содержимое видно сразу:
нет stagger-зависимости, scanning, обязательного transform-входа и плавного
скролла. Состояние выбора и обновлённая подпись не зависят от анимации.
Базовый CSS не скрывает содержимое ради будущего reveal; оно читается без JS.

## Адаптивность и доступность

Контейнер ограничен 1360 px; поля адаптивны. Grid использует `minmax`, чтобы
дочерние блоки не задавали минимальную ширину страницы. На узких экранах
layout собирается в одну колонку, направляющая сборки становится вертикальной,
а сводка остаётся в потоке. На desktop компактная сцена закрепляется внутри
аппаратной группы; длинный manifest расположен сбоку от дополнительных
групп и прокручивается вместе со страницей, его CTA доступен.
Скролл вкладок ограничен tablist.

Контрольные ширины: 320, 375, 768, 1024, 1280 и 1440 px. Есть skip link,
один H1, явные labels и нативные radio/checkbox/select. Высота основных
контролов — не менее 44 px; фокус явно виден. Русские имена групп остаются
главными, технический индекс служит дополнительной навигацией.

Radio поддерживают нативные стрелки. Tabs используют Left/Right, Home/End
и roving tabindex. Accordion меняет `aria-expanded`/`aria-controls`.
Нативный `<dialog>` обеспечивает модальность, Escape и inert-фон; JS возвращает
фокус к открывшему контролу и блокирует прокрутку фона. Toast использует
`role=status`, не исчезает по таймеру и закрывается кнопкой.

Без JS доступны страницы, radio/select/checkbox и исходные содержимое вкладок
и ответы FAQ. Диалоги, переключение вкладок, повтор motion и синхронизация
подписей требуют JS.

## Prototype-only Summary Sync

`prototype.js` разделяет поведение navigation/dialog, tabs/accordion,
подписи конфигурации и запуск/replay motion. Сводка оформлена как manifest
с семантическим `<dl>`: фиксированные CPU/GPU и выбранные подписи корпуса,
памяти, накопителей, ОС, программ и сервиса.

Presentation metadata использует `data-summary-key`, `data-summary-value`
и `data-summary-output`. В `select` значение подписи хранит выбранный `option`.
JS сразу переносит текст выбранного контрола в соответствующую строку через
`textContent`; короткая активация rail сопровождает уже состоявшийся выбор.
Это локальная синхронизация отображения, без производственного XML_ID,
compatibility/availability rules и конфигурационного API.

**Регрессионное правило:** изменение любых опций не меняет цену hero,
сводки или карточки продукта. Цены и дельты остаются статическими числами
в HTML; JS не выполняет `price += delta` или иной ценовой арифметики.
Подпись demo price сохраняется в интерфейсе. Состояния confirmed/pending/error
в UI Kit — визуальные примеры будущего расчёта, а не результат валидации сборки.

## Interactive Product Experience v3.1

`product-experience.js` создаёт scoped controllers относительно
`data-product-experience`: hero, Explorer и сцена конфигуратора получают
выбранные подписи из тех же native controls. На desktop Explorer
использует обычную двухколоночную композицию сцены и единой detail-панели.
Кнопки контекстов, hotspots и Prev/Next вызывают один state controller;
счётчик 00/05–05/05, labels и highlight обновляются синхронно. На mobile/tablet
сцена, controls, explanation и navigation следуют обычным потоком.
Скролл, focus и URL не управляются состоянием сцены.

Пять button-hotspots открывают синхронизированные HTML-пояснения. Корпус меняет
условный силуэт; RAM — метаданные; SSD/SSD2 — подписи и второй слот.
SYSTEM ID показывает preview выбранных labels. Контексты измерений сохраняют
пустые метрики, а четыре всегда видимых этапа сборки имеют focus/click-пояснения.
Без JS overview и весь рассказ доступны. Reduced motion сохраняет переключение
состояния без expressive resolve. Цены не меняются.

В UI Kit добавлены Interactive Product Primitives с отдельным playground.
Архитектура слоёв, события, адаптивность и будущий media/kk.korsac adapter
описаны в [документе v3.1](KORSAC-INTERACTIVE-PRODUCT-EXPERIENCE.md).

«Добавить в корзину» открывает информацию о прототипе. Счётчик корзины,
заказы, localStorage, авторизация, поиск, фильтры, аналитика и сеть отсутствуют.

## Premium Site Shell и Homepage v1

Главная строит путь от сообщения «Компьютеры, точно собранные под задачу.»
к выбору PLAY, одному featured 1440 и рассказу об архитектуре/сборке/SYSTEM ID.
Нет повторных full-range cards, comparison dialog и шестисценарного Explorer.
Discovery — компактный экземпляр принятого `catalog-experience.js` с authored
HTML, пятью сценариями и MINI-веткой от 1440. Native details раскрывают один
аспект featured продукта и структуру будущего паспорта; результаты тестов
и реальные записи не выдуманы.

Общая публичная оболочка применяется к index/catalog/product/UI Kit:
sans navigation, text wordmark slot, inline SVG utility icons, native drawer
и открытый footer с большим wordmark. Developer/version bars удалены.
На homepage header sticky и переходит от hero к graphite за 220 ms; internal
pages сохраняют нормальный flow. Без JS работают nav/details/CTA и все пять
source summaries. Hero использует конечную 940 ms последовательность,
немедленно отменяемую live reduced motion. Brand/media slots ожидают
утверждённые logo SVG и фотографии. Подробнее — в двух новых документах выше.

## Catalog & Product Family Experience v1

Каталог начинает discovery с четырёх сценарных ступеней PLAY и отдельной
MINI-ветки от 1440. Выбор обновляет крупный preview и отметку source card;
все пять карточек постоянно доступны ниже в едином компактном scan layout.
PLAY 1440 выделен rail/индексом/акцентом; MINI непосредственно соединён
с узлом 1440 и подписан «Тот же 1440p · Mini-ITX». PRO объяснён более высоким CPU/GPU-классом, задачей high refresh
и SSD 2 ТБ; MINI — компактным Mini-ITX исполнением того же сценария 1440p.
CREATE/WORK показаны disabled buttons с подписью «В разработке».

`catalog-experience.js` создаёт собственный controller для каждого root.
Имена, baseline и CTA читаются из HTML-карточек; JS хранит presentation state,
а не второй каталог компонентов. Сравнение 2–3 моделей открывает native dialog
с семью документированными свойствами на desktop. Небольшая панель
появляется после первой отметки. Mobile comparison показывает пять коротких
свойств по строкам, с 2–3 значениями рядом и sticky model header; длинные
purpose/setup prose скрыты в этой матрице. Горизонтального overflow нет.
Цена PLAY 1440 — 179 900 ₽ с пометкой «Цена — пример», остальные неизвестны.
Рекомендации authored по сценарию и не используют ценовые пороги.

Без JS доступны anchor-сценарии, вся линейка и обычные ссылки; enhanced
preview/comparison скрыты. Reduced motion оставляет мгновенный выбор без
320 ms resolve. Карточки линейки показывают сценарий, форм-фактор, GPU,
RAM/SSD и одну CTA; подробности и обе CTA остаются в выбранном preview. Архитектура, media adapter и перенос в `bitrix:catalog.section`
описаны в [Catalog Experience](KORSAC-CATALOG-EXPERIENCE.md).

## Данные макета

В продукте PLAY 1440 CPU/GPU фиксированы: Ryzen 7 9700X и RTX 5070 12 ГБ. Основные опции — RAM
32/64 ГБ, SSD и корпус. OS/software/service — визуальные группы, требующие
согласования; недопущенные варианты disabled. Корпуса из shortlist — кандидаты,
а выбор LANCOOL 217 в макете не утверждает производственный default.
MINI остаётся отдельным товаром.

Wordmark — временный текст, не финальный логотип. Wireframe — placeholder
для будущей фотографии. SYSTEM ID показывает паспорт с вымышленным номером
без fake QR/barcode. Производительность содержит структуру будущих измерений:
игра, разрешение, preset, AVG FPS, 1% low, температура, шум и методика;
измеренные значения не подставлены. Гарантия и доставка требуют согласования.
Линия сборки показывает рабочий процесс, а не обещание SLA.

## Будущий перенос в Bitrix

| Основа прототипа                        | Будущая точка интеграции                                |
| --------------------------------------- | ------------------------------------------------------- |
| Header/footer                           | `local/templates/korsac/header.php` / `footer.php`      |
| Каталожная карточка / family / сценарий | `bitrix:catalog.section`, sections и product properties |
| Hero, описание, характеристики          | шаблон `bitrix:catalog.element`                         |
| Опции, выбор, validation rail           | тема `kk.korsac.configurator-renderer`                  |
| Группы и сводка конфигурации            | `kk:korsac.configurator`                                |
| Будущий интерфейс корзины               | шаблон `Bitrix sale.basket.basket`                      |

Выбор renderer, calculate pending/calculated/error, ConfiguratorCore selection
и authoritative calculate response должны стать реальными источниками
состояния. [Подробное соответствие](KORSAC-VISUAL-MOTION-DIRECTION.md#будущий-renderer)
отделяет мгновенный selected-state от серверного результата расчёта.

При переносе shell-дублирование убирается в header/footer. Имена, физические
SKU, разрешённые варианты, наличие и цена поступают из реальных данных.
Backend сохраняет проверенный snapshot конфигурации для корзины.
Статические числа и тексты прототипа не становятся бизнес-логикой,
контрактом SKU, production-статусами или гарантийными обязательствами.

## Проверка перед PR

Следующий список определяет проверки; факт выполнения и ограничения среды
фиксируются в PR, а не подразумеваются самим наличием списка.

- HTTP открывает все четыре страницы; относительные ресурсы целы. `file://` проверяется, если браузерная политика среды позволяет.
- Консоль без ошибок; нет внешних запросов или remote fonts.
- При 320/375/430/768/1024/1280/1440 px страница не имеет горизонтального overflow; mobile CTA идёт перед компактными характеристиками.
- Tab, Shift+Tab и стрелки работают для radio, tabs и обычных контролов; focus виден.
- Accordion корректно меняет `aria-expanded`; dialog/drawer закрываются кнопкой, Escape и фоном, возвращая фокус.
- Корпус, RAM, SSD, дополнительный накопитель, ОС, программы и сервис обновляют соответствующие подписи manifest.
- После всех изменений опций цены hero, сводки и карточки остаются неизменными; сетевых запросов нет.
- Motion replay работает без reload и бизнес-действий; анимации конечны и не лишают контролы доступности.
- Reduced motion показывает содержимое сразу и отключает последовательности; no-JS сохраняет смысл и native controls.
- Homepage/shell: восемь ширин 320–1920, native utility dialogs/drawer/focus, no-JS меню/сценарии/CTA, конечный hero и live reduced motion.
- Каталог: все пять моделей, MINI как ветка узла 1440, preview/CTA и MAX3 comparison; touch375/430, no-JS320 и live reduced motion.
- Контраст текста, copper, синего, CTA, selected/disabled state проверен отдельно от декоративных линий.
- Ссылки, labels, IDs и `aria-controls` согласованы; `git diff --check` проходит.

[Материалы визуального ревью](review/README.md) сохраняют product v1/v2/v2.1/v3.1 и добавляют homepage/shell v1; исходные v3 и catalog captures сохраняются.
Снимки не используются runtime. Проверка одного браузера не заменяет ручной
приёмочный прогон во всех целевых браузерах.
