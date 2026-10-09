# Computer Families v1 — review

Этот отчёт фиксирует PR #10. Current Projects stage / audit / navigation evidence:
[Projects v1](projects-v1.md). Прежние PNG остаются историческим baseline.

Base: merged PR #9, `main` at `148c901befb8214f49f9307fbb6cdc90971da7c5`.
[Architecture / static mapping / publication boundary](../KORSAC-COMPUTER-FAMILIES-EXPERIENCE.md).
[Authoritative production indexability matrix](../KORSAC-INFORMATION-ARCHITECTURE.md#единая-матрица-production-indexability)
сохраняет условную публикацию CREATE/WORK. Review landing не утверждает
коммерческую модельную линейку или production launch.

## Review assets

Все family PNG — настоящие full-page Chromium screenshots: desktop1440px,
mobile375px. Они сняты в reduced mode после settle, без overlay; full content
и native routes сохраняются в normal/no-JS. Отдельного нового motion sequence
нет; Brand Intro переиспользует прежнюю timeline, MP4 не требуется.

- [Computers hub — desktop](computers-hub-v1-desktop.png), 1440×2807.
- [Computers hub — mobile](computers-hub-v1-mobile.png), 375×3726.
- [CREATE — desktop](create-family-v1-desktop.png), 1440×3579.
- [CREATE — mobile](create-family-v1-mobile.png), 375×5304.
- [WORK — desktop](work-family-v1-desktop.png), 1440×3189.
- [WORK — mobile](work-family-v1-mobile.png), 375×4934.
- [Homepage family links + сохранённый compact PLAY discovery](homepage-family-links-v1.png), 1440×950.

Hub: быстрые три маршрута + разные decision summaries, без второго catalog
navigator. CREATE: process map и workload questions. WORK: work-context brief,
operational priorities и handoff в CREATE. Заголовки, rails и open sections
используют общую identity, но читаются в разном порядке.

## Local SEO audit

```sh
python3 tools/seo_audit.py
python3 tools/seo_audit.py --json
python3 -m unittest discover -s tools -p 'test_seo_audit.py'
```

Результат: **15 pages, 0 errors, 37 intentional warnings; 11 tests PASS**.
[Детерминированный JSON output](seo-audit-v1.json),
[полный перечень detected types](seo-foundation-v1.md#аудит).
Hub/Catalog/CREATE/WORK — CollectionPage + BreadcrumbList; ни одна family
landing не содержит Product/Offer/Review/AggregateRating. Images имеют alt/
dimensions; один H1, unique metadata и global staging noindex сохранены.

Warnings: 15 × prototype canonical/og:url omitted, 15 × no approved og:image,
7 × relative schema URLs/IDs. Production hostname не выдуман. Новый тест
проверяет family schema type, а также auto-discovery и действующие guards на
новых страницах. Старые tests не ослаблены. Visible crumbs и schema одинаковы,
все non-final item URL указывают на существующие static ancestors.
Audit не заменяет внешние validators/production SEO acceptance.

## Browser QA

Chromium HTTP: **15 pages × 8 widths = 120 layouts** —
320/375/430/768/1024/1280/1440/1920. Zero horizontal overflow, duplicate IDs,
console/request errors и external runtime requests. Нет fixed-height clipping
content; страницы полностью читаются обычной прокруткой. Новые family primary
CTA и три hub routes находятся внутри первого800px mobile viewport.

Проверены Home → Computers → PLAY → Product → PLAY → Computers;
Homepage primary/final CTA→hub и CREATE/WORK; family switcher в PLAY; sidebar/native fallback меню;
visible breadcrumb names/order/href совпадают с JSON-LD и дают HTTP200.
Без JS hub/family routes, headings, критерии выбора и mobile navigation доступны.
Native in-page CTA/skip link не скрываются sticky header; keyboard Tab/focus,
drawer containment/Escape/opener return прошли. Прямой `file://` browser test
заблокирован managed Chromium policy (`ERR_BLOCKED_BY_ADMINISTRATOR`), поэтому
не заявлен как passed. Relative local resources проверены audit/HTML checker;
HTTP/no-JS navigation прошла. Отдельный обычный local-browser file review остаётся
непроверенным в этой среде.

Axe WCAG2A/AA + 2.1AA: **0 violations in 9 family states**
(Computers/CREATE/WORK на320/375/1440). Дополнительно commerce/UI suite:
**0 violations in 16 states**, включая company/validation/pickup/empty/drawer.
Некоторые checks incomplete; полного screen-reader audit/physical-device test
нет. Firefox/Safari в среде не проверены.

Existing browser regressions прошли: Homepage compact controller/discovery/
native dialogs/drawer/no-JS/normal+reduced hero; Catalog five-model source/
scenario ladder/MINI/compare bounds/scoped UIKit/rapid input/reduced/no-JS;
Product Explorer/PrevNext/configurator/stable stage/static pricing;
Cart quantity/remove/restore/empty/reset; guest+B2B Checkout independent payment
selection/validation/delivery-dialog/no-JS/static Success без передачи PII.
Header18 baseline layouts: home16px top state, opaque internal, hash/reload/
restoration, no header CLS и dialogs/drawer top layer. Generic/error pages входят
в120 layouts, app/error CSS/JS семантика не менялась.

## Brand Intro / motion

Baseline Brand Intro daily/expiry/storage-denial/delayed CSS/no-JS/initial+live
reduced/eight-width regressions прошли. Новые direct entry Computers/CREATE/WORK
играют тот же1500ms intro, имеют разрешённые local SVG IDs/references и общий
24h key с Home/Catalog/Product. Навигация между шестью browsing routes/reload
не replay. Initial reduced: intro skipped + timestamp; live normal→reduce:
cleanup; возвращение no-preference не replay. Contacts/Cart/Checkout/Success/
errors остаются исключёнными. Existing application JS и SVG masters/derivatives
не менялись; новая family page-entry timeline не создана.

HTML nesting/labels/IDs/local resources+fragments и documentation links прошли,
все PNG decoded, `git diff --check` — PASS. Старые PNG/MP4 остальных stage
сохраняются как исторические baselines; их footer/menu могут показывать прежний
набор routes. Этот stage не переснимает прежние motion sequences.

Human visual review остаётся обязательным: читаются ли family choices быстро,
отличаются ли decision models, понятна ли граница модельных линеек. Не сливать
автоматически. Projects — следующий stage; Bitrix migration не реализована.
