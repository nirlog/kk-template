# KORSAC — Final holistic / semantic / SEO audit

Base: PR #15 merged into `main`, `e2a693b9bb4a33786ebe2859fd952a79a8d5e356`.
Audit date: 12 October 2026 (Europe/Moscow). This is the complete current static
product specification before Bitrix architecture planning, not a feature release.

## Executive summary

**READY for Bitrix architecture/migration planning.** The prototype has coherent
public commercial, public System utility, private Account and internal Admin
boundaries. It is **not ready for production deployment or backend implementation
without the integration decisions listed at the end**. No real auth, commerce,
System mutation, email, QR/credential generator or Bitrix implementation exists.

The review inventory is 31 HTML documents. Real Projects/monitor facts retain
provenance; PLAY prices/configuration choices, Orders, Systems and Account records
are review fixtures. Authenticated ownership is a future server guarantee, never
proved by static HTTP 200 or `noindex`.

This PR fixes actual contradictions: mobile Account placeholder links/stale scope-dialog copy, mismatched
mixed Checkout/Success source summaries, a Product purchase CTA that ended in a
scope dialog, outdated warranty/default/preparation descriptions and unstable
feature-branch review document links. The Product CTA now honestly opens an
**example Cart**, without implying addition or transferring choices. No accepted
family, catalog, Explorer, pricing, ownership or service architecture is redesigned.

Contract precedence:

| Subject                                        | Authoritative owner                            | Role of this audit                                   |
| ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------------- |
| Production tree/indexability/publication gates | [IA](KORSAC-INFORMATION-ARCHITECTURE.md)       | One concrete static → production mapping below       |
| Metadata/schema/HTTP/canonical                 | [SEO](KORSAC-SEO-FOUNDATION.md)                | Cross-page semantic and privacy checks               |
| Physical System/lifecycle/ownership/warranty   | [System](KORSAC-SYSTEM-PASSPORT.md)            | Confirms domain invariants and projection boundaries |
| Auth/private access/Bitrix components          | [Account](KORSAC-ACCOUNT-EXPERIENCE.md)        | Connects private UX to its future owners             |
| Commerce methods/properties/price              | [Commerce](KORSAC-CART-CHECKOUT-EXPERIENCE.md) | Bitrix Sale owns rules; source fixtures aligned      |
| Projects/equipment facts/media                 | Source ledgers linked below                    | Retains provenance; no newly invented facts          |

Historical review assets remain evidence of their named revision. They do not
override current contracts or this final report. PASS means reviewed static
behavior/contract; it never certifies an unimplemented backend operation.

## Final route inventory

This is the **authoritative complete static → production mapping**. IA owns the
production policy. `{approved-slug}` requires a real editorial/catalog decision;
review filenames and King-Komp legacy slugs do not select production slugs.

| Static document                          | Production route / role                | Page type                        |
| ---------------------------------------- | -------------------------------------- | -------------------------------- |
| `prototype/index.html`                   | `/`                                    | Homepage                         |
| `prototype/computers.html`               | `/computers/`                          | Computer hub                     |
| `prototype/catalog.html`                 | `/computers/play/`                     | PLAY family                      |
| `prototype/create.html`                  | `/computers/create/`                   | CREATE family                    |
| `prototype/work.html`                    | `/computers/work/`                     | WORK family                      |
| `prototype/product.html`                 | `/computers/play/1440/`                | Computer model                   |
| `prototype/projects.html`                | `/projects/`                           | Projects archive                 |
| `prototype/project.html`                 | `/projects/{approved-slug}/`           | Historical project               |
| `prototype/equipment.html`               | `/equipment/`                          | Equipment hub                    |
| `prototype/monitors.html`                | `/equipment/monitors/`                 | Curated category                 |
| `prototype/monitor.html`                 | `/equipment/monitors/{approved-slug}/` | Ordinary product                 |
| `prototype/cart.html`                    | `/cart/`                               | Transactional cart               |
| `prototype/checkout.html`                | `/checkout/`                           | Transactional checkout           |
| `prototype/order-success.html`           | `/order-success/`                      | Transactional result             |
| `prototype/contacts.html`                | `/contacts/`                           | Contacts                         |
| `prototype/passport.html`                | `/passport/{PUBLIC_ID}/`               | Active public System projection  |
| `prototype/passport-pending.html`        | `/passport/{PUBLIC_ID}/`               | Pending public System projection |
| `prototype/account-login.html`           | `/account/login/`                      | Authentication                   |
| `prototype/account-register.html`        | `/account/register/`                   | Registration                     |
| `prototype/account-forgot-password.html` | `/account/forgot-password/`            | Recovery                         |
| `prototype/account-orders.html`          | `/account/orders/`                     | Private Orders                   |
| `prototype/account-order.html`           | `/account/orders/{id}/`                | Private Order snapshot           |
| `prototype/account-systems.html`         | `/account/systems/`                    | Private current Systems          |
| `prototype/account-inquiries.html`       | `/account/inquiries/`                  | Private inquiries                |
| `prototype/account-profile.html`         | `/account/profile/`                    | Private profile                  |
| `prototype/404.html`                     | `REQUESTED URL; HTTP 404`              | Error response                   |
| `prototype/500.html`                     | `REQUESTED URL; HTTP 500`              | Resilient error response         |
| `prototype/503.html`                     | `REQUESTED URL; HTTP 503`              | Resilient error response         |
| `prototype/system-workflow.html`         | `NO PUBLIC ROUTE`                      | Disposable Bitrix Admin review   |
| `prototype/ui.html`                      | `NO PUBLIC ROUTE`                      | UI Kit review                    |
| `prototype/review.html`                  | `NO PUBLIC ROUTE`                      | Review navigation                |

Future routes: real CREATE/WORK `{model}` below their family namespace, other
approved PLAY models, and `/search/?q={query}` (noindex). They are **DEFERRED**,
not missing review files or active links to imaginary products. `/account/` is
an entry resolver: authenticated → Orders; unauthenticated → Login with safe
return context. There is no dashboard file or additional private section.

No public `/passport/` directory, System search by SYSTEM_ID or internal
workflow route exists. Active/pending are two projections of the **same**
`/passport/{PUBLIC_ID}/`, not separate production endpoints. Invalid token →
HTTP 404. Internal System administration belongs inside Bitrix Admin only.
404/500/503 render at the original requested URL with the corresponding status.

## Page-type inventory

| Design family               | Static documents                                                                                 | Meaning / schema                             | Brand Intro                                            |
| --------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------- | ------------------------------------------------------ |
| Public expressive browsing  | Home; Computers; PLAY; CREATE; WORK; Product; Projects/list/detail; Equipment; Monitors; Monitor | Authored content/catalog; schema by entity   | Existing shared daily eligibility on these 11 pages    |
| Public informational        | Contacts; 404                                                                                    | Verified contact slots / navigation recovery | None                                                   |
| Resilient errors            | 500; 503                                                                                         | Standalone CSS/local logo/no application JS  | None                                                   |
| Commerce utility            | Cart; Checkout; Success                                                                          | Static mixed source order; no schema         | None                                                   |
| Service utility             | Active/pending Passport                                                                          | Public physical-System projection; no schema | None                                                   |
| Private utility/auth        | Eight Account documents                                                                          | Synthetic private/auth review; no schema     | None                                                   |
| Development/internal review | Review hub; UI Kit; System workflow                                                              | No production page entity                    | None automatically; UI Kit explicit motion replay only |

The 11-page Intro policy is preserved, including reduced-mode skip/timestamp,
24-hour local frequency and no unexpected replay on preference changes. Service,
private and transactional contexts never read/write that eligibility key.

## Entity and domain inventory

| Entity                 | Meaning / source                                              | Must not become                                               |
| ---------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| Product                | Current sale/catalog entity; computer or ordinary product     | A physical System or historical purchase snapshot             |
| Computer Family        | PLAY/CREATE/WORK editorial decision model                     | A price tier or generic cloned catalog                        |
| Computer Model         | Approved PC positioning/current options/current catalog state | A real SYSTEM ID, S/N or service record                       |
| Ordinary Product       | Monitor identity/specs/media plus backend commercial state    | CONFIG or physical computer System                            |
| Order                  | Authorized Bitrix Sale transaction and saved commercial state | Current System-owner identity                                 |
| Order Line             | Purchase-time product/configuration/quantity/price snapshot   | A live read-through of current Product values                 |
| System                 | One physical computer, independently persistent               | Catalog Product, Account or Passport page                     |
| SystemComponent        | Actual confirmed component record; type/slot/serial/history   | A selected configurator label                                 |
| SystemServiceEvent     | Internal maintenance/upgrade/repair event and changes         | Public v1 marketing/service feed                              |
| SystemOwnershipRequest | Verified request, manual approval/rejection                   | Automatic takeover from code                                  |
| SystemOwnershipHistory | Internal association-change audit                             | Public ownership listing                                      |
| SystemInquiry          | Support request with System context and protected contact/ACL | An ownership request or transferable prior-owner conversation |
| User / Account         | Standard Bitrix User and authorized private presentation      | The immutable physical identity of a machine                  |
| Project                | Historical completed-build evidence / editorial content       | Current Product or Offer                                      |

PLAY remains scenario/resolution/performance-first; MINI branches from 1440.
CREATE is workflow/application/workload-first; WORK is task/context/operational
priorities-first. CREATE/WORK have no invented model lineups. Monitor family
membership is editorial many-to-many: 10 unique products, 4 PLAY / 4 CREATE /
5 WORK placements, one entity/destination per product.

## Navigation audit

**FIXED / PASS.** Logo → Home. Primary public menu retains exactly Computers,
Configurator, Business, Support, About. Account is a utility, including the
mobile header and drawer; both now use native Login links. Search remains an
honest scope placeholder. Cart utility opens the static Cart. All meaningful
family/catalog/project/equipment/private routes remain native without JS.

Public footer exposes families, Projects, Equipment/Monitors and Contacts,
not private Orders/Systems/Profile, Passport directory or internal workflow.
The existing «Материалы прототипа» link is explicitly review-only and is removed
from production. Review hub alone exposes the disposable Admin wireframe.
Utility Account footer offers Contacts only. Compact checkout/success and
resilient error shells intentionally omit marketing navigation.

Visible breadcrumbs and JSON-LD agree in names, order, positions and ancestor
URLs. Product resolves via PLAY → Computers; ordinary product via Monitors →
Equipment. No breadcrumb invents CREATE/WORK model pages.

## CTA audit

| Page/context    | Native route or review action                                   | Result / boundary                                                         |
| --------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Home            | Computers / family / existing PLAY model                        | PASS; family landing does not imply model availability                    |
| Computers       | PLAY / CREATE / WORK                                            | PASS; three different selection logics                                    |
| PLAY            | PLAY 1440 / authored other scenario information / compare       | PASS; no imaginary model pages                                            |
| CREATE / WORK   | Workflow/task sections; Contacts                                | PASS; no fake catalog/price/model CTA                                     |
| Product         | Configurator; example Cart; labelled Passport example           | FIXED; Cart opens a fixture, choices are not added/transferred            |
| Projects/detail | Actual original case or local fixture; relevant PLAY            | PASS; historical case does not become today's model                       |
| Equipment       | Monitors                                                        | PASS; one implemented curated category                                    |
| Monitors        | One local detail; other actual King-Komp originals              | PASS; no fabricated local details                                         |
| Monitor detail  | Cart `#cart-monitor`; relevant PLAY                             | PASS; ordinary line, no guaranteed compatibility                          |
| Cart            | Checkout / product edit / ordinary detail                       | PASS; local changes do not persist between documents                      |
| Checkout        | Valid presentation → static Success                             | FIXED; same authored mixed source summary, no order/payment/contact send  |
| Success         | Safe password setup/recovery concept; Orders; continue choosing | PASS; explicit future account/mail state, no false auth success           |
| Passport        | Contextual inquiry; Contacts fallback                           | PASS; no secret required for public support                               |
| My Systems      | Same public Passport; inquiry; Add; Unlink                      | PASS; mock validation/confirmation does not change association            |
| Orders/detail   | One local detail; My Systems                                    | PASS; Systems are not prior-owner orders; no fake unprepared Passport URL |
| My Inquiries    | Contextual inquiry; native disclosures                          | PASS; support and ownership requests stay separate                        |
| Auth/Profile    | Native private/auth links; presentation checks                  | PASS; no backend success/session/account claims                           |
| Errors          | Home/Contacts; 503 original-request retry                       | PASS static; production retry/HTTP routing is server-owned                |

No new marketing CTA or feature is introduced. Review-only link handling must
be removed/replaced by production entity-aware routing during migration.

## Terminology audit

**FIXED / PASS.** Customer-facing «модель», «заказанная конфигурация», «фактически
установленная комплектация», «паспорт компьютера/системы», «личный кабинет» remain
contextual Russian. Technical documents use System and named fields precisely.
Cart's legacy `data-cart-line-type="system"` means **configurable PC commerce
line**, never an already-created System. Production classification comes from
backend metadata, not this string or the word «Система» in an eyebrow.

CONFIG / 01/02 identifies two authored PC configuration examples; PRODUCT marks
the monitor. Counts/announcements use «товар/позиция», not “all systems”. Public
Passport explanatory text now says confirmed **installed комплектация**. UI Kit
SYSTEM ID motion is illustrative review content, not real machine identity.

## Commerce-flow audit

| Journey                                                                                                                    | Static result                                                                     | Production continuation                                                  |
| -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| A. Home → Computers → family → model → configuration → Cart → Checkout → Success → Order → handoff → My Systems → Passport | FIXED / PASS for available PLAY path; CREATE/WORK stop at honest landing/Contacts | Sale/auth/assembly/physical handoff/server DTOs are DEFERRED integration |
| B. Equipment → Monitors → ordinary product → Cart → Checkout → Order                                                       | FIXED / PASS; source mixed fixture coherent                                       | Ordinary products never create System                                    |
| C. QR → public Passport → inquiry                                                                                          | PASS direct Passport/inquiry UX; no fake QR                                       | QR generation and actual submission DEFERRED                             |
| D. Account → My Systems/My Inquiries → support                                                                             | PASS native contextual routes and review checks                                   | Server requester/ACL authorization DEFERRED                              |
| E. Add System → ID + code → pending → manager approval → association                                                       | PASS review structure, no simulated mutation                                      | Verification/request/approval transaction DEFERRED                       |
| F. My Systems → Unlink → NULL                                                                                              | PASS exact confirmation/invariant copy, fixture unchanged                         | Authorized lock/recheck + USER_UNLINK transaction DEFERRED               |

All six flows have clear owners and no unresolved frontend transition blocker.
Their backend portions are conceptual, not a claim of end-to-end commerce.

Cart, Checkout and Success now start with two PLAY snapshots (179 900 ₽ each)
and ordinary MSI monitor (22 050 ₽): **381 850 ₽**, delivery unknown. JS sums
integer authored prices × quantities only within Cart. Local configuration,
quantity/removal and checkout contact changes are never persisted/transferred.
Payment methods, delivery compatibility and required order properties come
from Bitrix, not a buyer-type JS business matrix. Guest checkout stays available.

## Product System Order Account boundaries

**PASS. Product current configuration ≠ Order configuration snapshot ≠ System
actual confirmed configuration.** Current Product updates never rewrite saved
purchase prices/options. Assembly confirms actual components separately; audited
service can later change System components without rewriting historical Orders.
One purchased PC unit creates one System; quantity two creates two. Monitor
creates none. Unit-key uniqueness/idempotency/reconciliation belong to D7/Sale.

Product retains a labelled static visual Passport example, independent of
configurator. The illustrative ID is not an existing/sold machine claim and no
transfer/warranty/actual-component projection is generated from selections.
`data-passport-output` is permanently absent from Product and controllers.

System.USER_ID is nullable **current association**, not identity or proof of
legal ownership. First handoff uses authoritative Order.USER_ID. Account B's
fixture owns transferred 0012 but does not display Account A's original Order
or conversations. B has its own completed monitor Order and current mixed Order
with future Systems 0015/0016. Pending request 0014 is not an associated System.

## System Passport audit

**PASS**, with Admin preparation copy aligned to the current application-service
contract. Full lifecycle remains in [System contract](KORSAC-SYSTEM-PASSPORT.md).

| Concern            | Authoritative invariant                                                                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SYSTEM_ID          | `KS-YYMM-NNNN`; creation-time atomic sequence; immutable/unique/not reused; never COUNT + 1                                                                         |
| PUBLIC_ID          | Server CSPRNG 128 bits; unique, unpredictable, immutable; allocated at preparation                                                                                  |
| SECRET_CODE        | Private random eight digits, human `####-####`; CSPRNG server only; not public token                                                                                |
| createSystem()     | Idempotent per immutable computer-unit key; no physical System for ordinary monitor                                                                                 |
| preparePassport()  | READY_FOR_DELIVERY + confirmed components + permitted lifecycle; allocate PUBLIC_ID and SECRET_CODE **if absent**; commit atomically; then URL and QR/label allowed |
| Retry              | Reuses existing token/code; cannot reset active state or print failed/rolled-back allocation                                                                        |
| activatePassport() | First confirmed handoff saves TRANSFER_DATE, warranty snapshot, initial Order.USER_ID/history and PUBLIC_ACTIVE atomically; retries preserve later ownership        |
| QR regeneration    | Rebuild representation of same URL; preserves token/code                                                                                                            |
| Code replacement   | Only future privileged explicit operation with audit/protected update/replacement label                                                                             |
| CANCELLED          | Same credential/projection privacy; no identity recycling or public secret                                                                                          |
| Manual fallback    | Create/prepare/activate/QR recovery remain staff operations with checks/audit                                                                                       |
| Components         | Actual confirmed records; slot keys support multiple SSD/RAM etc.; private S/N                                                                                      |
| Service            | Internal maintenance/upgrade/repair; ADD / REPLACE / REMOVE; transactional component history                                                                        |
| Data correction    | Separate audited correction, not fake repair or silent historical rewrite                                                                                           |
| Pending            | Prepared inactive projection: readable ID/message only; no components/transfer/warranty                                                                             |

Warranty defaults: **24 months + optional 12**, starts at **TRANSFER_DATE**.
Save applied months/extension/end once. Repair, replacement and maintenance do
not extend it; later global defaults do not recalculate existing Systems. Public
Passport/Account display saved results, never legal-date arithmetic in JS.
The authored 07.10.2026 → 07.10.2029 example includes extension and is synthetic.
Product copy now states the approved default while leaving legal terms pending.

## Account and privacy audit

**PASS.** Eight files: three auth, four private sections and nested Order detail;
no dashboard/extra section. Email mandatory for registration/checkout; normalized
email is Bitrix LOGIN, phone is contact data. Login has no independent username.
New guest email → future User + Order; existing email requires authentication/
verification before attachment. Password setup/recovery uses protected standard
flow; no plaintext password mail. Profile EMAIL/LOGIN changes need verified,
authorized consistency, not browser field equality.

Public Passport needs no Account. Add System takes ID + private code as input,
uses no default secret and does not echo/store/send it in this prototype. Future
backend verifies with rate limiting/audit, creates manager-reviewed request and
never transfers automatically. Normal transfer, unlink, activation and QR
regeneration preserve code. `<7 days` warning is prominent but not a hard block.
Unlink sets current USER_ID NULL and records USER_UNLINK atomically after auth,
without changing identity/Passport/components/warranty/service. Manager Ownership
stays a separate Admin tab, not Service or Account.

The client-supplied return parameter is ignored by the prototype. Production
return resolution is origin-relative allowlisted Account context, without
scheme-relative/encoded separator/control character bypasses, followed by
resource authorization. Static private files contain synthetic data only;
real privacy requires server access controls, safe responses and cache policy.

### Public private data projection matrix

“Protected” is not a permission for generic Admin DTOs/logs to disclose secrets.
Only a separately privileged label/credential service may retrieve protected
material for printing. Verification results expose a boolean/result, never code.

| Field                                       | Public Product                      | Public Passport                                   | Account                                                 | Bitrix Admin                                  |
| ------------------------------------------- | ----------------------------------- | ------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------- |
| Current Product name/options/price          | Yes, backend state                  | No live Product state                             | Purchased snapshot only                                 | Catalog/Sale context                          |
| Illustrative SYSTEM ID                      | Labelled example only on PC Product | No illustrative mixing                            | No false association                                    | Review fixture only                           |
| Actual SYSTEM_ID                            | No                                  | Yes                                               | Authorized human ID                                     | Yes                                           |
| PUBLIC_ID / Passport URL                    | No real locator                     | Route only                                        | Allowed public link only                                | Yes                                           |
| SECRET_CODE                                 | No                                  | No, including pending/cancelled                   | Empty input only for verification                       | Protected printing/verification service only  |
| Component S/N                               | No                                  | No                                                | No                                                      | Authorized component record                   |
| Confirmed installed component names         | No physical records                 | Current active projection                         | Short authorized summary                                | Full actual records/history                   |
| Transfer date / warranty result             | General concept/default only        | Saved active result                               | Saved authorized result                                 | Snapshot + audited correction                 |
| Warranty arithmetic/internal fields         | No                                  | No raw internals                                  | No                                                      | Backend/legal snapshot service                |
| USER_ID / current account                   | No                                  | No                                                | Server context, no raw ID in customer HTML              | Authorized association/account                |
| Ownership history                           | No                                  | No                                                | No                                                      | Internal audited history                      |
| Ownership request                           | No                                  | No                                                | Own concise pending state only                          | Authorized processing; no submitted code      |
| SECRET_VERIFIED evidence                    | No                                  | No                                                | No                                                      | Result only, never raw credential             |
| Service/component history / removed records | No                                  | No v1                                             | No v1                                                   | Authorized service/history                    |
| Order number/lines/configuration/prices     | No                                  | No                                                | Authorized purchase snapshot                            | Sale detail                                   |
| Order internal IDs/unit keys                | No                                  | No                                                | Authorized route/projection only; not hidden System key | Sale/D7 relationship                          |
| Requester contact/message                   | No                                  | Input for inquiry only; not machine payload       | Authorized own/ACL conversation                         | Authorized support                            |
| Prior-owner Order/private inquiry           | No                                  | No                                                | Never inherited through System transfer                 | Permission-controlled separate source         |
| Supplier/cost/RMA/staff notes               | No                                  | No                                                | No                                                      | Privileged internal access                    |
| Password/token/session payload              | No                                  | No                                                | Empty password entry; no source defaults/meta           | Standard auth internals, never printed/logged |
| Public metadata/schema                      | Generic Product truth               | Generic service metadata, no machine/owner fields | Generic private/auth metadata, no customer data/schema  | Review-only generic metadata                  |

## SEO indexability audit

**PASS.** All 31 static documents remain `noindex, nofollow, noarchive`; no
production canonical or `og:url`. No invented host, sitemap or robots.txt.
Private/noindex does not grant confidentiality. Future production policy is
page-specific and comes from IA, not a global replacement of staging robots.

| Production class                                                  | Indexability / canonical / sitemap                                                      |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Home/Computers/PLAY/real model                                    | Published real content: index, absolute self-canonical, sitemap                         |
| CREATE/WORK/future models                                         | Only after unique real content/product readiness; prototype is not publication approval |
| Projects/detail/Equipment/Monitors/real ordinary product/Contacts | Same real-content publication gate; self-canonical and sitemap                          |
| Cart/Checkout/Success/Auth/Account/Search                         | noindex; no canonical; excluded from sitemap; private access for private contexts       |
| Active Passport                                                   | noindex, follow; no canonical/schema; no sitemap                                        |
| Pending Passport                                                  | noindex, nofollow; no canonical/schema; no sitemap                                      |
| 404/500/503/review                                                | No indexable content entity/canonical/sitemap; real HTTP errors owned by server         |
| Filter/sort                                                       | No automatic SEO entities; default noindex, no canonical/sitemap                        |
| Configurator options                                              | Same Product, not new Product URL/schema; primary-model canonical policy in production  |

Relative semantic URLs are intentionally review-only; production uses approved
origin/router/entity context for absolute schema/canonical. Metadata is unique,
truthful and server-owned; no private System/account facts enter head.

## Structured data audit

**PASS**, now enforced for **all** page types, not just recently added ones.

| Page type                                                     | Prototype / future semantic contract                                                   |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Home                                                          | Organization + WebSite; no fabricated corporate/contact facts                          |
| Computers / PLAY / CREATE / WORK                              | CollectionPage + BreadcrumbList                                                        |
| Projects                                                      | CollectionPage + BreadcrumbList                                                        |
| Project                                                       | Article + BreadcrumbList; real visible local image; no Offer/current model equivalence |
| Equipment / Monitors                                          | CollectionPage + BreadcrumbList                                                        |
| Computer model / ordinary monitor                             | Product + BreadcrumbList; supported facts; no static Offer                             |
| Contacts                                                      | ContactPage + BreadcrumbList; no invented contact values                               |
| Passport / Account/Auth / commerce / errors / internal review | No structured data v1                                                                  |

Production Offer comes only from real backend commercial state. No Review or
AggregateRating/AggregateOffer/sample prices in prototype schema. Visible and
structured crumbs are compared structurally, including non-final item URLs.

## Accessibility responsive and visual consistency audit

**PASS within the tested scope.** Eight widths: 320/375/430/768/1024/1280/1440/1920;
31 pages, 248 layouts. One H1, main/skip link, unique IDs, valid label targets,
no document overflow. Focus, native drawer/dialog Tab/Escape/return, errors,
no-JS routes/fallbacks and reduced/live preference checks retain the baseline.
Axe results and exact coverage are in [final review evidence](review/final-audit.md).
Automated Axe does not replace screen-reader/physical-device/human assessment.

Intentional design families remain distinct: open expressive public content,
compact transaction utility, 1180px Account utility, mobile-first Passport,
operational Admin wireframe and standalone errors. Public content retains the
1360px container and shared tokens. This width variation follows role rather
than accidental CSS drift. Buttons/inputs/dialog behavior reuse shared control
and motion primitives; no new animation system is added.

Reduced mode keeps visible short opacity/color/border feedback; no spatial
entrance, large clip/scale/stagger or Brand Intro. Native content/nav remains
available without JS. Representative screenshot set is compact, not another
full archive; no MP4 is needed for these copy/link/summary corrections.

## Prototype fixture and media audit

| Value class                            | Current examples                                                                                                                                           | Source / production treatment                                                                                                                                                                                           |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A — approved source-derived fixture    | Three real historical Projects, eight supported components of local case; 10 monitors/specs/13 media                                                       | [Projects media](review/projects-media-sources.json), [monitor facts](review/equipment-product-sources.json), [monitor media](review/equipment-media-sources.json); retain provenance, not automatic KORSAC publication |
| A → B commercial example               | Monitor retail snapshots incl. 22 050 ₽                                                                                                                    | Source-derived amount visibly “Цена — пример”; replacement by backend price/Offer/availability mandatory                                                                                                                |
| B — approved authored synthetic review | PLAY prices 179 900 ₽ and option deltas; other scenario GPU/RAM/SSD labels; CONFIG 01/02; same-price PCs; static arithmetic                                | Design/positioning fixtures, not validated compatibility/final SKU/configuration or pricing engine                                                                                                                      |
| B — synthetic transaction/account      | DEMO-4101/4102, dates/statuses/payments/delivery context, synthetic inquiry IDs, empty auth fields                                                         | [Account ledger](review/account-fixture-v1.json); no existing customer/order/session claims                                                                                                                             |
| B — synthetic physical System          | KS-2610-0012/13/14, future-order 15/16, authored token in internal review, actual-component example, transfer/warranty snapshots, staff/account history    | [System ledger](review/system-passport-fixture.json); no real generated IDs, code or QR; no frontend coupling                                                                                                           |
| C — future backend field               | Live price/stock/order properties/methods, immutable Order snapshots, actual installed parts, saved warranty, public state/current association/support ACL | Bitrix Catalog/Sale/User plus custom KORSAC D7, not browser inference                                                                                                                                                   |
| D — future/deferred                    | CREATE/WORK models, approved slugs/hostname/legal/Contacts values, live measurement results and galleries requiring real media                             | Omit unconfirmed claims; publication/deployment gates apply                                                                                                                                                             |

No fake availability, FPS/render benchmarks, certifications, clients, reviews or
SLAs are introduced. Contact slots remain unfilled rather than inventing data.
Cart ordinary monitor does not become a System merely because ordered with PCs.

All **23 original source images** (10 Projects + 13 Equipment) match ledger
SHA-256 and byte count; decoded dimensions/HTML media associations are checked
in browser/media QA. Sources were verified at their recorded retrieval dates,
not re-scraped in this audit; live commercial availability is not established.
Local media/no hotlinks; explicit dimensions, appropriate informative/decorative
alt, eager primary/lazy secondary loading remain. PC media is a labelled schema,
not a misleading real photograph. No picture/image is edited/generated here.

## Dead stale links audit

**FIXED / PASS.** All local HTML files/resources/fragments resolve; document
links and CSS media paths are checked. Feature-branch GitHub document links in
review hub now use `main`, and the new final report is discoverable from README
and review materials. No `product.html#product-passport`, internal public link,
private SEO footer route or imaginary future page is exposed.

External King-Komp originals remain intentional source/review destinations.
No external catalog is claimed as local KORSAC commercial functionality. Stored
source evidence is retained; this is not a guarantee that every external URL
will remain permanently reachable. Production links need real published entities.

## Documentation consistency audit

**FIXED / PASS.** IA now includes the full Account subtree and Passport locator,
links the one complete mapping table and makes Passport canonical omission
explicit. SEO counts/page contracts are current. Commerce/Equipment descriptions
match the three-line source fixture. Shell/brand docs reflect actual Account
utilities and all 11 public Intro participants. Product/Commerce/Account/System
owners all state the three distinct configuration snapshots.

Older art-direction/static docs retain historical motion evidence with explicit
current-domain precedence. Product example wording no longer implies missing
identity content or generated Passport; warranty default differs from still
unapproved legal delivery/service terms. Admin preparation description includes
both credentials, idempotency and commit-before-print. Current review entry
points use stable repository paths. No settled IA decision is reopened.

## Bitrix migration ownership matrix

“Custom template” means KORSAC presentation for a standard component; it is not
a separate account/order datastore. D7 column identifies required application/
domain ownership, without deciding ORM/HL/iblock schema inside this audit.

| Feature / data                    | Frontend template                               | Bitrix standard                                               | Custom D7                                                       | Data source                                        | Indexability                   | Notes                                                                  |
| --------------------------------- | ----------------------------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------- | -------------------------------------------------- | ------------------------------ | ---------------------------------------------------------------------- |
| Home/shell/contact globals        | KORSAC SSR/header/footer/include areas          | Site settings/menu                                            | Page context adapter if needed                                  | Approved content/brand/contact settings            | Public per IA                  | One metadata/contact owner                                             |
| Computer families/hub             | Distinct family landings                        | Content sections/iblock mapping TBD                           | Family resolver/relations if needed                             | Approved editorial entities                        | Conditional publication        | No fake CREATE/WORK models                                             |
| Computer/ordinary Products        | Two distinct detail templates                   | Catalog elements / `bitrix:catalog.element`                   | KORSAC model adapter                                            | Catalog/content/media + Catalog/Sale               | Published indexable            | Different decision models, same sale ownership                         |
| Configurator                      | Native controls/Explorer/manifest               | Catalog/Sale values only                                      | `kk.korsac` validation/configuration identity/snapshot adapter  | Approved options/compatibility/commercial snapshot | Same model entity              | Never copy prototype label-only controller into business logic         |
| Computer pricing                  | Display backend price/errors                    | Catalog/Sale authoritative integration                        | Existing/future `kk.price-update` boundary to resolve           | Approved PC pricing source                         | Offer backend only             | No frontend engine; no automatic ordinary-price reuse                  |
| Projects                          | Archive/narrative/gallery template              | Content entity/iblock TBD                                     | Editorial relation adapter if needed                            | Real projects/provenance/media                     | Published indexable            | Historical case ≠ Product/Offer                                        |
| Equipment/category                | Curated hub/family placements                   | Catalog/category/entity mapping                               | Editorial recommendation adapter if needed                      | Real products + many-to-many editorial links       | Published indexable            | One entity/URL; no supplier catalog dump                               |
| Media                             | Local meaningful galleries/base images          | File/media persistence                                        | Source/order/projection adapters if needed                      | Approved originals/manifests                       | Entity context                 | Shared viewer decision DEFERRED                                        |
| Cart                              | Custom standard-component template              | `bitrix:sale.basket.basket`                                   | Config identity/edit validation adapter                         | Sale basket + computer metadata                    | noindex                        | SYSTEM commerce discriminator ≠ physical System                        |
| Checkout                          | KORSAC single-page template/wrapper             | `bitrix:sale.order.ajax`, Sale delivery/payment/properties    | Verified guest/new-account orchestration as required            | Sale order context                                 | noindex                        | Frontend never owns restrictions                                       |
| Success                           | Authorized result template                      | Sale order result                                             | Safe account continuation adapter                               | Real authorized order/payment result               | noindex                        | No trusting URL “success” alone                                        |
| Orders/list/detail                | Custom component templates                      | `bitrix:sale.personal.order.list/detail`                      | Authorized System relation projection                           | Sale immutable purchase snapshots                  | noindex/private                | Ownership transfer grants no prior-owner Order                         |
| Login                             | Custom component template                       | `bitrix:system.auth.form`                                     | Only integration where needed                                   | Standard Bitrix User/session                       | noindex                        | No custom credential datastore                                         |
| Registration                      | Custom component template                       | `bitrix:main.register`                                        | Normalized Email/LOGIN contract if needed                       | Standard User                                      | noindex                        | Email mandatory; phone contact only                                    |
| Recovery/setup                    | Custom component template                       | `bitrix:system.auth.forgotpasswd`, protected setup/reset flow | Safe checkout continuation adapter                              | Standard User/auth                                 | noindex                        | No plaintext password mail; verify version-specific setup component    |
| Profile                           | Custom component template                       | `bitrix:main.profile`                                         | Verified EMAIL+LOGIN update as required                         | Current authenticated User                         | noindex/private                | Atomic/authorized consistency                                          |
| Account entry/nav                 | Utility/private shell                           | Optional personal.section-style composition                   | Context/return authorization                                    | Current session/resource context                   | noindex/private                | No dashboard/custom order-user store                                   |
| My Systems                        | Custom authorized component/template            | Standard auth only                                            | Current USER_ID query + allowed DTO                             | KORSAC System domain                               | noindex/private                | Standard Sale components do not solve this                             |
| System                            | No public edit UI                               | Sale event/order relation; Bitrix Admin host                  | Unit creation/identity/lifecycle/reconciliation                 | KORSAC persistence TBD                             | Admin only                     | Independent of User/Product                                            |
| System components                 | Public name summary; Admin forms                | Admin framework                                               | Actual slots/SN/history/confirmation                            | Confirmed physical records                         | Public only allowed projection | Never current configurator labels                                      |
| Passport/QR/label                 | Active/pending service template                 | Routing/HTTP integration                                      | Token resolution/projection/prepare/activate/privileged label   | System/confirmed parts/snapshots                   | noindex/no sitemap             | No public directory/search; SECRET_CODE never public                   |
| Warranty                          | Display saved snapshot                          | Settings/admin framework                                      | First-handoff snapshot/legal arithmetic/correction              | Applied 24/+12 defaults + saved result             | Projection only                | No frontend date calculation or repair extension                       |
| Ownership requests/history/unlink | Account input/confirmation; Admin Ownership tab | Auth/admin permissions                                        | Verify/rate limit/request/manual approval/atomic change/history | System + requester context                         | Private/admin only             | Less-than-7-day warning, no automatic takeover                         |
| Service events                    | Admin forms/history                             | Admin framework                                               | Maintenance/upgrade/repair/ADD/REPLACE/REMOVE/correction        | Actual System records/audit                        | Admin only v1                  | Not a public custom app                                                |
| Inquiries                         | Public input; private own list; Admin review    | Auth/admin/notifications integration TBD                      | Context/ACL/spam/rate limit/retention                           | SystemInquiry + verified requester relation        | noindex/private                | Old owner conversation never inherited                                 |
| Statuses/settings                 | Admin management                                | Bitrix Admin framework/Sale status references                 | Domain directories/permissions/event mappings                   | Authorized module settings                         | Admin only                     | No localized-status-string frontend business logic                     |
| Errors/SEO                        | Resilient SSR/error templates/page head         | Router/HTTP/metadata integration                              | Entity page-context resolver if needed                          | Published entities + response state                | IA policy                      | Root/server-resolved error assets/links independent of requested depth |

## Blocking issues fixed in this PR

No unresolved **prototype BLOCKER** remains. These concrete contradictions were
fixed without adding product functionality:

| Issue                   | Before → after                                                                                           | Status |
| ----------------------- | -------------------------------------------------------------------------------------------------------- | ------ |
| Mobile Account utility  | Drawer placeholder → native Login, matching header; scope copy no longer calls Account a missing concept | FIXED  |
| Mixed commerce source   | Checkout two PCs/359 800 vs Cart/Success mixed/381 850 → same three-line source summary                  | FIXED  |
| Product continuation    | “Добавить” scope dialog dead end → honest example-Cart native link, no state transfer claim              | FIXED  |
| Warranty wording        | Default described as unknown → approved 24/+12 from handoff; legal terms still pending                   | FIXED  |
| Admin preparation copy  | Token-only summary → token + private code if absent, reuse and commit-before-print                       | FIXED  |
| Stale docs/review URLs  | Old stage counts/shell/commerce language, feature branches → aligned contracts/stable main links         | FIXED  |
| Missing holistic guards | Partial page-type checks → full structural schema/crumb/menu/route/privacy/mixed-source/media audit      | FIXED  |

## Deferred issues

Implementation-only portions of all journeys are explicitly owned in the matrix.
They are not silently treated as working or solved with browser fixtures. The
remaining backend decisions and optional enhancements are separated below.
No new families/products/equipment/private sections/filters/search/viewer or
real commerce/auth/System operations are added by this audit.

## Migration readiness

Overall: **READY — for architecture/migration planning**. Production deployment
and backend implementation remain gated by the integration decisions below.

| Area          | Verdict                                                                                            |
| ------------- | -------------------------------------------------------------------------------------------------- |
| Public UX     | PASS within static review scope; published CREATE/WORK/model readiness remains conditional         |
| Commerce      | PASS source/journey/ownership contract; no live basket/order/payment implementation                |
| System domain | PASS invariants, lifecycle and admin/public separation; backend transactions not implemented       |
| Account       | PASS static/auth/private UX and server ownership contract; no real authentication                  |
| SEO           | PASS staging/schema/route policy; approved production host/HTTP/output still required              |
| Privacy       | PASS authored projections/negative guards; real ACL/cache/security requires server implementation  |
| Accessibility | PASS tested Chromium/layout/Axe/keyboard/no-JS/reduced scope; human/target-browser review required |
| Documentation | PASS current precedence, mapping, source provenance and migration ownership                        |

## Remaining migration-design decisions

These are **BLOCKER FOR MIGRATION DESIGN / implementation gates**, not unresolved
frontend contradictions or feature requests. Planning can now assign them to
their authoritative owners; do not start backend implementation by guessing.

| Decision before affected implementation                      | Owner / required outcome                                                                                                                                        |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Production hostname/router/canonical/redirect/error handling | Deployment + SEO; one origin, real error statuses, root-absolute/server-resolved error assets/Home/Contacts, 503 retry original URL                             |
| Catalog/family/project/monitor storage and publication       | Bitrix architecture/editorial; exact iblock/HL/ORM responsibilities, real slugs/data feed mapping, publication gates and Project source                         |
| PC options/configuration/pricing integration                 | Catalog + KORSAC module; identity, compatibility, authoritative price adapter and immutable Sale snapshot                                                       |
| Sale status codes / System event mappings                    | Sale + production operations; exact creation/ready/handoff conditions, never buyer/status-label inference                                                       |
| Guest/new/existing-email/account setup                       | Auth/Sale security; verified existing account flow, standard setup/reset/component version, transactional account/order linkage                                 |
| System ORM/unit key/sequence/token/credential preparation    | D7/security; unique constraints, locks/idempotency/cancellation/reconciliation, monthly timezone/overflow, CSPRNG allocation                                    |
| SECRET_CODE storage/verification/printing/recovery           | Security/operations; protected storage, rate limits, constant safe responses, no logs/raw request-review code, audited privileged reissue and replacement label |
| QR URL/generation/cache/storage/label pipeline               | D7/production operations; committed preparation only, safe approved URL, same immutable PUBLIC_ID/code on normal regeneration                                   |
| Warranty end-date legal arithmetic/transfer evidence         | Legal + D7/operations; calendar/inclusive policy, confirmed handoff snapshot and audited correction                                                             |
| Module permissions/admin IA/audit                            | Bitrix architecture/security; Systems / Ownership Requests / Inquiries / Statuses / Settings; Main / Components / Passport / Service / Ownership / History tabs |
| Support requester relation/ACL/retention/notifications       | Security/support; public contact inquiry vs authenticated own conversation, no prior-owner disclosure, spam/rate limits                                         |
| Private resource/cache/session/CSRF protection               | Bitrix/security; enforce orders/current systems/inquiries/profile independently, safe return handling, no caching another customer's data                       |
| Final contact/legal/commercial values                        | Business/legal/content + Sale; approved contacts/terms/real stock/payment/delivery context before publication                                                   |

No real Bitrix module, schema, deployment/sitemap/robots, generator, email or
backend auth/commerce implementation is part of this PR.

## Deferred product enhancements

- Shared **site-wide Media Viewer/lightbox**, candidate Fancybox: **DEFERRED TO
  LATER IMPLEMENTATION / PRE-PRODUCTION DECISION**. Applies to Projects, PC
  Product media, Equipment and other galleries; base media stays usable without
  JS. No library is installed/selected by this audit.
- Additional approved equipment categories/real family model content.
- Future public service-history projection, subject to separate privacy scope.
- B2B organization Accounts (current optional company context is not organization hierarchy).
- Future search and other separately approved capabilities; no wishlist,
  loyalty/reviews/ratings/analytics/CRM/feed or marketplace feature is implied.

Human visual **and architecture** review is required before merge. Do not auto-merge.
