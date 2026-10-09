# KORSAC — Projects Experience v1

Base: merged PR #10, `main` at `b6436f1149c1dd0a5f40676753b34568458a1aa6`.
Authoritative URL/SEO policy remains the [IA matrix](KORSAC-INFORMATION-ARCHITECTURE.md#единая-матрица-production-indexability).
Projects — completed-build cases, не Blog/Journal, не supplier catalog и не
ещё одна линейка компьютеров. Equipment, System Passport и Bitrix migration
не реализованы в этом stage.

## Назначение и путь

List отвечает «что команда уже собрала?». Три открытые записи имеют индекс,
название, реальную фотографию готовой сборки, provenance, известные компоненты
и обычную ссылку на case. Это photographic case archive, без дат сортировки, цен, filters или product controls.
На первом проекте доступен локальный detail; второй/третий ведут на свои реальные
King-Komp originals. Один static detail не выдаётся за три разные case pages.
Нет infinite scroll или декоративной pagination для несуществующих страниц.
Будущая pagination следует PR #9: реальные crawlable pages, self-canonical,
не canonical всех страниц на первую; filters не порождают indexable query URLs.

Detail — narrative/evidence page: project identity → крупный реальный снимок →
контекст → конфигурация → галерея сборки/деталей → происхождение → связь с PLAY. Длинная product stage, configurator, SYSTEM ID и measurement
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

Все три original HTML получены по HTTPS 200 в media revision 9 октября 2026.
Контекст и восемь component values A сверены с source body. B/C сохраняют
прежний ограниченный subset фактов; доступ к источнику не расширяет scope
этого PR и не разрешает перенос исторических цен/дат/новых claims.

Фотографии извлечены только из соответствующего `data-fancybox="big-gallery-top"`
в каждой из трёх публикаций, не из меню, related projects или component catalog.
Скачаны 10 уникальных JPEG: 8 фотографий A и по 1 cover B/C. Все визуально проверены.
[Media source manifest](review/projects-media-sources.json) фиксирует original
project URL, exact asset URL, gallery position, локальный файл, dimensions,
byte count, SHA-256 и authored alt. Байты оригиналов сохранены без обработки;
нет cropping, генерации или переноса фотографий между разными проектами.

Прежний CONNECT 403 — устранённое ограничение первого commit, а не intended
final review state. Текущий review обязательно содержит source photography.
No-media fallback не является достаточным для принятия Projects v1.

Не переносится историческая цена A. Не добавлены клиентская личность,
authors/project dates, benchmark/thermal/noise claims, rationale, testimonials
или выдуманный результат теста. Дата получения media в manifest не становится
Article.datePublished/dateModified.

## Content model: sparse и rich cases

Обязательные данные: утверждённые title, origin, context/configuration evidence,
source reference для archive, publication state, stable identity и media.
Cover image — обязательный first-class field для опубликованного review case;
Gallery — ordered images для detail. Historical и native KORSAC projects
используют одну media модель, без другого шаблона по происхождению. List может
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
comments обозначают вставку approved approach/rationale и measured results.
Photography не является отсутствующим optional section текущего review.
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
citation на видимый original source. `Article.image` — только реально видимый
cover `assets/images/projects/white-i5-02.jpg`, локальный review path.
Нет author/datePublished/dateModified, пока этих подтверждённых видимых данных нет. Отсутствие optional Article data
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
rules. Media guards проверяют photograph в каждом authored list record,
detail cover/gallery в base HTML, local asset path, non-empty alt и positive
width/height; Article.image должен ссылаться на видимый project image.
Audit не доказывает photographic authenticity — это source manifest / byte
verification / visual review. [Deterministic report](review/seo-audit-v1.json), [QA](review/projects-v1.md).

## Media, motion, accessibility

Photography — содержимое и evidence проекта. Cover/gallery хранятся локально
в `prototype/assets/images/projects/`; hotlink из HTML не используется.
Все original aspect ratios сохранены через explicit width/height + responsive
`width:100%; height:auto`, без `object-fit:cover`, crop или масок. List covers
600px не увеличиваются выше 600px; prominent detail 1280px ограничен 1120px.
Макроснимки галереи отображаются меньше native 1280px. Width caps не создают
fixed-height clipping. First prominent images eager/high priority; below-fold
records/gallery — native lazy. Alt описывает видимое, captions не выдуманы;
повторяющийся project title в source link не объявляется отдельной caption.

Detail cover перед контекстом; после configuration идут все 7 дополнительных
кадров (общий ракурс и детали той же собранной системы). В base HTML видны
все 8 снимков A, без hidden panels, JS-only slides или ecommerce controls.
Desktop gallery — широкая общая фотография и пары деталей; mobile — один
последовательный столбец. Lightbox/swipe/enlarged-view controller не добавлены;
обычная прокрутка достаточна и без JS. Поэтому нет open-state PNG/MP4.
При будущем enhancement: native keyboard/focus, Escape/opener return,
accessible Prev/Next, reduced safe, без autoplay и third-party framework.

Media entity contract для обоих origins:

| Field                              | Meaning                                                            |
| ---------------------------------- | ------------------------------------------------------------------ |
| `cover_image`                      | Утверждённый снимок готового проекта для list/detail cover         |
| `gallery_images`                   | Ordered asset references, включая разные виды/детали той же сборки |
| `alt`                              | Обязательное authored описание видимого в каждом informative image |
| `source_caption`                   | Optional подтверждённая caption; null не создаёт пустой caption    |
| `sort_order`                       | Явный порядок в story/gallery, отдельно от source gallery position |
| `width`, `height`, aspect metadata | Native dimensions + ratio, responsive reservation/caps             |
| provenance/source reference        | Связь фотографии с конкретным проектом/origin, без inference       |

Content/routes полностью server-like HTML. Нет нового JS controller или
motion system, autoplay, parallax, scroll reveal, typing или spatial media
transition. New public browsing Projects/list/detail используют прежний
Brand Intro: shared 24h key, 1500ms sequence, отдельные SVG ID prefixes.
Initial reduced пропускает intro и записывает timestamp; live reduce отменяет,
возвращение no-preference не replay. Existing transaction/error/Contacts
eligibility unchanged. Поэтому новый MP4 не требуется.

Открытые строки register на desktop превращаются в последовательные photo / title /
component groups на mobile. Configuration — semantic dl, на 320px dt/dd идут
друг под другом; нет широкой таблицы/overflow scroller. Breadcrumbs и long
component strings wrap, content без fixed heights. Skip link, landmarks,
heading order, native links/focus-visible и shared drawer/no-JS menu сохранены.
Проверки и реальные PNG находятся в [review](review/projects-v1.md).

## Будущий Bitrix contract — документ, не implementation

Project — отдельная content entity с примерно такими capabilities:
identity/title/slug/status; origin/provenance/source evidence; short context;
ordered optional body sections; immutable configuration snapshot; approved
cover image + ordered gallery images/alt/optional source caption/sort/native dimensions/aspect; measured results с условиями при наличии;
related family IDs и отдельно related model IDs; real publication/modified date
и author при наличии; SEO fields/publication policy.

Не превращать optional narrative/results в giant flat property set. Структура
storage/infoblock будет выбрана во время Bitrix migration. Server entity/page
resolver обеспечивает один источник breadcrumbs/schema/metadata; frontend
рендерит только опубликованные sections/relations, не угадывает authors,
measurements или model mapping. Archive origin и native KORSAC origin —
содержимое, не два несовместимых шаблона. No price/Sale/basket/backend logic.

Human visual review обязателен; автоматического merge нет. Equipment и System Passport остаются вне этого PR; System Passport — отдельный более поздний stage.
