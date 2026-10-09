# Projects v1 — review

Base: merged PR #10, `main` at `b6436f1149c1dd0a5f40676753b34568458a1aa6`.
PR #11 media revision: architecture/provenance/PLAY relationship unchanged.
[Content / media contract](../KORSAC-PROJECTS-EXPERIENCE.md).
[Source media manifest](projects-media-sources.json).
[Authoritative IA](../KORSAC-INFORMATION-ARCHITECTURE.md).

## Реальные исходники

Все три approved King-Komp original pages теперь получены по HTTPS 200.
Контекст и 8 component values A сверены с source body. Прежнее CONNECT 403
ограничение первого commit устранено; no-media version не является финальным
review state. B/C сохраняют approved CPU/GPU subset, без расширения commercial data.

Фотографии получены из `big-gallery-top` каждой соответствующей публикации:
8 кадров A, 1 cover B,1 cover C. Все 10 JPEG визуально просмотрены, decoded;
локальные байты/SHA-256/native dimensions совпадают с downloaded originals.
Manifest фиксирует project/asset URLs, source position, display order, alt,
nullable source caption и dimensions. Три covers связаны именно со своими
fixtures; нет stock/AI/generic renders/component shots вместо готовой системы.
Снимки деталей A показывают компоненты внутри той же реальной сборки.

Photos хранятся локально, HTML не hotlink. Price/date/client identity/author/
benchmark/temperature/noise claims не добавлены. Дата получения media не
публикуется как дата проекта. King-Komp origin сохранён; это не KORSAC product.

## Обновлённые screenshots

Настоящие Chromium captures, reduced mode after all relevant images decoded:

- [Projects list — desktop](projects-v1-desktop.png), 1440×2890.
- [Projects list — mobile](projects-v1-mobile.png), 375×3878.
- [Project detail — desktop](project-v1-desktop.png), 1440×5822.
- [Project detail — mobile](project-v1-mobile.png), 375×6300.
- [Detail gallery — desktop](project-gallery-v1-desktop.png), 902×1806.
- [Detail gallery — mobile](project-gallery-v1-mobile.png), 343×2207.

Первые 4 PNG full page, gallery 2 — component captures. Только для component
capture floating header/skip link скрыты через screenshot style, чтобы они не
перекрывали снимки при длинном element capture; application CSS не меняется.
Все 6 PNG просмотрены. Covers — крупная часть открытого register, не metadata
thumbnails. На mobile фото компактны и читается identity каждой сборки.

Detail flow: identity → крупный finished-build cover → context → configuration
→ дополнительный общий ракурс и 6 installed-details photographs → origin/source
→ PLAY. Все 8 изображений A видны в base HTML, gallery — обычный ul/figure/img.
Captions не придуманы. Нет ecommerce carousel, hidden slides, lightbox/PrevNext/
swipe controller, autoplay или нового temporal interaction; open-state PNG и
MP4 не требуются.

## SEO / media audit

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/seo_audit.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/seo_audit.py --json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_seo_audit.py'
```

**17 pages, 0 errors, 43 intentional warnings; 17 tests PASS.**
[Deterministic JSON](seo-audit-v1.json) совпадает с повторным выводом.
List остаётся CollectionPage/BreadcrumbList; detail Article/BreadcrumbList.
Article.image — только реально видимый local cover `white-i5-02.jpg`.
Ни production image URL/canonical, ни Product/Offers/ratings, ни invented
Article authors/dates не добавлены. Все 17 pages noindex/nofollow/noarchive.
Warnings: 17× no canonical/og:url; 17× no approved social artwork; 9× relative schema URLs/IDs.

Media guards требуют image в каждом authored record; detail cover и gallery
в base HTML; local project-photo path; non-empty alt; positive width/height;
Article.image должен совпадать с видимым project image. Новые 3 negative tests
проверяют отсутствующий/чужой/remote media, отдельную record без cover,
missing alt/dimensions и invalid/unseen Article.image. Прежние 14 tests/guards
сохранены; valid fixtures дополнены media, assertions не выключены.
Audit проверяет присутствие/разметку, не самостоятельно подлинность фото:
для этого source mapping, SHA/byte verification и visual inspection выше.

## Browser QA

Chromium HTTP: **17 pages × 8 widths = 136 layouts**:
320/375/430/768/1024/1280/1440/1920. Zero document overflow, duplicate IDs,
console/request errors или external runtime requests. All project images
scroll into view и decode, alt/dimensions match native JPEGs; aspect ratio
не искажён, rendered width не превышает native width. Covers capped 600px,
large detail 1280px capped 1120px. Нет crop/mask/fixed-height clipping.
First prominent covers eager/high priority; below-fold previews/gallery lazy.

Verified exact per-fixture cover mapping, 3 list records, 8 configuration rows,
8 detail photos (cover+gallery 7), all visible без JS. Native no-JS scrolling
достаточна для lazy images. Все source/case routes остаются ordinary anchors.
Home trust→Projects→detail→Projects→PLAY→Product→PLAY→Computers работает;
Home→Computers unchanged. Breadcrumb names/order/href совпадают с JSON-LD,
local ancestors HTTP 200. Header 5 entries, internal sticky/opaque сохранены.

Keyboard skip/focus-visible, in-page configuration/source clearance,
mobile drawer Tab containment/Escape/opener return прошли.
**Axe WCAG2A/AA/2.1AA: 0 violations in 6 media states** (2 pages×320/375/1440).
Один H1 и case H2/H3 hierarchy сохранены. Некоторые axe checks incomplete;
physical-device/full screen-reader и Firefox/Safari review не выполнены.
Прямой file-protocol review не заявлен; HTTP/no-JS/local-resource QA прошли.

## Regression / motion boundary

В этой media revision business JS, shared motion/controller/logo assets,
Home/Computer Families/PLAY/Product/Cart/Checkout/Success/Contacts/error HTML
не изменены. Все 17 страниц участвуют в 136 layouts; native hierarchy/PLAY routes
проверены повторно. Existing static prices/backend boundaries остаются прежними.

Brand Intro: те же public eligibility/shared 24h key/1500ms/reduced cleanup;
media не управляет её timeline. Gallery content не анимируется и не скрывается
при reduced motion. Existing baseline intro/commerce/scoped catalog/product
regression evidence первого PR #11 commit сохраняется в принятой архитектуре;
новая media не добавляет controls или state coupling.

HTML nesting/labels/IDs/local resources/fragments/docs links, PNG decode,
source JPEG hashes/dimensions и `git diff --check` — PASS.
Google/Schema.org/Yandex validators/production indexing не заявлены.

Human visual review обязателен до merge: реальные preview identities,
понятный case-study flow, photography как evidence, ясное historical origin
и family relation. Do not auto-merge. Equipment, System Passport и Bitrix вне scope.
