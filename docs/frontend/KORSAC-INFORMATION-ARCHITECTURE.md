# KORSAC — Information Architecture v1

Контракт переноса в Bitrix. Текущий прототип — review-среда, а не набор
production URL. Все `prototype/*.html` имеют `noindex, nofollow, noarchive`.
Computer hub и CREATE/WORK реализованы как static review landings. Projects
теперь имеют archive list/detail fixtures. Equipment реализован как curated hub,
Monitors category и один ordinary product detail. Модельные линейки CREATE/WORK
и прочие equipment-категории остаются future content, без активных ссылок на
несуществующие страницы; publication gate матрицы сохранён.

## Production URL tree

```text
/
├── computers/
│   ├── play/
│   │   └── 1440/                 # текущая модель PLAY 1440
│   ├── create/
│   │   └── {model}/              # паттерн, без придуманных моделей
│   └── work/
│       └── {model}/              # паттерн, без придуманных моделей
├── projects/
│   └── {slug}/
├── equipment/
│   └── monitors/
│       └── {slug}/
├── contacts/
├── cart/
├── checkout/
├── order-success/
├── search/                       # будущий поиск, noindex
└── account/                      # приватные страницы, noindex
```

404/500/503 — состояния ответа запрошенного URL, не публичные разделы дерева.
Имена `404.html`, `500.html`, `503.html` относятся только к статическому review.
Остальные equipment-категории добавляются после утверждения содержания,
по паттерну `/equipment/{category}/` и `/equipment/{category}/{slug}/`.
Новых каталогов поставщика автоматически не создаём.

## Роли страниц и рост семейств

**Главная** направляет к семействам и объясняет подход KORSAC.
**Компьютеры** — короткий выбор PLAY / CREATE / WORK (`computers.html`), без повторения
подробного сравнения моделей. Не подменять этот hub каталогом PLAY в production.

**PLAY** — сценарий игры сначала: 1080 → 1440 → 1440 PRO → 4K.
MINI остаётся ответвлением от 1440 для компактного Mini-ITX, а не следующей
ступенью производительности. Утверждённый navigator и compare сохраняются.
Только URL PLAY 1440 закреплён сейчас; остальные model slugs утверждаются
с реальными сущностями. RAM/SSD/Case не образуют новые model URL.

**CREATE** — самостоятельная индексируемая family landing с выбором по
творческому workflow: приложения, характер проекта, требования к системе.
**WORK** — самостоятельная landing по рабочей задаче и контексту бизнеса.
Это разные предложения, не копии PLAY с другим заголовком. Публикация только
после появления реального уникального содержания; модели, измерения и
производительность не выдумываются. Семейства растут в своих URL-пространствах.

**Проекты** — публичное название completed-build кейсов KORSAC / King-Komp.
Не Blog и не будущий редакционный раздел. Список помогает выбрать релевантный
опыт, detail объясняет решение и ведёт к семейству/модели. Модель содержания:
название; краткая задача клиента без частных данных; подход; система и
конфигурация с причинами выбора; сборка и реальные фотографии; измеренные
результаты, только если измерения существуют; итог; связанные системы; CTA.
Автор, даты, клиент и результаты берутся из реального проекта, не placeholders.

**Оборудование** — curated дополнения к системам. Первое предусмотренное
направление — мониторы. Категория должна помогать выбрать, а не копировать
supplier feed. Обычная product detail проще PC-template: медиа, имя,
backend-цена/статус, ключевые характеристики, описание, доставка/оплата,
CTA и связанные системы. Не нужны Explorer, SYSTEM ID, конфигуратор PC
и история сборки. Пустые категории и слабые placeholder-сущности не публикуются.

**Контакты** — общая точка связи, в footer всех публичных страниц.
**Cart / Checkout / Success** — транзакционный путь, вне поиска и sitemap.
Платежи, доставка, доступность и order-property sets определяет Bitrix Sale.
Frontend не закрепляет ограничения по типу покупателя.

## Единая матрица production indexability

`Index` применяется только к опубликованным полноценным сущностям с реальным
уникальным содержанием. До публикации — закрытый preview, не пустая indexable
страница. `Self` = один абсолютный self-canonical на утверждённом hostname,
без tracking-параметров, согласованный с URL сервера, ссылками и sitemap.
`Нет` = canonical не выводится. Таблица — единый источник политики для миграции.

| Page type                    | Production URL pattern                                             | Index / noindex                     | Canonical behavior                                    | Breadcrumbs                                | Structured-data type                                             | Sitemap inclusion                            | Bitrix owner/source                                      |
| ---------------------------- | ------------------------------------------------------------------ | ----------------------------------- | ----------------------------------------------------- | ------------------------------------------ | ---------------------------------------------------------------- | -------------------------------------------- | -------------------------------------------------------- |
| Главная                      | `/`                                                                | Index                               | Self                                                  | Не нужны                                   | Organization + WebSite                                           | Да                                           | Настройки бренда + содержимое главной                    |
| Computer hub                 | `/computers/`                                                      | Index                               | Self                                                  | Главная → Компьютеры                       | CollectionPage + BreadcrumbList                                  | Да                                           | Утверждённые семейства / navigation hierarchy            |
| PLAY family                  | `/computers/play/`                                                 | Index                               | Self                                                  | Главная → Компьютеры → PLAY                | CollectionPage + BreadcrumbList; ItemList при реальных сущностях | Да                                           | Family content + каталог PLAY                            |
| CREATE family                | `/computers/create/`                                               | Index при готовом workflow-content  | Self                                                  | Главная → Компьютеры → CREATE              | CollectionPage + BreadcrumbList                                  | Да после публикации                          | CREATE family content                                    |
| WORK family                  | `/computers/work/`                                                 | Index при готовом task-content      | Self                                                  | Главная → Компьютеры → WORK                | CollectionPage + BreadcrumbList                                  | Да после публикации                          | WORK family content                                      |
| PLAY model                   | `/computers/play/{model}/`, текущий `/computers/play/1440/`        | Index                               | Self                                                  | Главная → Компьютеры → PLAY → Модель       | Product + BreadcrumbList; Offer только из backend                | Да                                           | Product entity + Bitrix catalog/Sale                     |
| CREATE model                 | `/computers/create/{model}/`                                       | Index при реальной модели           | Self                                                  | Главная → Компьютеры → CREATE → Модель     | Product + BreadcrumbList; backend Offer                          | Да после публикации                          | CREATE product entity + catalog/Sale                     |
| WORK model                   | `/computers/work/{model}/`                                         | Index при реальной модели           | Self                                                  | Главная → Компьютеры → WORK → Модель       | Product + BreadcrumbList; backend Offer                          | Да после публикации                          | WORK product entity + catalog/Sale                       |
| Projects list                | `/projects/`                                                       | Index                               | Self                                                  | Главная → Проекты                          | CollectionPage + BreadcrumbList                                  | Да                                           | Project content repository / инфоблок                    |
| Project detail               | `/projects/{slug}/`                                                | Index                               | Self                                                  | Главная → Проекты → Название               | Article + BreadcrumbList                                         | Да                                           | Реальный project content, media, dates/author            |
| Equipment hub                | `/equipment/`                                                      | Index при curated content           | Self                                                  | Главная → Оборудование                     | CollectionPage + BreadcrumbList                                  | Да                                           | Редакционно утверждённые категории                       |
| Equipment category           | `/equipment/{category}/`, `/equipment/monitors/`                   | Index при полезном содержании       | Self                                                  | Главная → Оборудование → Категория         | CollectionPage + BreadcrumbList                                  | Да                                           | Category content + каталог                               |
| Ordinary product             | `/equipment/{category}/{slug}/`                                    | Index                               | Self                                                  | Главная → Оборудование → Категория → Товар | Product + backend Offer + BreadcrumbList                         | Да                                           | Product entity, real media, catalog/Sale                 |
| Contacts                     | `/contacts/`                                                       | Index                               | Self                                                  | Главная → Контакты                         | ContactPage + BreadcrumbList                                     | Да                                           | Централизованные настройки контактов                     |
| Cart                         | `/cart/`                                                           | noindex                             | Нет                                                   | Не обязательны                             | Нет Product/Offer                                                | Нет                                          | Sale basket / текущий пользовательский контекст          |
| Checkout                     | `/checkout/`                                                       | noindex                             | Нет                                                   | Не обязательны                             | Нет                                                              | Нет                                          | Sale order, методы/ограничения/properties                |
| Order success                | `/order-success/`                                                  | noindex                             | Нет                                                   | Не обязательны                             | Нет                                                              | Нет                                          | Sale order + доступ текущего пользователя                |
| Internal search              | `/search/?q={query}`                                               | noindex                             | Нет                                                   | Главная → Поиск, при необходимости         | Нет                                                              | Нет                                          | Search context; не SEO phrase generator                  |
| Account / private            | `/account/`, `/account/{section}/`                                 | noindex + контроль доступа          | Нет                                                   | UI hierarchy по контексту                  | Нет                                                              | Нет                                          | Авторизация + приватные сущности                         |
| Unapproved facets / sort     | `{category-url}?filter=…`, `?sort=…`                               | noindex                             | Нет; не создавать SEO routes автоматически            | Базовая категория                          | Не генерировать отдельные Product/Offer по фильтрам              | Нет                                          | Catalog filter UI; whitelist отсутствует в v1            |
| Configurator state           | `{model-url}?ram=…&ssd=…&case=…` если нужны presentation-параметры | Не отдельная indexable сущность     | Primary model Self, состояние не SEO URL              | Та же модель                               | Один primary Product                                             | Нет отдельных entries                        | Presentation state; backend владеет заказом              |
| Реальная пагинация           | `/projects/?page={n}`, `/equipment/{category}/?page={n}`           | Index при реальных страницах списка | Self для каждой страницы; не canonical всех на page 1 | Тот же раздел                              | CollectionPage + BreadcrumbList                                  | Основные сущности; pagination не обязательна | Server pagination / content repository                   |
| 404 missing URL              | Любой отсутствующий URL                                            | noindex, HTTP 404                   | Нет                                                   | Не нужны                                   | Нет                                                              | Нет                                          | Router/server error handler                              |
| 500 failure                  | URL с internal failure                                             | noindex, HTTP 500                   | Нет                                                   | Не нужны                                   | Нет                                                              | Нет                                          | Server exception handler / static fallback               |
| 503 maintenance              | Запрошенный URL при недоступности                                  | noindex, HTTP 503                   | Нет                                                   | Не нужны                                   | Нет                                                              | Нет                                          | Server maintenance gate; Retry-After при известном сроке |
| Намеренно удалено без замены | Бывший content URL                                                 | noindex, возможен HTTP 410          | Нет                                                   | Не нужны                                   | Нет                                                              | Нет                                          | Content lifecycle + router; дизайн 410 не добавлен       |
| Development / review         | Непубличная среда, static prototype                                | noindex, nofollow, noarchive        | Нет                                                   | Только для проверки компонентов            | Safe semantic scaffold, без mock Offer                           | Нет                                          | Environment/template policy                              |

Состояние конфигуратора не является результатом фильтра каталога: изменяет
presentation/заказ одной модели и не создаёт индексируемые URL. Для нормализации
прямых configuration URLs будущий сервер должен определить модель как основную
сущность и согласовать canonical/redirect без потери необходимого заказу состояния.

## Breadcrumb hierarchy и static mapping

| Static review                                        | Production                                  | Видимый путь                                          |
| ---------------------------------------------------- | ------------------------------------------- | ----------------------------------------------------- |
| `index.html`                                         | `/`                                         | Главная                                               |
| `computers.html`                                     | `/computers/`                               | Главная → Компьютеры                                  |
| `create.html`                                        | `/computers/create/`                        | Главная → Компьютеры → CREATE                         |
| `work.html`                                          | `/computers/work/`                          | Главная → Компьютеры → WORK                           |
| `catalog.html`                                       | `/computers/play/`                          | Главная → Компьютеры → PLAY                           |
| `product.html`                                       | `/computers/play/1440/`                     | Главная → Компьютеры → PLAY → PLAY 1440               |
| `projects.html`                                      | `/projects/`                                | Главная → Проекты                                     |
| `project.html`                                       | `/projects/{approved-slug}/`                | Главная → Проекты → Белый игровой компьютер           |
| `equipment.html`                                     | `/equipment/`                               | Главная → Оборудование                                |
| `monitors.html`                                      | `/equipment/monitors/`                      | Главная → Оборудование → Мониторы                     |
| `monitor.html`                                       | `/equipment/monitors/{approved-slug}/`      | Главная → Оборудование → Мониторы → MSI MAG 274QF X24 |
| `contacts.html`                                      | `/contacts/`                                | Главная → Контакты                                    |
| `cart.html` / `checkout.html` / `order-success.html` | `/cart/` / `/checkout/` / `/order-success/` | Транзакционные экраны                                 |

В прототипе «Компьютеры» теперь реальный ancestor link `computers.html`.
Catalog/Product/CREATE/WORK имеют тот же путь в видимых crumbs и JSON-LD;
PLAY на Product использует `catalog.html`. Hub сам — current final item.
Каждый non-final ListItem имеет `item`; final может его опустить. Допустим
URL string или `item: {"@id": URL}`. В production server hierarchy формирует
абсолютные canonical paths. Static prototype URLs не определяют hostname.

CREATE/WORK теперь имеют review landing pages, но **production readiness rule
матрицы не меняется**: наличие static design не является publication approval.
Модели/slugs/Offers не добавлены. См. [Computer Families v1](KORSAC-COMPUTER-FAMILIES-EXPERIENCE.md).

Projects реализуют case archive команды King-Komp: list + один local detail,
прочие записи ведут к реальным originals. `project.html` — review fixture,
не final slug; legacy slug не является автоматическим KORSAC canonical.
Исторические проекты не выдаются за модели KORSAC. Article не содержит
выдуманных author/date/image/measurements; absent sections не заполняются.
См. [Projects content/source contract](KORSAC-PROJECTS-EXPERIENCE.md).

Equipment review теперь реализован: три source-verified monitors, один local
ordinary Product detail, остальные records ведут к своим King-Komp originals.
`monitor.html` не утверждает production slug/ассортимент. Prototype completion
не меняет publication/indexability gates. Price/availability/Offer/basket
остаются backend-owned; demo monitor line — PRODUCT, не PC CONFIG.
Shared Media Viewer, System Passport и Bitrix migration не реализованы.
См. [Equipment contract](KORSAC-EQUIPMENT-EXPERIENCE.md).

## URL, navigation и sitemap

Clean content URL заканчиваются `/`; альтернативы нормализуются серверным
redirect, не JavaScript. Canonical host пока не известен. Единственная
утверждённая scheme/host/trailing-slash версия согласуется с navigation,
canonical, redirects и sitemap. UTM/tracking не меняют основное содержимое
и не становятся отдельными entries; canonical исключает tracking.

Ссылки основного пути — настоящие `<a href>` в server-rendered HTML:
Home → семьи → модели; модели → релевантные проекты/оборудование;
проекты → соответствующее семейство/модель; оборудование → связанные системы.
Нереализованные будущие страницы не имеют активных ссылок в static prototype.
Contacts доступны через footer, header density сохраняется.

Bitrix генерирует sitemap из опубликованных indexable canonical сущностей.
Исключаются private/transaction/search/filter/sort/configuration/review/error URL,
пустые категории и draft. Sitemap не управляет индексированием вместо robots.
Production XML и robots.txt сейчас не создаются. Пагинация будущих Projects/
Equipment имеет crawlable ссылки на каждую реальную страницу; infinite scroll
может дополнять их, но не заменять. Не canonical все pages на первую.

## Self-review A–L

- **A:** полное production дерево выше не зависит от `.html` review-файлов.
- **B:** PLAY/CREATE/WORK имеют собственные namespaces и независимые модели.
- **C:** «Проекты» — case studies сборок, не Blog; Article не меняет их роль.
- **D:** Equipment публикуется по полезности содержания, без массового supplier dump.
- **E:** матрица отделяет опубликованные content entities от transactional/technical state.
- **F:** audit запрещает Offer/AggregateOffer/Review/AggregateRating в prototype; demo цены не вошли в schema.
- **G:** server template получает metadata, schema и breadcrumb hierarchy от page/entity context; globals имеют одного владельца.
- **H:** каждый HTML имеет явный noindex. Это инструкция crawler, не защита доступа: публичный hosting обязан сохранить её; закрытый staging предпочтителен. Реальный deployment и индексы не проверялись.
- **I:** production router обязан вернуть 404; static server отвечает 200 и не доказывает этот контракт.
- **J:** 503 использует standalone CSS/local asset, без JS/Bitrix; production server должен отдавать её вне неисправного приложения.
- **K:** Contacts содержит только неподтверждённые slots, без выдуманных телефона/email/адреса/графика.
- **L:** будущие Projects/Equipment/CREATE/WORK могут использовать зафиксированные URL, источники и SEO policy без нового архитектурного разделения.

См. [SEO foundation](KORSAC-SEO-FOUNDATION.md),
[Generic pages](KORSAC-GENERIC-PAGES.md), [Review](review/seo-foundation-v1.md).
