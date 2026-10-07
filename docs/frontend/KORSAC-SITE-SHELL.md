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

Desktop: утверждённый horizontal SVG lockup, пять навигационных ссылок и Search / Account / Cart.
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

## Approved brand assets

Публичный Header и Drawer используют `assets/images/brand/korsac-lockup-horizontal.svg`
из утверждённого V2. Width: **164 px desktop / 140 px mobile**, без увеличения
88/64 px header. Link сохраняет один `aria-label="KORSAC — главная"`, image —
пустой `alt`. Иконки utility остаются 44×44 px. Знак и wordmark не анимируются.
Практический header gap — 32 px desktop / 12 px mobile; это layout spacing,
не формальная brand clear-space норма.

```html
<a class="k-site-brand" href="index.html" aria-label="KORSAC — главная">
  <span class="k-brand-wordmark" data-brand-wordmark>
    <img
      src="assets/images/brand/korsac-lockup-horizontal.svg"
      width="450"
      height="100"
      alt=""
    />
  </span>
</a>
```

`data-brand-wordmark` теперь содержит реальный asset. Empty mark slot удалён
из статического lockup; `data-brand-mark-motion` остаётся у UI Kit replay.
Отдельного дублирующего logo controller нет. Все static instances — external
SVG; fragment IDs не пересекаются с документом или друг с другом.

Footer: V1 stacked lockup шириной **224 px**. До 600 px тот же `<picture>`
переключает asset на horizontal V2 шириной **200 px**, сохраняя компактность.
CSS резервирует aspect ratio обеих версий до image load; `object-fit: contain`
сохраняет геометрию. Глаза выключены во всех статических web assets, никаких
hover/viewport logo effects нет. Masters остаются неизменными.

Hero использует static external ICON с eyes off. Автоматический Hero Eye
Flash и `korsac:hero-enter` удалены. Animated geometry теперь принадлежит
общему [Brand Intro](KORSAC-BRAND-ASSET-INTEGRATION.md), не homepage controller.

## Site-entry Brand Intro

Только `index.html`, `catalog.html`, `product.html`: единая декоративная
full-viewport композиция mark → real eyes → wordmark → eyes off → exit.
Target 1500 ms; JS watchdog 1700 ms и независимый CSS safety cutoff 1800 ms.
`review.html`/`ui.html` не запускают intro и не расходуют eligibility.

Небольшой inline head boot проверяет `korsac:brand-intro:lastShown` и пишет
`Date.now()` **до** активации. Следующий вход/navigation/reload/new tab на том
же origin/browser profile пропускает intro, пока не прошли rolling 24 часа.
Это browser-local timestamp, не account/device sync; backend, cookies или
consent dependency не используются. При отказе localStorage — sessionStorage;
если оба недоступны, direct page access без intro. Session fallback действует
в пределах tab session, без гарантии общей частоты между независимыми tabs.

Reduced Motion записывает timestamp, но не включает overlay. Live toggle
немедленно скрывает overlay через CSS и отменяет effects через controller.
Возврат к normal motion не запускает intro заново. Hero/header/footer статичны.

Overlay hidden по умолчанию, `aria-hidden`, без focusable content/aria-live.
Head boot включает только presentation attribute; motion — external
`brand-intro.js`. Нет scroll lock, inert/focus trap, focus/scroll restoration
или layout insertion. Native controls становятся доступны после exit без
смещения. CSS safety скрывает и отключает pointer blocking даже при отказе
controller; broken/missing CSS оставляет нативный hidden state.

## Reduced-motion mode

Общий CSS сохраняет 80/120 ms opacity/color/border feedback вместо global
`animation/transition: none`. Navigation underline не растёт: static rail
появляется через opacity. Native dialogs/drawer/accordion могут коротко
settle по opacity без translate. Focus, hover и selected/validation states
остаются видимыми и не ждут motion completion. Hero/каталог/Explorer используют
[общую policy](KORSAC-VISUAL-MOTION-DIRECTION.md#reduced-motion-и-отсутствие-js).
Полный site-entry Brand Intro по-прежнему skipped с timestamp write.

## Footer

Один главный жест — утверждённый stacked metallic lockup с «Точно под задачу.».
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
Footer anatomy раскрывается через `details`; Brand Assets показывает все варианты
и отдельный безопасный Eye Flash replay. Сам UI Kit использует публичную
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
