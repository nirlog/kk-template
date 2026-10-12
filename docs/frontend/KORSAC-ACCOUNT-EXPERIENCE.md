# KORSAC — Account Experience v1

Base: merged PR #14, `main` at `eaa071fc2b1bc37ea63b610f3dad081040ca030f`.
Static review and future production integration contract only. There is no
Bitrix/PHP implementation, session, auth, email, ownership verification or persistence.

## Scope and utility hierarchy

Eight review pages cover Registration, Login, Recovery, Orders, Order detail,
My Systems, My Inquiries and Profile. There is no account.html dashboard,
statistics, recommendations or marketplace widgets. Authenticated `/account/`
resolves to Orders. The private navigation has exactly Заказы / Мои системы /
Мои обращения / Профиль, with a separate Выйти utility. Logout in review only
acknowledges the concept; it creates/deletes no session or cookie.

The compact shell uses local KORSAC identity, one H1, skip link and native links.
There is no Brand Intro, eligibility write, commercial hero or page-entry
sequence. Mobile account navigation is a readable two-column set of four links,
not a JavaScript-only menu. Existing public shell Account utility now links to
Login and remains separate from its five primary entries. Public Passport
support still works without an Account.
In production, the server renders «Войти» for guests and «Личный кабинет»
linking to Orders for authenticated users. The prototype always uses the Login
utility; no browser storage simulates global authentication.

## Routes and Bitrix components

| Static review                | Production route          | Integration owner                            |
| ---------------------------- | ------------------------- | -------------------------------------------- |
| account-login.html           | /account/login/           | bitrix:system.auth.form                      |
| account-register.html        | /account/register/        | bitrix:main.register                         |
| account-forgot-password.html | /account/forgot-password/ | bitrix:system.auth.forgotpasswd              |
| account-orders.html          | /account/orders/          | bitrix:sale.personal.order.list              |
| account-order.html           | /account/orders/{id}/     | bitrix:sale.personal.order.detail            |
| account-systems.html         | /account/systems/         | KORSAC D7 System module / custom integration |
| account-inquiries.html       | /account/inquiries/       | SystemInquiry / custom integration           |
| account-profile.html         | /account/profile/         | bitrix:main.profile                          |

Prefer normal Bitrix authentication/User/Sale infrastructure and suitable standard
components with KORSAC custom templates. A sale.personal.section-style composition
may group routes, but its stock layout must not dictate UX. Do not duplicate users
in a custom KORSAC account table or Sale orders in a parallel account datastore.
System queries/ownership requests and inquiries require module integration;
no PHP components, ORM or data storage are implemented here.

Unauthenticated production protected-route access redirects to Login, preserving
a **safe intended return path**. Backend accepts only normalized origin-relative
paths belonging to the approved Account route allowlist; reject protocols,
external origins, protocol-relative `//`, backslashes, encoded separator bypasses
and header/control-character injection. Prefer deriving return context from the
actual requested private route. Re-check order/System permissions after login;
a safe path does not grant access. Reject invalid return paths and default to
Orders. The prototype ignores URL/query return parameters and does not imitate
authentication or redirects; all navigation is fixed native links.

## Email = LOGIN

One visible identity field: Email. Required in registration and checkout;
normalized email is Bitrix LOGIN. Phone is contact data, never login. Consistent
backend normalization across registration/login/checkout/profile uses conservative
trim + canonical lowercase; preserve contact/display representation where needed.
No provider-specific Gmail dots/plus stripping. Backend uniqueness, races and
verification apply centrally; browser string equality does not establish identity.
There is no independent username/LOGIN input.

Registration requires Email, Password and confirmation. Name/Phone are optional
contact fields. Email autocomplete=email; both password fields=new-password.
There is no SMS, phone/social login or loyalty enrollment. Review checks required
fields, email format and password equality; password policy belongs to Bitrix
security configuration, with no invented length/complexity rules.

Login uses type=email/autocomplete=username and password/current-password.
Remember me is a presentation checkbox only. The review form reports that login
was not performed and no session was created. Passwords are never prefilled,
stored, sent or echoed; successful presentation validation clears password fields.
No global authentication state is simulated in localStorage or elsewhere.

Recovery asks only Email (no username/phone/System/order). Standard Bitrix recovery
with a KORSAC template must use enumeration-safe wording: «Если аккаунт с таким
email существует, инструкции будут отправлены». Apply consistent status/timing
and standard abuse controls on the backend without publicly confirming existence.
Review returns the same generic response, explicitly noting no email was sent.

## Checkout and automatic account continuation

Checkout stays available to guests; no pre-registration requirement or registration
checkbox is added. Email remains required; short copy explains order/account use.
Authenticated checkout uses current authenticated USER_ID. A new guest email creates
a Bitrix User with normalized LOGIN and attaches Order.USER_ID. A guest email already
belonging to an account **must not silently attach the order**: require a safe
login/email-verification flow first. Bitrix/Sale owns properties and availability;
frontend does not invent payment/delivery or buyer-type restrictions.

A checkout-created user establishes a password through protected normal setup/
recovery, never an emailed plaintext generated password. Static Success demonstrates
future new-user continuation with «Установить пароль» → Recovery, while clearly
stating no real account/email was created. A native alternate explanation shows
«Заказ доступен в личном кабинете» for an already-authenticated customer. These
are authored review states, not status inferred in JS. No entered checkout contact
is copied into Success, a URL or storage. Success remains a static source-order
sample, not the result of browser-auth or basket backend integration.

## Orders and access ownership

Sale owns order number/date/status, lines, quantities, immutable ordered configuration,
saved purchase prices, payment/delivery and access. UI renders backend values without
business logic around localized Russian status names. The one detail fixture preserves
two ordered PC configurations and an ordinary monitor with static saved demo prices.
No reorder, cancel, return, invoice download or unapproved backend actions.

Production must authorize the requested order against the authenticated account and
Bitrix permissions; knowing `/account/orders/1847/` grants nothing. Current ownership
of a physical System does not grant its previous owner's Sale order or private contacts.
Order relations and System account association are separate. Related System human
IDs may appear as an authorized order projection, but never internal DB IDs, serials,
credentials, ownership/service history or staff/supplier data. Before handoff, Systems
can exist with NULL current USER_ID and no public Passport. Once the backend supplies
an allowed public locator, link the same public Passport; do not manufacture a token
or link to an unrelated fixture merely to provide a button.

## My Systems and public Passport

Production selection is exactly `System.USER_ID = CurrentAuthenticatedUser.ID`.
Never infer current association from historical Order.USER_ID, email, PUBLIC_ID,
human SYSTEM_ID alone or secret alone. Server supplies the authenticated identity;
no hidden/browser USER_ID is trusted. The compact card shows model snapshot, human
SYSTEM ID, transfer/warranty snapshot and short current KORSAC-confirmed configuration.
No S/N, secret, former owner, staff notes, component/service or ownership history.

«Открыть паспорт» leads to the **same** public `/passport/{PUBLIC_ID}/` entity,
not a private duplicate. Account provides navigation only. The authorized card's
«Задать вопрос» goes to that public System inquiry context without requiring login.
The static route uses existing passport.html and its native inquiry fallback.

## Add System and pending request

Add System has exactly ID системы and Код системы, with a single empty text code
input, numeric-friendly input mode, autocomplete off and human ####-#### format.
Eight digits without the hyphen are also accepted for mobile numeric keyboards;
future backend normalizes display separators before secure verification.
There is one DOM form; progressive enhancement moves it into a native dialog, rather
than cloning sensitive fields. No-JS exposes it in a native disclosure. Code remains
only while the user types: it is cleared after presentation validation and on dialog
close. It never reaches URLs, hidden fields, status messages, logs or storage.

Future flow: authenticated requester → submitted ID/code → secure server verification/
rate limiting → SystemOwnershipRequest PENDING → manual manager APPROVED/REJECTED.
Only approval changes USER_ID. Verification is evidence, not automatic transfer.
Backend prevents duplicate active requests for the same requester + System; do not
encode that business rule in JS. Do not disclose current owner or even System
existence before safely verifying the request context. Generic invalid-pair feedback:
«Не удалось подтвердить данные системы. Проверьте ID и код».

Review validates format/requiredness only and explicitly reports **no verification,
request creation or attachment**. A separate authored pending card for KS-2610-0014
says «На проверке» and explains manager review. It is not part of the associated
Systems list and not My Inquiries. OwnershipRequest and SystemInquiry remain separate.
Manager verification evidence/history/request processing belong to Bitrix Admin,
with its separate Ownership tab; no manager fields appear in customer Account.

## Unlink and immutable physical identity

Confirmation names the exact machine:
«Вы уверены, что хотите отвязать систему KS-2610-0012 от своего аккаунта?»
Supporting copy: «Система исчезнет из раздела «Мои системы». Публичный паспорт,
гарантия и история компьютера сохранятся».

Future backend authorizes current user, locks/re-checks System.USER_ID, sets NULL
and atomically appends SystemOwnershipHistory SOURCE=USER_UNLINK. Repeated/stale
requests cannot unlink a later owner or append duplicate history. Preserve SYSTEM_ID,
PUBLIC_ID, SECRET_CODE, Passport state/URL, transfer date, warranty, components and
service history. Nullable association supports resale and future B2B contexts;
registration is not required for System existence. No multi-user company hierarchy
is implemented. Review confirmation gives non-execution feedback and never removes
or rewrites the card/request/history, including after reload.

The [System contract](KORSAC-SYSTEM-PASSPORT.md) remains authoritative: initial code
allocation belongs to successful preparation with first PUBLIC_ID, all ordinary
operations reuse it, and only explicit privileged audited regeneration may replace
it. Account implements no generator, preparation/activation or ownership processor.

## Inquiries and private conversation access

My Inquiries renders SystemInquiry/support records, with configurable topics
Гарантия / Техническая поддержка / Апгрейд / Обслуживание / Комплектующие / Другое.
Statuses are backend/configuration-owned, no SLA is promised. Two synthetic examples
use native expandable context, without a new ticketing/detail-route application.
New inquiry navigation is contextual to the currently associated System.

Backend resolves System server-side (public locator where appropriate), never trusts
browser internal SYSTEM_ID. Account visibility requires an authorized requester/
account relationship and appropriate System access policy. Do not expose previous
owners' private conversations simply because current System.USER_ID changed, or use
matching anonymous inquiry contact email as proof of access. Future integration may
need an authenticated requester relation/ACL on SystemInquiry; public anonymous
support remains available. Frontend composes the permitted projection, not raw staff
comments, service records or contact identities. No inquiry backend is implemented.

## Profile and controlled identity change

Profile presents optional name/phone and required Email, plus current/new/confirmed
password fields with current-password/new-password autocomplete. Review fields start
empty, no real person or default credentials. Password policy/current-password check
are backend responsibilities. Feedback explicitly says nothing was updated.

Production email change validates format, uniqueness and approved verification/
security flow, then updates EMAIL + normalized LOGIN through **one controlled backend
operation**. Keep verified old identity until safe completion; do not leave EMAIL=new
and LOGIN=old as a lasting state. The frontend must not submit an independently
editable LOGIN, bypass verification or mutate identity locally.

## Data owners and authorization

Bitrix User owns auth/email-login/name/phone/password/security. Sale owns orders/
lines/saved prices/payment/delivery/access. KORSAC D7 owns physical Systems, nullable
USER_ID, ownership requests, inquiries and confirmed Passport/warranty/component/
service domain. Account composes those projections without new user/order storage.
Private routes require authentication, server access checks and normal CSRF/security
controls. Profile is the current authenticated user only; My Systems is current
association only; order and inquiry access are authorized independently. Neither
URL IDs nor hidden USER_ID grant permissions. Admin stays a disposable review-only
wireframe, absent from customer navigation.

## SEO, privacy and JavaScript boundary

All eight review pages: noindex, nofollow, noarchive; one H1; unique generic title,
description and OG metadata; no canonical, og:url or JSON-LD of any type.
Production auth/private pages remain noindex, excluded from sitemap, without a
required public canonical. Staging noindex is not access control. No real email,
phone, password, token/session ID or private System/admin data is committed.
A code input is the only user-entry exception, not a persisted/default code value.
Private routes do not enter public footer SEO or primary marketing navigation.

Account JS performs presentation validation, native-dialog enhancement and explicit
review acknowledgements only. No fetch/API, authentication, cookie writes, persistent
storage, code generation, server lookup, ownership, unlink or profile mutation.
It never creates a successful auth/session/account/order outcome. All forms use
non-submitting method=dialog and type=button actions; submit listeners prevent default.
No-JS keeps routes, fields and explanatory fallbacks but executes no saving action.

## Fixture and review decisions

[Ledger](review/account-fixture-v1.json): Account B matches the approved current
association of KS-2610-0012 after the 09.10 manager transfer. Its original Order A
belongs to another user and is not shown. Account B has a completed ordinary-monitor
order and a current mixed order (two PLAY snapshots + monitor), using existing static
179900/22050 RUB sample prices. Untransferred new Systems 0015/0016 belong to the
current order; they are not the associated 0012 and have no fabricated Passport links.
This deliberately separates current association from historical order access.

Pending request 0014 belongs to this requester and is separate from the internal
Admin fixture's pending 0012 request by User C. Support examples belong to the current
Account context. There is no real customer/order/sold-machine claim or new model/SKU.
All prior ownership/identifier/warranty/component rules remain.

Review at 320/375/430/768/1024/1280/1440/1920; cards and semantic lists replace wide
mobile tables. Long field values and product names wrap without fixed-height clipping.
Labels, native input types/autocomplete, focus-visible, textual errors and aria-current
remain. Shared native dialogs provide Escape, focus containment/return and existing
finite/reduced opacity feedback; no new animation system or MP4 is needed.
See [validation/screenshots](review/account-experience-v1.md). Human visual and
architecture review is required before merge. Do not auto-merge.
