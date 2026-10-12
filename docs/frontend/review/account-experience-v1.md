# Account Experience v1 — review

Base: merged System ownership PR #14, `main` at `eaa071fc2b1bc37ea63b610f3dad081040ca030f`.
[Account / Bitrix / authorization contract](../KORSAC-ACCOUNT-EXPERIENCE.md) ·
[Synthetic fixture ledger](account-fixture-v1.json).

## Implemented boundary

Eight auth/private review pages, no standalone dashboard or marketplace widgets.
Orders is the authenticated landing concept; four native account sections and
separate logout utility. Public Account icon now leads to Login without adding
a sixth primary marketing item. The utility works at narrow mobile widths.
Account/auth pages run no Brand Intro and write no eligibility timestamp.

Forms validate required/type/equality presentation only. No network/API, real
registration/login/recovery/profile mutation, cookie/session, password/code
storage, automatic ownership transfer or unlink. All response wording makes
non-execution explicit. Recovery is enumeration-safe; password fields are empty
at entry and cleared after presentation validation. Remember me is a mock checkbox.
No separate LOGIN/username/phone login, fake password policy or default credentials.

My Systems exposes currently associated KS-2610-0012 with saved transfer/warranty
and confirmed names, linked to the same public Passport. Add System has one empty
user code field, moved into a native dialog rather than cloned. It accepts grouped
or ungrouped eight digits for numeric mobile keyboards and performs no server
verification. Code is cleared on validation/close, never echoed to status or URL.
A pre-authored separate PENDING 0014 request is not an associated System or support
inquiry. Unlink confirmation names the exact System and preserves its fixture.
Manager requests/evidence/ownership history stay only in Bitrix Admin.

Account B is the current association after the approved synthetic transfer.
Its old owner’s Order A is not displayed. A completed monitor-only order and a
current mixed two-PC/monitor order belong to Account B; upcoming Systems 0015/0016
are untransferred and not the already associated 0012. This keeps Sale order access
independent from current physical-machine association. There are no fabricated
Passport links for the upcoming machines. My Inquiries contains two synthetic
support records; no SLA, staff notes or previous-owner conversation is exposed.
Profile shows empty review contact/security fields without real personal data.

Checkout remains guest-accessible, with required Email and short account context.
Success demonstrates a future password setup/recovery path and alternate authenticated
Orders path, without claiming a real account/email. Its static source summary now
includes two PCs plus ordinary monitor (381850 RUB), matching the mixed source order.
Entered checkout data never becomes a URL/account payload. Prices and backend-owned
payment/delivery restrictions remain static/future respectively.

## Actual browser evidence

Twenty actual Chromium PNGs over HTTP, 1440 desktop / 375 mobile, reduced mode.
No generated imagery or real credential values. Code placeholder is a format example;
no code is typed for screenshots. Shared dialog behavior needs no new MP4.

| View                | Desktop                                                       | Mobile                                                     |
| ------------------- | ------------------------------------------------------------- | ---------------------------------------------------------- |
| Login               | [desktop 1440 × 1000](account-login-v1-desktop.png)           | [mobile 375 × 1008](account-login-v1-mobile.png)           |
| Registration        | [desktop 1440 × 1207](account-register-v1-desktop.png)        | [mobile 375 × 1258](account-register-v1-mobile.png)        |
| Password recovery   | [desktop 1440 × 1000](account-forgot-password-v1-desktop.png) | [mobile 375 × 1000](account-forgot-password-v1-mobile.png) |
| Orders              | [desktop 1440 × 1213](account-orders-v1-desktop.png)          | [mobile 375 × 1368](account-orders-v1-mobile.png)          |
| Order detail        | [desktop 1440 × 1524](account-order-v1-desktop.png)           | [mobile 375 × 2189](account-order-v1-mobile.png)           |
| My Systems          | [desktop 1440 × 1404](account-systems-v1-desktop.png)         | [mobile 375 × 1774](account-systems-v1-mobile.png)         |
| Add System dialog   | [desktop 1440 × 1000](account-add-system-v1-desktop.png)      | [mobile 375 × 1000](account-add-system-v1-mobile.png)      |
| Unlink confirmation | [desktop 1440 × 1000](account-unlink-system-v1-desktop.png)   | [mobile 375 × 1000](account-unlink-system-v1-mobile.png)   |
| My Inquiries        | [desktop 1440 × 1075](account-inquiries-v1-desktop.png)       | [mobile 375 × 1262](account-inquiries-v1-mobile.png)       |
| Profile             | [desktop 1440 × 1140](account-profile-v1-desktop.png)         | [mobile 375 × 1826](account-profile-v1-mobile.png)         |

## Deterministic guards and audit

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 tools/seo_audit.py --json
PYTHONDONTWRITEBYTECODE=1 python3 tools/monitor_curation_audit.py
```

**55 tests pass**: 20 SEO, 7 curation, 14 Passport/ownership, 14 Account guards.
SEO/privacy audit: **31 pages, 0 errors, 74 warnings**; repeated JSON matches
[the deterministic report](seo-audit-v1.json). Existing staging canonical/social-art
and 12 relative semantic-ID warnings remain, not production approval.

New guards reject Account structured data, canonical/og:url, Brand Intro,
personal/credential defaults, hidden identity fields, internal System/admin/owner
history, serials, secrets and customer metadata. Auth requires one Email and correct
password/autocomplete contracts; Recovery has only Email. Only the single Add System
code input is permitted. Customer order/System pages cannot expose manager verification
or previous-owner fields. JS cannot store/send credentials or generate codes; forms
are non-submitting. Private routes do not enter public footer SEO or marketing nav.
Unlink names the exact System; fixture ownership/order/sums are coherent.

The previous Passport context-link guard now permits the required contextual links
from My Systems/My Inquiries, retaining global header/footer/drawer restrictions and
all serial/secret/schema/state guards. Product, families, Projects and Equipment tests
remain intact. Monitor curation/media/source ledgers are unchanged. Regex/static checks
do not prove production authorization, privacy DTO completeness, actual Bitrix auth,
backend email synchronization, ownership idempotency or cryptographic verification.

## Browser validation

**248 layouts = 31 pages × eight widths** at
320/375/430/768/1024/1280/1440/1920. No horizontal document overflow, missing H1/noindex,
duplicate IDs or runtime errors. Private mobile navigation remains legible; long
product names, facts and form values fit without wide tables/fixed-height clipping.

**Axe 0 violations in 30 Account states**: eight pages × 320/375/1440 plus Add/Unlink
open at those widths. Some checks are incomplete; results do not replace human
screen-reader/visual review. Two additional updated Add-dialog checks cover numeric-only
code entry at 375/1440. Existing Passport/internal/dialog Axe checks also pass in
12 states.

Keyboard form error focus, email validity, requiredness and password mismatch pass.
Password values clear after mock validation; recovery feedback remains generic.
Add/Unlink native dialogs contain Tab, support Escape and restore opener focus.
Successful format checks do not create a request; code cleanup/absence in messages
pass. Unlink leaves the associated card and pending request unchanged. Logout changes
no auth/session. No private interaction requests or URL payload mutation occur.
Normal/reduced/live preference checks retain full content and clean up spatial dialog
motion; no Brand Intro or eligibility write occurs. An arbitrary external return query
is ignored and native links stay within the fixed review routes.

No-JS at 320: all eight routes, fields and account navigation remain readable;
Add/Unlink native disclosures expose their meaning/input without submission. Enter
in Login or Add fields and action buttons make no request. Existing Passport native
inquiry fallback works after native smooth fragment scrolling settles.

## Regression and limits

Homepage header/scroll/native drawer/dialog/focus, discovery, touch/no-JS and
normal/reduced finite hero pass. Its harness now checks Account as a native Login
route while Search keeps its review dialog; existing feature assertions remain.
PLAY ladder/MINI/preview/comparison, rapid switching, keyboard and live reduce pass.
Product Explorer/configurator, static Passport example independence, rapid 242 actions,
seven widths/touch/UI Kit/no-JS pass. Mixed cart quantity/static totals/remove/restore/
empty/reload/focus pass. Checkout guest/B2B validation, required email/delivery/consent,
payment preservation and non-submitting static Success pass. Projects, Equipment,
Contacts, Errors, public Passport and Bitrix Admin participate in all 248 layouts.

Human visual and architecture review is required. Verify the compact auth/forms,
mobile account navigation, current-vs-historical access distinction, pending request
semantics and public Passport independence. No real auth/authorization, password reset,
email, System lookup/verification, ownership processing/unlink, PHP components or
persistence was implemented or tested. Physical-device keyboards, full screen readers,
Firefox/Safari, file protocol and production HTTP/auth/Bitrix integration were not run.
Do not auto-merge.
