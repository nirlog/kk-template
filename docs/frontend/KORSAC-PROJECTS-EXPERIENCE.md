# KORSAC — Projects Experience v1

Base: merged PR #10, `main` at `b6436f1149c1dd0a5f40676753b34568458a1aa6`.
Authoritative URL/SEO policy remains the [IA matrix](KORSAC-INFORMATION-ARCHITECTURE.md#единая-матрица-production-indexability).
Projects — completed-build cases, не Blog/Journal, не supplier catalog и не
ещё одна линейка компьютеров. Equipment, System Passport и Bitrix migration
не реализованы в этом stage.

## Назначение и путь

List отвечает «что команда уже собрала?». Три открытые записи имеют индекс,
название, provenance, известные компоненты и обычную ссылку на case. Это
configuration-led archive, без дат сортировки, цен, filters или product controls.
На первом проекте доступен локальный detail; второй/третий ведут на свои реальные
King-Komp originals. Один static detail не выдаётся за три разные case pages.
Нет infinite scroll или декоративной pagination для несуществующих страниц.
Будущая pagination следует PR #9: реальные crawlable pages, self-canonical,
не canonical всех страниц на первую; filters не порождают indexable query URLs.

Detail — narrative/evidence page: контекст → конфигурация → происхождение →
связь с PLAY. Длинная product stage, configurator, SYSTEM ID и measurement
panels не копируются. Shared graphite/copper/blue, rails, interrupted corners
и typography связывают страницу с KORSAC, но чтение идёт по case, а не по
модели/опциям/разрешению.

## Источники и предел проверки

Ровно три approved fixtures из ТЗ владельца, без импорта всего архива:

| Fixture                     | Оригинал King-Komp                                                                                                                                                  | Отображаемые факты                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| A — белый игровой компьютер | [i5-14600KF / RTX 4070 SUPER](https://www.king-komp.com/projects/sobrannye-kompyutery/belyy-igrovoy-kompyuter-i5-14600kf-rtx-4070-super/)                           | Игровой компьютер для клиента, белое исполнение; 8 компонентов ниже |
| B — белая сборка на Ryzen 9 | [9950X / RTX 4090 MSI SUPRIM](https://www.king-komp.com/projects/sobrannye-kompyutery/topovyy-belyy-kompyuter-amd-ryzen-9-9950x-rtx-4090-msi-suprim/)               | Белое исполнение; AMD Ryzen 9 9950X; RTX 4090 MSI SUPRIM            |
| C — сборка на Ryzen 5       | [7500F / RTX 4070 SUPER Palit Dual](https://www.king-komp.com/projects/sobrannye-kompyutery/amd-ryzen-5-7500f-rtx-4070-super-palit-dual-32gb-ddr5-6200mhz-patriot/) | AMD Ryzen 5 7500F; RTX 4070 SUPER Palit Dual                        |

Fixture A snapshot, дословные component values из source-supported списка в ТЗ:

| Role        | Value                         |
| ----------- | ----------------------------- |
| CPU         | Intel Core i5-14600KF         |
| GPU         | RTX 4070 SUPER iGame          |
| Motherboard | MSI Z790-A MAX Wi-Fi          |
| RAM         | DDR5 KingBank 32GB 6000MHz    |
| SSD         | Kingston KC3000 1TB           |
| Case        | Cougar Airface Pro White      |
| CPU cooling | ARCTIC Liquid Freezer III 360 |
| PSU         | Deepcool PN750M 750W White    |

**Источник данных текущего review — утверждённые excerpts в ТЗ и указанные там
original URLs. Прямая проверка HTML источников не выполнена:** egress proxy
среды возвращает CONNECT 403 для `www.king-komp.com` и `king-komp.com`.
Домены добавлены в draft network allowlist с сохранением прежних разрешений;
сохранённый draft сам по себе не подтверждает runtime access.
Фотографии надёжно не получены, поэтому используются предусмотренные ТЗ
страницы без media, без stock/AI/подставных PC images и без пустых frames.
Ни photos, ни gallery screenshot, ни Article.image не заявлены как доступные.

У B/C не выводятся дополнительные RAM/SSD/board/PSU/cooling/context из
предположений или слов в legacy slug. Source extraction/full configuration
потребует доступного оригинала. Не переносится историческая цена A. Не
добавлены клиенты, даты, author names, software/benchmark/thermal/noise claims,
причины выбора компонентов, testimonials или выдуманный результат теста.
Сверка approved excerpts при доступе к источнику не должна расширять факты
без отдельной фиксации provenance.

## Content model: sparse и rich cases

Обязательные данные: утверждённые title, origin, context/configuration evidence,
source reference для archive, publication state и stable identity. List может
показывать короткое subset известной конфигурации, detail — полный snapshot,
а не live catalog components. Historical hardware не обновляется, чтобы
совпасть с сегодняшней моделью.

Шаблон поддерживает optional sections в порядке IA:

1. Задача/контекст.
2. Выбранный подход.
3. Configuration snapshot.
4. Объяснение выбора компонентов.
5. Сборка / media.
6. Измеренные результаты с реально известными conditions/units.
7. Outcome/provenance.
8. Related families/models и CTA.

Если source не подтверждает section, она отсутствует и не оставляет layout hole.
У текущего A нет выдуманных rationale, measurement/outcome dashboards. HTML
comments обозначают вставку approved approach/rationale и media/results.
Rich project в будущем добавляет semantic sections, не переключает страницу
в Product и не требует новой архитектуры. Назначение клиента и имя клиента
разные поля: наличие «для клиента» не разрешает публикацию личности.

## Provenance и связь с KORSAC

Historical origin = `king-komp-team`: видимое «Проект команды King-Komp» /
«Из архива команды King-Komp», original source link. KORSAC использует опыт
той же команды, не объявляет историческую сборку своей проданной моделью.
King-Komp — небольшая provenance строка, не второй logo/header brand.

Future native origin = `korsac`: label «Проект KORSAC» только для действительного
KORSAC project. Те же list/detail templates; origin не выводится из даты или
family relation. Не придумывать historical publication date ради такого решения.

Три approved gaming fixtures связаны только с `catalog.html` / PLAY по типу
задачи. Ни одна не заявлена как PLAY 1440 или конфигурация сегодняшнего товара.
Detail возвращается в Projects, PLAY и Computers. Будущий related model ID
добавляется при доказанной связи, не по похожему GPU и не из frontend inference.

## Static → production mapping

| Static review   | Production concept           | Breadcrumb                                  |
| --------------- | ---------------------------- | ------------------------------------------- |
| `projects.html` | `/projects/`                 | Главная → Проекты                           |
| `project.html`  | `/projects/{approved-slug}/` | Главная → Проекты → Белый игровой компьютер |

Для A возможен `/projects/belyy-igrovoy-kompyuter-i5-14600kf-rtx-4070-super/`,
но это **кандидат, не утверждённый production slug**. `project.html` — review
fixture. Legacy slug может быть сохранён либо переопределён осознанно при
migration; он не устанавливает автоматически KORSAC canonical/redirect policy.
Существующий Computer Families mapping и readiness gates не меняются.

Projects доступны одной content-ссылкой в Homepage trust block и в shared
public «Компания» footer, включая UI Kit specimen. Пять header entries
сохранены; Home → Computers unchanged. Review hub содержит обе новые страницы,
этот документ и review evidence. Нет fake links на другие local detail pages.

## SEO / semantics

List: CollectionPage + BreadcrumbList. Detail: Article + BreadcrumbList,
`og:type=article`. Article имеет только headline, description, review URL и
citation на видимый original source. Нет author/datePublished/dateModified/image
пока этих подтверждённых видимых данных нет. Отсутствие optional Article data
не маскируется invented validator fillers. Ни Product, ни Offer/AggregateOffer,
ни Review/AggregateRating не допускаются на Projects.

У 17 static pages сохраняется noindex/nofollow/noarchive. Metadata уникальны,
один H1, visible breadcrumb names/order/URLs соответствуют JSON-LD. Все
non-final ancestors имеют `item`; final item может быть без URL. Production
host, canonical, og:url/social artwork не придуманы. Future production schema
использует реальные canonical URLs только после publication readiness.

Audit автоматически читает оба файла; требует правильный entity type и
BreadcrumbList, запрещает Product на case/list, сохраняет все прежние guards.
Новые negative fixtures проверяют wrong/missing schema, extra Product,
Offer/Review types и действующие staging/IDs/H1/link/image/breadcrumb/canonical
rules. [Deterministic report](review/seo-audit-v1.json), [QA](review/projects-v1.md).

## Media, motion, accessibility

Текущая версия не содержит project photos/gallery. При добавлении реально
полученных утверждённых снимков: описывать только видимое в alt, фиксировать
width/height, сохранять source aspect ratio; LCP image не lazy, ниже fold — lazy.
Authored captions требуют своего source evidence. Gallery базово доступна
без JS; optional lightbox — native/keyboard/focus-return/reduced compatible,
без стороннего framework/autoplay. Будущее наличие media не обязывает
Article.image, пока оно не является подтверждённым видимым content.

Content/routes полностью server-like HTML. Нет нового JS controller или
motion system, autoplay, parallax, scroll reveal, typing или spatial media
transition. New public browsing Projects/list/detail используют прежний
Brand Intro: shared 24h key, 1500ms sequence, отдельные SVG ID prefixes.
Initial reduced пропускает intro и записывает timestamp; live reduce отменяет,
возвращение no-preference не replay. Existing transaction/error/Contacts
eligibility unchanged. Поэтому новый MP4 не требуется.

Открытые строки register на desktop превращаются в последовательные title /
component groups на mobile. Configuration — semantic dl, на320px dt/dd идут
друг под другом; нет широкой таблицы/overflow scroller. Breadcrumbs и long
component strings wrap, content без fixed heights. Skip link, landmarks,
heading order, native links/focus-visible и shared drawer/no-JS menu сохранены.
Проверки и реальные PNG находятся в [review](review/projects-v1.md).

## Будущий Bitrix contract — документ, не implementation

Project — отдельная content entity с примерно такими capabilities:
identity/title/slug/status; origin/provenance/source evidence; short context;
ordered optional body sections; immutable configuration snapshot; approved
media/captions/alt/dimensions; measured results с условиями при наличии;
related family IDs и отдельно related model IDs; real publication/modified date
и author при наличии; SEO fields/publication policy.

Не превращать optional narrative/results в giant flat property set. Структура
storage/infoblock будет выбрана во время Bitrix migration. Server entity/page
resolver обеспечивает один источник breadcrumbs/schema/metadata; frontend
рендерит только опубликованные sections/relations, не угадывает authors,
measurements или model mapping. Archive origin и native KORSAC origin —
содержимое, не два несовместимых шаблона. No price/Sale/basket/backend logic.

Human visual review обязателен; автоматического merge нет. Equipment и System Passport остаются вне этого PR; System Passport — отдельный более поздний stage.
