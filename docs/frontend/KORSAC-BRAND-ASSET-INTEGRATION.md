# KORSAC — Brand Asset Integration & Logo Motion v1

## Approved artwork и web mapping

Работа основана на `main` **a46204e1fc30f09ed81183ac9323a73718bb4352**,
после принятой Premium Shell/Homepage PR #6. Исходники в
`prototype/assets/images/` неизменны, включая первоначальные blue eye shapes.
Визуально подтверждены ICON / TEXT / V1 stacked / V2 horizontal.

| Approved source master               | Web derivative в `prototype/assets/images/brand/` | Назначение                             |
| ------------------------------------ | ------------------------------------------------- | -------------------------------------- |
| `KORSAC_LOGO_ICON_FINAL_REVISED.svg` | `korsac-mark.svg`                                 | Static totem, UI Kit                   |
| `KORSAC_LOGO_TEXT_FINAL_REVISED.svg` | `korsac-wordmark.svg`                             | Отдельный wordmark, UI Kit             |
| `KORSAC_LOGO_V2_FINAL_REVISED.svg`   | `korsac-lockup-horizontal.svg`                    | Header, drawer, mobile footer          |
| `KORSAC_LOGO_V1_FINAL_REVISED.svg`   | `korsac-lockup-stacked.svg`                       | Desktop/tablet footer                  |
| `KORSAC_LOGO_ICON_FINAL_REVISED.svg` | `korsac-mark-motion.svg`                          | Eyes-off inline template для hero/demo |

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
не увеличен. На 1024 mark смещён влево, чтобы оба глаза были видны рядом с
корпусом. Headline, copy и ранняя mobile CTA сохраняют прежнюю компоновку.
Ambient blue уменьшен до 6%, маленький copper registration — до 18 px.

Static instances — внешние `<img>`: их defs изолированы браузером. Hero
содержит **один** inline SVG из motion template с `home-brand-` prefix.
Единственный UI Kit demo использует `kit-brand-` prefix в другом документе.
Все fragment references переписаны вместе с IDs; source SVG не вставляются
inline без prefix. Inline geometry сверяется с template; новые экземпляры
должны получать собственный prefix. Product/catalog content не изменён.

Выбран допустимый inline вариант вместо внутренней CSS animation external
SVG. Inline даёт родительской странице прямую отмену WAAPI и гарантирует,
что live reduced-motion toggle не запустит asset заново. External static
SVG остаются обычными локальными URLs. Motion template не содержит autoplay.

## KORSAC Eye Flash

`brand-motion.js` обслуживает прежний `data-brand-mark-motion` hook.
`homepage.js` отправляет `korsac:hero-enter` в начале существующей hero
последовательности. Однократный listener запускает эффект с **420 ms delay**
и duration `--k-motion-reveal` **620 ms**; общий entrance заканчивается через
**1040 ms** вместо прежних 940 ms. Отдельного scroll trigger/timer loop нет.

| Время относительно flash | Состояние                       |
| ------------------------ | ------------------------------- |
| 0 ms                     | Eyes off                        |
| ~112 ms                  | Быстрое появление (.85 opacity) |
| ~217–298 ms              | Краткий peak (1 opacity)        |
| ~434 ms                  | Затухание (.45 opacity)         |
| 620 ms                   | Eyes off; filter освобождён     |

WAAPI меняет opacity **реальных** SVG eye groups с оригинальными eye/core
polygons и gradients. Оригинальный `feGaussianBlur` остаётся локальным вокруг
глаз, только на время flash. У каждой фазы существующий easing token;
нет дополнительных glow layers, CSS-псевдоглаз, halo вокруг логотипа,
flicker, particles, sound или pointer tracking.

По завершении WAAPI возвращает base `opacity="0"`, filter удаляется.
Cancel также очищает filter/effects. Generation guard не позволяет finished
callback предыдущего replay сбросить новое состояние. Resize/scroll не
перезапускают hero, повторный enter event игнорируется. Header/drawer/footer
никогда не запускают eye motion.

Reduced Motion: CSS сразу принудительно выключает opacity/filter; media-query
listener отменяет active WAAPI. Возврат к normal motion не повторяет hero.
No-JS и unsupported WAAPI сохраняют видимый mark с глазами off. Без WAAPI
UI Kit replay disabled; без JS hidden. Информация/CTA от эффекта не зависят.

UI Kit **Brand Assets** показывает четыре static варианта и Eye Flash demo.
Replay доступен только там: предыдущий запуск отменяется, новый начинается
с нуля, final state всегда eyes off. Reduced Motion блокирует replay.

## Accessibility

Logo home link имеет единственное имя `KORSAC — главная`; внешнее image —
`alt=""`. Исходные внутренние `role/aria-label` удалены из web derivatives.
Hero wrapper/inline SVG декоративны (`aria-hidden`, `focusable="false"`).
UI Kit static figures имеют осмысленный image alt; demo один `role="img"`
на wrapper и отдельный status для review button. Нет повторного KORSAC
announcement внутри hero или фокусируемых SVG paths.

## Future Bitrix mapping

| Текущая область                  | Будущая интеграция                                     |
| -------------------------------- | ------------------------------------------------------ |
| Header/footer static derivatives | Template asset directory и обычные local SVG URLs      |
| Responsive footer picture        | `header.php` / `footer.php` template markup            |
| Animated hero mark               | Homepage include/component, один prefixed SVG template |
| Eye presentation controller      | Local template JS/CSS с теми же hooks и reduced motion |

Не хранить artwork как PHP strings; approved masters остаются отдельно от
web assets. У каждого будущего inline instance свой prefix. Search/profile/cart
здесь по-прежнему prototype-only, backend и pricing logic не добавлены.

## Validation и review

[Материалы](review/README.md) содержат 11 новых PNG и normal-speed Eye Flash
MP4. Chromium HTTP: 40 page/width layouts; native drawer/dialog/anchors;
catalog/scenario/comparison/MAX3; Product v3.1/Explorer/configurator/static
prices; no-JS; finite/reduced motion; 25 быстрых replay. Проверены masters,
geometry/gradients/fragments и загрузка logo с задержкой без CLS на
320/768/1440/1920. Обе eye shapes видны рядом с PC на восьми ширинах.
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
- E: peak краткий, blue локален вокруг настоящих eyes; субъективный motion feel требует human review.
- F: finish/cancel/replay возвращаются к base eyes-off; live toggle не оставляет glow.
- G: external isolation и уникальные inline prefixes исключают fragment collisions текущих экземпляров.
- H: CSS/JS reduced motion выключают effect полностью; возврат не повторяет hero.
- I: approved artwork заменяет placeholders без новых navigation rails/chrome.
- J: большой offset totem приближает атмосферу hero к brand direction; фотография пока provisional.
- K: semantic local assets и прежние shell hooks подходят для template/include migration.
- L: mobile/header/drawer/anchors и прежние product/catalog/configurator regressions прошли.
