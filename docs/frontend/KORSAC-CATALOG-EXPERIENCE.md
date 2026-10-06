# KORSAC — Catalog & Product Family Experience v1

## Задача и источники

Каталог начинается с выбора игрового сценария и класса системы. Карточки
подтверждают выбор компонентами; покупателю не нужно самостоятельно собирать
позиционирование из длинного названия CPU/GPU. `prototype/catalog.html`
развивает Visual/Motion v2.1 и Product Experience v3.1, сохраняя спокойный
язык, технические rails и сценарные названия.

Источники содержания:

- [Brand Guide](../brand/KORSAC-BRAND-GUIDE.md).
- [Архитектура PLAY v0.2](../product/KORSAC-PLAY-ARCHITECTURE.md).
- [Архитектура MINI](../product/KORSAC-MINI-ARCHITECTURE.md).
- [PLAY 1440 baseline v0.1](../product/KORSAC-PLAY-1440-SPEC-v0.1.md).
- [Visual & Motion Direction](KORSAC-VISUAL-MOTION-DIRECTION.md).
- [Interactive Product Experience v3.1](KORSAC-INTERACTIVE-PRODUCT-EXPERIENCE.md).

Для PLAY 1440 указаны Ryzen 7 9700X, RTX 5070 12 ГБ GDDR7, 32 ГБ DDR5 и
1 ТБ NVMe TLC. Остальные CPU/GPU обозначены рабочими классами архитектуры;
X3D — ориентир высокого игрового класса, а не обещание конкретного SKU.
MINI требует проверенных физических исполнений GPU и собственной ревизии.
Единственная точная цена — **179 900 ₽**, с подписью **«Цена — пример»**.
Для остальных моделей стоимость уточняется при подборе конфигурации.

## Discovery и семейства

Первый блок объясняет принцип и показывает семейства PLAY / CREATE / WORK.
PLAY — текущая линейка. CREATE/WORK представлены настоящими disabled buttons
с текстом «В разработке»; ложных ссылок и продуктов этих семейств нет.
Будущая смена семейства сможет открыть собственный набор сценариев, используя
тот же visual shell и локальный экземпляр controller.

Navigator показывает четыре ступени: **1080 → 1440 → 1440 PRO → 4K**.
Нет числовой шкалы производительности, FPS или процентов. Под 1440 находится
компактная ветка **MINI** с подписью **«Тот же 1440p · Mini-ITX»**. Она
вложена в узел 1440; короткий соединитель идёт от его rail и на desktop,
и в мобильной сетке. Дополнительных текстовых блоков вокруг ветки нет.
При выборе MINI общий узел 1440 сохраняет сигнал связи, а выбранным control
становится MINI. Связь задаётся HTML `data-catalog-parent`, не положением
элемента в DOM и не порядком в JS-массиве.

| Модель         | Смысл выбора                                  | Графический класс                      | RAM / SSD по умолчанию |
| -------------- | --------------------------------------------- | -------------------------------------- | ---------------------- |
| PLAY 1080      | Full HD, высокий FPS в соревновательных играх | RTX 5060 Ti 16 ГБ class                | 32 ГБ / 1 ТБ           |
| PLAY 1440      | Основной баланс для 2560×1440                 | RTX 5070 12 ГБ                         | 32 ГБ / 1 ТБ           |
| PLAY 1440 MINI | Сценарий 1440p в компактном Mini-ITX          | RTX 5070 class, проверенные исполнения | 32 ГБ / 1 ТБ           |
| PLAY 1440 PRO  | 1440p high refresh, тяжёлая графика и RT      | RTX 5070 Ti 16 ГБ class                | 32 ГБ / 2 ТБ           |
| PLAY 4K        | Разрешение 3840×2160, верх основной линейки   | RTX 5080 16 ГБ class                   | 32 ГБ / 2 ТБ           |

Четыре основных control и отдельная MINI-button — нативные кнопки с
`aria-pressed`, `aria-controls` и visible focus. Выбор обновляет preview,
identifier, активную rail и отметку соответствующей карточки. Текст «Выбрано»,
наклонная отметка control и pressed-state дополняют цвет. После enhancement
название модели в карточке становится нативной selection-button; оно
и сценарная рекомендация вызывают тот же setter. Hover/focus не выбирают
модель автоматически. Нет autoplay, карусели, swipe-зависимости, фильтров,
сортировки и изменений URL/history. Выбор модели не управляет scroll/focus.

## Preview и карточки

Крупный preview по умолчанию показывает PLAY 1440: имя, назначение,
форм-фактор, четыре ключевых hardware-поля, область настройки, цену и CTA.
Модель меняется локально. Нейтральная схема MINI заметно компактнее;
цветовая система остаётся общей. Схема каталога проще Product Stage:
нет hotspots, airflow, внутренних сценариев или повторного hero reveal.
Подпись явно обозначает условную схему.

Все пять source cards постоянно доступны ниже как слой быстрого просмотра.
Каждая показывает индекс/модель, сценарий, маркер форм-фактора, GPU-класс,
базовые RAM/SSD и одну CTA **«Подробнее»**. Длинные purpose/setup copy, CPU,
схема, цена и дополнительная CTA остаются в полном source HTML для preview,
но скрыты в линейке. Повторного product-detail layout нет. PLAY 1440
выделяется rail, индексом и акцентом; ширина и структура всех карточек одинаковы.
Hover/focus кратко удлиняют rail; 3D tilt и narrative-анимации отсутствуют.

Для PLAY 1440 «Подробнее» ведёт на `product.html`, «Настроить» — на его
конфигуратор. Для остальных моделей ссылку enhancement превращает в локальное
информационное окно с названием модели. Без JS ссылка ведёт на явное пояснение
границы прототипа. Это не попытка открыть несуществующую карточку или API.

Рекомендации authored в HTML и объясняют другую задачу: например, PRO для
высокого refresh rate и тяжёлой графики, MINI ради компактности, 4K под другой
экран. Цены, пороги и выбранные апгрейды в рекомендациях не участвуют.

## Сравнение

Нативные checkbox на карточках позволяют выбрать **две или три модели**.
При одной модели действие «Сравнить» недоступно. При трёх невыбранные
checkbox disabled; понятная status-подпись объясняет, как заменить модель.
После снятия отметки controls снова доступны. Состояние не сохраняется
между загрузками и не смешивается с выбранным сценарием Navigator.

Небольшая нижняя панель появляется после первой отметки. Она показывает
счётчик и действие «Сравнить», поэтому не требуется возвращаться к дальнему
разделу страницы. Очистка сбрасывает отметки, закрывает панель и возвращает
фокус к последнему изменённому checkbox без прокрутки. Постоянный раздел
сравнения под линейкой содержит инструкцию, выбранные названия и то же действие.

Native dialog содержит семантическую HTML-таблицу с model column headers
и property row headers. Desktop сохраняет все семь свойств: сценарий,
графический класс, RAM default, SSD default, форм-фактор, область настройки
и назначение. Данные читаются из source cards в момент открытия.

На mobile ≤767 px сравнение идёт **по строкам свойств**: одна общая подпись,
затем 2–3 значения рядом в выровненных колонках. Видны пять коротких строк:
сценарий, GPU-класс, RAM, SSD и форм-фактор. Полные purpose/setup prose
скрыты; они доступны в desktop comparison и подробном preview. Заголовки
моделей закреплены над свойствами при прокрутке. Header с close-button
остаётся вне внутренней scroll-region, доступной с клавиатуры.
Горизонтальный scroll не требуется. Dialog имеет
именованный заголовок, close-button, Escape, focus containment, inert-фон и
возврат фокуса к открывшей кнопке через общий `prototype.js`.

Сравнение не вычисляет преимущества, цену, доступность, сроки, FPS,
температуру, шум или проценты. Это presentation над документированными
свойствами, а не коммерческий compare engine.

## HTML как источник данных

`prototype/assets/js/catalog-experience.js` — отдельный classic deferred script,
создающий controller для каждого `[data-catalog-experience]`. Product controller
не импортируется и не меняется. В UI Kit собственный scope демонстрирует
те же механизмы на 1440, PRO и MINI, независимо от Product Primitives.

| HTML                                                              | Назначение                                |
| ----------------------------------------------------------------- | ----------------------------------------- |
| `data-catalog-model`                                              | Локальный model key source card           |
| `data-catalog-title` / `data-catalog-property`                    | Название и фактический baseline           |
| `data-catalog-compact`                                            | Короткое значение для mobile comparison   |
| `data-catalog-content` / `data-catalog-actions`                   | Media, copy и CTA для derived preview     |
| `data-catalog-recommendation`                                     | Authored recommendation template          |
| `data-catalog-selection`                                          | Текущий presentation key конкретного root |
| `data-catalog-pick` / `data-catalog-rail` / `data-catalog-parent` | Выбор и связь MINI-ветки                  |
| `data-catalog-compare`                                            | Native checkbox отдельного сравнения      |

Map хранит ссылки на карточки, не копии hardware/spec/price в JS-массивах.
Source cards видны как компактная линейка; полные свойства остаются в их
HTML. Preview клонируется до enhancement заголовка карточки и сохраняет
подробности и обе CTA. Comparison переносит безопасный `textContent`
и authored `data-catalog-compact` по ключам строк из HTML template. В runtime нет второго
справочника SKU или четырёх независимых массивов контента. UI Kit содержит
намеренные HTML fixtures; production сможет рендерить оба варианта из одного
серверного шаблона. Model keys не являются XML_ID или будущим API contract.

Неактивные preview panels получают `hidden` и `inert`. Scoped CSS оставляет
их невидимые intrinsic размеры в общем grid slot, поэтому preview не меняет
высоту между моделями. Неактивные ссылки исключены из Tab и accessibility
tree. Fixed giant height и измерение высоты в JS не нужны.

## Motion и media

Выбор обновляет семантическое состояние сразу. Затем локальный WAAPI resolve
использует общие `--k-motion-brand` **320 ms** и `--k-ease-precision`:
декоративная старая схема исчезает за половину интервала, новая схема получает
8 px mask/resolve, designation и scenario — короткий 6 px сигнал. Цена и CTA
не скрываются. Повтор отменяет предыдущие animations и ghost; finite finished
promises очищают эффекты. Живое включение reduced motion также отменяет их.
Нет блокировки клика, задержанного business-state, observer, scroll interception,
таймера автопереключения и animation library. Hover/focus используют 140–220 ms.

Позже внутреннее содержимое `[data-catalog-media]` можно заменить локальным
`<picture>` с responsive фотографией. Card/preview layout, model key, свойства
и CTA сохраняются. Нужно согласовать crop/object-fit для обоих размеров;
placeholder не является фотографией, физической компоновкой или обещанием
габаритов корпуса. Review PNG/MP4 никогда не загружаются runtime.

## Mobile и progressive enhancement

На 320–430 px Navigator показывает две компактные строки и отдельную MINI-ветку
с явной подписью сценария 1440. Preview располагает небольшой силуэт рядом
с названием, затем explanation, baseline и CTA. Повторная техническая register
строка скрыта; выбранная модель читается в основном заголовке рядом с controls.
Карточки идут вертикально без повторных media и длинного назначения.
Проверенная высота карточек примерно **400–423 px** на 320/375/430 px;
высота получается из содержимого, без fixed height. Tablet сохраняет обычный
flow и две колонки карточек. На mobile comparison это короткая матрица,
а не вертикальная последовательность полных product blocks.

Без JS видны семейства, сценарные anchor-links, все пять карточек и раздел
объяснения 1440/PRO/MINI. Anchor ведёт прямо к соответствующей карточке;
PLAY 1440 сохраняет обычные ссылки. Navigator buttons, derived preview и
comparison controls скрыты до успешного enhancement. Страница не требует
JS для понимания линейки или чтения ключевых различий.

## Перенос в Bitrix

| Prototype                | Будущий источник / адаптер                          |
| ------------------------ | --------------------------------------------------- |
| Catalog source card      | Шаблон `bitrix:catalog.section`                     |
| Семейство и сценарий     | Sections / реальные product properties              |
| Локальный model key      | KORSAC product metadata и стабильный detail route   |
| CPU/GPU class и defaults | Catalog properties и утверждённая ревизия           |
| Область настройки        | Разрешённые properties/options с backend validation |
| CTA                      | Реальный product detail URL / конфигуратор          |
| Цена                     | Bitrix catalog price / authoritative KORSAC pricing |
| Наличие                  | Backend data, когда они появятся                    |
| Comparison               | Presentation реальных catalog properties            |

Renderer может оставить rails, карточки, media/preview и локальный setter,
заменив source HTML реальным SSR-контентом. URL можно связать с
`/catalog/play/` и `/catalog/play/1440/`; текущий JS не зависит от случайных
DOM positions. Цена, stock, compatibility и basket остаются backend-owned.
`kk.korsac`, Bitrix и production APIs в этом PR не изменены.

## Проверка и human acceptance

[Review assets](review/README.md) содержат шесть обновлённых catalog PNG,
включая mobile comparison 1440/MINI/PRO, и короткий MP4.
Automated HTTP Chromium-проверки покрывают четыре страницы при
320/375/430/768/1024/1280/1440 px, все selection routes, stable preview,
MAX3/удаление/очистку сравнения, keyboard/dialog focus, touch375/430,
no-JS320, rapid input и live reduced motion. Дополнительные проверки
320/375/430/768/1440 px подтверждают одну видимую CTA и три факта на каждой
равной по ширине карточке, связь MINI с 1440, aligned values сравнения
2/3 моделей и native table semantics. При высоте viewport 500 px проверены
keyboard PageDown и закрепление model header; close-control остаётся видимым. Цены статичны, runtime-запросы
только локальные. Axe и regression shared/product controls фиксируются в PR.

`file://` заблокирован политикой браузера среды; relative classic resources
сохраняют рассчитанную на него структуру. Firefox/Safari, физические устройства
и физический screen-reader не проверены. Снимки и automated tests не завершают
человеческую визуальную приёмку. Перед принятием человек проверяет:

1. За несколько секунд читается лестница 1080 → 1440 → PRO → 4K и отдельная MINI-ветка.
2. Выбор 1440 → PRO объясняет другой игровой класс, GPU и SSD default.
3. MINI объясняет компактное исполнение сценария 1440p.
4. Desktop сравнение 1440/PRO показывает назначение и baseline; на mobile
   значения 1440/MINI/PRO сравниваются рядом по пяти коротким свойствам.
5. На 375 px сценарий, выбранная модель и переход в карточку находятся быстро,
   без horizontal overflow; motion остаётся коротким и спокойным.

Вопросы self-review A–G: линейка читается без всех specs; PRO объяснён классом
и задачей; MINI — форм-фактор; identity держится на rails/media/designation;
discovery сокращает путь до одного сценарного выбора; семейства смогут иметь
собственные сценарии; SSR/Bitrix заменит данные без смены visual architecture.
Это ответы по реализации, а не результаты пользовательского исследования.

## Границы

Нет homepage, basket/checkout, search, sorting, inventory, reviews, ratings,
favorites, full compare engine, API/remote JSON, pricing thresholds, fake
benchmarks, финальных цен/фотографий и выдуманных CREATE/WORK продуктов.
