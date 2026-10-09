# Projects v1 — review

Base: merged PR #10, `main` at `b6436f1149c1dd0a5f40676753b34568458a1aa6`.
[Source ledger / content model / static mapping / future Bitrix contract](../KORSAC-PROJECTS-EXPERIENCE.md).
[Authoritative production IA](../KORSAC-INFORMATION-ARCHITECTURE.md).

## Источники и честная граница

Три реальные approved King-Komp fixtures из ТЗ. A: локальный detail с 8
source-supported компонентами; B/C: только явно указанные CPU/GPU и название,
ссылки на реальные originals. Факты воспроизведены из утверждённых excerpts
в ТЗ; live HTML extraction/verification не выполнена: egress proxy отвечает
CONNECT403 на King-Komp. Оригиналы не заявлены как заново проверенные по HTTP.
Требуемые два домена сохранены в network draft; это не runtime connectivity.

Photos надёжно не получены: review показывает полноценный config-led вариант
без project media, без stock/AI/подставных photographs и empty gallery frames.
Поэтому дополнительного gallery PNG нет. Перед будущим расширением source
facts/media сверяются с доступным original; текущий ledger не дополнен
предположениями. Историческая цена, клиентская личность, dates/authors,
benchmarks/temperatures/FPS/noise и причины component choice не выдуманы.
King-Komp provenance видим; кейсы не названы продуктами KORSAC.

## Screenshots

Настоящие full-page Chromium PNG, reduced mode after settle, без intro overlay:

- [Projects list — desktop](projects-v1-desktop.png), 1440×2207.
- [Projects list — mobile](projects-v1-mobile.png), 375×3191.
- [Project detail — desktop](project-v1-desktop.png), 1440×3057.
- [Project detail — mobile](project-v1-mobile.png), 375×3805.

List — открытый register cases, не product card grid/news feed. Detail —
контекст, immutable historical configuration и origin/source; optional отсутствующие
rationale/media/results не оставляют пустых секций. PLAY relation по задаче,
не привязка старого hardware к текущей модели. Все четыре PNG просмотрены.

Новой timeline/галереи нет; существующий Brand Intro не изменён. MP4 не нужен.

## SEO audit

```sh
python3 tools/seo_audit.py
python3 tools/seo_audit.py --json
python3 -m unittest discover -s tools -p 'test_seo_audit.py'
```

**17 pages, 0 errors, 43 intentional warnings; 14 tests PASS.**
[Deterministic JSON](seo-audit-v1.json) совпадает с повторным выводом audit.
List: CollectionPage/BreadcrumbList; detail: Article/BreadcrumbList. Статья
использует только headline/description/local review URL и visible original
citation; нет fabricated date/author/image, Product/Offers/ratings.

Новые tests проверяют missing/wrong entity type, BreadcrumbList, дополнительный
Product, все четыре forbidden commercial/review types, implicit offers/review,
auto-discovery и старые staging/ID/H1/link/image/canonical/ancestor guards.
Предыдущие 11 tests не ослаблены. Все страницы noindex/nofollow/noarchive;
unique title/description, один H1, valid JSON, local resources и alt/dimensions.
Warnings:17× no prototype canonical/og:url;17× no approved og:image;9× relative
schema URLs/IDs. Production domain/social artwork не придуманы. Внешние
Google/Schema.org/Yandex validators и production indexing здесь не проверены.

## Chromium / navigation / accessibility

**17 pages × 8 widths = 136 layouts:**320/375/430/768/1024/1280/1440/1920.
Zero horizontal document overflow, duplicate IDs, console/request errors или
external runtime requests. Configuration dt/dd и breadcrumbs wrap; новый
content без fixed-height clipping. Projects имеет3 records, detail8 snapshot
rows, header5 entries sticky/opaque. Все local breadcrumb ancestors HTTP200;
visible names/order/href совпадают с JSON-LD, включая прежний PLAY hierarchy.

Проверены Home trust→Projects→real detail→Projects→PLAY→Product→PLAY→Computers;
Home primary→Computers unchanged; Projects route из10 public footers. Source
links — authored external anchors, не runtime fetch. Новые pages не создают
catalog/configurator state, price controls, filter URLs или бизнес-логику.

Keyboard: первый Tab показывает focus-visible skip; skip/in-page targets ниже
sticky header; mobile drawer Tab containment, Escape и opener focus return.
**Axe WCAG2A/AA/2.1AA: 0 violations in 6 Projects states** (2 pages×320/375/1440).
Дополнительная commerce/UI suite:0 violations in16 states, включая validation,
company, pickup dialog, empty cart и drawer. Некоторые checks incomplete;
полный screen-reader/physical-device audit и Firefox/Safari не выполнены.

No-JS320px: list/detail headings, все configuration rows, native mobile fallback
и Home→Projects→detail→PLAY работают; intro остаётся hidden. Прямой `file://`
browser review не повторялся: managed Chromium уже блокировал его в PR #10.
HTTP/no-JS и relative-resource checks не заявляют file-protocol validation.

## Motion / регрессии

Оба новых direct-entry pages: прежний1500ms Brand Intro, валидные local SVG
references и уникальные page prefixes. Все8 browsing routes разделяют rolling24h
key; навигация/reload не replay. Initial reduced: skip+timestamp. Live
normal→reduce отменяет overlay; возвращение no-preference не replay. Existing
Contacts/commerce/errors eligibility unchanged. Нового spatial content motion нет.
Baseline intro suite также прошла: daily/expired timestamp, multiple tabs,
storage failures, delayed CSS, eight widths, reduced/no-JS.

Existing browser suites прошли: Homepage scoped discovery/controller/native
inspection/dialog/drawer/reduced+normal hero/no-JS; PLAY source fidelity/scenario
ladder/MINI/compare bounds/rapid input/live reduced/UIKit scope/touch/no-JS;
Product Explorer/Next/Prev/configurator/stable stage/static displayed prices;
Cart quantity/remove/restore/empty/reset; guest/company Checkout validation,
independent payment presentation, pickup dialog/no-JS/static Success без PII.
Header suite:18 baseline layouts, small-scroll opaque Homepage, stable internal
surface, hash/reload/restoration/no CLS и top-layer dialog/drawer.
Computers/CREATE/WORK/Contacts/errors/UI/review входят в136 layouts.

Existing application JS/logo assets, Checkout/Success/error templates и
transaction payloads не менялись. Изменения существующих public pages —
footer route и одна Homepage trust link; её copy spacing сохранён CSS selector
correction. Family hierarchy, sample pricing и Bitrix boundary сохранены.
HTML nesting/labels/IDs/local resources/fragments/doc links, PNG decode и
`git diff --check` прошли. Старые captures — historical stage baselines.

Human visual review требуется до merge. Проверить: доверие к архивным cases,
видимость origin, удобство чтения configuration-led варианта без photos,
чёткую связь с PLAY без переименования historical hardware в KORSAC products.
Do not auto-merge. Equipment, System Passport и Bitrix вне scope.
