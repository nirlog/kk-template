# Equipment / Simple Product v1 — review

Base: merged PR #11, `main` at `d68b98c`.
[Content / media / cart / Bitrix contract](../KORSAC-EQUIPMENT-EXPERIENCE.md) ·
[Product source ledger](equipment-product-sources.json) ·
[Media manifest](equipment-media-sources.json).

## Review result

Equipment → Monitors → MSI MAG 274QF X24 → ordinary cart line is a native,
no-JS-compatible path. The hub curates a context, the category compares three
real fixtures, and the detail uses ordinary product identity/media/specifications
instead of a PC stage. PLAY configurations remain separate system lines.

Three King-Komp product publications and all three manufacturer specification
pages were retrieved over HTTPS 200. Displayed facts were checked against those
pages; source URLs/HTML hashes are in the ledger. Six corresponding original
WebP assets were retrieved locally, decoded and visually inspected; byte
counts/SHA-256/native dimensions match. There are no substitute/AI images or
runtime hotlinks. Source retail prices are snapshots, visibly marked examples;
stock/order promises, warranty/payment/delivery restrictions are not copied.

No Product Explorer, SYSTEM ID, configurator, System Passport or assembly flow
is introduced into monitor content. No new interaction/motion system, viewer,
Fancybox, hidden media panels or MP4 is added. Site-wide Media Viewer evaluation
is deferred; all images remain readable through native scrolling without JS.

## Browser captures

Actual Chromium screenshots, reduced mode after visible images decoded:

| View               | Desktop                                      | Mobile                                     |
| ------------------ | -------------------------------------------- | ------------------------------------------ |
| Equipment hub      | [1440 × 2365](equipment-v1-desktop.png)      | [375 × 3311](equipment-v1-mobile.png)      |
| Monitors category  | [1440 × 2695](monitors-v1-desktop.png)       | [375 × 5119](monitors-v1-mobile.png)       |
| MSI monitor detail | [1440 × 4199](monitor-v1-desktop.png)        | [375 × 6608](monitor-v1-mobile.png)        |
| Mixed cart         | [1440 × 2210](equipment-cart-v1-desktop.png) | [375 × 3936](equipment-cart-v1-mobile.png) |

[Monitor gallery component — 1344 × 402](monitor-gallery-v1-desktop.png).
Eight full-page captures and one component capture were visually inspected.
Only component screenshot capture hides the floating header/skip link through
Playwright screenshot style; application shell/CSS behavior is unchanged.
List media areas align on desktop and use natural height on mobile. Images fit
inside their areas without cropping, stretching, overlap or upscaling.

## SEO and source checks

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_seo_audit.py'
PYTHONDONTWRITEBYTECODE=1 python3 tools/seo_audit.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/seo_audit.py --json
```

**20 tests PASS; 20 pages, 0 errors, 52 intentional warnings.**
[Deterministic report](seo-audit-v1.json) matches repeated JSON output.
Warnings: 20 omitted prototype canonical/og:url, 20 pending approved social
artwork, 12 relative schema URL/ID review warnings. No production host is added.

Equipment/category require CollectionPage + BreadcrumbList and reject Product.
Monitor detail requires Product + BreadcrumbList, with the actual visible local
primary image. Commercial guards reject Offer/AggregateOffer/Review/
AggregateRating, including implicit offers/review/rating properties. Media
guards require a local asset, informative alt and explicit positive dimensions;
each category record needs media. The three new negative fixture tests cover
wrong/missing types, commercial properties, absent/per-record/remote/wrong-path
media, missing alt/dimensions and invalid/unseen Product.image. Previous 17
Family/Projects/PC tests and assertions remain intact.

All pages are noindex/nofollow/noarchive, one H1, unique title/description and
valid JSON-LD. Visible breadcrumb names/order/hrefs match schema; ancestor
links resolve over HTTP. HTML nesting/IDs/labels/local resources/fragments/docs
links, original image hashes/dimensions and nine PNG decodes pass. Audit checks
markup/presence; source ledger and inspection establish media provenance.

## Responsive, keyboard and no-JS

Chromium: **20 pages × 8 widths = 160 layouts** at
320/375/430/768/1024/1280/1440/1920. No horizontal document overflow,
duplicate IDs, console/page/request errors or external runtime requests.
Monitor photos decode at every width; markup dimensions match native WebP,
rendered aspect ratio is preserved and width does not exceed native width.
Photos remain inside card media areas. All long model names, breadcrumbs,
semantic dl specifications and mixed-line cart layouts wrap safely.

**Axe WCAG 2 A/AA/2.1 AA: 0 violations in 12 states**:
Equipment/Monitors/Monitor/Cart × 320/375/1440. Some checks are incomplete;
this does not replace human screen-reader/visual acceptance.

Keyboard checks pass: first-tab skip link, focus-visible, anchor clearance,
mobile drawer Tab containment, Escape and opener focus return; ordinary cart
quantity Enter activation, minimum-one disabled state/focus recovery,
remove → undo focus and restore → line focus. Native source/product links
retain meaningful names. No JS-only navigation is introduced.

No-JS at 320px passes Equipment → Monitors → detail → cart#cart-monitor →
checkout. All three records and four MSI views remain visible; lazy images
load through ordinary scrolling. Mixed cart has three authored readable lines;
unavailable JS quantity/removal controls stay hidden. Shared native navigation
fallback and existing checkout fallback remain usable.

## Commerce and motion regressions

Mixed cart checks pass: two `system` lines retain CONFIG snapshots/disclosure/
edit links; one `product` line has no CONFIG/System ID/configuration wording.
Generic product/position counts, integer demo totals, PC and monitor quantity
changes, min-one, remove/restore, empty state and reload reset all pass.
Removing the monitor returns the existing two-PC example total. UI Kit PC
specimen remains scoped and uses authored identity in feedback, without
`undefined` labels. No storage, pricing engine, supplier rules or basket request
is added.

Checkout validation/error focus/links, guest/company properties, delivery
selection/dialog, buyer changes without losing payment choice and valid
individual/company → static Success pass. All three payment methods remain
available in both authored buyer states. No form payload/network mutation is
sent. Checkout/Success remain their separate two-system fixture; cart makes
that boundary clear before navigation.

Homepage discovery/native controls/touch/no-JS, PLAY scenario ladder/MINI/
selection/compare/dialog/touch/no-JS and Product Explorer/configurator/scoped
UI/rapid input/responsive/no-JS regression helpers pass. Their harnesses use
port 8004 and current mixed-cart/Reduced Motion contracts: short opacity/color
feedback is allowed, spatial transform/clip is checked separately, then effects
must settle. Repository tests/controllers were not weakened or changed to make
old zero-motion fixture assumptions pass. Projects list/detail/gallery,
Contacts, Errors and review/UI pages also participate in all 160 layouts;
their existing content/controller/media assets are preserved except shared
footer discovery links and the UI Kit line identity fields.

Each new public page participates intentionally in the existing 24h Brand Intro
policy: direct normal entry, approved timing/local SVG references and shared
suppression across eleven browsing routes pass. Initial reduce skips intro and
records timestamp; live normal → reduce removes the overlay and settles;
returning to no-preference does not replay. Transactional eligibility and the
existing shared intro controller are unchanged.

Reduced cart acknowledgement is 180ms opacity-only, with live cancellation;
new static routes/gallery remain immediately available. Existing header is
sticky/opaque on internal pages with five global entries. Home/content paths,
PLAY product ↔ monitor ↔ PLAY 1440, 13 shared public footer routes and scoped
UI controls pass. No new temporal interaction requires video acceptance.

## Human acceptance boundary

Review the ordinary-product distinction, scenario-led curation, true model
photography, card scanning, mobile CTA/readability and PRODUCT versus SYSTEM
cart line clarity. Confirm prices/status cannot be mistaken for live commerce.
Human visual review is required before merge; do not auto-merge.

Physical-device/full screen-reader, Firefox/Safari, direct file-protocol review,
external Google/Schema.org/Yandex validators and production indexing/Bitrix
integration were not run. Static completion is not publication/assortment
approval. Shared Media Viewer, System Passport, feeds/import, account/search,
production stock/pricing/backend basket and deployment remain outside this PR.
