# KORSAC — Cart & Checkout Experience v1

## Назначение и граница прототипа

Cart отвечает, какие системы выбраны и чем отличаются их конфигурации.
Checkout — одна спокойная страница для гостя или компании. Success показывает
будущее завершение оформления, явно помеченное `DEMO / ORDER`.

**Production pricing — только backend / Bitrix Sale.** Frontend никогда не
рассчитывает authoritative configuration/item price, discount, delivery, tax,
payment surcharge или final order total. В этом PR нет Bitrix, `kk.korsac`,
pricing/logistics/payment API, настоящего заказа или basket persistence.

Основа: `main` на `7acd51ab55746dd3c6681aec2d51aaf101dc315f`, включающий PR #7.

## Страницы, shell и Brand Intro

- `prototype/cart.html`: обычный public shell, sticky opaque header, native drawer,
  footer. Cart utility на Homepage/Catalog/Product теперь ведёт сюда; поиска и
  аккаунта по-прежнему нет. Count badge не добавлен.
- `prototype/checkout.html`: sticky logo + название оформления + возврат в Cart;
  компактный footer, без marketing navigation. Mobile: logo / Оформление / Назад.
- `prototype/order-success.html`: тот же спокойный shell, статическая approved mark,
  результат, будущие шаги и краткая сводка.
- `prototype/review.html`: все три страницы доступны из review hub.
- `prototype/ui.html#commerce-primitives`: cart line, CONFIG discriminator, quantity,
  summary, delivery/payment choices, field/error, CTA и empty state.

**Все три транзакционные страницы исключены из daily Brand Intro.** На них нет
inline intro boot, overlay, intro CSS/controller. Они не читают/не записывают его
24h timestamp. Header/footer artwork остаётся статическим; browsing intro policy
Homepage/Catalog/Product не меняется. Нет Hero-like entrance или field-by-field
stagger.

## Cart line и identity

Семантический `article[data-demo-cart-line]` — источник строки. Две PLAY 1440
различаются сразу, без раскрытия:

| Пример      | RAM        | Основной SSD  | Корпус-кандидат      | Дополнительные опции                                                            |
| ----------- | ---------- | ------------- | -------------------- | ------------------------------------------------------------------------------- |
| CONFIG / 01 | 32 ГБ DDR5 | 1 ТБ NVMe TLC | Lian Li LANCOOL 217  | Второй SSD не установлен; Без ОС; софт не выбран; Базовый сервис                |
| CONFIG / 02 | 64 ГБ DDR5 | 2 ТБ NVMe TLC | Fractal Design North | 1 ТБ NVMe; Windows 11 · макет; Microsoft Office Trial; Помощь с первым запуском |

CPU Ryzen 7 9700X / GPU GeForce RTX 5070 · 12 ГБ — базовый класс обеих систем.
Все выбранные значения взяты из текущих `data-summary-value` в Product.
Совместимость не выводится из этих значений. Корпуса сохраняют статус shortlist
кандидатов. Media — компактная локальная CSS-схема, не фотография.

`CONFIG / 01` и `CONFIG / 02`, `data-cart-config` — generic prototype metadata,
**не SYSTEM ID, серийный номер, property/XML ID или production contract**.
SYSTEM ID относится к построенной системе позднее.

CPU/GPU/RAM/SSD/Case всегда видимы. Изменённые RAM/SSD/Case второй строки выделены
весом текста и короткой синей меткой. Дополнительный SSD, OS, Software и Service
доступны в нативном `details`. Это сводка каждой строки, не compare table.

«Изменить конфигурацию» ведёт в `product.html#configurator`. Восстановления
выбранных опций из Cart нет; production будет передавать canonical configuration
identity/state из `kk.korsac`.

## Demo arithmetic и взаимодействия Cart

`cart-experience.js` работает только внутри `[data-demo-cart]`, включая отдельный
UI Kit specimen. Данные не продублированы в JS object. В каждой строке авторское
`data-demo-unit-price-minor="17990000"`; обе используют существующий пример
179 900 ₽, без новых цен за выбранные компоненты. Исходный subtotal — 359 800 ₽.
Одинаковые sample amounts не утверждают реальную цену конфигураций.

**Prototype display arithmetic only**: `updateDemoCartSummary` читает integer
minor units из HTML, умножает на quantity и суммирует видимые строки. Деление на
100 происходит только для `Intl.NumberFormat("ru-RU")` display. RAM/SSD/Case/
software/service никогда не участвуют в вычислении. Safe-integer guard защищает
числовое представление, это не business maximum quantity.

Quantity — native buttons 44×44px и читаемый `output`. Minimum 1; arbitrary max
не задан. При уменьшении до 1 фокус переходит на доступный `+`, а не остаётся
на disabled button. Изменение обновляет стоимость строки и subtotal/total по
товарам. Delivery не имеет цены: «Рассчитывается при оформлении».

Remove скрывает авторскую строку. Последнюю удалённую строку можно восстановить
с прежним локальным quantity. После удаления обеих остаются shell, intentional
empty state и Catalog CTA. Последний Undo остаётся доступен, клавиатурный фокус
не теряется. Перезагрузка восстанавливает исходный HTML fixture.

Один polite live region объявляет результат действия, число систем и demo total.
Остальные DOM updates не являются отдельными live regions.

**Нет cross-page cart state**: Checkout/Success используют собственную авторскую
исходную сводку двух систем. Изменённые количества/удаления туда не переносятся;
Cart перед CTA и Checkout перед формой явно объясняют это. Нет localStorage,
sessionStorage, cookies, query payload или глобального live cart count.
UI Kit summary справа — самостоятельный статический specimen.

## Single-page guest / company Checkout

Последовательность: покупатель → доставка → оплата → подтверждение. Регистрация,
wizard, hardware editor и account gate отсутствуют. Контактные inputs нативные:
name, tel, email, правильные type/inputmode/autocomplete. Поля имеют font-size
16px. Имя/Телефон/Email — обязательны.

Native buyer radios выбирают «Частное лицо / Компания». Компания получает:
Контактное лицо, Телефон, Email, Название организации, ИНН; КПП необязателен.
У выключенного company fieldset поля disabled, conditional required снят.
В активном company mode организация/ИНН обязательны. Нет company lookup,
DaData, production INN regex или фиктивной проверки реквизитов.

Individual: СБП / Наличные. Company: Счёт без НДС и текст о реквизитах.
Неактуальные payment radios disabled и hidden; invoice выбирается при переходе
к Company. При возврате сохраняется последний retail выбор. Все choices —
компактные native selection rows, без provider logos, QR, карты, кредитов,
рассрочки или финансовой логики.

## Delivery / СДЭК

Один CDEK вариант: пункт выдачи / постамат. Курьер — будущая возможность там,
где он поддерживается backend integration; сейчас выбрать/обещать его нельзя.

«Выбрать пункт выдачи» открывает native dialog. Authored picker переносится
из открытого no-JS блока в dialog; radio сохраняет `form="checkout-form"`.
Представлены disabled city/address search, CSS map area, список с одним
**«Демонстрационным пунктом · без физического адреса»** и подтверждение примера.

Никаких map libraries/requests, реальных или вымышленных физических адресов,
доставочных тарифов, `0 ₽`, сроков или stock/shipping promises. Выбранное
состояние: «Пункт выдачи выбран · пример, без физического адреса».
Native selection сразу становится состоянием формы; Escape закрывает dialog,
сохраняя выбранный пример. Доставка required, стоимость остаётся неизвестной.

## Review, comment, consent и submit

Desktop summary sticky ниже header: CONFIG / 01 / 02, quantities, subtotal,
delivery status, total по товарам, «Изменить корзину». Полная конфигурация здесь
не повторяется. На mobile summary — компактный disclosure до формы; перед
единственной Submit CTA total показан повторно. Mobile CTA в normal flow:
нет fixed bottom bar, duplicate focus targets или перекрытия keyboard/content.

Comment — secondary `details`. Required consent — native checkbox, ссылки на
локальное обозначение будущих privacy/terms документов. Legal URLs и финальные
юридические формулировки не выдуманы. Disclosure объясняет статус макета.

«Прототип оформления — заказ не отправляется» находится отдельно от primary
label. Валидный JS submit делает только `location.assign("order-success.html")`.
Никакого endpoint, fetch, payment initiation, email/SMS, сохранения контактов
или реального order object.

## Validation и accessibility

JS включает `noValidate`, читает native `willValidate` / `validity`, формирует
короткую focused error summary с links к ошибочным полям/секциям. Required,
email type, phone presence, активные company fields, pickup point, payment,
consent проверяются; aggressive input-time validation отсутствует. После первой
неудачной отправки выбор radio/checkbox обновляет ошибки; текстовые поля
перепроверяются на submit. Blur не удаляет строки ошибок под pending pointer click.
До submit пользователя не
прерывают. Нет exact production phone/INN regex.

У полей есть visible text errors, `aria-invalid` и `aria-describedby`; при
ошибке доставки ссылка открывает dialog и фокусирует native point radio.
Color/border дополняют текст, не заменяют его. Error summary получает фокус,
не noisy live region. Native details, fieldset/legend, radio/checkbox и dialog
сохраняют keyboard semantics. Dialog: Escape, trap, background inert и возврат
на opener через existing generic controller. Cart utility имеет `aria-current`.

## Mobile, motion и no-JS

Контейнер ограничен текущими 1360px; desktop inputs не растянуты на весь экран.
На 320–430px cart line идёт model/CONFIG → media → specs → price+quantity →
edit/remove. Нет side-by-side mobile spec matrix или горизонтальной прокрутки.
Контакты/реквизиты — одна колонка; buyer choices остаются 2 компактными rows.
Header height постоянна 88/64px, native dialog выше sticky shell.

Motion — finite opacity/color acknowledgement и immediate selected rails,
без маркетинговой последовательности. Central normal/reduced tokens используются
для totals/company/payment/pickup feedback. Reduced: 110ms hover/focus/selection,
180ms meaningful opacity feedback (.76→1); без transform/scale/clip/stagger.
Live preference change отменяет active WAAPI effects, state остаётся правильным.
Существующий reduced native dialog branch — opacity-only 180ms. Brand Intro
на transactional pages отсутствует при любых preferences.

No-JS Cart: исходные строки/quantity/prices читаемы, details и checkout link
работают. Quantity/remove enhanced controls скрыты.
No-JS Checkout: обе buyer groups и все payment methods доступны, company fields
помечены для Company (не условно required), picker — открытый блок native controls внутри
формы. Required contacts/pickup/consent и native email validity остаются.
Submit открывает статический success через обычную GET document navigation.
**У контактных/company/comment inputs нет `name`: личные данные никогда не
сериализуются даже без JS.** Только demo-mode radios могут появиться в URL;
Success их не читает. Company required conditional / custom summary доступны
при JS. Пример checkout остаётся понятным без enhancement.

## Success и будущий production contract

«Заказ принят» соседствует с `DEMO / ORDER`, явным текстом «реальный заказ не
создан» и исходной сводкой. Нет plausibly real order ID, «email отправлен»,
«оплата принята», «доставим завтра» или иной имитации произошедшего события.
Будущие шаги описаны в будущем времени.

| Prototype responsibility                | Future mapping — не реализовано                                                                             |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Cart HTML lines                         | `bitrix:sale.basket.basket` template                                                                        |
| CONFIG discriminator, canonical options | Basket properties/data supplied by `kk.korsac`; production identity carried through edit                    |
| Unit amount                             | Bitrix Catalog/Sale authoritative price                                                                     |
| Quantity                                | Sale basket quantity                                                                                        |
| Remove                                  | Sale basket item removal                                                                                    |
| Checkout                                | `bitrix:sale.order.ajax` или KORSAC wrapper/template                                                        |
| Buyer/company fields                    | Bitrix order properties                                                                                     |
| Delivery/pickup                         | Bitrix delivery services / CDEK integration                                                                 |
| Payment choices                         | Bitrix payment systems                                                                                      |
| Subtotal/final total                    | Sale order calculation, включая delivery/discount/tax                                                       |
| Success                                 | Реальный order state/result: order number, payment instruction, delivery status, contact/email confirmation |

Frontend будет отображать canonical data и authoritative backend values.
Generic demo selectors не объявляют production property/XML IDs. Prototype
arithmetic/controller заменяются реальным owner, не расширяются до pricing engine.

## Review и self-review A–J

[Снимки и MP4 в обычной скорости](review/README.md#cart--checkout-experience-v1).

- A: две конфигурации различаются CONFIG и видимыми RAM/SSD/Case, без раскрытия.
- B: approved shell, copper identity и compact blue state rails сохраняют KORSAC.
- C: base/core specs открыты; вторичные опции в native disclosure.
- D: одна страница, без marketing nav/intro, ровная иерархия четырёх секций.
- E: guest contacts → delivery → payment → consent → static success, без аккаунта.
- F: компания имеет отдельный блок реквизитов, contact wording и invoice-first flow.
- G: normal-flow CTA, 16px native inputs, touch controls, focused errors; реальный
  software keyboard требует human review на физическом устройстве.
- H: только authored integer display arithmetic; нет component-based pricing/persistence.
- I: basket/config identity/order fields/summary mapping выделены, Bitrix не подключён.
- J: calm transactional shell и approved assets; motion служит state feedback.

Cloud проверяет Chromium/HTTP, media emulation и touch simulation. Не утверждаем
проверку физических устройств/Windows OS, Firefox/Safari или screen reader.
Human acceptance по скорости сканирования, B2B tone и keyboard остаётся review gate.
PR не сливать автоматически.
