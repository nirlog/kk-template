# KORSAC — SEO Foundation v1

Технический контракт до переноса в Bitrix. Авторитетная production policy —
[матрица IA](KORSAC-INFORMATION-ARCHITECTURE.md#единая-матрица-production-indexability).
Никаких production domain, контактов, Offer по demo-ценам или fake ratings.

## Staging и production — разные политики

Каждый `prototype/*.html`, включая Homepage/Product и review/error pages:

```html
<!-- prototype = noindex environment; production policy is page-specific. -->
<meta name="robots" content="noindex, nofollow, noarchive" />
```

`robots.txt: Disallow` не заменяет noindex: если crawler не может прочитать HTML,
он не увидит директиву; заблокированный URL всё ещё может появиться в индексе.
Не удалять noindex на staging. Для публичного staging предпочтительна password/
access protection; crawler directives не защищают коммерческую/частную информацию.
Deployment обязан отдавать этот head и не переопределять его небезопасными headers.
Факт отсутствия страницы в поисковых индексах в этой среде не проверяется.

При production migration blanket policy заменяется по матрице, а не копируется
весь staging head. Publish gate проверяет environment, page type, entity status,
canonical, robots и sitemap membership. Cart/Checkout/Success/Search/Account/
ошибки/неутверждённые filters остаются noindex; private pages требуют авторизации.
Production robots.txt и XML sitemap здесь не созданы.

## Metadata: одна серверная ответственность

Bitrix page-context/entity resolver формирует в HTML до JS:
`title`, `description`, `robots`, canonical, Open Graph, JSON-LD, H1, основное
описание/статью, breadcrumbs и важные внутренние ссылки. JS отвечает за
presentation, не генерирует SEO. Не размещать второй generator в браузере.

В review у всех 17 страниц уникальные nonempty title/description, `lang="ru"`,
viewport и один H1. Product H1 сохраняет имя PLAY 1440, а не логотип как heading.
Примеры production naming: «Игровые компьютеры PLAY — KORSAC»,
«PLAY 1440 — игровой компьютер KORSAC», «Контакты — KORSAC».
Review/UI/transaction/error descriptions объясняют свой реальный тип, без
keyword stuffing. Существующие developer/demo disclosures остаются честными.

Metadata хранится в page/entity content и центральных brand settings. Будущий
контент-редактор может утвердить title/description; fallback выводится сервером
из реального имени/описания. Никакой генерации массовых SEO-текстов.

## Canonical и параметры

Production indexable canonical content имеет **ровно один абсолютный
self-canonical** на согласованном hostname. В prototype canonical намеренно
отсутствует: неизвестный домен нельзя заменить example.com, testhost или localhost.
`og:url` также ждёт hostname. Требуемый slot — production canonical URL,
вычисляемый router/entity resolver, а не frontend configuration.

Server redirects нормализуют host/scheme/trailing slash; clean content URL
заканчиваются `/`. Ссылки, canonical и sitemap используют ту же версию.
Tracking-параметры не меняют primary content, не индексируются отдельно и
исключаются из canonical. Не строить sitemap из необработанных request URLs.

Фильтры и сортировки default noindex, без автоматических landing routes и
canonical в v1. Любая будущая indexable filter landing требует явного editorial
whitelist, уникального полезного содержания и собственного migration decision.
RAM/SSD/Case — состояние конфигурации primary model, не новые Product entities
или страницы для поиска. Price/availability не выводятся из URL параметров.

Реальная пагинация Projects/Equipment имеет server-rendered crawlable links,
свой canonical и реальное содержимое. Не canonical каждую страницу на page 1.
Pagination пока не реализована; infinite-scroll-only запрещён контрактом.

## JSON-LD: известные факты и связь entities

JSON-LD — один выбранный механизм. Не смешивать десятки microdata `itemprop`
с отдельным schema generator. Schema и видимая информация согласованы, но
markup визуальных компонентов остаётся независимым от JSON-LD.

Текущие минимальные graph examples (локальные URLs допустимы **только review**):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "#organization",
      "name": "KORSAC",
      "logo": "assets/images/brand/korsac-lockup-horizontal.svg"
    },
    {
      "@type": "WebSite",
      "@id": "#website",
      "name": "KORSAC",
      "url": "index.html",
      "publisher": { "@id": "#organization" }
    }
  ]
}
```

Organization — представление бренда, не утверждение отдельного юридического лица.
Не задано legalName/parentOrganization/адрес/ИНН/телефон/email/social links.
Homepage служит source identity; Contacts ссылается на `index.html#organization`.
Production IDs — абсолютные `${canonical-home}#organization` / `#website`;
approved logo получает реальный абсолютный URL. Все global company/brand/contact
значения приходят из **одних настроек сайта**, которые также питают Header,
Footer и Contacts. Не хранить четыре независимых набора реквизитов.

Catalog: CollectionPage + BreadcrumbList. ItemList необязателен и будет уместен
при наличии реальных публикуемых product entities. Текущий graph не публикует
offers на авторские карточки.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "CollectionPage",
      "name": "Компьютеры KORSAC PLAY",
      "url": "catalog.html"
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Главная",
          "item": "index.html"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Компьютеры",
          "item": "computers.html"
        },
        { "@type": "ListItem", "position": 3, "name": "PLAY" }
      ]
    }
  ]
}
```

У каждого non-final ListItem обязателен `item`: URL string или объект с URL
в `@id`. Опустить его можно только у последнего элемента. Для промежуточного
«Компьютеры» используется `computers.html`: hub теперь существует и видимый
crumb имеет такую же ссылку. На Product PLAY ссылается на `catalog.html`;
только final PLAY 1440 может не иметь `item`. Видимый `<nav><ol>` сохраняет
те же names/order. Hub/CREATE/WORK используют CollectionPage + BreadcrumbList
без Product/Offer; их наличие в review не меняет production publication policy.
В production единый server hierarchy resolver формирует реальные абсолютные
ancestors/current canonical на утверждённом host. Audit проверяет наличие и
URL representation non-final items, без заявления внешней rich-results validation.

Projects list (`projects.html`): CollectionPage + BreadcrumbList. Review detail
(`project.html`): Article + BreadcrumbList; headline/description/citation только
из approved historical case facts. Видимые crumbs — Главная → Проекты [→ title],
ancestors `index.html`/`projects.html`. Нет Product/Offers/ratings на case,
нет invented author/dates/image для заполнения optional Article properties.
Legacy slug — кандидат, production slug и hostname утверждаются при migration.
[Projects source contract](KORSAC-PROJECTS-EXPERIENCE.md) фиксирует provenance,
source access limitation и отсутствие project photography в текущем review.

Product: безопасный scaffold + BreadcrumbList, без Offer.

```json
{
  "@type": "Product",
  "name": "KORSAC PLAY 1440",
  "brand": { "@type": "Brand", "name": "KORSAC" },
  "model": "PLAY 1440",
  "category": "Игровые компьютеры",
  "description": "Система PLAY для игр в 1440p с выбором памяти, накопителя и корпуса."
}
```

Цена «179 900 ₽ — пример» не участвует в Offer/AggregateOffer, merchant listings,
XML feed или sitemap metadata. Нет invented availability, SKU, GTIN, image,
ratings/review counts. Configurator не переписывает JSON-LD при выборе опций.
Primary indexed entity — KORSAC PLAY 1440.

Contacts: sparse ContactPage + BreadcrumbList.

```json
{
  "@type": "ContactPage",
  "name": "Контакты KORSAC",
  "url": "contacts.html",
  "about": { "@id": "index.html#organization" }
}
```

Нет ContactPoint/telephone/email/address/openingHours до подтверждения данных.
Cart/Checkout/Success и errors не получают content/product schema.
Не копировать giant identical graph на каждую страницу.

## Будущие structured-data templates

Project list: CollectionPage + BreadcrumbList. Project detail: Article +
BreadcrumbList. Сервер формирует Article из реального case study:
`headline`, body/description, canonical URL, реальная cover image; даты/author
только если существуют и видимы. Customer и измерения не выдумываются.

Ordinary product: Product + Offer + BreadcrumbList. **Только при появлении
backend-authoritative данных** server template формирует такую структуру:

```text
Product.name / description / brand / image <- реальный product entity/media
Product.offers.@type = Offer
Offer.price                              <- catalog/Sale authoritative price
Offer.priceCurrency                      <- backend currency
Offer.availability                       <- backend order/stock state mapping
Offer.url                                <- canonical entity URL
BreadcrumbList                           <- тот же server hierarchy, что UI
```

Это source contract, не JSON с вымышленными значениями и не текущий runtime Offer.
Page price, Cart и JSON-LD используют один backend источник, без трёх независимых
расчётов. Платёж/доставка/ограничения/properties также определяются Bitrix,
frontend только рендерит доступные для заказа lists.

Будущий Yandex OfferCatalog с nested Offer опционален и возможен только при
полноте реальных требуемых данных. Не заполнять fake required fields ради
validator. Review/AggregateRating возможны только при наличии реальных
отзывов и соблюдении требований поисковой системы; dummy stars запрещены.

## Open Graph и медиа

Сейчас: реальные page-level og:title, og:description, og:site_name=KORSAC,
og:type=website. Они уже присутствуют в HTML. `og:url` и `og:image` отсутствуют
намеренно. В production type задаётся типом содержимого (например, Article),
URL — canonical, image — утверждённое медиа. Homepage — brand social artwork;
family — family artwork; product — реальное product media; project — cover;
обычный товар — реальная фотография; Contacts — допустимое brand artwork.
Большая отдельная Twitter/X metadata framework в v1 не нужна; cards optional.

Meaningful image alt описывает изображение, не набивает keywords. Декоративный
brand имеет `alt=""`; brand home link получает имя один раз. Все текущие img
имеют width/height; существующие aspect ratios сохраняются. Будущие real media:
`picture`, современные форматы, responsive sources/sizes, lazy loading ниже
первого viewport. Critical Hero/product LCP не lazy-load по умолчанию.
Будущая production acceptance включает Core Web Vitals с реальным медиа,
без synthetic claims о нынешних placeholder photographs.
Нет новых frameworks, remote fonts или тяжёлых SEO scripts.

## Robots, sitemap и HTTP

Sitemap создаёт Bitrix из опубликованных indexable canonical сущностей по
матрице IA, не из любой сущности CMS или URL текущего запроса. Empty families,
thin supplier rows и placeholder projects не publishable. Транзакции/private/
search/filter/sort/configuration/review/errors исключаются. Crawlability и
indexability проверяются отдельно от sitemap membership.

404 — actual 404 Not Found, 500 — 500 Internal Server Error, 503 — 503 Service
Unavailable с Retry-After только при известной полезной оценке. Для намеренно
удалённого без замены контента возможен 410. Не branded soft-404 с HTTP 200,
не JS redirect/auto-reload. Статические HTML не задают response status.
Production error CSS/logo и Home/Contacts links должны разрешаться независимо
от глубины исходного requested URL: origin-root-absolute или server-resolved
assets, `/` и `/contacts/` для действий. File-relative prototype paths нельзя
копировать в production error templates. 503 retry обращается к исходному URL.
См. [Generic pages](KORSAC-GENERIC-PAGES.md).

## Локальная проверка

```sh
python3 tools/seo_audit.py
python3 tools/seo_audit.py --json
python3 -m unittest discover -s tools -p 'test_seo_audit.py'
```

Stdlib tool проверяет все `prototype/*.html`: lang, unique title/description,
viewport/robots/OG, один H1, JSON syntax/schema safety, обязательный URL string
или `item.@id` у каждого non-final BreadcrumbList ListItem, duplicate IDs,
относительные static links/fragments, alt/dimensions, отсутствие canonical. Hub/family pages дополнительно требуют CollectionPage +
BreadcrumbList и не могут публиковать Product schema.
Exit 1 при ошибке; warnings не скрывают ошибки. `--root` поддерживает отдельные
fixtures/checkout; output сортируется и не содержит времени/локального hostname.
CSS aspect ratio вместо img width/height требует human review warning.
Audit проверяет file links, не будущие production redirects или remote href.

Negative regression tests вводят нарушенный noindex, broken anchors/ресурсы,
повтор ID, invalid JSON, sample Offer, Review/rating, missing semantics и metadata,
а также missing/invalid breadcrumb URL и допустимый final-item omission.
[Report](review/seo-foundation-v1.md) перечисляет types, known warnings и результат.
Это не Google Rich Results Test, Schema.org/Yandex validator, Lighthouse или
Search Console. Полноценность rich results и production crawl/status/host
проверяется отдельно после реальных данных/deployment. Правдоподобный scaffold
не дополняется ложными полями для прохождения внешнего validator.
