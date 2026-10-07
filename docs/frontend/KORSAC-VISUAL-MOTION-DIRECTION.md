# KORSAC — Visual Identity & Motion Direction v2

## Концепция

KORSAC — точный инженерный инструмент. Интерфейс соединяет подачу продукта
с читаемостью технической документации: сценарий использования, факты,
конфигурация, измерения и паспорт системы. Обычный текст остаётся спокойным,
а технические элементы организуют информацию и помогают найти действие.

Основу узнаваемости составляют несколько повторяемых механизмов:

- Индексы разделов и групп: номер, техническое имя и понятный русский заголовок.
- Тонкие направляющие связывают секции, опции и этапы сборки.
- Асимметричный hero отдаёт большую долю ширины product stage.
- Рамка с прерыванием угла и короткой регистрационной меткой выделяет ключевые блоки.
- Copper обозначает ревизию и серийную идентичность; синий обозначает действие и выбор.
- Manifest конфигурации и SYSTEM ID связывают интерфейс с конкретной системой.
- Короткие последовательности подтверждают событие через появление линии и разрешение деталей.

Эта грамматика повторяется в header/footer, product stage, конфигураторе,
измерительном блоке, паспорте и каталожной карточке. Она может перейти
в каталог, корзину и checkout через те же rails, индексы и состояния.
В версии v2 wordmark был текстовым.
[Brand Asset Integration](KORSAC-BRAND-ASSET-INTEGRATION.md) использует
утверждённые SVG masters для современной public shell и hero.
В [Premium Site Shell v1](KORSAC-SITE-SHELL.md) публичные header/footer
становятся спокойнее: grammar v2 остаётся у продуктового содержания,
а version/registration chrome сохраняется только в review hub.

## Цвет и типографика

Electric Blue `#397BFF` служит сигналом взаимодействия: focus, выбранный
вариант, ссылка, active tab и короткое подтверждение. Для ссылок и фокуса
используются соответствующие семантические оттенки с читаемым контрастом.
Copper `#C38E5D` применяется к ревизии, серийному номеру, индексу и регистрационной
метке. Он не превращается в основную заливку кнопок или фон целого раздела.

Основной стек `system-ui`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`,
`sans-serif` использует установленный системный шрифт. Технический стек —
`SFMono-Regular`, `Consolas`, `Liberation Mono`, `monospace`. Это явный набор
fallback без отсутствующих Inter/Manrope/Geist и без remote fonts; форма
системного шрифта зависит от ОС. Mono используется для индексов, чисел,
ревизий и серийных обозначений, обычный текст — для чтения и выбора.

### Выбор primary CTA

В `ui.html` показаны две допустимые пары. Контраст вычислен по относительной
яркости sRGB для сплошных заливок:

| Вариант                               | Заливка / текст       | Контраст |
| ------------------------------------- | --------------------- | -------- |
| A, текущий primary                    | `#245DDD` / `#F4F6F8` | 5,26:1   |
| B, сравнение                          | `#397BFF` / `#0B0E13` | 5,02:1   |
| Недопустимая пара для обычного текста | `#397BFF` / `#FFFFFF` | 3,85:1   |

Обе демонстрационные пары A/B проходят AA для обычного текста. Рабочий
primary остаётся A: белая подпись сохраняет иерархию действия на тёмном фоне,
а Electric Blue продолжает связывать выбранные состояния. B остаётся
отдельным образцом для визуального сравнения, без изменения primary token.
Hover/active, подписи на поверхностях и disabled проверяются отдельно.

## Рамка, rails и индексы

`k-frame` — тонкая рамка с прерыванием у угла, небольшим угловым сигналом
и регистрационным акцентом. Декоративная геометрия строится CSS-слоями
и pseudo-elements; она не обрезает нативные контролы и не уменьшает hit area.
Примитив предназначен для product stage, важных технических блоков и паспорта.
Selected option наследует угол и короткую синюю rail без необходимости
окружать каждое поле новой панелью.

Section rail объединяет номер, вторичное техническое имя и линию. Индекс
помогает ориентироваться, но не заменяет название «Оперативная память»
или «Характеристики». Русские подписи остаются главными в customer-facing
контролах; serial/revision и технический английский — дополнительный слой.

Техническая плотность должна соответствовать роли блока. Полный набор
revision, product/configuration labels, serial и registration сохраняется
для главных якорей: hero, конфигуратора и SYSTEM ID. В будущих карточках
каталога, корзине и checkout достаточно одного идентификационного якоря
и ясного названия; каждый блок не требует новой серии технических меток.
Rails и состояния поддерживают узнаваемость без декоративного насыщения.

В review-навигации v2 номер задаёт явный `k-nav-index` в HTML. CSS оформляет
его, но не генерирует дополнительную нумерацию через counters/pseudo-elements.
Публичный drawer Shell v1 использует названия без numeric indices.

Product stage готов к будущей фотографии: модель, категория и ревизия
на краях кадра, спокойные позиционные отметки, свободное поле media.
Текущий wireframe не имитирует фотографию. На desktop сцена занимает
большую часть hero, на mobile ограниченная высота сохраняет её важность
и оставляет место для цены и CTA перед характеристиками.

Конфигуратор использует последовательные группы, ясный selected-state
и manifest на `<dl>`. Синий rail и активация угла читаются сразу благодаря
`:checked`; анимация сопровождает готовый выбор. Process rail и assembly
timeline связывают этапы общей линией, которая становится вертикальной
на mobile. Performance — зона будущих измерений с пустой шкалой и полями
для игры, разрешения, preset, AVG FPS, 1% low, температуры, шума и методики;
числовые результаты не выдумываются.

SYSTEM ID — паспортный якорь: label, крупный серийный пример, ревизия,
технические данные, небольшая сетка и copper registration. Вымышленный
серийный номер явно остаётся демонстрационным; QR/barcode не генерируются.

## Motion System

Принцип: интерфейс спокоен, пока не происходит значимое событие. Motion
обозначает действие, новый контекст или состояние; непрерывного scanning,
typing, bounce, большого zoom и декоративного прогресса нет.

### Motion Visibility Pass v2.1

В v2 сдвиги 2–6 px были слишком малы для уверенного восприятия brand motion.
V2.1 усиливает четыре существующих момента: hero, подтверждение опции,
validation и SYSTEM ID. Композиция, палитра, содержимое продукта, drawer
и select остаются теми же. Обычный hover/focus, tabs, accordion и dialog
сохраняют короткое interface motion; новые scroll anchors не добавляются.

| Механизм                                | V2.1                                                                                   |
| --------------------------------------- | -------------------------------------------------------------------------------------- |
| Product media                           | `translateY(16px) scale(.985)` → исходное положение                                    |
| Brand marker                            | 12 px по горизонтали                                                                   |
| Scenario / description / system details | 16 px по вертикали                                                                     |
| Цена и CTA                              | 8 px по вертикали, без scale и скрытия                                                 |
| Большое 1440                            | горизонтальная `clip-path` маска, без обычного fade                                    |
| Serial                                  | горизонтальная маска и 12 px сдвиг; номер раскрывается целиком                         |
| Frame / registration                    | рост top rail по X и side rail по Y; copper завершает вход                             |
| Option / manifest                       | rail/corner за 320 ms, 6 px resolve подписи и короткий сигнал только изменённой строки |

Рамка использует один декоративный `k-frame-trace` с двумя CSS-линиями.
Он заменяет верхнюю и левую границы только во время последовательности,
а затем уступает место обычной рамке. SYSTEM ID начинает с copper-линии.
Нет ожидания JS для чтения, дополнительных панелей или постоянного свечения.
Сильнее стали амплитуда, линейная геометрия и ритм тех же четырёх моментов;
количество событий и два наблюдаемых passport/index якоря не увеличились.

На узких экранах media фиксируется с горизонтального смещения 12 px
и того же `scale(.985)`. Вертикальный сдвиг в компактном stage пересекал
неподвижные metadata/caption; смена оси сохраняет видимый вход без изменения
высоты сцены, неподвижных metadata/caption или mobile CTA. Маска 1440 и
остальные brand-последовательности сохраняются. Подпись placeholder media
поднята на 2 px внутри сцены, чтобы округление размеров в конце scale не
пересекало caption; положение wireframe и высота сцены не меняются.

Токены централизованы в `prototype/assets/css/tokens.css`:

| Токен                | Длительность | Роль                                           |
| -------------------- | ------------ | ---------------------------------------------- |
| `--k-motion-reduced-fast` | 80 ms | Reduced Motion: hover/focus/color/border |
| `--k-motion-reduced-base` | 120 ms | Reduced Motion: opacity/state acknowledgement |
| `--k-motion-instant` | 80 ms        | микросигнал                                    |
| `--k-motion-fast`    | 140 ms       | hover/focus и короткий отклик                  |
| `--k-motion-base`    | 220 ms       | интерфейс, угол, price/CTA                     |
| `--k-motion-brand`   | 320 ms       | подтверждение опции/строки и narrative content |
| `--k-motion-slow`    | 420 ms       | rail, frame и важный технический блок          |
| `--k-motion-reveal`  | 620 ms       | однократная calibration sweep                  |

| Easing token         | Значение                         | Роль                                       |
| -------------------- | -------------------------------- | ------------------------------------------ |
| `--k-ease-standard`  | `cubic-bezier(0.2, 0, 0.2, 1)`   | переход между состояниями интерфейса       |
| `--k-ease-enter`     | `cubic-bezier(0.16, 1, 0.3, 1)`  | быстрое появление со спокойным завершением |
| `--k-ease-exit`      | `cubic-bezier(0.4, 0, 1, 1)`     | освобождение контекста                     |
| `--k-ease-precision` | `cubic-bezier(0.65, 0, 0.35, 1)` | контролируемое разрешение направляющей     |

Кривые определены вместе с duration в tokens, а не повторяются по компонентам.
Три уровня motion используют эту общую шкалу: interface, brand и ограниченные
narrative-последовательности hero/SYSTEM ID.

### Последовательности

| Событие         | Последовательность                                                    | Ограничение                                   |
| --------------- | --------------------------------------------------------------------- | --------------------------------------------- |
| Hero            | frame/guide → media → marker → 1440 mask → copy → price → CTA → facts | 840 ms, цена/CTA доступны сразу               |
| Выбор опции     | native selection + label → blue rail/corner + manifest row            | 320 ms, только изменённая строка, нет расчёта |
| Validation demo | явный pending/confirmed/error + конечная rail                         | 620 ms для sweep, состояние задаёт reviewer   |
| SYSTEM ID       | copper side → frame → label → serial mask → details → registration    | 840 ms, serial целиком, без typing            |
| Section index   | видимый индекс → короткое раскрытие rail                              | только выбранные важные якоря                 |

Hero: top frame стартует в 0 ms, side guide — 80 ms, media — 160 ms,
marker — 240 ms, 1440 — 320 ms, scenario — 420 ms, description — 460 ms,
price — 520 ms, CTA — 600 ms, copper registration — 620 ms, facts — 700 ms.
Последний этап завершается в 840 ms. Смысловые подписи сохраняют полную
непрозрачность; цена и CTA находятся в документе и принимают фокус/клик
на всём протяжении входа. Маска designation не применяется к контролам.

SYSTEM ID: copper side стартует в 0 ms, top frame — 100 ms,
label — 220 ms, serial — 320 ms, details — 450 ms, registration/footer —
620 ms. Последний этап завершается в 840 ms. Serial не меняет текст
и не набирается посимвольно; клип раскрывает его как один объект.

Confirmed, recalculating и error представлены отдельными доступными
состояниями. Короткая validation rail показывает процесс расчёта, а явная
подпись объясняет результат; подтверждение расчёта не утверждает, что
система прошла производственную проверку. Sweep конечен и не подменяет
текст доступного статуса.

Pending rail проходит от 8% до 100% и возвращается к устойчивым 32%.
В validation demo rail усилена до 4 px. Короткий светлый calibration head
подчёркивает проход; он заканчивается вместе со sweep. Confirmed раскрывает
полную rail; error сразу показывает
danger rail и подпись без мигания. В UI Kit три кнопки выбирают эти
визуальные состояния вручную. Таймер не превращает pending в confirmed:
демонстрация не имитирует запрос и не утверждает успех реального расчёта.

В `prototype.js` motion отделён от navigation/dialog и summary labels.
`data-motion="hero|selection|validation|passport|index"` выбирает пример,
`k-motion-run` запускает CSS-последовательность; кнопка
`data-motion-replay="id"` повторяет её без reload. IntersectionObserver
используется только для нескольких значимых passport/index anchors.
Остальное содержимое находится в документе без scroll fade-up.

Основные свойства анимации — `transform`, `clip-path` и декоративная `opacity`;
линии используют `scaleX`/`scaleY`. Только изменённая manifest row получает
краткий low-contrast background signal; вся summary card не анимируется.
Motion не блокирует hit area, не удаляет focus и не переносит его.
Смысловой текст сохраняет `opacity: 1` на всём протяжении анимации; его
последовательность задают короткие смещения. Изменение прозрачности применяется
к декоративным copper-фрагментам рамки, чтобы контраст подписей оставался полным.
Новые animation frameworks, canvas, WebGL и внешние зависимости не нужны.

### Reduced Motion и отсутствие JS

KORSAC использует **reduced-motion mode, не blanket zero-motion mode**.
`prefers-reduced-motion: reduce` уменьшает движение, сохраняя быстрый visual
feedback. Общие tokens: `--k-motion-reduced-fast: 80ms` и
`--k-motion-reduced-base: 120ms`; interface fast/base переходят на эту шкалу.
Нет глобального `animation/transition: none` для всего сайта.

| Остаётся полностью отключённым | Сохраняется как low-motion feedback |
| --- | --- |
| Shared 1500 ms Brand Intro; timestamp записывается | Короткие opacity/color/border changes 80–120 ms |
| Translate/scale entrances, clip/mask reveals | Homepage: opacity .9 → 1 для основных групп, 120 ms, без stagger |
| Decorative rail growth/sweeps и scroll identity reveals | Catalog: opacity .86 → 1 на выбранном preview, 120 ms |
| Parallax/scroll-driven decoration | Explorer/summary/selected rails, validation acknowledgement |
| UI Kit brand Eye Flash replay | Dialog/drawer/accordion opacity, hover/focus/active controls |

Смысловое состояние, labels/hidden/inert/ARIA и native input обновляются
синхронно до feedback. Текст/CTA доступны с первого кадра: opacity settle
не начинается с нуля. Decorative Hero field/guide/copper остаются в final
state, Hero mark — внешний static eyes-off SVG. Product stage и Explorer
не получают animated transform/clip; статические геометрические размеры и
контуры сохраняются. Selected state, validation status и focus rings видимы
независимо от animation; не нужно ждать completion.

Live normal → reduce отменяет активные WAAPI/CSS effects и pending frames/timers,
возвращает итоговое состояние без spatial движения. Будущие взаимодействия
используют reduced feedback. Возврат в no-preference не повторяет entry/intro;
identity anchors, встреченные при reduce, считаются уже просмотренными.
Смысловые элементы не скрыты в ожидании JS. Без JS читаются страницы,
manifest базовой конфигурации, вкладки/FAQ и работают нативные контролы;
replay и summary sync требуют JS.

[Motion/accessibility review](review/README.md#reduced-motion-refinement-v1)
фиксирует Chromium media emulation и remaining human gate. Windows animations
setting поступает через browser media query; реальная Windows-система в cloud
не доступна, проверка проведена с `prefers-reduced-motion: reduce`.

## Подписи конфигурации и статические цены

Прототип знает выбранный control и его отображаемую подпись. Metadata
`data-summary-key`/`data-summary-value` переносится в `data-summary-output`
через `textContent`; у `select` выбранный `option` задаёт подпись. Это касается
корпуса, RAM, SSD, дополнительного накопителя, ОС, программ и сервиса.
Label обновляется синхронно с native change. Только соответствующая
`k-manifest-row` получает blue sweep, короткий фон и resolve значения;
вся summary card и её validation/price не повторяют анимацию.

Цены hero, manifest и product card — статический HTML. Изменение выбора
не меняет их; дельты опций не используются в арифметике. Никаких production
XML_ID, правил совместимости, availability, API, корзины и persistence нет.
Регрессионная проверка должна сравнить цены до и после всех изменений опций.

## Будущий renderer

Ниже направление для `kk.korsac.configurator-renderer`, а не реализованная
интеграция. `kk.korsac`, Bitrix и ConfiguratorCore в этой задаче не изменяются.

| Визуальный механизм                | Будущий источник состояния                             |
| ---------------------------------- | ------------------------------------------------------ |
| Selected option + blue rail/corner | выбранное состояние renderer                           |
| Validation rail + pending label    | `calculate pending`                                    |
| Confirmed calculation label        | `calculated` для актуального выбора                    |
| Error rail + понятное сообщение    | ошибка renderer / расчёта                              |
| Manifest labels                    | `ConfiguratorCore selection` и реальные display labels |
| Price и разрешение действия        | authoritative calculate response                       |

Renderer показывает выбранный control сразу, затем подтверждает стоимость
только актуальным серверным ответом. Во время pending/error UI должен
различать выбранные параметры и ещё не подтверждённый расчёт. Ответ для
устаревшего выбора не должен подтверждать новую конфигурацию. Совместимость,
наличие, SKU и цена принадлежат production-данным и backend; статическая
presentation metadata не становится их контрактом.

## Ревью

[Снимки v1/v2](review/README.md) позволяют сравнить композицию, положение
mobile CTA, manifest и паспорт. Motion проверяется через replay в UI Kit,
поскольку статичный снимок не показывает последовательность.

Для v2.1 в [материалах ревью](review/README.md) есть короткая запись
реального проигрывания. Она помогает увидеть ритм, но не заменяет ручное
ревью в браузере на desktop/mobile, с обычной и reduced motion настройками.
Человек должен подтвердить, что четыре момента заметны при нормальном
использовании, остаются точными и спокойными, а состояние понятно без motion.

При ревью важны связность системы и читаемость: узнаются ли rails и рамка
без wordmark; помогают ли индексы ориентироваться; сохраняет ли photography
главную роль; подтверждает ли движение смысловое событие; остаются ли
selected-state и данные доступными при reduced motion. Фактические результаты
responsive, keyboard, contrast и console проверок фиксируются в PR.
