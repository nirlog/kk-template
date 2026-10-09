# KORSAC — Equipment / Simple Product Experience v1

Base: merged Projects PR #11, `main` at `d68b98c`. This stage implements
Equipment with Monitors as its only category. System Passport and Bitrix
migration are later work. Static completion is not production publication or
assortment approval.

## Role and selection

Equipment answers “what complements a KORSAC system?”. It is a curated layer,
not a mirror of King-Komp inventory. The hub introduces the screen as part of
the usage context and leads to a small, understandable selection. No keyboard,
mouse/accessory catalogs or disabled future-category cards are added.

The monitor category begins with native scenario links, not brands or facets.
It contains **10 unique real products**, presented as **4 PLAY, 4 CREATE and
5 WORK recommendations**. Each family offers alternatives rather than one
prescribed monitor:

- PLAY: compact or larger Full HD, flat high-refresh QHD or larger curved QHD.
  Resolution, diagonal, shape and refresh are independent decision factors;
  no FPS or computer compatibility is promised.
- CREATE: QHD with USB-C, 4K with USB-C, wider 21:9 workspace or QHD with
  HDMI/DisplayPort. These are workspace choices, not color-critical suitability,
  certification or application compatibility claims.
- WORK: QHD/USB-C, wide multitasking, QHD/HDMI/DP, video calls or a smaller
  height/pivot-adjustable Full HD screen. USB-C power limits remain explicit.

PLAY → CREATE → WORK sections are exposed in base HTML. Native links scroll
to the existing `#selected-play`, `#selected-create`, `#selected-work` section
anchors without hiding products. Each section links to its computer family;
return links lead to the task guide. No family/filter page, query facet,
controller or indexable URL is introduced. Unapproved filters/sort remain
noindex in production per the authoritative IA.

LG 27U631A-B, LG UltraWide 34WR50QK-B and MSI PRO MP275Q appear in CREATE
and WORK for separately stated editorial reasons. This is a many-to-many
relationship, **not separate product entities**: each has one `product_id`,
one ledger record, one cover file and one consistent destination URL across
all appearances. `data-monitor-product` is an authored review identity, not
an invented manufacturer SKU or approved production slug. Heading IDs are
unique per placement for accessibility; they do not define product URLs.

## Static → production mapping

| Static review              | Production contract                    | Schema                          |
| -------------------------- | -------------------------------------- | ------------------------------- |
| `prototype/equipment.html` | `/equipment/`                          | CollectionPage + BreadcrumbList |
| `prototype/monitors.html`  | `/equipment/monitors/`                 | CollectionPage + BreadcrumbList |
| `prototype/monitor.html`   | `/equipment/monitors/{approved-slug}/` | Product + BreadcrumbList        |

`monitor.html` demonstrates MSI MAG 274QF X24. It does not set a production
slug. The other nine products link to their own actual King-Komp publications;
there are no invented local detail pages. Related cards on the detail lead
back to family sections containing those recommendations.

Visible crumbs and JSON-LD share Home → Equipment → Monitors → product name.
Each non-final item has a real local ancestor URL. Production uses the approved
host and server hierarchy, independently of static filenames.

## Verified review assortment

[Product source ledger](review/equipment-product-sources.json) records catalog
and manufacturer URLs, retrieved date, HTML hashes and every displayed fact.
The ledger has one record per unique product, including stable identity,
per-family editorial reasons, consistent review URL and displayed card values.
All 20 catalog/manufacturer source pages were retrieved with HTTPS 200 and
reviewed on 9 October 2026 (six retained from the initial pass, fourteen newly
retrieved for the expansion). MSI/LG manufacturer specifications confirm the
model-specific facts; model names or supplier descriptions do not substitute
for verification. Regional offers/accessories are not inferred.

| Product                 | Families     | Source-supported selection facts                                        | Price example |
| ----------------------- | ------------ | ----------------------------------------------------------------------- | ------------- |
| MSI MAG 274QF X24       | PLAY         | 27″ · 2560 × 1440; Rapid IPS; до 240 Гц · DisplayPort                   | 22 050 ₽      |
| LG UltraGear 24GS60F-B  | PLAY         | 23,8″ · 1920 × 1080; IPS; до 180 Гц                                     | 14 250 ₽      |
| MSI MAG 274F            | PLAY         | 27″ · 1920 × 1080; Rapid IPS; до 200 Гц                                 | 14 870 ₽      |
| LG UltraGear 32GS60QC-B | PLAY         | 31,5″ · 2560 × 1440; VA · изгиб 1000R; до 180 Гц                        | 23 920 ₽      |
| LG 27U631A-B            | CREATE, WORK | 27″ · 2560 × 1440; IPS · до 100 Гц; USB-C · PD 15 Вт                    | 14 460 ₽      |
| MSI Modern MD271UL      | CREATE       | 27″ · 3840 × 2160; IPS · до 60 Гц; USB-C · PD 65 Вт                     | 23 510 ₽      |
| LG UltraWide 34WR50QK-B | CREATE, WORK | 34″ · 3440 × 1440; VA · до 100 Гц; 21:9 · изгиб 1800R                   | 30 370 ₽      |
| MSI PRO MP275Q          | CREATE, WORK | 27″ · 2560 × 1440; IPS · до 100 Гц; HDMI · DisplayPort                  | 16 540 ₽      |
| MSI PRO MP272PMG        | WORK         | 27″ · 1920 × 1080; IPS · до 120 Гц; Камера · регулировка высоты         | 18 200 ₽      |
| MSI PRO MP251P          | WORK         | 24,5″ · 1920 × 1080; IPS · до 100 Гц · HDMI; Высота · поворот в портрет | 14 150 ₽      |

These are review fixtures, not an approved final KORSAC assortment. Scenario
assignment is editorial, not a manufacturer certification. Price numbers are
King-Komp retail snapshots, visibly marked “Цена — пример”; they are not
permanent product facts or an Offer. Supplier order timing, stock claims,
payment restrictions, delivery fees and warranty terms were not copied.
Availability is “Наличие уточняется”, with no fabricated stock state.

The MSI detail additionally uses the manufacturer’s flat/16:9 description,
2 × HDMI 2.0b, 1 × DP 1.4a, headphone output, −5°…+20° tilt, VESA 100 × 100 mm
and 613.5 × 249.7 × 438.5 mm dimensions with stand. WQHD is up to 144 Hz over
HDMI, up to 240 Hz over DP. Refresh rate is not a promise of rendered FPS.
No invented model/SKU/GTIN/MPN, HDR/color/response/benchmark claims, reviews,
ratings, certification, availability or commercial terms are published.

## Ordinary product content model

A catalog product has stable identity, manufacturer/brand, model, category,
approved media, supported characteristics, description/selection context,
editorial relations and publication state. Commercial values/status are
separate backend outputs, not characteristics or scraped permanent attributes.
Real variants can be added when approved; no variant or configuration snapshot
is required for this monitor.

Detail flow: media + identity/positioning + review price/status/CTA → key
specifications → selection context → fuller characteristics → visible alternate
views → delivery/payment/service information → PLAY relationship → other
selected monitors. The mobile identity/price/CTA precedes the large photograph,
so a purchase route remains practical. This is intentionally simpler than PC
Product Explorer. No PC stage, FPS panel, SYSTEM ID, assembly process,
configurator or System Passport is present in the ordinary product content.
Shared shell navigation can still lead to the existing computer experience.

Delivery/payment/service blocks explain where actual terms will appear and
link to Contacts. They do not define fees, warranty, SLAs or restrictions.
Bitrix determines methods, compatibility and required order properties for the
current order context; frontend renders those data rather than inferring them.

## Cart contract

Static cart now contains the two existing PLAY configurations plus one MSI
monitor. The monitor’s native “В корзину” link leads to `cart.html#cart-monitor`;
its ordinary line already exists in base HTML. There is no hidden configurator,
persistence, URL cart payload or implied live add-to-basket request.

| Line kind | Identity          | Payload/representation                                                                             |
| --------- | ----------------- | -------------------------------------------------------------------------------------------------- |
| `system`  | KORSAC PLAY 1440  | Authored immutable configuration snapshot; existing CONFIG / 01 or / 02 and edit link              |
| `product` | MSI MAG 274QF X24 | Ordinary product identity/specifications; PRODUCT marker, no CONFIG/System ID; product detail link |

HTML declares `data-cart-line-type` and a human-readable `data-cart-label` for
each line. The controller uses authored labels for announcements, undo and
quantity feedback. It never constructs a monitor CONFIG label from a PC model.
The UI Kit PC specimen declares the same fields. Cart count/summary/empty copy
uses “товар/позиция”, with correct quantity plurals instead of counting systems
or pretending all lines are PLAY configurations.

Quantity, min-one numeric guard, remove/restore, focus return, native PC
configuration disclosure and editing remain. Demo totals sum integer authored
unit amounts × quantity only. Initial three-line total is 381 850 ₽;
removing the monitor leaves the existing 359 800 ₽ PC example. No component
price engine, storage or network mutation is involved. Reload resets the
fixture. Existing reduced opacity feedback is reused.

Checkout/Success still open their original, separate two-system example. Cart
explains this explicitly before checkout: changes are not transferred between
pages. This stage does not invent basket persistence or change checkout
availability/payment/delivery rules. Production navigation instead reads the
same Bitrix Sale basket across cart and checkout.

## Commercial and future Bitrix ownership

| Owner                          | Data/responsibility                                                                                                           |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| Catalog/content product entity | Identity, name, brand, model, category, real media, characteristics, description, relations, publication state and SEO fields |
| Bitrix Catalog/Sale            | Authoritative price, currency, stock/order-state mapping, basket and checkout                                                 |
| Frontend                       | Render the provided products/methods/properties/statuses; accessible controls and local presentation state                    |

Ordinary product price does not reuse PC HL component pricing logic.
`kk.price-update` belongs to configured KORSAC computer pricing; applying it
to generic monitor retail pricing would require a separate future design.
No Bitrix code, HL/infoblocks, supplier import/feed, stock/pricing API or checkout
backend is implemented. Production line identity/type must be backend-derived,
not parsed from a label, SKU spelling or frontend scenario.

## Relationships and discovery

Home trust content exposes Equipment; all shared public product footers expose
Equipment and Monitors. The five-entry global header is preserved, as are the
compact transactional footers. Existing PLAY product content has a monitor
handoff; MSI detail links to PLAY’s 1440 record and the existing PLAY product.
These are “Рассмотреть для PLAY 1440” scenario relations, not guaranteed
compatibility/performance matches. Category links back to Computers; CREATE/
WORK choices remain connected through the family hierarchy. The review hub
exposes the three pages and mixed-cart fixture.

## Media and shared Media Viewer decision

[Media manifest](review/equipment-media-sources.json) maps 13 original WebP
files to the corresponding King-Komp product, source asset URL, native
dimensions, byte count/SHA-256, source order, authored alt and nullable caption.
Files are byte-for-byte originals in `prototype/assets/images/equipment/`;
all 10 products use distinct cover media, not stock/AI/substitute monitor renders.
All were decoded and visually inspected. Seven new covers retain their source bytes, including original white margins.
Shared-family placements reuse the same file; there are no duplicated downloads.
No image edits or hotlinks are used.

MSI detail shows its primary view and three alternate views. Every photograph
is visible `figure/img` or `ul/li/figure/img` HTML; there are no hidden slides.
Primary likely-LCP images are eager/high priority; lower images lazy/async.
Explicit dimensions reserve source aspect ratios. List photos fit equal media
areas without crop/stretch; other photos use natural responsive proportions.
No source is enlarged above its native width. Informative alt describes the
actual view, not a marketing claim; no source captions are fabricated.

`data-monitor-image` marks media; `data-monitor-gallery="msi-mag-274qf-x24"`
groups primary/alternate views with the same product identity. A future
progressive enhancement can resolve ordered original media from this identity
while preserving base content, links and source provenance. Projects keeps its
existing media contract; no incompatible viewer-specific markup is added.

A single shared site-wide Media Viewer should later be evaluated for Projects,
ordinary products, PC product media and other collections. Fancybox is only
one candidate. **No library, lightbox, viewer controls or enlargement behavior
is selected/installed in this PR.** Future enhancement must support keyboard,
Escape, focus return, accessible Prev/Next, reduced motion and no autoplay;
meaningful base galleries remain usable without JavaScript.

## SEO, responsive and accessibility

All 20 prototype pages remain `noindex, nofollow, noarchive`, without production
canonical or `og:url`. Equipment/category have CollectionPage; only ordinary
detail has Product, with source-supported name/brand/model/description/image/
category. Its image is the actual visible local primary view. No static price
enters Offer/AggregateOffer, Review or AggregateRating. Production Offer is
backend-owned per PR #9, and publication/indexability gates stay unchanged.

SEO audit extends existing guards with required page schemas, Product rejection
on hub/category, visible local monitor media, per-card media, informative alt,
explicit positive dimensions and matching Product.image. It checks markup/file
presence, not photographic authenticity; source/hash/visual evidence is separate.
A separate `tools/monitor_curation_audit.py` verifies the review assortment
counts/order, ledger membership, editorial relationship presence, stable
identity/name/link/specification/price/cover consistency and original media
bytes. Its numerical bounds are review acceptance checks, not production
assortment or business rules. Seven negative tests reject collapsed family
choice, duplicate entities, unknown models, family/query URL drift, changed
facts/prices, missing relationships/source evidence and swapped/edited media.
It cannot certify editorial suitability or photographic authenticity.
Existing Family/Projects/PC tests remain intact. The deterministic audit report
is refreshed; no test is weakened to admit these pages.

Family selections use two columns on desktop/tablet and one on mobile,
retaining a shared ordinary-product card architecture and family-specific
selection explanations. Layouts use fluid columns, wrapped native breadcrumbs/names and semantic dl
specifications. At 320px cards, gallery and spec rows become a single column.
No fixed-height text clipping or horizontal spec tables are used. Shared skip
link, landmarks, one H1, heading hierarchy, native navigation, visible focus
and drawer keyboard behavior remain. The base selection/gallery/cart content
works without JavaScript. There is no new animation system; Reduced Motion
keeps full meaning/navigation and the existing short state feedback.

See [review evidence and validation](review/equipment-v1.md). Human visual
review is required before merge. Do not auto-merge.
