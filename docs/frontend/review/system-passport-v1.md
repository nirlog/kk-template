# System Passport Experience v1 — review

Base: merged Equipment PR #12, `main` at
`01219297b9af159102feaa95d9e9569659642310`.
Ownership addendum is reviewed separately after merged PR #13, `main` at
`5750d45dfddf9ecd9c1bd3b3a815a2021e9b76d9`. Account Experience remains a
subsequent feature stage.

[Domain / workflow / D7 contract](../KORSAC-SYSTEM-PASSPORT.md) ·
[Synthetic fixture ledger](system-passport-fixture.json).

## Implemented review boundary

Public active and pending passports use a restrained KORSAC service shell,
with immediate content and no Brand Intro or eligibility writes. Active shows
SYSTEM ID, confirmed names, transfer and saved warranty dates, an extended
flag and System-bound inquiry. Pending shows only minimal inactive context.
Neither public document exposes serials, order/customer/internal keys, service
history or a fixture PUBLIC_ID. The inquiry validates input without sending,
storing, placing contact data into URL or claiming successful submission.

The main internal order has two computer Systems and one ordinary monitor:
KS-2610-0012 active; KS-2610-0013 ready/confirmed but not prepared. Separate
KS-2610-0014 is the prepared/inactive pending review fixture. It does not imply
that unprepared 0013 already has a public URL. Independent recovery examples
cover creation eligibility, partial missing units, preparation, transfer,
activation, already-prepared state and QR representation reuse.

Lifecycle management belongs to the future KORSAC D7 module in the **1C-Bitrix
administrative area**, not the public frontend. The disposable wireframe is
labelled **Bitrix Admin workflow concept / review only**; its review bar has no
public logo/Home link or commercial site shell. It shows the likely admin menu
(Systems, Ownership Requests, Inquiries, Statuses, Settings) and System card
tabs (Main, Components, Passport, Service, Ownership, History). Order detail exposes related Systems and opens
their admin cards; full System data are not flattened into order properties.

Internal forms cover maintenance, multi-record replacement, ADD, REMOVE,
repair with/without replacement and separate Data Correction. S/N values are
DEMO-\* placeholders, used only in this internal review specimen. Every enabled
action gives explicit non-execution feedback; forms do not mutate components,
identity, dates, warranty, history or audit. No client business lifecycle,
backend persistence, event automation, generator, QR, account or override is
implemented. Future guarantees are documented, not claimed as tested backend.

Approved ownership contract adds nullable current `System.USER_ID`, assigned
from authoritative `Order.USER_ID` at first handoff, with private request/history
entities. The secret is physical-machine evidence for a manager-reviewed
request, not an automatic takeover credential. Neither ordinary transfer nor
unlink changes machine/public identity, warranty or System/service history.
Initial SECRET_CODE allocation belongs to successful preparePassport(), in the
same transaction as first PUBLIC_ID preparation. Retries reuse both; activation,
transfer, USER_UNLINK and QR regeneration never replace the code. Only future
explicit privileged code regeneration may invalidate/replace it, with audit and
replacement-label handling. CANCELLED Systems retain the same secret/privacy
exclusions. This is an application-service/transaction contract only; no real
generator is implemented. Ownership remains a separate admin tab from Service.
Mandatory registration/checkout email, normalized email as Bitrix LOGIN,
existing-account guest verification and future unlink/«Мои системы» are
documentation only. No Account UI or Bitrix authentication is implemented;
Account Experience remains a subsequent, separate feature stage.

Ownership wireframe shows synthetic current user 52002, requested user 52003,
verified evidence only, PENDING request and internal INITIAL_ORDER /
ADMIN_TRANSFER history. Last change is 09.10.2026, 15:00 МСК; authored review
time is 11.10.2026, 15:00 МСК. The two-day warning is conspicuous but does not
disable approval. Native approve/reject actions and exceptional staff transfer
form never mutate USER_ID, request or history. No secret value, real label/QR
or browser verification/generator is present in the manager specimen.

Product has a visual **«Пример паспорта»** with illustrative KS-2610-0012 and
explicit wording that no existing/sold System is represented. It describes
confirmed components after assembly and transfer/warranty after handoff. The
example is authored HTML and remains unchanged by configuration selections;
`data-passport-output` stays removed. Its native CTA opens `passport.html` only
as a static review example. Scene/manifest synchronization remains. Homepage
ownership copy matches the v1 public projection. Legacy footer links lead to
Support/Contacts. Global navigation exposes no Passport directory or fixtures;
only the contextual Product example CTA and review materials link to the
active fixture. Internal workflow remains reachable only from review materials.

## Actual browser evidence

Chromium screenshots over HTTP, reduced mode, decoded local brand asset:

| View                                                   | Evidence                                                |
| ------------------------------------------------------ | ------------------------------------------------------- |
| Active desktop                                         | [1440 × 1706](passport-v1-desktop.png)                  |
| Active mobile                                          | [375 × 2242](passport-v1-mobile.png)                    |
| Pending desktop                                        | [1440 × 1000](passport-pending-v1-desktop.png)          |
| Pending mobile                                         | [375 × 1000](passport-pending-v1-mobile.png)            |
| Inquiry open, mobile                                   | [375 × 1000](passport-inquiry-v1-mobile.png)            |
| Internal workflow                                      | [1440 × 9230](system-workflow-v1-desktop.png)           |
| Internal confirmed components                          | [1376 × 860](system-workflow-components-v1-desktop.png) |
| Service forms / two actual replacements selected       | [1376 × 2204](system-workflow-service-v1-desktop.png)   |
| Manual fallback / eligibility scenarios expanded       | [1376 × 1491](system-workflow-actions-v1-desktop.png)   |
| Bitrix Admin IA / review bar                           | [1440 × 1000](system-workflow-admin-v1-desktop.png)     |
| Account ownership, request, history and staff transfer | [1376 × 2018](system-workflow-ownership-v1-desktop.png) |
| Product static Passport example, desktop               | [1344 × 468](product-passport-info-v1-desktop.png)      |
| Product static Passport example, mobile                | [343 × 1181](product-passport-info-v1-mobile.png)       |

Thirteen actual PNGs; component captures hide the floating header/skip link only
through Playwright screenshot style. Application behavior is unchanged. No
new temporal interaction needs MP4. No generated imagery, QR or lightbox.
Previous stage screenshots are historical baselines; the Product correction
component is current evidence of the removed identity concept.

## Static SEO, privacy and domain fixture checks

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 tools/seo_audit.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/seo_audit.py --json
PYTHONDONTWRITEBYTECODE=1 python3 tools/monitor_curation_audit.py
```

**41 tests pass**: 20 existing SEO, 7 Equipment curation, 14 Passport
projection/domain fixture guards. Audit: **23 pages, 0 errors, 58 warnings**.
[Deterministic report](seo-audit-v1.json) matches repeated JSON output.
Warnings: 23 omitted staging canonical/og:url, 23 pending social artwork,
12 existing relative schema URL/ID semantic-review warnings.

New guards require one SYSTEM ID in the documented shape, expected public
state, active components/snapshot dates/inquiry context and textual pending
status. Reject serial/internal/history markers even in comments/hidden markup,
hidden inquiry identity fields, prefilled customer fields, forbidden Passport
schema, System-specific social metadata and Brand Intro inclusion. Pending
cannot contain active components, transfer dates or warranty even hidden.
Real fixtures have unique component slots including SSD 1 and SSD 2. Product
legacy fake identity/live passport selectors and stale footer URLs are absent;
the illustrative Product ID is contained in the explicitly labelled static
example, with one contextual fixture link and no configurator output hooks.
Workflow is a disposable admin concept without public brand/Home shell;
workflow/fixture paths are not exposed in global navigation. Existing
Family/Projects/Equipment/Product/cart guards are retained.

Additional negative fixtures for **both active and pending** reject secret-code
markers/values, USER_ID, ownership request/history, verification/processing and
ownership source markers, including metadata, comments, hidden markup and
inline JSON. Valid SYSTEM ID formatting remains accepted. Existing serial and
internal-ID guards stay unchanged. Internal fixture tests ensure verified
request evidence has no secret, matches the current/history association and
leaves approval enabled under the warning.

Static checks cannot establish authorization, completeness of a future public
DTO allowlist, cryptographic strength, real warranty correctness, server HTTP
routing or transactional/idempotent backend behavior. No fake order automation
tests are added. Source monitor ledger/media hashes and 4/4/5 curation remain
unchanged and pass their separate audit.

## Browser validation

**23 pages × 8 widths = 184 layouts** at
320/375/430/768/1024/1280/1440/1920. No horizontal document overflow, duplicate
IDs, missing H1/noindex, page/console errors or external runtime requests.
SYSTEM ID is readable; transfer/end dates and inquiry CTA fit the first
practical viewport on all required widths. Long component names wrap; there
are no wide tables. Pending is a status screen, not a fake error.

**Axe WCAG 2 A/AA/2.1 AA: 0 violations in 12 states**:
active/pending/workflow × 320/375/1440 plus inquiry-open at those widths.
Some checks remain incomplete; automated results do not replace human visual
or full screen-reader acceptance.

Keyboard: skip link, dialog Tab containment, Escape/opener return, labels,
native selects and required topic/message focus pass. Inquiry success wording
explicitly says not sent and excludes entered contact data. Reduced dialog
feedback has no spatial transform; live normal → reduce cancels motion and
returning does not run an entry sequence. Direct normal/reduced/live passport
entry never displays Brand Intro or creates its timestamp.

Internal forms: nine distinct actual-record choices, multiple replacement
selection, correct hidden/disabled unselected input groups and retained input
when reselected. Eight form paths (seven service/correction plus internal
ownership transfer) validate required inputs without saving.
Disabled fallback actions explain their conditions. All enabled fallback/QR
review actions leave identity, dates and domain records unchanged.

Ownership actions also pass **24 layouts**, all eight widths in normal,
reduced and no-JS modes. Keyboard Enter can activate approve/reject; the
warning never disables either. Manual staff transfer validates its required
target and gives explicit non-execution feedback. Current account, request
evidence/status and history remain byte-for-byte unchanged; there are no
submission/network/storage operations. No-JS keeps all context and native
actions visible without saving. Whole-page Axe checks include the new section.

No-JS at 320px: active component list, pending meaning, native inquiry fallback
and Contacts route work. Internal service paths remain visible and native
input/button interactions make no request. HTML nesting, IDs, labels, local
resources/fragments/document links and PNG decoding are separately checked.

Revision: the Product example is also checked at all eight widths in normal,
reduced and no-JS modes (**24 layouts**). Changing case/RAM/SSD/SSD2 leaves its
HTML byte-for-byte unchanged. The native example CTA works by keyboard in
every mode and lands on the active fixture without Brand Intro. Product
header/footer/drawer contain no fixture link. Axe checks the example at 320
and 1440 in normal/reduced modes, with 0 violations in four additional states.

## Existing experiences

Homepage native discovery/dialogs/keyboard/touch/no-JS and normal/reduced hero
checks pass. PLAY ladder/MINI/preview/compare/rapid selection/live reduced
checks pass. Product Explorer six states/hotspots/Prev/Next/inert panels,
configuration scene + manifest, 242 rapid actions, seven responsive widths,
UI Kit isolation/touch/no-JS pass. The Product harness now expects only the
measurement observer and asserts that the old fake passport selector is gone;
stage/manifest/pricing checks remain intact.

Mixed cart retains two `system` snapshots plus one ordinary `product` monitor.
Integer static totals, quantity, min-one/focus, remove/restore, empty/reload and
PC edit/disclosure semantics pass. Checkout guest/company/validation/delivery/
payment preservation/static Success pass without payload mutation. Pricing,
cart/checkout controllers and Bitrix-owned restrictions are unchanged.

Existing Equipment/Monitors/Monitor Brand Intro normal eligibility, shared 24h
suppression across public routes, reduced skip/timestamp and live cancellation
pass. Those existing scripts are preserved; public Passport opts out entirely.
Projects/gallery, Contacts, Errors, Equipment, all computer families and review
UI participate in all 184 layouts; source media and ordinary product contracts
remain unchanged.

## Human acceptance

Review the restored Product example and its clear illustrative boundary;
confirm lifecycle ownership and order-card links belong to Bitrix admin.
Review current/requested owner context, verification without secret disclosure,
the non-blocking recent-change warning, exceptional staff form and future
initial-association/unlink invariants.
Review the utility hierarchy, mobile dates/CTA, pending privacy, read-only
System inquiry context, internal form clarity and lifecycle recovery reasons.
Confirm the documentation distinguishes stored physical Systems from changing
Product data and explains every future transactional boundary.

Human visual and architecture review is required before merge. Do not auto-merge.
Physical-device/full screen-reader, Firefox/Safari, direct file protocol,
external search/schema validators and real D7/order/QR/support integrations
were not run. All data are synthetic review fixtures; prototype completion is
not backend/publication acceptance.
