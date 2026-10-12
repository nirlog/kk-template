# KORSAC final audit — review evidence

Base: merged PR #15, `main` at `e2a693b9bb4a33786ebe2859fd952a79a8d5e356`.
Date: 12 October 2026 (Europe/Moscow). Primary specification/mapping/ownership:
[Final holistic report](../KORSAC-FINAL-AUDIT.md).

## What changed

Mobile public drawer now routes Account to native Login, matching the header. Scope-dialog copy also describes the existing static
Account rather than a missing concept. Checkout starts with the same two PLAY configurations + ordinary monitor as
Cart/Success, total 381 850 ₽; the documents remain independent static fixtures.
Product opens an honestly labelled example Cart instead of a scope-dialog dead
end; selected options do not transfer. Warranty/preparation copy and dependent
contracts were aligned. No new feature, backend, generator or motion system.

## Compact final captures

Actual Chromium HTTP captures, settled reduced-mode feedback, no Brand Intro,
blank checkout fields and no real customer/credential/QR values. Desktop public
images are **viewport overviews**, not full-page review of every section. Utility
captures show the complete document. All eight widths were checked separately.
Original Projects/Equipment images were not edited, cropped or generated.

| File                                                                 | Dimensions  | Representative role                                              |
| -------------------------------------------------------------------- | ----------- | ---------------------------------------------------------------- |
| [final-home-desktop.png](final-home-desktop.png)                     | 1440 × 1100 | Expressive public shell/hero/family handoff                      |
| [final-product-desktop.png](final-product-desktop.png)               | 1440 × 1100 | PC model identity / approved schematic media                     |
| [final-project-desktop.png](final-project-desktop.png)               | 1440 × 1100 | Historical narrative/provenance/source photography               |
| [final-monitors-desktop.png](final-monitors-desktop.png)             | 1440 × 1100 | Curated category with distinct family decision routes            |
| [final-checkout-mobile.png](final-checkout-mobile.png)               | 375 × 2528  | Calm transaction, three source items/total, required Email       |
| [final-passport-mobile.png](final-passport-mobile.png)               | 375 × 2242  | Public System utility, saved warranty, actual components/inquiry |
| [final-account-orders-desktop.png](final-account-orders-desktop.png) | 1440 × 1213 | Private utility / synthetic authorized purchase snapshots        |
| [final-account-systems-mobile.png](final-account-systems-mobile.png) | 375 × 1774  | Current physical-System association, distinct pending request    |
| [final-product-cart-desktop.png](final-product-cart-desktop.png)     | 370 × 1155  | Element capture: fixed honest Product→example Cart CTA           |
| [final-account-drawer-mobile.png](final-account-drawer-mobile.png)   | 375 × 1100  | Fixed native Account utility, compact five-entry menu            |

No MP4: this PR adds no temporal interaction/motion requiring new video evidence.
Earlier motion/source/detail screenshots remain historical evidence, not the
current authoritative route/domain contract.

## Deterministic validation

From repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 tools/final_audit.py --json
PYTHONDONTWRITEBYTECODE=1 python3 tools/seo_audit.py --json
PYTHONDONTWRITEBYTECODE=1 python3 tools/monitor_curation_audit.py
```

- Complete suite: **73 tests**, retaining all prior suites unchanged and adding
  negative cross-page architecture fixtures.
- [Final deterministic audit](final-audit.json): 31 HTML documents, **0 errors**.
  Exact route/schema types; visible/schema crumb names/positions/ancestor URLs;
  five-entry menus/logo/native Account links; public/private/Admin boundaries;
  no old Passport coupling; mixed line types/source identities/amounts; local
  resources/anchors including Markdown/CSS; stable GitHub doc references;
  authoritative mapping parity; protected source markers; deferred viewer guard.
- [SEO report](seo-audit-v1.json): **0 errors, 74 intentional staging warnings**.
  Byte-identical to the current Account baseline. Relative semantic URL/host/
  social-artwork warnings remain explicit production work, not audit suppression.
- [Monitor curation](monitor-curation-v1.json) is unchanged: 10 unique real
  products, PLAY4/CREATE4/WORK5, shared entities/URLs and source media.
- All **23 source images** retain manifest hashes/byte counts (Projects10 +
  Equipment13). Every one of **99 HTML image instances** decodes; source image
  natural dimensions match authored HTML. All 31 heading outlines have no upward
  level skips; decorative/brand images preserve their intended empty alt.

Reports contain no assertion that a backend generator, ACL or transaction was
executed. Test fixtures mutate temporary copies, never real source data or users.

## Browser and regression scope

Current Chromium 151 / installed Playwright, HTTP server over `prototype/`.
Machine reports are summarized in [final browser validation](final-browser-validation.json).

- **248 layouts**: all31 × 320/375/430/768/1024/1280/1440/1920, no horizontal
  document overflow/duplicate IDs/H1/noindex/runtime failures.
- **62 complete-inventory Axe base states** (375/1440): zero violations for
  WCAG2A/AA and WCAG2.1AA tags. Additional focused checks: Account30,
  Passport/Admin/inquiry12, monitor/Cart12, families9, Projects6, updated scope-dialog2; zero violations.
  These runs overlap and are not a count of distinct pages. Axe incomplete
  checks remain human review; feedback is sampled after finite animation settles.
- Home shell/top-state/sticky header/drawer/search-dialog keyboard and no-JS;
  normal/reduced/live Hero behavior. All native Account utilities and drawer
  destinations checked at every requested width on representative public pages.
- Families: Home→Computers→PLAY→Product ancestors and Home→CREATE/WORK;
  first practical mobile CTA, native anchor clearance, skip/focus/no-JS.
- PLAY scenario/preview/MAX3 comparison and mobile matrix retain existing
  controller/semantics; Product Explorer/configurator/measurements/assembly,
  rapid state changes and independent Passport example remain unchanged.
- Projects: three source covers, eight detail photos including gallery; native
  Home→Projects→detail→PLAY routes; dimensions/aspect/no upscale; no-JS.
- Equipment: shared family identity, one real local ordinary detail, actual
  images/links; ordinary Monitor→Cart line; quantity/min1/remove/restore/focus/
  empty/reload/static integer totals, UI Kit scoped Cart specimen.
- Checkout: guest/B2B native validation/focused errors, pickup dialog, three
  neutral methods independent of buyer, generic extra method/property fixtures,
  no contact/URL payload or network mutation; source total now381850.
- Full **static** journey: Home→Computers→PLAY→Product→example Cart→mixed
  Checkout→Success→Orders/detail→My Systems→same public Passport. Product
  selections do not rewrite Passport or become a real basket operation.
- Passport: direct normal/reduced/live entry never runs/writes Brand Intro;
  pending content/privacy; inquiry focus/Tab/Escape/return/native fallback;
  all internal review actions/forms remain non-saving, Ownership separate.
- Account: mandatory Email/password confirmation, generic recovery, focus,
  code format/cleanup/non-echo, pending vs association, exact unlink confirmation,
  unchanged fixtures/session on actions; no-JS implicit Enter does not submit;
  external return query ignored. Native dialog close/event cleanup is awaited.
- Fixed Product→Cart→mixed Checkout works without JS at320. All prior auth,
  System/ownership/privacy/Equipment/SEO deterministic guards remain green.

## Human gate and limits

READY applies to **architecture planning**, not production/backends. Review the
primary ownership/projection matrices and remaining migration-design gates,
then visually review the compact current set and the existing detailed captures.

This environment does not establish Windows OS behavior, physical keyboards/
phones, screen-reader output or Safari/Firefox. Reduced-motion media is emulated
in Chromium. Automated findings do not prove every real production content size,
source URL permanence, HTTP status, server permission, authentication, mail,
legal date calculation, QR/credential security or transactional idempotency.

No unresolved static BLOCKER remains. Human visual **and architecture** acceptance
is required; do not auto-merge.
