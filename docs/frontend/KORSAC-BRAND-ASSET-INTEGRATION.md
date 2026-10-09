# KORSAC — Brand Asset Integration & Logo Motion v1

## Approved artwork и web mapping

Работа основана на `main` **a46204e1fc30f09ed81183ac9323a73718bb4352**,
после принятой Premium Shell/Homepage PR #6. Исходники в
`prototype/assets/images/` неизменны, включая первоначальные blue eye shapes.
Визуально подтверждены ICON / TEXT / V1 stacked / V2 horizontal.

| Approved source master               | Web derivative в `prototype/assets/images/brand/` | Назначение                              |
| ------------------------------------ | ------------------------------------------------- | --------------------------------------- |
| `KORSAC_LOGO_ICON_FINAL_REVISED.svg` | `korsac-mark.svg`                                 | Static totem, UI Kit                    |
| `KORSAC_LOGO_TEXT_FINAL_REVISED.svg` | `korsac-wordmark.svg`                             | Отдельный wordmark, UI Kit              |
| `KORSAC_LOGO_V2_FINAL_REVISED.svg`   | `korsac-lockup-horizontal.svg`                    | Header, drawer, mobile footer           |
| `KORSAC_LOGO_V1_FINAL_REVISED.svg`   | `korsac-lockup-stacked.svg`                       | Desktop/tablet footer                   |
| `KORSAC_LOGO_ICON_FINAL_REVISED.svg` | `korsac-mark-motion.svg`                          | Eyes-off inline template для intro/demo |

Derivatives убирают XML declaration/DOCTYPE, editor namespaces, физические
mm dimensions и внутренние accessibility labels. Каждый ID и `url(#…)`
получает semantic asset prefix. Внешние dimensions определяет image wrapper;
исходные viewBox/aspect ratio сохраняются. Eye groups имеют `opacity="0"`.
Неиспользуемые source CSS rules убраны; static derivatives не содержат glow
filter. Motion template сохраняет оригинальный localized filter.

Path/polygon/rect, stroke attributes, clip paths, gradient coordinates и
stops сверены с masters. Геометрия букв, facets и eyes не менялась; palette
не перекрашена, CSS color filters не применяются. SVG остаются небольшими
(примерно 6–15 KB); prefix isolation важнее минимизации каждого байта.
Master files проверены byte-for-byte относительно base commit.

## Shell и scale

Header/drawer: external V2, **164 px desktop / 140 px mobile**. Height header
сохранилась: **88 / 64 px**. SVG помещается в прежний lockup hook
`data-brand-wordmark`; пустой totem slot больше не нужен. Horizontal artwork
показывает и mark, и wordmark, включая 320 px рядом с Cart/Menu 44×44.
Header logo статичен: нет hover replay, eye effect или metallic animation.

Footer: тот же home link содержит один responsive `<picture>`. Desktop/tablet
использует V1 шириной **224 px**, mobile до 600 px — V2 шириной **200 px**.
Слоган и существующие navigation groups сохранены. Stacked mark делает
завершение сайта более выраженным; horizontal уменьшает mobile height.
Новых decorative rails, borders или footer effects нет.

Header spacing: gap 32 px desktop / 12 px mobile; logo box центрирован в
существующей высоте. Это практическая optical компоновка, не выдуманная
формальная clear-space норма. Известные размеры/aspect ratios резервируются
до image load. `object-fit: contain` предотвращает растяжение/crop.

Проверка 16/24/32 px: на 16 px facets сливаются, на 24/32 silhouette яснее.
Для favicon нужна отдельная утверждённая small-size версия. `data:,`
placeholder оставлен; упрощённый/перерисованный знак не создан. В header,
footer и hero реальные размеры читаются лучше.

## Hero и SVG isolation

Hero добавляет approved ICON отдельным decorative layer за product media.
Width: **320 px на 1280–1920**, **220 px на 1024**, **210 px на tablet**,
**148 px на mobile**; opacity .68. Продукт остаётся foreground, размер схемы
не увеличен. На 1024 mark смещён влево, чтобы контур узнавался рядом с
корпусом. Headline, copy и ранняя mobile CTA сохраняют прежнюю компоновку.
Ambient blue уменьшен до 6%, маленький copper registration — до 18 px.

Static instances, включая Hero, — внешние `<img>`: их defs изолированы браузером.
Каждая browsing public page (Homepage/Catalog/Product) содержит **один** inline intro SVG с собственным prefix:
`intro-index-`, `intro-catalog-`, `intro-product-`. Единственный UI Kit demo
использует `kit-brand-` prefix в другом документе.
Все fragment references переписаны вместе с IDs; source SVG не вставляются
inline без prefix. Inline geometry сверяется с template; новые экземпляры
должны получать собственный prefix. Product/catalog content не изменён.

Inline intro даёт родительской странице прямую отмену WAAPI. External static
SVG остаются обычными локальными URLs. Motion template не содержит autoplay.
Автоматический Hero Eye Flash удалён после live review вместе с coupling
`korsac:hero-enter`; заменяющей hero animation нет.

## Transactional exception — Cart & Checkout v1

`cart.html`, `checkout.html`, `order-success.html` используют статическую approved
identity, **полностью исключены из daily Brand Intro** и не consume/stamp его
eligibility. На них отсутствуют inline intro boot/SVG overlay и intro CSS/JS.
Блокирующая brand activation не участвует в завершении заказа. Policy browsing
Homepage/Catalog/Product сохранена; UI Kit/review по-прежнему исключены.
[Commerce architecture](KORSAC-CART-CHECKOUT-EXPERIENCE.md).

## Shared site-entry Brand Intro

Brand Intro принадлежит shared public shell, не homepage. Только
`index.html`, `catalog.html`, `product.html`; прямой вход в любую страницу
работает одинаково. `ui.html` и `review.html` не показывают intro и не
расходуют eligibility. Hero/Header/Drawer/Footer — static eyes off.

Малый inline head boot читает `korsac:brand-intro:lastShown` и проверяет
`Date.now()`. Intro eligible, если timestamp отсутствует, некорректен или
прошло **24 × 60 × 60 × 1000 ms**. Корректный timestamp — positive safe integer,
не из будущего. Rolling window считается от последнего eligible входа;
navigation/reload не продлевает его. Timestamp записывается **до** установки
`html[data-brand-intro]`, значит следующая tab обычно уже пропускает intro.
Это не распределённый transactional lock.

Policy — **browser/profile-local на том же origin**. Нет backend, cookie,
account sync, cross-device sync или cookie-consent dependency. При отказе
`localStorage` boot использует тот же key в `sessionStorage`; повторные
переходы/reload в tab session не запускают intro. Независимые новые tabs
не обязаны разделять session fallback. Если оба storage API недоступны,
intro пропускается полностью. Business/configuration/cart data не сохраняются.

Reduced Motion при входе **записывает timestamp и сразу открывает страницу**,
без one-frame flash/overlay. Выключение preference позже в том же окне 24h
не вызывает intro. Live Reduced Motion CSS немедленно скрывает active overlay,
controller отменяет effects и удаляет его. Автоматического повторения нет.

Это правило относится к полной brand activation. Остальной UI использует
**reduced-motion mode**, сохраняя opacity/color/border feedback 110–180 ms;
Hero opacity settle не активирует глаза. [Общая motion/accessibility policy](KORSAC-VISUAL-MOTION-DIRECTION.md#reduced-motion-и-отсутствие-js).

## Composition и timing

Полноэкранный graphite, центральный approved ICON, actual SVG eye geometry,
отдельный approved wordmark. На desktop mark 320 px; на mobile — 56vw.
Wordmark — 220–340 px. Header/Footer/Hero sizing не меняется. Intro не содержит
spinner, progress/percent, сообщений, audio, particles или RGB/glitch.

| Фаза                         | Время от начала видимого intro       |
| ---------------------------- | ------------------------------------ |
| Mark resolve                 | 0–220 ms                             |
| Eye activation / peak / fade | 250–950 ms; peak примерно 446–649 ms |
| Wordmark resolve             | 450–850 ms                           |
| Eyes off / settle            | 950–1200 ms                          |
| Overlay exit                 | 1200–1500 ms                         |

Real eye/core polygons и metallic/blue gradients неизменны. Оригинальный
localized filter активен только во время eye phase; opacity достигает 1
на коротком plateau и возвращается к base `opacity="0"`. Full mark opacity
1 обеспечивает заметность в центре. Нет псевдоглаз или full-logo halo.
Timing tokens — в `brand-intro.css`; easing использует существующий token.
Часы последовательности следуют видимому CSS overlay, а не времени download
head resources. Поздний controller догоняет этот clock либо пропускает expired
intro, не растягивая блокировку. Intro — brand presentation, не actual loader.

## Failure safety и interaction

Overlay `hidden` по умолчанию. Только eligible head attribute включает его
через CSS. Boot ограничен timestamp policy / Reduced Motion / атрибутом;
actual motion находится в external `brand-intro.js`. Homepage controller
больше не связан с brand activation. `brand-motion.js` — только UI Kit replay.

Нормальная completion удаляет overlay и attribute на 1500 ms. Независимый
JS watchdog завершает его до 1700 ms при потере finished promises. CSS safety
на 1800 ms скрывает overlay и отключает pointer events даже при missing/broken
controller. Missing CSS оставляет native hidden state; no-JS не включает
head attribute. Unsupported/throwing WAAPI даёт direct page access. Header,
footer и native no-JS content не зависят от intro initialization.

No layout insertion, body scroll lock, inert/focus trap, focus restoration
или scrollTo. Overlay decorative (`aria-hidden`), без focusable content и
aria-live. Существующий keyboard focus/scroll сохраняются при удалении.
После exit страница сразу доступна. Повторная animation не запускается.

UI Kit сохраняет manual **Replay Eye Flash** для review geometry. Его
контроллер отменяет предыдущий запуск, использует generation guard и всегда
завершает eyes off. Reduced/unsupported motion блокирует replay. Public
replay controls отсутствуют; UI Kit не запускает site-entry policy.

## Accessibility

Logo home link имеет единственное имя `KORSAC — главная`; внешнее image —
`alt=""`. Исходные внутренние `role/aria-label` удалены из web derivatives.
Hero image имеет пустой `alt`; intro wrapper/inline SVG декоративны
(`aria-hidden`, `focusable="false"`).
UI Kit static figures имеют осмысленный image alt; demo один `role="img"`
на wrapper и отдельный status для review button. Нет повторного KORSAC
announcement внутри hero или фокусируемых SVG paths.

## Future Bitrix mapping

| Текущая область                  | Будущая интеграция                                     |
| -------------------------------- | ------------------------------------------------------ |
| Header/footer static derivatives | Template asset directory и обычные local SVG URLs      |
| Responsive footer picture        | `header.php` / `footer.php` template markup            |
| Shared entry overlay             | Public template/include, один prefixed SVG template    |
| Eye presentation controller      | Local template JS/CSS с теми же hooks и reduced motion |

Не хранить artwork как PHP strings; approved masters остаются отдельно от
web assets. У каждого будущего inline instance свой prefix. Search/profile/cart
здесь по-прежнему prototype-only, backend и pricing logic не добавлены.

## Validation и review

[Материалы](review/README.md) содержат обновлённые brand PNG, full-viewport
rest/active intro composition и normal-speed first-entry MP4. Chromium HTTP: 40 page/width layouts; native drawer/dialog/anchors;
catalog/scenario/comparison/MAX3; Product v3.1/Explorer/configurator/static
prices; no-JS; finite/reduced motion; 25 быстрых UI Kit replay. Проверены masters,
geometry/gradients/fragments и загрузка logo с задержкой без CLS на
320/768/1440/1920. Daily flow: clear key → direct Catalog intro → Product/Home/
reload/new tab skip → expired timestamp intro. Missing/malformed/future values,
initial/live reduced, local/session denial, both storage unavailable,
missing controller/CSS, lost promises, throwing WAAPI и delayed script/CSS
проверены. Intro layout без overflow на восьми ширинах, focus/scroll не меняются.
Axe WCAG2A/AA+2.1AA: zero violations в 12 состояниях; некоторые contrast/link
checks incomplete, полного screen-reader audit нет.

Firefox и Safari отсутствуют в среде; физические устройства не проверены.
Human acceptance остаётся открытым: узнаваемость, optical scale/clear space,
premium feel и заметность/сдержанность flash в живом браузере. Не сливать
автоматически. Фотография продукта остаётся временной; логотип утверждён.

## Self-review A–L

- A: real metallic identity видна в header, hero и footer.
- B: V2 даёт целый lockup при 164/140 px, помещаясь в прежний header и 320 px mobile.
- C: V1 создаёт выраженный desktop endpoint; V2 компактнее в mobile footer.
- D: static variants сохраняют глаза off и не применяют filters/animation.
- E: реальная activation вынесена в центр короткого site-entry intro; субъективная заметность требует повторного live review.
- F: finish/cancel/watchdogs завершают intro; live toggle не оставляет blocker/glow.
- G: static Hero external, intro имеет один prefix на public page; UI Kit — отдельный prefix.
- H: Reduced Motion пропускает intro, записывает timestamp и не включает его после preference toggle.
- I: approved artwork заменяет placeholders без новых navigation rails/chrome.
- J: большой offset totem приближает атмосферу hero к brand direction; фотография пока provisional.
- K: semantic local assets и прежние shell hooks подходят для template/include migration.
- L: mobile/header/drawer/anchors и прежние product/catalog/configurator regressions прошли.

## IA / SEO / Generic Pages v1

[IA и production indexability matrix](KORSAC-INFORMATION-ARCHITECTURE.md),
[SEO server-side contract](KORSAC-SEO-FOUNDATION.md),
[Contacts и error states](KORSAC-GENERIC-PAGES.md).
Все static prototype pages явно `noindex, nofollow, noarchive`.
Catalog/Product/Contacts используют общий breadcrumb primitive; safe JSON-LD
не публикует demo price/availability/reviews. Canonical host пока не утверждён.
Contacts доступны из public и compact transactional footer, без нового Header
пункта. Contacts и 404/500/503 не имеют Brand Intro boot/overlay/controller
и не меняют timestamp; policy Home/Catalog/Product сохраняется. 500/503
работают без JS и shared application CSS. Static HTML не задаёт HTTP errors:
production server обязан сохранить настоящий 404/500/503.
