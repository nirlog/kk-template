# Материалы визуального и motion-ревью KORSAC

## Brand Asset Integration & Site-entry Intro v1

[Brand Intro — normal-speed MP4](brand-eye-motion-v1.mp4): первый прямой вход
в Catalog, переход в Product → Homepage → reload без повтора intro; затем
отдельный fresh browser context: прямой вход в Product на mobile и drawer.
Оба intro показывают actual SVG eyes, короткий localized blue glow, approved
wordmark, eyes off и переход к странице. В начале фрагментов — короткий
пустой graphite кадр захвата; последовательность не замедлена.
Chromium 151, desktop 1440×1080 / touch-emulated mobile 375×800.
H.264 **1440×1080 / 25 fps**, **11.96 s**, около **1.59 MiB**.
Mobile по центру общего кадра. Encode полностью декодирован; в Chromium
проверены playback и seek. Файл предназначен только для review.

PNG:

- [Resting intro — desktop](brand-intro-rest-v1.png), 1440×1080: mark/wordmark, eyes off.
- [Active intro — desktop](brand-intro-active-v1.png), 1440×1080: реальный eye peak.
- [Resting intro — mobile](brand-intro-rest-v1-mobile.png), 375×800.
- [Brand Assets / UI Kit](brand-assets-v1.png), 1344×826: ICON/TEXT/V2/V1 и reduced-motion demo.
- [Header desktop](brand-header-v1-desktop.png), 1440×88: static horizontal V2.
- [Header mobile](brand-header-v1-mobile.png), 375×64: V2, Cart/Menu 44×44.
- [Footer desktop](brand-footer-v1-desktop.png), 1440×478: stacked V1.
- [Footer mobile](brand-footer-v1-mobile.png), 375×700: compact horizontal V2.
- [Homepage desktop](homepage-brand-v1-desktop.png), 1440×1080: static eyes-off Hero.
- [Homepage wide](homepage-brand-v1-wide.png), 1920×1080.
- [Homepage mobile](homepage-brand-v1-mobile.png), 375×800: прежняя ранняя CTA.
- [Drawer mobile](brand-drawer-v1-mobile.png), 375×800.
- [Intro eye off](brand-eye-off-v1.png) / [Intro eye peak](brand-eye-active-v1.png), 320×287.

Intro PNG — pose captures штатного WAAPI sequence (rest 1050 ms / peak 600 ms),
без изменений geometry/цвета. Остальные обновлённые PNG — reduced motion.
MP4 показывает реальную скорость. Masters byte-identical; derivative
geometry/eyes/strokes/gradients/viewBox сохранены. Header/Footer/Hero — external
static SVG; один inline intro на public document получает `intro-index-`,
`intro-catalog-` или `intro-product-`; UI Kit demo — `kit-brand-`.

Общий intro работает только в `index.html`, `catalog.html`, `product.html`.
**1500 ms**; JS watchdog 1700 ms; независимый CSS cutoff 1800 ms. Hero Eye Flash
и `korsac:hero-enter` coupling удалены. Public replay/loop отсутствуют;
manual Eye Flash доступен только в UI Kit.

Policy: key `korsac:brand-intro:lastShown`, rolling **24h** от последнего
eligible входа. Timestamp записывается до visual sequence. Browser/profile-local
на одном origin, без backend/cookie/account/cross-device synchronization.
LocalStorage unavailable → sessionStorage fallback для этой tab session;
независимые tabs не обязаны разделять fallback. Оба API unavailable → skip.
Initial Reduced Motion записывает timestamp и сразу открывает страницу;
live toggle отменяет intro, выключение preference не повторяет его.

Проверен точный daily flow: clear → direct Catalog intro → Product skip →
Homepage skip → reload skip → new tab skip → timestamp старше 24h → intro.
Missing/malformed/future values, rapid tabs, initial/live Reduced Motion,
local/session denial, no-JS, missing controller/CSS, delayed script/CSS,
lost finished promises и throwing WAAPI прошли. Failure safety не оставляет
pointer blocker. Overlay decorative, без focus/scroll changes; cleanup не
создаёт CLS. Intro без overflow на 320–1920 px.

40 page/width layouts, Product/Catalog/Configurator/Explorer/shared regressions
прошли; static prices и no-JS сохранены. 25 rapid UI Kit replay завершаются eyes off.
SVG masters/inline copies/IDs/local resources проверены. Axe WCAG2A/AA+2.1AA:
zero violations в 12 состояниях; некоторые contrast/link checks incomplete.
Firefox/Safari, physical devices и screen reader не проверены.

[Mapping, implementation и self-review A–L](../KORSAC-BRAND-ASSET-INTEGRATION.md).
Human acceptance: optical scale/clear space, premium feel, заметность глаз и
ритм intro в живом браузере. Не сливать автоматически.

Материалы ниже — предыдущие accepted baselines с временным text wordmark;
новые PNG выше показывают текущую approved identity. Product photography
всё ещё временная; brand assets уже финальные.

## Premium Site Shell + Homepage Experience v1

[Normal-motion запись — MP4](homepage-v1.mp4): примерно **0–9,8 s** — initial
hero, переход header к graphite, PRO → MINI → 1440, featured inspection,
раскрытие содержания SYSTEM ID и footer; **9,8–17,5 s** — mobile hero,
native drawer, touch scenario selection и переход в PLAY 1440.

Chromium 151, desktop 1440×1080 / touch-emulated mobile 375×800.
H.264 **960×720 / 25 fps**, **17,48 s**, около **0,51 MiB**. Mobile по центру
общего кадра. Это обычная скорость; без autoplay, замедления, fake progress
и runtime video background. Файл предназначен только для ревью.

Основные PNG, reduced motion:

- [Homepage desktop](homepage-v1-desktop.png), 1440×1080.
- [Homepage mobile](homepage-v1-mobile.png), 375×800: header, headline, CTA и часть схемы в первом viewport.
- [Homepage wide](homepage-v1-wide.png), 1920×1080.
- [Premium header](shell-header-v1.png), 1440×88: navigation и utility icons без developer rails.
- [Premium footer](shell-footer-v1.png), 1440×394: большой wordmark, группы и тихая prototype note.
- [Compact scenario discovery](homepage-scenario-v1.png), 1440×1080: 1440/MINI branch и краткий preview.
- [Mobile drawer](shell-drawer-v1-mobile.png), 375×800: native navigation без numeric indices.
- [Featured PLAY 1440](homepage-feature-v1.png), 1440×1080: native inspection открыта, GPU-зона выделена.
- [Ownership / SYSTEM ID](homepage-ownership-v1.png), 1440×1080: структура паспорта без verification claims.
- [Catalog с новой оболочкой](shell-catalog-v1.png), 1440×1080.
- [Product с новой оболочкой](shell-product-v1.png), 1440×1080.
- [Premium Shell Primitives](shell-primitives-v1.png), 1344×821: header states, mobile anatomy/drawer entry и footer disclosure.
- [Homepage Primitives](homepage-primitives-v1.png), 1344×1066: CTA composition, отдельный compact selector и trust block.

[Homepage architecture](../KORSAC-HOMEPAGE-EXPERIENCE.md) и
[Site Shell / asset integration](../KORSAC-SITE-SHELL.md) описывают authored
HTML, future SVG/photography slots, no-JS и Bitrix mapping. Схемы не являются
product photography; text wordmark не является финальным logo asset.

Проверены пять страниц на 320/375/430/768/1024/1280/1440/1920 px без horizontal
overflow. Preview height delta — 0 px для пяти моделей на каждой ширине.
Hero заканчивается через 940 ms и отменяется при live reduced motion.
На 320/375/430×800 primary hero CTA заканчивается примерно на 414/414/428 px;
схема начинается примерно на 490/490/452 px. Header не меняет размер при
переходе от hero. Native dialogs/drawer/details, keyboard, no-JS navigation,
сценарии и scoped UIKit независимость проверены. Catalog MAX3/mobile matrix
и Product v3.1 synchronization/static pricing regressions прошли.
Axe WCAG2A/AA+2.1AA: zero violations; contrast/link-in-text-block часть
результатов остаётся incomplete. Полноценный screen-reader run не проводился.

Human gate остаётся открытым: premium feel оболочки, ясность hero с первого
экрана, естественный переход Homepage → Catalog → Product и motion в живом
браузере. Нужна проверка на целевых браузерах/устройствах. Не сливать автоматически.

Ниже сохранены принятые catalog/product материалы. Они фиксируют исходную
оболочку соответствующих PR; актуальный public shell показывают новые
`shell-catalog-v1.png` / `shell-product-v1.png` выше. Контентные
взаимодействия прежних версий сохраняются.

## Catalog & Product Family Experience v1 — после visual review

[Каталог: обновлённая запись — MP4](catalog-v1.mp4) показывает normal motion:
примерно 0–9,3 s — PLAY 1440 → PRO → MINI → 4K → 1080 → 1440,
keyboard focus/selection заголовка MINI в компактной линейке и desktop
comparison 1440/PRO; примерно 9,3–17 s — mobile touch PRO → MINI → 1440,
местное обновление preview/CTA и сравнение 1440/MINI/PRO по свойствам.

Захват: Chromium 151, desktop viewport 1440×1080 и touch-emulated mobile
375×800. MP4 H.264: 960×720 / 25 fps, **17,04 s**, около **0,73 MiB**.
Mobile-фрагмент расположен по центру общего кадра. Нет замедления,
автопереключения Navigator или fake performance/price calculation.

Все шесть PNG обновлены с reduced motion:

- [Каталог desktop](catalog-v1-desktop.png), 1440×1200: семейства, четыре ступени,
  одна MINI-ветка непосредственно от 1440 и подробный выбранный preview.
- [Каталог mobile](catalog-v1-mobile.png), 375×1440: компактный selector,
  соединённая MINI-ветка, выбранная модель, пример цены и CTA.
- [Вся линейка PLAY](catalog-range-v1.png), 1440×1080: пять одинаковых по структуре
  scan cards — сценарий, форм-фактор, GPU/RAM/SSD и одна CTA. PLAY 1440
  выделен rail/индексом/акцентом без отдельного hero layout.
- [Desktop-сравнение 1440 / PRO](catalog-compare-v1.png), 1440×1080:
  model columns и семь свойств с семантическими заголовками строк/колонок.
- [Mobile-сравнение 1440 / MINI / PRO](catalog-compare-v1-mobile.png), 375×800:
  пять свойств по строкам, по три значения рядом, закреплённые model headers.
- [Catalog Primitives](catalog-primitives-v1.png), 1344×1879: component capture
  из UI Kit — family switch, ladder, соединённая MINI-ветка, единые scan cards,
  независимый Navigator и comparison row.

[Документ каталога](../KORSAC-CATALOG-EXPERIENCE.md) описывает единый HTML
source, MAX3 comparison, mobile/no-JS/reduced-motion и future Bitrix mapping.
На 320/375/430 px карточки примерно 400–423 px. Проверены матрицы 2/3 моделей
на 320/375/430/768/1440 px, выравнивание значений, native table semantics
и отсутствие horizontal overflow. При высоте viewport 500 px model headers
остаются над строками после keyboard PageDown; close-control видим.
Высота preview стабильна при переключении пяти моделей на контрольных ширинах.
Review assets не загружаются страницами. Материалы продукта v3.1 ниже остаются
актуальной отдельной основой; каталог не меняет Product Explorer.

Human acceptance остаётся открытым: быстро ли читается компактная MINI-ветка,
легко ли сканировать всю линейку, удобно ли сравнивать значения рядом на mobile,
соответствует ли короткий resolve KORSAC. Запись и tests не заменяют live-оценку.
Автоматическое слияние не выполняется.

## Актуальный Explorer v3.1 — synchronized state

[Запись взаимодействий v3.1 — MP4](interactive-v31.mp4) показывает контекстные
кнопки, GPU/memory hotspots, Next и обратный Prev, смену корпуса, RAM/SSD/SSD2
и сохранение Explorer context. Desktop — примерно 0–16 s; mobile — 16–23 s:
обычная короткая прокрутка, touch context/hotspot и Prev/Next с местным
видимым пояснением. Нет замедления или автопереключения самого Explorer.

Захват: Chromium 151, normal motion, desktop viewport 1440×1080 и mobile
375×800 с touch emulation. MP4 H.264: 960×720 / 25 fps, 22,8 s, около 1,06 MiB.
Mobile-фрагмент расположен по центру общего видеокадра.
Файл используется только для ревью и не загружается прототипом.

Актуальные PNG, снятые с reduced motion:

- [PLAY 1440 — desktop](product-v31-desktop.png), 1440×1080 px.
- [PLAY 1440 — mobile](product-v31-mobile.png), 375×1000 px.
- [Explorer — desktop](explorer-v31-desktop.png), 1440×1080 px: AIRFLOW,
  общий counter 01/05 и destination labels.
- [Explorer — mobile](explorer-v31-mobile.png), 375×1200 px: весь компактный
  модуль, controls, explanation и Prev/Next.
- [Interactive Product Primitives](interactive-primitives-v31.png), 1440×1440 px:
  synchronized platform и независимый native fixture с выбранной RAM 64.
- [Конфигуратор и stage](configurator-stage-v3.png): сохранённая компоновка
  аппаратных controls/scene; в v3.1 она не перерабатывалась.

Высота Explorer при 1440×1080 уменьшилась 3242→837 px, при 375 px — 3383→1103 px.
State transitions и CPU/memory subannotations не меняют высоту раздела
на 320/375/430/768/1024/1280/1440 px. Счётчик всегда 00/05–05/05;
навигация имеет конечные границы и не зависит от прокрутки.

[Архитектура и human checklist v3.1](../KORSAC-INTERACTIVE-PRODUCT-EXPERIENCE.md)
описывают single state, annotations, visibility/inert, normal-flow mobile,
no-JS/reduced-motion и media/kk.korsac adapters. Человеческое live-ревью
остаётся acceptance gate; запись и автоматические проверки его не заменяют.

## Архив v3 — до synchronized Explorer

Эти материалы фиксируют PR #4 на head `22d5893` и больше не являются текущей
UX-моделью Explorer. Для ревью текущего изменения используйте файлы v3.1 выше.

- [Предыдущая запись](interactive-v3.mp4).
- [Продукт desktop](product-v3-desktop.png) / [mobile](product-v3-mobile.png).
- [Прежний Explorer desktop](explorer-v3-desktop.png) /
  [mobile](explorer-v3-mobile.png).
- [Прежний UI Kit](interactive-primitives-v3.png).

Предыдущие v1/v2/v2.1 assets также сохраняются под исходными именами.
Схемы во всех материалах — placeholders, не product photography и не точная
компоновка физического корпуса.

## Motion Visibility Pass v2.1

[Короткая запись движения — MP4](motion-v21.mp4) показывает нормальное
проигрывание без замедления: hero (примерно 0–2 s), выбор корпуса и его
manifest row (2–4 s), pending/confirmed/error (4–9 s), SYSTEM ID (9–11 s).
Запись: Chromium, viewport 1440×1080 px, видео 960×720 px / 25 fps,
11,2 s, около 1,44 MiB; `prefers-reduced-motion: no-preference`.
Файл нужен только для ревью и не загружается прототипом.

Это материал для оценки ритма, а не подтверждение визуальной приёмки.
В браузере следует проверить те же четыре момента на desktop/mobile,
быстрый повтор, работу контролов во время входа и reduced motion.
Ручной checklist и вопросы о заметности/характере движения включены в PR.

## Visual & Motion Direction v2

Снимки v2 показывают новую композицию hero, indexed rails, frame/corner,
manifest конфигурации, SYSTEM ID и примитивы визуальной системы:

- [PLAY 1440 v2 — desktop](product-v2-desktop.png).
- [PLAY 1440 v2 — mobile](product-v2-mobile.png).
- [UI Kit v2 — desktop](ui-v2-desktop.png).
- [UI Kit v2 — mobile](ui-v2-mobile.png).

Дополнительные фрагменты:

- [Конфигуратор v2](configurator-v2-desktop.png).
- [SYSTEM ID v2](system-id-v2.png).
- [Motion playground](motion-ui.png).
- [Мобильное меню v2 — явные индексы 01–06](drawer-v2-mobile.png).
- [Select v2 — обычный, focus, disabled и error](select-v2-states.png).

Захват v2: Chromium 151, reduced motion, desktop 1440×1080 px, mobile
375×1000 px. Дополнительные desktop-фрагменты сняты при 1440×1440 px,
чтобы в кадр помещались длинный manifest и все пять motion-примеров.
Select-состояния сняты отдельным фрагментом раздела форм при ширине 1440 px.

Статические снимки используются для сравнения композиции и состояний.
Последовательности движения нужно смотреть в разделе Motion на
[`prototype/ui.html`](../../../prototype/ui.html): hero, validation,
selection, SYSTEM ID и section index повторяются отдельными кнопками.
Параметры захвата и фактические результаты проверок фиксируются в PR.

Для принятия v2 baseline требуется человеческое ревью движения в браузере:
hero, подтверждение выбора, validation sweep, SYSTEM ID, мобильное меню
и `prefers-reduced-motion`. Автоматические проверки и PNG не заменяют
эту проверку ощущения движения.

## Static UI Foundation v1

Исходные четыре файла сохранены под прежними именами для сравнения направлений:

- [UI Kit — desktop, 1440 px](ui-desktop.png).
- [UI Kit — mobile, 375 px](ui-mobile.png).
- [PLAY 1440 — desktop, 1440 px](product-desktop.png).
- [PLAY 1440 — mobile, 375 px](product-mobile.png).

Снимки v1 сделаны в Chromium 151 с reduced motion. UI Kit показывает кнопки
и формы, продукт — начало страницы. В исходном ревью v1 горизонтальное
переполнение проверялось отдельно при 320/375/768/1024/1280/1440 px;
это не заменяет повторную проверку v2.

## Использование

Это только материалы ревью: HTML/CSS/JS не ссылаются на них и не загружают
их. Они не являются product photography, финальными ассетами бренда или
обязательными файлами для запуска. Снимки добавлены, чтобы встроить визуальное
подтверждение в PR без отдельного механизма загрузки GitHub-вложений.
