# KORSAC — Computer Families Experience v1

Computer Families реализует следующий stage после
[IA / SEO Foundation](KORSAC-INFORMATION-ARCHITECTURE.md).
Base: merged PR #9, `main` at `148c901befb8214f49f9307fbb6cdc90971da7c5`.
Projects — следующий roadmap stage; Bitrix migration не начата.

## Hub и три разных модели выбора

`/computers/` отвечает «какое семейство подходит моей задаче?». Это короткий
маршрутизатор, не ещё один PLAY catalog. В первом mobile viewport доступны
три обычные ссылки. Ни selector state, ни fetch, ни JS для выбора не нужны.
Ниже — открытые editorial sections: один family index, короткое объяснение
decision model и одна ссылка в семейство. Нет трёх product-card grids,
повторного PLAY navigator, полного сравнения или invented model preview.

| Семейство | Начало выбора                                 | Содержание landing                                                                                                           | Чего здесь нет                                                    |
| --------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| PLAY      | Разрешение, игровой сценарий, класс           | Утверждённый `catalog.html`: ladder, preview, MINI и compare                                                                 | Новых моделей или перестроенной игровой архитектуры               |
| CREATE    | Рабочий процесс, приложения, характер проекта | Workflow map; 3D/rendering, CAD, video, graphics; требования к вычислениям/памяти/хранению/среде                             | Fictional lineup, benchmarks, certified software compatibility    |
| WORK      | Рабочий день, совместная нагрузка, место      | Context brief; повседневная работа/многозадачность/профессиональное место; expansion/form-factor/эксплуатационные приоритеты | Дешёвой копии PLAY, gaming resolutions, SLA/корпоративных условий |

CREATE — process-first: diagram «материал → работа → результат», workflow
questions и список требований к архитектуре. WORK — task-first: brief рабочего
дня, последовательно читаемый список контекстов и обзор operational priorities.
WORK имеет осмысленный handoff в CREATE для content-production workflows.
Это разные information hierarchies, а не одна страница с заменённым названием.

Общий язык — system typography, copper indices, rails, blue native navigation,
открытое пространство и interrupted frame в CREATE workflow map. Metadata
rationed: indices маркируют маршруты/этапы; не добавлены serial/SKU/revision
fiction, HUD, product photographs или invented chassis artwork.

## Static → production mapping

| Static file      | Production target       | Visible breadcrumb / schema hierarchy   |
| ---------------- | ----------------------- | --------------------------------------- |
| `index.html`     | `/`                     | Главная                                 |
| `computers.html` | `/computers/`           | Главная → Компьютеры                    |
| `catalog.html`   | `/computers/play/`      | Главная → Компьютеры → PLAY             |
| `create.html`    | `/computers/create/`    | Главная → Компьютеры → CREATE           |
| `work.html`      | `/computers/work/`      | Главная → Компьютеры → WORK             |
| `product.html`   | `/computers/play/1440/` | Главная → Компьютеры → PLAY → PLAY 1440 |

`catalog.html` сохраняет имя, исходный scoped controller и HTML model data.
«Компьютеры» на Catalog/Product теперь настоящий `<a href="computers.html">`;
JSON-LD использует тот же static file. PLAY на Product по-прежнему ссылается
на `catalog.html`. Все non-final ListItems имеют item URL; final может его
опустить. Production resolver заменяет static file URLs согласованными
абсолютными canonical paths; hostname ещё не утверждён.

## Интеграция с Homepage и shell

Пять global header entries сохранены. «Компьютеры» теперь ведёт в hub,
«Для бизнеса» — на WORK; новые family names не добавлены в top-level header.
Hub использует `aria-current="page"`, descendants — `aria-current="location"`
на primary computer route. Native fallback menu и enhanced drawer имеют те
же маршруты. Все internal browsing headers sticky/opaque с прежней высотой.

Homepage primary/final «Выбрать компьютер» теперь ведут в hub, включая UI Kit CTA specimen.
Homepage PLAY/CREATE/WORK теперь native links; CREATE/WORK labels говорят
«линейка формируется». Отдельная ссылка ведёт ко всем семействам.
Существующий компактный PLAY discovery остаётся под ними со своими пятью
сценариями, HTML fallback и label-only selection. PLAY family switcher и
UI Kit specimen теперь используют реальные CREATE/WORK links вместо disabled
buttons. Footer Products связывает hub и три семейства, сохраняя PLAY1440 и
конфигуратор. Contacts B2B link ведёт на WORK, 404 choose action — в hub.
Cart/Checkout/Success, error HTTP semantics и search/account prototype scope
не изменены. Старый `index.html#business` target сохранён для прежних ссылок.

## Модельные линейки и production publication

**Prototype completion != production publication approval.**
[Единая IA matrix](KORSAC-INFORMATION-ARCHITECTURE.md#единая-матрица-production-indexability)
остаётся authoritative: CREATE/WORK production indexability условна и требует
полезного реального content/product readiness. Сейчас это designed review
landings, а не заявление опубликованного commercial catalog.

Каждая landing заканчивается честным объяснением, что модельная линейка
формируется. Нет цен, available stock, component configurations, FPS/render
scores, certifications, guarantee/delivery/production-time promises, customer
counts/logos/reviews, model names или SKU. Family routes существуют;
модельная линейка от этого не считается запущенной.

Future insertion point обозначен HTML-комментарием после workflow/operational
criteria, перед final next-step area. Там можно добавить утверждённые модели,
когда появятся реальные entities. Не размещать пустые catalog tiles до этого.
CREATE models наследуют workflow description; WORK models — task/operational
context. Не копировать PLAY resolution ladder. Не придумывать модельные slugs
до реальных моделей; production patterns остаются `/computers/{family}/{model}/`.

## SEO / аудит

Hub/PLAY/CREATE/WORK: **CollectionPage + BreadcrumbList**.
Все 15 static pages остаются `noindex, nofollow, noarchive`; уникальные title,
description и один H1. OG title/description/site_name/type присутствуют в HTML.
Никаких production canonical host/og:url/og:image fiction, Product на family
landings, Offer/sample pricing, Review/AggregateRating. Schema и важные ссылки
не формируются JS. Hub не объявляет ItemList несуществующих коммерческих моделей.

`tools/seo_audit.py` автоматически читает все `prototype/*.html` и теперь
дополнительно требует CollectionPage/BreadcrumbList на hub/family filenames,
запрещая там Product. Общие guards сохранены: unique metadata, staging policy,
H1, IDs, local links/fragments, images и schema safety; breadcrumb URL rule из
PR #9 не ослаблена. Tests включают новые filenames, неверный page type и
ошибки staging/IDs/link/H1 у каждой новой landing.

```sh
python3 tools/seo_audit.py
python3 tools/seo_audit.py --json
python3 -m unittest discover -s tools -p 'test_seo_audit.py'
```

[Current deterministic report](review/seo-audit-v1.json) и
[Families review evidence](review/computer-families-v1.md).
Это локальные guards, не Search Console или внешняя rich-results validation.

## Motion, responsive и accessibility

Нового animation/controller нет. Family content отображается сразу и
статически; native links, hover/focus и blue interaction signal используют
существующие токены. Нет autoplay, infinite scanning/slider, typing или scroll
reveal. Поэтому нового temporal review / MP4 не требуется.

Новые browsing pages намеренно участвуют в том же public Brand Intro:
прежние boot/controller/CSS и approved inline SVG с отдельным prefix на страницу.
Frequency key общий с Home/Catalog/Product, rolling24h; 1500ms sequence не
изменена. Reduced Motion пропускает intro и записывает timestamp; live reduce
отменяет его, переключение обратно не replay. Contacts/transactions/errors
сохраняют прежнее исключение. Intro copy не является новой artwork/animation.

Grid columns исчезают на mobile в порядке чтения документа. Нет fixed heights
для content, скрытых обязательных sections или overflow scroll вместо wrap.
На320/375/430px hub routes и primary family CTA доступны в первом800px viewport;
остальные sections читаются обычной прокруткой. Breadcrumbs безопасно wrap.
Один H1, semantic sections/headings, nav/ol/dl, skip link, native focus-visible,
keyboard drawer и no-JS fallback. Decorative SVG/arrow имеет aria-hidden;
brand link именуется один раз, images имеют dimensions и пустой decorative alt.

## Будущий Bitrix mapping — без реализации

Server page context выбирает hub/family type, template content и одну hierarchy
для visible breadcrumbs и JSON-LD. Shared shell/intro — template includes;
workflow/task descriptions — утверждённый family content. Model entity
collection подключается в обозначенную секцию только после readiness gate.
Title/description/robots/canonical/OG/schema и publication status формируются
сервером по PR #9. Frontend не выводит business rules из выбранного семейства:
цены, stock/order availability, payment/delivery restrictions и property sets
по-прежнему будущая backend/Sale responsibility. Никаких infoblocks/HL blocks,
API, migration, production robots/sitemap или deployment config в этом PR.

## Acceptance

Home → Computers → PLAY/CREATE/WORK работает обычными ссылками; PLAY ведёт
к существующему Product, Product возвращает в PLAY и hub. CREATE/WORK имеют
различные criteria и честные lineup boundaries. [Review assets и проверки](review/computer-families-v1.md)
позволяют оценить эту архитектуру до следующего Projects stage.
Human visual review обязателен; автоматического merge нет.
