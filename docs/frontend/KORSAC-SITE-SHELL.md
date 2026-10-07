# KORSAC — Premium Site Shell v1

## Назначение

Оболочка соединяет главную, каталог и продукт в один сайт. На публичных
страницах нет постоянных `DIRECTION`, `VISUAL REV`, `KORSAC / SYSTEMS`
и prototype bars. Инженерные обозначения остаются внутри содержательных
product/catalog блоков; глобальная навигация использует обычный sans,
свободное пространство и короткий active rail.

`index.html`, `catalog.html`, `product.html` и `ui.html` используют один
markup pattern, `assets/css/shell.css` и `assets/js/shell.js`. Различия —
только current navigation и homepage state. В статическом прототипе HTML
развёрнут в каждой странице для no-JS; отдельных публичных CSS-реализаций
header/footer нет. `review.html` сохраняет прежнюю оболочку для разработки.
[Главная](KORSAC-HOMEPAGE-EXPERIENCE.md) описана отдельно.

## Header

Desktop: text wordmark, пять навигационных ссылок и Search / Account / Cart.
Иконки — локальный inline SVG с `aria-hidden` и без icon library. Utility
links имеют русские `aria-label`, visible focus и область 44×44 px. Без JS
они ведут к пояснению в footer; JS открывает существующий native dialog,
сохраняя URL. Реальных поиска, аккаунта и корзины нет.

Маршруты:

| Название     | Маршрут и смысл                                            |
| ------------ | ---------------------------------------------------------- |
| Компьютеры   | `catalog.html`, текущая линейка PLAY                       |
| Конфигуратор | `product.html#configurator`, существующий пример PLAY 1440 |
| Для бизнеса  | `index.html#business`, WORK явно в разработке              |
| Поддержка    | `product.html#warranty`, существующий раздел               |
| О KORSAC     | `index.html#why`, подход бренда                            |

Active state — короткая Electric Blue линия и `aria-current`. Filled pills,
технические индексы и рамки вокруг utility actions отсутствуют.

На главной header sticky, **88 px desktop / 64 px mobile**, без изменения
размеров. Один IntersectionObserver следит за hero boundary с небольшим
запасом высоты header. При выходе из hero появляется graphite surface;
переход использует `--k-motion-base` **220 ms**. Нет scroll handlers,
resize/shrink animation, blur, scroll-jacking и смещения содержимого.
Без IO/JS остаётся стабильная тёмная поверхность.

В каталоге, продукте и UI Kit header сразу тёмный и остаётся в обычном
потоке. Это сохраняет принятую компоновку первого экрана Explorer и
локальные product controls. Sticky здесь не требуется. Homepage anchors
учитывают высоту закреплённой панели; внутренние страницы сохраняют обычный
scroll padding. Layout/motion интерфейса каталога и продукта не переработаны.

## Mobile и no-JS

До 1100 px верхняя строка: **KORSAC / Cart / Menu**. Search/account перенесены
в drawer. Используется прежний native `dialog`: Escape, backdrop close,
focus containment, opener return и `aria-expanded`. Ссылки закрывают drawer
и переходят обычным способом. Крупные названия, спокойные интервалы и
отсутствие numeric indices поддерживают новую иерархию.

Menu-button появляется только после enhancement. Без JS вместо неё есть
нативный `details` с теми же навигационными ссылками. Он имеет тот же размер,
поэтому включение JS не меняет высоту header. Utility anchors ведут к
`#site-prototype`, где честно объяснена граница прототипа.

## Brand slot и будущие assets

Текущий `KORSAC` — временный текст, не финальный логотип. Ни fox/totem SVG,
ни custom letterforms, ни raster tracing не созданы.

Стабильный lockup:

```html
<a class="k-site-brand" href="index.html" aria-label="KORSAC — главная">
  <span class="k-brand-mark" data-brand-mark-motion aria-hidden="true"></span>
  <span class="k-brand-wordmark" data-brand-wordmark>KORSAC</span>
</a>
```

После утверждения знак вставляется в `k-brand-mark`, wordmark SVG — в
`data-brand-wordmark`. `--k-brand-mark-size` и `--k-brand-mark-gap` выделяют
место под знак; сейчас оба равны 0. `--k-brand-wordmark-width` задаёт ширину
SVG, footer использует свой масштаб. Задавайте реальный `viewBox`/dimensions
asset и сохраняйте доступное название ссылки. `COMPUTERS` добавляется только
в согласованный extended lockup, не в каждый header по умолчанию.

`data-brand-mark-motion` — будущая точка подключения короткой вспышки глаз
внутри **утверждённого** SVG. Сейчас hook не запускает эффекты. Eye layers
и их конечная последовательность подключаются после появления вектора,
с тем же reduced-motion cleanup. Выдуманных glowing eyes нет.

Layout probe с нейтральным 32 px слотом проверил header height и отсутствие
overflow на 320/768/1440/1920 px. Это проверка размеров, не разработка знака.

## Footer

Один главный жест — большой спокойный wordmark с «Точно под задачу.».
Рядом открытые группы «Продукты», «Компания», «Поддержка»; без карточек,
serial markers, повторной рамки и набора декоративных rails. На mobile бренд
отделён от двух колонок ссылок; support занимает следующую строку.

Bottom line: `KORSAC by King-Komp`, placeholder юридических документов,
ссылка в review hub и одно небольшое пояснение «Визуальный прототип».
Адреса, телефоны, почта, social accounts, регистрационные данные и сроки
гарантии не выдуманы. Utility placeholders не представлены работающим магазином.

## UI Kit

`Premium Site Shell` показывает hero-integrated и graphite состояния,
utility icons, мобильную анатомию и нативное открытие реального drawer.
Footer anatomy раскрывается через `details`. Сам UI Kit использует публичную
оболочку; developer metadata находится в содержании, не над header.
`review.html` обеспечивает отдельный доступ ко всем prototype pages.

## Future Bitrix mapping

| Область                  | Будущая интеграция                                 |
| ------------------------ | -------------------------------------------------- |
| Header/footer markup     | `local/templates/korsac/header.php` / `footer.php` |
| Navigation/current state | SSR menu и текущий маршрут                         |
| Brand slot               | Утверждённые локальные SVG assets                  |
| Search                   | Реальный site search                               |
| Account                  | Bitrix auth/profile                                |
| Cart                     | Bitrix sale basket state                           |
| Footer/legal             | Согласованные include areas и реальные документы   |

Native dialog в прототипе — пояснение, не auth/search/cart adapter. Текущие
IDs/data attributes описывают presentation и не становятся backend contract.
Bitrix/PHP/API в этом PR не реализованы.

## Проверка и human gate

[Материалы](review/README.md) показывают homepage, public header/footer,
drawer и оболочку на catalog/product. HTTP Chromium-проверки охватывают
320/375/430/768/1024/1280/1440/1920 px, keyboard, touch375/430, no-JS320,
visible focus, native dialogs и reduced motion. Отдельно проверены прежние
catalog/product взаимодействия и статические цены.

Human acceptance: header должен читаться как спокойная consumer technology
навигация; footer — как завершение бренда. Проверить реальный keyboard/focus,
ссылки и target browsers. Снимки и MP4 не заменяют live-review. PR не сливается
автоматически. `file://` ограничен политикой среды; Firefox/Safari и физические
устройства не проверены.
