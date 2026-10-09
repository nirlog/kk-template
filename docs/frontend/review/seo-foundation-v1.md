# SEO / IA / Generic Pages v1 — review

Base: `main` at `0b48224f7698b44f66808d53adbe94631c78be48`.
Статический staging, без утверждённого production domain/контактов/Offer.

## Аудит

Из корня checkout:

```sh
python3 tools/seo_audit.py
python3 tools/seo_audit.py --json
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/monitor_curation_audit.py
```

Результат: **23 страницы, 0 ошибок, 58 intentional warnings**.
[Детерминированный JSON output](seo-audit-v1.json). 37 tests (20 SEO + 7 monitor curation + 10 System Passport)
прошли: staging guard, canonical, metadata/H1, IDs/links/images, invalid/unsafe
JSON-LD и implicit offers/review properties; дополнительно non-final breadcrumb
URLs, URL string / `item.@id`, invalid URL/list shapes и final-item omission.
Family pages дополнительно требуют CollectionPage/BreadcrumbList без Product;
новые filenames участвуют в staging/IDs/H1/link guards. Projects list/detail
требуют CollectionPage/Article + BreadcrumbList; Product/Offer/Review запрещены.
Добавлены Projects и Equipment schema/media negative fixture tests без ослабления старых guards. Все текущие img имеют
размеры/alt. Equipment hub/category запрещают Product; monitor detail требует
Product.image из реально видимого local media. Commercial guards прежние.

| HTML                    | Detected JSON-LD types (recursive)       |
| ----------------------- | ---------------------------------------- |
| `404.html`              | Нет                                      |
| `500.html`              | Нет                                      |
| `503.html`              | Нет                                      |
| `cart.html`             | Нет                                      |
| `catalog.html`          | BreadcrumbList, CollectionPage, ListItem |
| `checkout.html`         | Нет                                      |
| `computers.html`        | BreadcrumbList, CollectionPage, ListItem |
| `contacts.html`         | BreadcrumbList, ContactPage, ListItem    |
| `create.html`           | BreadcrumbList, CollectionPage, ListItem |
| `equipment.html`        | BreadcrumbList, CollectionPage, ListItem |
| `monitors.html`         | BreadcrumbList, CollectionPage, ListItem |
| `monitor.html`          | Brand, BreadcrumbList, ListItem, Product |
| `index.html`            | Organization, WebSite                    |
| `order-success.html`    | Нет                                      |
| `product.html`          | Brand, BreadcrumbList, ListItem, Product |
| `project.html`          | Article, BreadcrumbList, ListItem        |
| `projects.html`         | BreadcrumbList, CollectionPage, ListItem |
| `review.html`           | Нет                                      |
| `ui.html`               | Нет                                      |
| `passport.html`         | Нет                                      |
| `passport-pending.html` | Нет                                      |
| `system-workflow.html`  | Нет; internal review                     |
| `work.html`             | BreadcrumbList, CollectionPage, ListItem |

Production indexability: [единая полная матрица](../KORSAC-INFORMATION-ARCHITECTURE.md#единая-матрица-production-indexability)
с Page type / URL / index policy / canonical / breadcrumbs / schema / sitemap /
Bitrix owner. Content-only published entities indexable; Cart/Checkout/Success,
Search/Account, filters/sort/configurations/review/errors не создают indexable
сущности. В этом review **все** 23 страницы noindex/nofollow/noarchive.

Known intentional warnings:

- 23 × canonical/og:url не заданы в prototype. Production следует page-type
  policy: approved-host self-canonical только для подходящих content pages;
  ошибки/транзакции не ждут canonical.
- 23 × нет approved og:image; social artwork остаётся future production slot.
- 12 × local schema URLs/fragment IDs для semantic review. Bitrix преобразует
  реальные entities в absolute canonical URLs; hostname сейчас не выдуман.

Computer Families v1 добавил настоящий hub: «Компьютеры» теперь UI link и
JSON-LD `item: "computers.html"`. На Product PLAY сохраняет `catalog.html`;
только final item может опустить `item`. [Family review](computer-families-v1.md) фиксирует PR #10;
[current Projects review](projects-v1.md) показывает актуальные audit/QA. Исторические PR #9 captures и browser QA ниже
относятся к Generic Pages baseline до новых family routes.
Current Product без Offer/image/availability/ratings intentional, sample price
не является production данными. Проверка JSON syntax не обещает rich results.
Audit не заменяет Google/Schema.org/Yandex validators/Lighthouse/Search Console;
ни один внешний validator или production HTTP/crawl acceptance здесь не заявлен.

## Browser QA — PR #9 baseline

Chromium по HTTP: 12 страниц × 8 ширин = **96 layouts**
(320/375/430/768/1024/1280/1440/1920), zero horizontal overflow и console/request
errors. Catalog/Product/Contacts visible crumbs совпадают с JSON-LD order/names.
Contacts есть во всех public/transactional/UI footer; header density сохранена.
Contacts keyboard drawer: native focus trap/Escape/focus return, sticky opaque
header. Новые informational/error pages не читают/пишут intro timestamp.
Никаких form/PII/tel/mailto fake values.

No-JS: Contacts/errors/Catalog/Product доступны; native menu404/Contacts,
breadcrumbs/content/real navigation links видимы. 500/503 не загружают JS и
остаются readable с заблокированными CSS/logo; manual503 retry без timer.
На320px error code/message/primary action внутри первого800px viewport.
Normal/reduced/live preference на Contacts не запускают entry sequences.

Axe WCAG2A/AA + 2.1AA: **0 violations, 8 states** — Contacts/404/500/503 на
320/1440. Некоторые contrast/link checks incomplete, full screen-reader audit
не заявлен. Firefox/Safari/physical devices в этой среде не проверены.

Existing browser regressions прошли: Homepage discovery/native dialogs/drawer/
no-JS/motion; Brand Intro daily timestamps/expiry/storage failures/delayed CSS/
initial+live reduced/no-JS на восьми ширинах; Catalog scenario selection/compare/
scoped UIKit/rapid input/reduced; Product Explorer/configurator/stable stage/
static pricing; Cart/Checkout quantity/remove/restore/validation/guest+B2B/
independent payment selection/no-JS/privacy; sticky header18 layouts, hash/reload/
restoration/no CLS/dialog top-layer. После переноса mobile breadcrumb padding проверены ещё24 затронутых layouts;
Product CTA остаётся в первом800px viewport на320/375/430.
Application JS и approved SVG assets
не менялись. `git diff --check` — PASS.

## Review assets

- [Contacts desktop](contacts-v1-desktop.png), 1440×1681, full page.
- [Contacts mobile](contacts-v1-mobile.png), 375×2482, full page.
- [404 desktop](error-404-v1-desktop.png), 1440×900.
- [404 mobile](error-404-v1-mobile.png), 375×800.
- [500](error-500-v1.png), 1440×900.
- [503](error-503-v1.png), 1440×900.
- [Breadcrumb primitive](breadcrumbs-v1.png), 1440×620, actual Product viewport.

PNG сняты после завершения opacity settle; без intro overlay. Новых interactions
нет, MP4 не требуется. Старые motion/commerce captures — предыдущие baselines;
не пересняты для metadata/footer changes. Error PNG — visual prototypes:
http.server/file opening не задают actual404/500/503, это server integration gate.

[IA и self-review A–L](../KORSAC-INFORMATION-ARCHITECTURE.md),
[SEO source contract и examples](../KORSAC-SEO-FOUNDATION.md),
[Generic pages / HTTP](../KORSAC-GENERIC-PAGES.md).
Human visual review остаётся перед merge; автоматического merge нет.

## Follow-up после review d4d5c10 — историческая проверка PR #9

Breadcrumb URLs проверены новым audit rule и regression fixtures. Runtime body,
CSS/JS/brand assets и семь PNG не менялись, визуальные QA выше относятся к тому
же интерфейсу. Дополнительно проверены Catalog/Product/Contacts breadcrumbs по
HTTP, names/order и non-clickable Computers, отсутствие overflow320/375/430/1440,
а также server-ready разметка без JS. Полный motion suite повторно не запускался.

[Production error deployment contract](../KORSAC-GENERIC-PAGES.md#пути-production-fallback-не-зависят-от-глубины-запроса)
теперь явно требует независимых от request depth CSS/logo URLs, Home `/`,
Contacts `/contacts/` и503 retry исходного requested URL. Prototype paths
сохранены. Actual production HTTP/asset routing требует отдельной integration
проверки после реализации server adapter.

System Passport v1 adds active/pending service projections without structured
data and a review-only internal specimen. Privacy guards reject serial/internal
markers in raw HTML, forbidden schema and hidden active data in pending state.
SYSTEM ID shape, active snapshot/inquiry content, generic metadata and absence
of Brand Intro are checked. Domain fixture tests also reject old Product identity
and stale footer links, and keep workflow/fixture URLs out of public navigation.
[Current System Passport review](system-passport-v1.md). Backend privacy/access
control, random identifiers, transactions and production status routing are not
validated by a static HTML audit.
