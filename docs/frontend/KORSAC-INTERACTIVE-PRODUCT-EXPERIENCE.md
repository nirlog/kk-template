# KORSAC — Interactive Product Experience v3.1

## Назначение

Взаимодействие помогает разобрать PLAY 1440: от пути воздуха и фиксированного
GPU-класса до выбранных RAM/SSD и подготовки системы. Сцена отвечает на
конкретный выбор пользователя и контекст рассказа. Motion подтверждает
состояние, но не является условием чтения или работы контролов.

Основа — принятый Visual/Motion v2.1: interrupted frame, copper registration,
синий selected-state, конечные resolve-последовательности. Большой 1440,
мобильный CTA, явные индексы drawer и локальный select chevron сохранены.
Технические подписи сосредоточены у сцены, manifest и SYSTEM ID;
остальной рассказ использует обычные заголовки и текст.

Источники: [бренд](../brand/KORSAC-BRAND-GUIDE.md),
[PLAY 1440](../product/KORSAC-PLAY-1440-SPEC-v0.1.md),
[архитектура PLAY](../product/KORSAC-PLAY-ARCHITECTURE.md),
[Visual & Motion Direction](KORSAC-VISUAL-MOTION-DIRECTION.md).
CPU Ryzen 7 9700X и GPU RTX 5070 12 ГБ остаются фиксированными.
Корпуса — кандидаты shortlist; схема не утверждает производственную ревизию.

## Файлы и экземпляры

`prototype/assets/css/product-stage.css` содержит сцену, оверлеи, состояния,
Explorer и адаптивную компоновку. `prototype/assets/js/product-experience.js`
— отдельный classic script с `defer`, загружаемый после `prototype.js`.
Нет модулей, загрузчика, сборки, npm или runtime-запросов.

Контроллер создаётся относительно каждого `[data-product-experience]`.
Внутри контейнера находятся native конфигуратор и независимые экземпляры
`[data-product-stage]`. На продукте роли — `hero`, `explorer`, `configurator`;
в UI Kit роль `playground` живёт в собственном контейнере. У экземпляров
различные IDs панелей и SVG markers. `window.korsacStage` и общий mutable
объект конфигурации отсутствуют.

Hero сохраняет обзор и реагирует на вариант корпуса. Explorer изучает систему.
Конфигуратор показывает область, связанную с текущим hardware-control.
UI Kit демонстрирует тот же контроллер в разделе **Interactive Product
Primitives**: кнопки, hotspots, панель, синхронизированные detail/Prev/Next и native fixture.

Слои отдельной сцены:

1. `data-stage-media`: условный корпус и базовые компоненты.
2. `data-stage-overlay`: airflow и направляющая подготовки, декоративные и
   `aria-hidden`, без перехвата pointer events.
3. Native buttons: контексты и пять annotations с hit area 44×44 px.
4. `data-stage-panel`: заголовок, identifier и короткое пояснение в HTML.
5. `data-stage-output`: подписи выбранных опций.

## Состояния и ручной выбор

| `data-stage-state` | Смысл и видимый сигнал |
| --- | --- |
| `overview` | Условный корпус, базовая архитектура и выбранные подписи |
| `airflow` | Направление притока и отвода; без температурного расчёта |
| `graphics` | Выделенная GPU-зона, фиксированный RTX 5070 |
| `platform` | CPU/RAM-зоны, метаданные выбранного объёма памяти |
| `storage` | Основной SSD и отдельный слот второго накопителя |
| `validation` | Этап подготовки и пояснение проверки; без статуса результата |

`data-stage-annotation` выбирает одну панель. CPU и memory annotations
используют общий `platform`, но показывают разные пояснения.
`data-stage-case` задаёт `standard`, `north` или `minimal` — три условных
силуэта и разных рисунка фронтальной зоны. `data-stage-extra` включает
второй слот. `data-stage-build` выделяет один из четырёх этапов подготовки.
Эти атрибуты описывают отображение, а не production selection/schema.

Кнопки контекстов используют `aria-pressed`. Hotspots имеют русские
`aria-label`, `aria-controls`, `aria-expanded` и обычную Tab-навигацию.
Enter/Space открывают соответствующее пояснение в detail-зоне Explorer
или под отдельной сценой конфигуратора. Hover лишь меняет
стиль кнопки. Модальность, автоматический перенос фокуса и hover-only
пояснения не используются.

## Synchronized Product Explorer

Explorer — компактный модуль «сцена → выбор аспекта → объяснение». При ширине
от 1100 px обычный grid делит пространство примерно 55/45 между Product Stage
с controls и единой detail-зоной. Sticky, scroll-driven переключение и длинная
последовательность articles в Explorer отсутствуют. Прежние viewport-якоря
брендового motion остаются в `prototype.js`; продуктовый controller не
создаёт observer и не следит за scroll position, resize или URL/history.

### Одно состояние

`data-stage-state` конкретного экземпляра — authoritative presentation state.
Единый порядок `explorerStates` в JS: overview, airflow, graphics, platform,
storage, validation. Один `setStageState(state, context)` синхронно меняет
highlight сцены, `aria-pressed` controls, active hotspot, видимый HTML article,
identifier, счётчик и кнопки соседних аспектов. Независимых slider/narrative
state и глобального singleton нет. Счётчик всегда **00 / 05 … 05 / 05**:
обзор имеет номер 00, затем пять инженерных аспектов.

Все пути ввода используют этот же метод:

- Контекстная кнопка задаёт state напрямую.
- Hotspot задаёт state и при необходимости CPU/memory subannotation platform.
- Prev/Next читают текущий `data-stage-state`, находят его в `explorerStates`
  и выбирают соседа; labels берутся из русских context controls.
- Разрешённое hardware-событие меняет контекст только сцены конфигуратора
  или UI Kit fixture. На странице текущая инспекция Explorer сохраняется.

Prev disabled на overview, Next disabled на validation. Нет looping,
autoplay, таймеров переключения, swipe-зависимости или horizontal scroll track.
Prev/Next — настоящие buttons высотой минимум 44 px. Они сохраняют естественную
keyboard-навигацию; controller не вызывает focus или scroll.

### Detail и annotations

Все шесть explanations находятся в HTML как `[data-explorer-slide]` /
`[data-stage-panel]`: индекс, heading, короткий текст и factual note.
CPU/memory — дополнительные paragraphs внутри единственного platform article;
они не добавляют седьмой основной state и не участвуют в Prev/Next order.
Их IDs остаются целями `aria-controls` соответствующих hotspots.
Platform и storage используют `data-stage-output` из native controls, поэтому
подписи обновляются также внутри временно невидимых explanations.

В enhanced mode articles занимают один grid slot: только активный виден.
Остальные получают `hidden` и `inert`. Scoped CSS оставляет их невидимые
intrinsic размеры в grid через `visibility: hidden`, сохраняя высоту модуля
и footer при переключении. Аналогично устроено место subannotations.
Неактивные элементы исключены из accessibility tree и Tab-порядка;
проверено браузерным accessibility snapshot. Большого fixed/min-height,
JS-измерения высоты и задержки замены текста нет.

До 1099 px схема, controls, detail и navigation идут обычным DOM-потоком.
Mobile использует 2×3 context buttons и более компактную схему, сохраняя
44×44 hit areas hotspots. Caption остаётся явным: это условная схема.
Выбор кнопки/hotspot обновляет рядом counter и explanation; из detail-footer
Prev/Next меняют ту же видимую панель, без необходимости возвращаться к
позднему article или прокручивать страницу программно. No-JS показывает
все шесть explanations обычной последовательностью и overview-схему;
дополнительные controls скрыты до enhancement.

На Chromium 1440×1080 высота раздела уменьшилась с 3242 до 837 px;
на 375 px — с 3383 до примерно 1103 px. При смене шести states и двух
platform subannotations высота стабильна на контрольных ширинах.
Эти размеры включают heading и отступы, а не только схему.

## Конфигуратор → сцена → паспорт

Единственный источник выбранных опций — native checked input или selected
option внутри `[data-prototype-config]`. Контроллер перечитывает их при
каждом событии; отдельно сохранённого case/RAM/SSD state нет.
`data-summary-key`/`data-summary-value` продолжают питать manifest через
`prototype.js`. Новый контроллер переносит только текст и presentation flags
в сцену и `[data-passport-output]` через `textContent`.

| Native control | Реакция сцены конфигуратора |
| --- | --- |
| Корпус | `overview`, вариант корпуса, его подпись во всех сценах и SYSTEM ID |
| RAM 32/64 ГБ | `platform`, memory annotation и метаданные; силуэт тот же |
| Основной SSD 1/2 ТБ | `storage`, подпись и основной слот |
| Второй SSD | `storage`, подпись и отдельный видимый слот или его отсутствие |
| ОС, software, service | Только прежние строки manifest |

`focusin` hardware-control выбирает контекст конфигуратора; `change`
синхронизирует подписи всех экземпляров. В Explorer текущий смысловой state и CPU/memory subannotation
сохраняются; обновляются только выбранные labels и case/slot media flags. Интеракция с одной сценой не переключает остальные сцены.
На большом desktop компактная сцена конфигуратора закрепляется только внутри
группы case/RAM/SSD/SSD2. При работе с памятью и накопителями реакция остаётся
рядом с controls; сцена не перекрывает следующий ряд. ОС/software/service и
длинный manifest расположены ниже и прокручиваются обычным образом.
На tablet/mobile и низком desktop сцена также в потоке; на узком экране она
идёт перед аппаратными controls в DOM и визуальном порядке.

SYSTEM ID отображает выбранные case/RAM/SSD/SSD2 как preview. Серийный номер
остаётся явным макетом; QR, barcode и verification endpoint отсутствуют.
Все цены и дельты — статический HTML. Ни один из контроллеров не вычисляет
`base + delta`, не меняет цену и не принимает выбор за подтверждение расчёта.

## Измерения и сборка

Контролы будущих измерений выбирают игровой сценарий, графический режим
и группу метрик. Они меняют подпись методики и активную rail соответствующих
карточек. FPS, 1% low, температура и шум остаются `—` с пояснением ожидания
реальных тестов. Числа не генерируются.

Assembly / Setup / Testing / Final Check всегда представлены четырьмя
читаемыми шагами. Focus/click кнопки выделяет этап, обновляет дополнительное
пояснение и переводит explorer/configurator в `validation`. Rail показывает,
что обсуждается, а не выдуманный прогресс или успешное прохождение проверки.
Hero сохраняет обзор. Автопроигрывания и carousel нет.

## Motion, быстрый ввод и доступность

Локальный DOM event `korsac:stage-motion` на конкретной сцене передаёт работу
существующему cancellable motion runner в `prototype.js`.
Контроллер обновляет смысловое состояние синхронно, затем запускает feedback.

Stage и detail resolve используют существующий `--k-motion-brand` (320 ms) и
`--k-ease-precision`: панель смещается на 8 px, декоративная rail раскрывается,
при смене корпуса media получает короткий clip/translate. Detail heading/index
получают тот же 8 px mask/resolve, техническая rail — конечный line resolve. Полный hero reveal
при переключении не повторяется. Нет задержки клика, вращения, большого zoom
или обязательного исчезновения текста.

Повтор прерывает motion только своего экземпляра; animationend и конечный
fallback удаляют служебные классы. Последний native input определяет итог.
При Reduced Motion state/labels меняются сразу; пространственный stage/clip
и rail sweep отключены. Stage panel/detail/case используют opacity-only settle
180 ms, summary/manifest — 180 ms opacity/color/accent acknowledgement; selected
controls, parts и hotspot border/color — 110 ms. Dialog/accordion — 180 ms opacity.
Stage figure/panels, Explorer heading и manifest row получают краткий selected
background и fixed 3 px inset blue accent, без border/layout/growth движения.
Это reduced-motion mode, не blanket zero-motion. CSS branch сохраняет static
геометрию сцены. Live preference change отменяет effects/frames/timers;
будущие input используют reduced feedback, обратный toggle не повторяет hero.
Mobile Explorer сохраняет ту же структуру и 44px hotspots/controls; внутренние
spacing tokens компактнее на ≤599px, чтобы после80px sticky-anchor offset
локальное пояснение оставалось в первом practical viewport. Нет forced scroll.
Desktop configurator pin стоит ниже88px header +24px gap.

Без JS сцены показывают `overview`, шесть explanations и annotation-пояснения
доступны, native controls остаются обычными controls. Только дополнительные
кнопки и интерактивные пояснения скрыты до enhancement. При этом label sync
не работает; HTML явно остаётся прототипом. Контекстные панели не объявляются
через live region: быстрый выбор не создаёт поток screen-reader announcements.
Прежний manifest сохраняет polite feedback от явного изменения опции.

## Замена схемы реальными media

Wireframe намеренно нейтрален: подпись «Условная схема · не фотография корпуса»
есть в каждой подробной сцене. Пропорции, рисунок фронта и позиции компонентов
не являются изображением конкретного физического корпуса.

На следующем этапе `data-stage-media` можно заменить локальным `<picture>`
с production-фотографией выбранного корпуса. Контекстные панели и native
выбор останутся прежними. Для каждого media-варианта потребуется согласовать
crop, object-fit, responsive размеры и расположение hotspots/airflow overlays.
Текущие координаты условной схемы нельзя считать точными координатами фото.
При отсутствии подробного снимка остаётся обзорное media и текстовая панель;
state не должен зависеть от загрузки изображения. Review PNG/MP4 не являются
такими product assets и не загружаются страницами.

## Перенос в kk.korsac / Bitrix

| Prototype presentation | Будущий источник / адаптер |
| --- | --- |
| Native checked/selected + `data-summary-value` | ConfiguratorCore selection и реальные labels опций |
| `data-stage-case` и media | Renderer сопоставляет разрешённый case/SKU с утверждённым media |
| RAM/SSD labels и слоты | Представление подтверждённого selection, без локальных compatibility rules |
| `change` → manifest/stage | Подписка темы `kk.korsac.configurator-renderer` на selection events |
| Выбор и короткий resolve | Мгновенный UI feedback, отдельно от calculate lifecycle |
| Pending/calculated/error | Только реальные события и authoritative calculate response |
| Цена / Cart / SYSTEM ID | Проверенный server snapshot, basket integration и производственный паспорт |

Stage controller остаётся локальным presentation-слоем. При интеграции native
чтение заменяется адаптером к ConfiguratorCore; нельзя переносить prototype
текст или DOM flags в business-state либо использовать их как XML_ID/API
contract. Цена поступает из authoritative ответа; сервер проверяет selection,
доступность, совместимость и snapshot корзины. CSS, синхронизированные detail-панели,
context/Prev/Next controls и ограниченный pin конфигуратора могут перейти в template/theme
без замены всей interaction architecture.

## Проверка и human acceptance

[Актуальные review assets и запись v3.1](review/README.md) показывают
синхронизированный Explorer; материалы v3 сохранены как архив предыдущего head.
Автоматически проверяются: layout всех трёх страниц при
320/375/430/768/900/1024/1280/1440 px; все четыре пути ввода и disabled boundaries;
единый counter; стабильность высоты states/subannotations; отсутствие scroll/URL
изменений от выбора; native case/RAM/SSD/SSD2/manifest/passport и независимость
Explorer; статичность цен; rapid Next/Prev и motion cleanup; Tab/Enter/Space,
touch375/430×800; no-JS320; live reduced-motion; WCAG axe и отсутствие console
errors/external runtime requests. Результаты и ограничения фиксируются в PR.
Chromium проверен по HTTP; `file://` заблокирован политикой браузера среды.
Firefox/Safari и физические screen-reader/device прогоны не выполнены.

Перед принятием v3.1 человек проверяет в браузере:

- Охлаждение → Next → Графика: stage/detail/control/counter согласованы.
- GPU hotspot и Platform → Prev → Graphics: обратная синхронизация.
- CPU/memory subannotations без отдельных main slides.
- North → RAM64 → SSD2ТБ → второй SSD: подписи верны, цена статична,
  текущий Explorer context сохраняется.
- Mobile375/430: local feedback кнопок/hotspots/footer без специального
  возврата к сцене; keyboard, no-JS и reduced motion.

Вопросы A–G: модуль существенно короче? Сцена и пояснение ощущаются одной
системой? Все пути ввода согласованы? Опыт похож на изучение продукта?
Mobile даёт местный видимый feedback? Упрощение сохраняет интерактивность?
DOM controller проще связать с ConfiguratorCore/renderer?
Архитектурные и поведенческие проверки дают ответы для ревью, но не заменяют
человеческую оценку visual/motion feel.

## Границы

В v3.1 нет Bitrix/PHP, API, pricing, Cart, inventory, compatibility engine,
финальных фото, выдуманных benchmarks, WebGL/3D/canvas, parallax,
custom cursor, scroll interception и внешних animation libraries.
Каталог, checkout, account, поиск и финальная главная страница вне задачи.
