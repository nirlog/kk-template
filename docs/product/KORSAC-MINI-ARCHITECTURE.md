# KORSAC MINI — Product Architecture v0.1

Дата: 2026-09-28

Статус: рабочая архитектура компактных KORSAC-систем.

Связанные документы:

- `docs/brand/KORSAC-BRAND-GUIDE.md`
- `docs/product/KORSAC-PLAY-ARCHITECTURE.md`

## 1. Назначение MINI

`MINI` — не отдельная линейка производительности и не бюджетная версия KORSAC.

Это обозначение компактного инженерного исполнения продукта на базе Mini-ITX, где сохранён исходный пользовательский сценарий основной модели.

Пример:

- `KORSAC PLAY 1440` — стандартное исполнение для 1440p;
- `KORSAC PLAY 1440 MINI` — тот же целевой игровой класс в компактном Mini-ITX формате.

Базовое сообщение:

> Та же производительность. Меньше объём.

Альтернативное продуктовое сообщение:

> Производительность PLAY 1440 в компактном Mini-ITX формате.

## 2. Почему MINI — отдельный товар

Переход на Mini-ITX затрагивает систему целиком и не должен моделироваться как простая опция корпуса.

Обычно меняются:

- материнская плата;
- блок питания;
- охлаждение CPU;
- корпус;
- допустимые физические модели GPU;
- fan layout;
- cable routing;
- температурный режим;
- акустический профиль;
- сложность сборки и тестирования.

Поэтому каждая MINI-модель имеет:

- отдельный товар Bitrix;
- собственную default configuration;
- собственные allowed options;
- собственный model code;
- собственную revision;
- отдельные thermal/noise test results.

## 3. Первая модель

Первым MINI-продуктом предлагается запускать:

`KORSAC PLAY 1440 MINI`

Причины:

- 1440p — центральный сценарий KORSAC PLAY;
- этот класс производительности достаточно заметен для premium compact-product;
- компактность даёт понятную дополнительную ценность;
- Mini-ITX аудитория обычно лучше принимает более высокую стоимость компонентов;
- продукт может стать визуально узнаваемой имиджевой моделью KORSAC.

`PLAY 1080 MINI`, `PLAY 1440 PRO MINI` и `PLAY 4K MINI` не вводятся автоматически. Каждая такая модель появляется только после проверки спроса, термики, шума, совместимости и экономики.

## 4. Product requirements: PLAY 1440 MINI

### Целевой сценарий

Игры в 2560×1440 на высоких настройках при сохранении компактного форм-фактора.

### Базовый класс компонентов

- CPU: balanced Ryzen 7 / сопоставимый gaming class;
- GPU: RTX 5070 class или эквивалентный по назначению;
- Motherboard: Mini-ITX, B850-class или сопоставимый актуальный chipset;
- Wi-Fi: обязателен;
- LAN: 2.5 GbE как целевой стандарт;
- RAM: 32 GB DDR5 default;
- SSD1: 1 TB NVMe default;
- SSD2: отсутствует по умолчанию;
- PSU: SFX или SFX-L, Gold-class, актуальный ATX/PCIe power standard;
- CPU cooling: только KORSAC-approved compact cooler/AIO;
- Case: только KORSAC-approved Mini-ITX cases.

Конкретные SKU не являются вечной частью публичного названия модели. Они фиксируются на уровне ревизии и конкретного `KORSAC SYSTEM ID`.

## 5. Требования к Mini-ITX motherboard class

Класс материнской платы должен хранить не только маркетинговое название chipset.

Минимально полезные атрибуты:

```text
FORM_FACTOR = MINI_ITX
CHIPSET
WIFI = Y
LAN_SPEED
RAM_TYPE
M2_COUNT
USB_CLASS
```

Дополнительно при необходимости:

```text
WIFI_STANDARD
VRM_CLASS
FRONT_USB_C_HEADER
PCIE_VERSION
```

Цель — не обещать конкретную физическую модель платы на карточке продукта, а гарантировать пользователю определённый функциональный класс.

## 6. Требования к PSU

Для MINI рекомендуется отдельный component class.

Пример:

```text
750W Gold SFX ATX 3.x
```

Полезные атрибуты:

```text
POWER_W
EFFICIENCY_CLASS
FORM_FACTOR = SFX | SFX_L
ATX_STANDARD
PCIE_POWER_STANDARD
MODULAR
```

Нельзя подменять Mini PSU обычной записью вроде `750W plus`: стоимость и физическая совместимость у компактной системы существенно отличаются.

## 7. Корпуса

Корпус MINI — критический компонент системы, поэтому одной ссылки на `Mini-Tower` недостаточно.

Для KORSAC-approved case желательно хранить:

```text
FORM_FACTOR
VOLUME_L
MAX_GPU_LENGTH_MM
MAX_GPU_HEIGHT_MM
MAX_GPU_SLOTS
MAX_CPU_COOLER_HEIGHT_MM
SUPPORTED_RADIATORS
PSU_FORMAT
FAN_LAYOUT
```

При необходимости:

```text
RISER_REQUIRED
RISER_INCLUDED
GPU_ORIENTATION
FRONT_IO
USB_C
```

Важно различать:

- внешний класс корпуса;
- реальные ограничения внутренней компоновки.

Два Mini-ITX корпуса одинакового объёма могут иметь совершенно разные ограничения для GPU и охлаждения.

## 8. GPU compatibility

Для MINI недостаточно свойства `RTX 5070`.

На уровне approved physical SKU нужно учитывать:

- длину;
- высоту;
- толщину / количество slots;
- расположение и пространство для power connector;
- рекомендованный airflow;
- тепловой режим конкретного исполнения.

Логика:

```text
GPU_CLASS = RTX_5070
        ↓
approved physical models
        ↓
compatibility with selected MINI case
```

Пользователю при этом можно показывать просто:

> GeForce RTX 5070 12 GB

а конкретный установленный производитель и SKU фиксируется в паспорте системы.

## 9. Cooling compatibility

MINI требует отдельного списка approved cooling solutions.

Нужно учитывать:

- CPU power/thermal profile;
- максимальную высоту air cooler;
- radiator support;
- radiator thickness;
- RAM clearance;
- motherboard clearance;
- влияние cooler/radiator на допустимые размеры GPU;
- noise profile.

Не следует автоматически считать AIO лучшим вариантом. Для каждой ревизии выбирается решение, которое проходит thermal/noise protocol.

## 10. Compatibility engine

MINI — первый сценарий, где простого списка `_OPTIONS` может быть недостаточно.

Базовая проверка должна учитывать совместимость как минимум между:

```text
CASE ↔ GPU
CASE ↔ PSU
CASE ↔ CPU_COOLER
CASE ↔ RADIATOR
CASE ↔ MOTHERBOARD
COOLER ↔ CPU thermal class
PSU ↔ GPU power class
```

На первом этапе правила могут быть реализованы через явные approved combinations, а не через универсальный экспертный движок.

Принцип:

> лучше небольшой whitelist проверенных сочетаний, чем сложный автоматический configurator, который допускает физически сомнительную сборку.

## 11. KORSAC-approved physical SKUs

HL-запись пользовательского component class и физический товар поставщика — разные уровни.

Пример:

```text
Component class:
750W Gold SFX ATX 3.x

Approved SKUs:
- Vendor A / Model A
- Vendor B / Model B
- Vendor C / Model C
```

Публичный сайт продаёт гарантированный класс.

Производство выбирает доступный approved SKU.

Фактически установленная модель фиксируется в `KORSAC SYSTEM ID`.

Так KORSAC может менять поставщика без изменения публичной карточки, сохраняя заявленный уровень продукта.

## 12. Pricing MINI

MINI не получает произвольную наценку только за компактность.

Базовая цена должна складываться из собственной default BOM:

```text
Mini-ITX motherboard
+ SFX/SFX-L PSU
+ compact cooling
+ MINI case
+ CPU
+ GPU
+ RAM
+ SSD
+ другие обязательные компоненты
```

При необходимости отдельно вводится сервисная составляющая:

```text
MINI_BUILD_PREMIUM
```

Она может покрывать:

- более сложную сборку;
- cable management;
- дополнительное время на compatibility check;
- расширенный thermal test;
- noise tuning.

Если такая составляющая вводится, она должна быть формализована в pricing engine, а не скрываться искусственным увеличением `UF_PRICE` у случайного компонента.

## 13. Ценовое позиционирование относительно PLAY 1440

`PLAY 1440 MINI` может стоить заметно дороже обычного `PLAY 1440` даже при том же CPU/GPU-классе.

Это не считается проблемой продуктовой лестницы, потому что MINI продаёт другую ценность: компактность и инженерное исполнение.

Поэтому автоматическое правило:

> «если цена MINI приблизилась к PLAY 1440 PRO — предложить PRO»

не должно срабатывать безусловно.

Пользователю можно показать нейтральное сравнение:

- MINI — компактность;
- PRO — дополнительная производительность.

Выбор остаётся за пользователем.

## 14. Thermal / noise validation

Для MINI требуется отдельный test protocol.

Минимальный набор:

- ambient temperature;
- idle temperature;
- CPU sustained load;
- GPU sustained load;
- combined CPU + GPU load;
- продолжительность теста;
- CPU max/average temperature;
- GPU max/average temperature;
- GPU hotspot при наличии данных;
- throttling check;
- fan RPM при возможности;
- noise level при наличии измерительной методики.

Также нужен реальный игровой тест, потому что synthetic load и игровой thermal pattern отличаются.

## 15. Performance claims

FPS-данные стандартного `PLAY 1440` нельзя автоматически копировать на `PLAY 1440 MINI`.

Если CPU/GPU одинаковы, performance может быть близкой, но публичные claims разрешаются только после проверки конкретной MINI revision.

Причина — возможные различия в:

- power limits;
- thermal limits;
- boost behavior;
- cooling;
- physical GPU model.

## 16. Revision и идентификация

Рабочий model code:

```text
KORSAC_MODEL_CODE = KP1440M
KORSAC_REVISION = 2026.1
```

Публичное название:

`KORSAC PLAY 1440 MINI`

Пример system passport:

```text
KORSAC SYSTEM ID
KS-26-001284

MODEL
KORSAC PLAY 1440 MINI

REVISION
KP1440M / 2026.1
```

Дальше паспорт содержит фактически установленные физические SKU и результаты тестирования.

## 17. Bitrix model

MINI — отдельный catalog element.

Пример свойств:

```text
KORSAC_MODEL_CODE
KORSAC_REVISION
KK_FORM_FACTOR
KK_CPU
KK_GPU
KK_MB
KK_RAM
KK_RAM_OPTIONS
KK_SSD1
KK_SSD1_OPTIONS
KK_SSD2
KK_SSD2_OPTIONS
KK_CASE
KK_CASE_OPTIONS
KK_PSU
KK_COOLER
```

Рекомендуемое значение:

```text
KK_FORM_FACTOR = MINI_ITX
```

Allowed options должны проходить server-side compatibility validation.

## 18. UX конфигуратора

Пользователь не должен видеть сложность Mini-ITX как набор технических ограничений.

Интерфейс показывает только совместимые варианты.

Пример:

> Корпус
>
> Compact Black
> Compact White
> Compact Premium

После выбора корпуса система автоматически исключает несовместимые скрытые physical SKU.

Если выбор одной опции требует изменения другой, интерфейс должен объяснить это до добавления в корзину.

Например:

> Для этого корпуса используется другой вариант охлаждения. Итоговая цена будет пересчитана автоматически.

## 19. Visual identity MINI

`MINI` остаётся частью основного бренда KORSAC.

Не создавать:

- отдельный логотип;
- отдельное тотемное животное;
- отдельную цветовую палитру.

Допустимо использовать компактный secondary badge:

```text
KORSAC
MINI
```

или суффикс в product lockup:

```text
KORSAC PLAY 1440
MINI
```

Визуальная идея MINI — высокая плотность, компактность и инженерная аккуратность.

## 20. Launch scope

Для первой версии достаточно:

- одной модели `KORSAC PLAY 1440 MINI`;
- 1 default case + 1–2 optional cases;
- одного motherboard class;
- одного PSU class;
- одного approved cooling class;
- 32/64 GB RAM;
- 1/2 TB SSD1;
- optional SSD2, если корпус и плата это позволяют;
- небольшого whitelist physical SKUs.

Не нужно на старте пытаться поддерживать десятки Mini-ITX корпусов и все возможные сочетания.

## 21. Следующий этап

Нужно спроектировать общую `KORSAC Components HL Schema`, которая поддержит одновременно standard и MINI системы.

Особое внимание:

- component class vs physical SKU;
- form factor;
- dimensions;
- compatibility metadata;
- approved SKU lists;
- pricing;
- availability;
- product revision snapshot.
