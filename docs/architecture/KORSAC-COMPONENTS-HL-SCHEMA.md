# KORSAC Components — HL Schema v0.1

Дата: 2026-09-29

Статус: рабочая архитектура данных для каталога, pricing, production и KORSAC SYSTEM ID.

Связанные документы:

- `docs/brand/KORSAC-BRAND-GUIDE.md`
- `docs/product/KORSAC-PLAY-ARCHITECTURE.md`
- `docs/product/KORSAC-MINI-ARCHITECTURE.md`
- `docs/product/KORSAC-PLAY-1440-SPEC-v0.1.md`

## 1. Цель

KORSAC не должен наследовать HL-структуру King-Komp один в один.

Текущий King-Komp может продолжать использовать свои коммерческие абстракции вроде:

```text
B850
750W plus
```

Для KORSAC нужен отдельный слой данных, потому что бренд обещает более конкретный гарантированный уровень продукта:

```text
B850 ATX / Wi-Fi / 2.5 GbE
750W / 80+ Gold / ATX 3.1
750W / 80+ Gold / SFX / ATX 3.1
32 GB DDR5-6000 CL30
1 TB NVMe PCIe 4.0 TLC
```

При этом публичный сайт по-прежнему не обязан обещать конкретную физическую модель MSI, ASUS, be quiet!, Kingston и т. п., если конкретный SKU не является частью продукта.

Основной принцип:

> Каталог продаёт гарантированный **component class**, производство выбирает **approved physical SKU**, а паспорт фиксирует фактически установленный SKU.

## 2. Четыре уровня данных

Архитектура делится на четыре независимых уровня.

```text
CATALOG PRODUCT
      ↓
COMPONENT CLASS
      ↓
APPROVED PHYSICAL SKU
      ↓
SUPPLIER OFFER / STOCK
```

Отдельно существует слой:

```text
VALIDATED COMBINATION / BUILD PROFILE
```

Он нужен для MINI и других конфигураций, где совместимость нельзя безопасно определить только по component class.

### 2.1. Catalog Product

Пример:

```text
KORSAC PLAY 1440
KORSAC PLAY 1440 MINI
```

Товар хранит default component classes и разрешённые пользовательские options.

### 2.2. Component Class

Это коммерчески гарантируемый класс комплектующей.

Примеры:

```text
GPU_RTX_5070_12GB
MB_B850_ATX_WIFI_2P5G
PSU_750_GOLD_ATX31
PSU_750_GOLD_SFX_ATX31
RAM_32_DDR5_6000_CL30
SSD_1TB_NVME_PCIE4_TLC
```

Именно этот уровень участвует в:

- свойствах товара Bitrix;
- базовой цене;
- конфигураторе;
- корзине и заказе;
- обещании покупателю.

### 2.3. Approved Physical SKU

Это конкретная физическая модель комплектующей, которую KORSAC разрешает устанавливать вместо component class.

Пример:

```text
Component class:
PSU_750_GOLD_ATX31

Approved physical SKUs:
- MSI MAG A750GL PCIE5
- be quiet! Pure Power 12 M 750W
- другая протестированная модель того же класса
```

Физический SKU не обязан показываться покупателю до сборки, если публично продаётся именно класс.

### 2.4. Supplier Offer

Это конкретное предложение поставщика:

```text
physical SKU
supplier
supplier SKU / external ID
purchase price
stock
updated_at
```

Поставщик не должен становиться частью публичной карточки товара.

## 3. Почему component classes лучше разделить по HL-блокам

Для KORSAC v0.1 рекомендуется **не делать один универсальный HL-блок всех component classes**.

Причины:

- Bitrix Directory-свойство естественно связывается с конкретным HL-блоком;
- у разных типов комплектующих разные обязательные характеристики;
- администрирование проще;
- меньше риска случайно выбрать PSU в свойстве RAM;
- проще валидировать `_OPTIONS`;
- проще развивать типовые фильтры и формы администратора.

Рекомендуемые HL-блоки:

```text
KorsacCpuClass
KorsacGpuClass
KorsacMotherboardClass
KorsacRamClass
KorsacSsdClass
KorsacPsuClass
KorsacCoolerClass
KorsacCaseClass
KorsacServiceClass       # неп physical BOM lines, если понадобятся
```

Фактические технические имена можно унифицировать при реализации, например:

```text
KorsacCpuClass
KorsacGpuClass
...
```

или через префикс проекта, если это требуется принятой Bitrix-конвенцией.

## 4. Общие поля component class

Каждый class HL-блок должен иметь общий минимальный набор.

| Поле | Тип | Назначение |
|---|---|---|
| `UF_XML_ID` | string, unique | стабильный машинный код класса |
| `UF_NAME` | string | административное название |
| `UF_PUBLIC_NAME` | string | название для сайта/заказа |
| `UF_ACTIVE` | bool | доступен ли класс для новых конфигураций |
| `UF_SORT` | int | порядок отображения |
| `UF_PRICE` | decimal | текущая цена component class для pricing engine |
| `UF_PRICE_UPDATED_AT` | datetime | когда цена обновлена |
| `UF_DESCRIPTION` | text | внутреннее/публичное пояснение при необходимости |

### 4.1. Правило `UF_XML_ID`

`UF_XML_ID` является постоянным идентификатором.

После появления класса в заказах его нельзя переименовывать из-за маркетинговых изменений.

Хорошо:

```text
PSU_750_GOLD_ATX31
MB_B850_ATX_WIFI_2P5G
RAM_32_DDR5_6000_CL30
```

Плохо:

```text
block-pitania-750-new
best_ram_32
option_17
```

Цена, поставщик и текущая доступность не кодируются в `UF_XML_ID`.

## 5. CPU class

Минимальные дополнительные поля:

```text
UF_VENDOR
UF_FAMILY
UF_MODEL
UF_SOCKET
UF_CORE_COUNT
UF_THREAD_COUNT
UF_TDP_W
UF_IGPU
```

Пример class:

```text
UF_XML_ID = CPU_AMD_R7_9700X
UF_PUBLIC_NAME = AMD Ryzen 7 9700X
UF_SOCKET = AM5
```

Для CPU допустимо, что component class практически совпадает с конкретной моделью CPU. Абстракция нужна прежде всего для единой pricing/BOM-модели.

## 6. GPU class

Дополнительные поля:

```text
UF_VENDOR_FAMILY
UF_GPU_MODEL
UF_VRAM_GB
UF_MEMORY_TYPE
UF_POWER_CLASS_W
UF_MIN_PSU_CLASS
```

Пример:

```text
UF_XML_ID = GPU_RTX_5070_12GB
UF_PUBLIC_NAME = GeForce RTX 5070 12 GB
```

Физические размеры GPU **не хранятся только на class level**, потому что разные исполнения RTX 5070 существенно отличаются по длине, высоте и толщине.

Эти размеры принадлежат approved physical SKU.

## 7. Motherboard class

Дополнительные поля:

```text
UF_SOCKET
UF_CHIPSET
UF_FORM_FACTOR
UF_RAM_TYPE
UF_WIFI
UF_WIFI_STANDARD
UF_LAN_SPEED
UF_M2_COUNT
UF_FRONT_USB_C
UF_PCIE_CLASS
```

Примеры:

```text
MB_B850_ATX_WIFI_2P5G
MB_B850_MINIITX_WIFI_2P5G
```

Важно: `B850` и `B850 Wi-Fi Mini-ITX` — разные component classes.

## 8. RAM class

Дополнительные поля:

```text
UF_CAPACITY_GB
UF_MODULE_COUNT
UF_RAM_TYPE
UF_SPEED_MT
UF_CAS_LATENCY
UF_PROFILE_TYPE
UF_ECC
```

Пример:

```text
RAM_32_DDR5_6000_CL30
RAM_64_DDR5_6000_CL30
```

При необходимости для MINI на physical SKU уровне хранится реальная высота модулей.

## 9. SSD class

Дополнительные поля:

```text
UF_CAPACITY_GB
UF_INTERFACE
UF_PCIE_GEN
UF_FORM_FACTOR
UF_NAND_CLASS
UF_DRAM_CLASS
UF_ENDURANCE_CLASS
```

Примеры:

```text
SSD_1TB_NVME_PCIE4_TLC
SSD_2TB_NVME_PCIE4_TLC
```

Не следует обещать TLC/DRAM-класс публично, если производство не может гарантировать его для каждого approved SKU.

## 10. PSU class

Дополнительные поля:

```text
UF_POWER_W
UF_EFFICIENCY_CLASS
UF_FORM_FACTOR
UF_ATX_STANDARD
UF_PCIE_POWER_STANDARD
UF_MODULAR
UF_NATIVE_GPU_CONNECTOR
```

Примеры:

```text
PSU_750_GOLD_ATX31
PSU_850_GOLD_ATX31
PSU_750_GOLD_SFX_ATX31
```

Запись вида `750W plus` для KORSAC считается недостаточно определённой.

## 11. Cooler class

Дополнительные поля:

```text
UF_COOLER_TYPE
UF_COOLING_CLASS
UF_MAX_CPU_POWER_CLASS
UF_SOCKET_SUPPORT
UF_SIZE_CLASS
```

Публичные class-примеры:

```text
COOLER_AIR_PREMIUM_AM5
COOLER_AIO_240_PREMIUM
```

Физическая высота, радиатор, толщина и clearance конкретной модели фиксируются на physical SKU level.

## 12. Case class

Для корпуса абстракция отличается от PSU/GPU.

Корпус является визуальной частью продукта, поэтому пользователь часто должен видеть **конкретный дизайн**, а не скрытый класс.

Дополнительные поля:

```text
UF_FORM_FACTOR
UF_VOLUME_L
UF_COLOR
UF_PANEL_TYPE
UF_MAX_GPU_LENGTH_MM
UF_MAX_GPU_HEIGHT_MM
UF_MAX_GPU_SLOTS
UF_MAX_CPU_COOLER_HEIGHT_MM
UF_PSU_FORMAT
UF_RADIATOR_CLASS
UF_USB_C
UF_IMAGE
UF_GALLERY
```

Для case component class допускается почти 1:1 соответствие физическому SKU или семейству цветовых вариантов.

Пример:

```text
CASE_KORSAC_COMPACT_A_BLACK
CASE_KORSAC_COMPACT_A_WHITE
```

## 13. Service class

`KorsacServiceClass` нужен только если сервисная составляющая должна участвовать в BOM/pricing как отдельная формализованная строка.

Примеры:

```text
BUILD_STANDARD
BUILD_MINI_PREMIUM
TEST_EXTENDED
```

Поля:

```text
UF_XML_ID
UF_NAME
UF_PUBLIC_NAME
UF_ACTIVE
UF_SORT
UF_PRICE
```

У service class нет physical SKU и supplier offer.

Это предпочтительнее, чем искусственно увеличивать цену PSU/корпуса для сокрытия стоимости более сложной MINI-сборки.

## 14. Каталожные свойства Bitrix

Каталог оперирует **только component classes**.

Базовый набор:

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
KK_SERVICE
```

При появлении реальной необходимости:

```text
KK_CPU_OPTIONS
KK_GPU_OPTIONS
KK_MB_OPTIONS
KK_PSU_OPTIONS
KK_COOLER_OPTIONS
```

Но их не следует добавлять заранее только ради универсальности.

### 14.1. Default / Options rule

Для конфигурируемого типа всегда есть две разные роли:

```text
KK_RAM          # single, default
KK_RAM_OPTIONS  # multiple, allowed alternatives
```

`*_OPTIONS` никогда не участвует в расчёте базовой цены.

Базовая цена формируется только из default-компонентов и service lines.

## 15. Approved Physical SKU registry

Для v0.1 рекомендуется отдельный HL-блок:

```text
KorsacPhysicalSku
```

Он является внутренним operational registry и не используется напрямую в товарных свойствах каталога.

### Общие поля

| Поле | Назначение |
|---|---|
| `UF_XML_ID` | стабильный внутренний код physical SKU |
| `UF_COMPONENT_TYPE` | CPU/GPU/MB/RAM/SSD/PSU/COOLER/CASE |
| `UF_CLASS_XML_ID` | component class, которому соответствует SKU |
| `UF_VENDOR` | производитель |
| `UF_MODEL` | точная модель |
| `UF_VENDOR_PN` | part number производителя |
| `UF_APPROVAL_STATUS` | DRAFT / APPROVED / SUSPENDED / EOL |
| `UF_SORT` | приоритет выбора |
| `UF_NOTES` | внутренние примечания |

Связь с component class намеренно хранится через стабильный `UF_CLASS_XML_ID`, а не через неоднозначный numeric ID из разных HL-блоков.

Приложение использует registry:

```text
COMPONENT_TYPE → class HL block
```

### 15.1. Compatibility-critical fields

На physical SKU level дополнительно могут храниться:

```text
UF_FORM_FACTOR
UF_LENGTH_MM
UF_HEIGHT_MM
UF_WIDTH_MM
UF_SLOT_WIDTH
UF_POWER_W
UF_COOLER_HEIGHT_MM
UF_RADIATOR_SIZE
UF_RAM_HEIGHT_MM
UF_CONNECTOR_TYPE
UF_CONNECTOR_CLEARANCE_MM
```

Поля могут быть пустыми для типов, где они неприменимы.

Критические для совместимости значения не следует прятать только в JSON/text.

## 16. Supplier offers

Отдельный HL-блок:

```text
KorsacSupplierOffer
```

Поля:

```text
UF_PHYSICAL_SKU_XML_ID
UF_SUPPLIER_CODE
UF_EXTERNAL_ID
UF_PURCHASE_PRICE
UF_CURRENCY
UF_AVAILABLE_QTY
UF_STOCK_STATUS
UF_DELIVERY_DAYS
UF_PRIORITY
UF_ACTIVE
UF_UPDATED_AT
```

Один physical SKU может иметь несколько supplier offers.

Пример:

```text
MSI MAG A750GL PCIE5
  ├─ Supplier A / 9 800 ₽ / stock 12
  └─ Supplier B / 10 150 ₽ / stock 40
```

Это не меняет публичный component class `PSU_750_GOLD_ATX31`.

## 17. Supplier registry

Если поставщиков несколько и по ним нужны метаданные, можно создать:

```text
KorsacSupplier
```

Минимально:

```text
UF_CODE
UF_NAME
UF_ACTIVE
UF_PRIORITY
UF_DELIVERY_DAYS_DEFAULT
```

На старте этот блок необязателен, если supplier metadata уже живёт в другой системе.

## 18. Pricing architecture

### 18.1. Source of truth для продажи

Для каталога source of truth остаётся:

```text
component class → UF_PRICE
```

Именно эти значения используются pricing engine для default BOM и configurable options.

### 18.2. Supplier price не равен автоматически `UF_PRICE`

Нельзя без отдельного бизнес-правила делать:

```text
UF_PRICE = cheapest supplier purchase price
```

Потому что нужно учитывать:

- маржу;
- резерв на замену supplier SKU;
- логистику;
- колебания закупочной цены;
- возвраты/гарантию;
- сервис;
- ценовое позиционирование бренда.

На v0.1 `UF_PRICE` может обновляться контролируемым механизмом так же, как сейчас работает концепция массового обновления цен, но уже на KORSAC data model.

Supplier offers подготавливают данные для будущей автоматизации, но не диктуют retail price напрямую.

### 18.3. Pricing engine

`kk.price-update` или его универсализированный pricing service должен уметь:

1. читать только default component properties;
2. игнорировать `*_OPTIONS` при базовой цене;
3. брать `UF_PRICE` из соответствующих KORSAC class HL;
4. применять product-level adjustments один раз согласно текущим правилам pricing;
5. рассчитывать selected configuration тем же алгоритмом;
6. не доверять цене из frontend.

## 19. Order snapshot и production snapshot

Нужно различать два момента.

### 19.1. Sales / order snapshot

Во время заказа фиксируется то, что было обещано покупателю:

```text
KORSAC PLAY 1440 MINI
GPU: GeForce RTX 5070 12 GB
PSU: 750W Gold SFX ATX 3.1
RAM: 32 GB DDR5-6000
...
```

Snapshot содержит:

- component class code;
- human-readable class name;
- цену/дельту на момент заказа;
- model code и revision.

Он не должен зависеть от будущих изменений HL.

### 19.2. Production / SYSTEM ID snapshot

После реальной сборки фиксируется то, что физически установлено:

```text
GPU physical SKU
Motherboard physical SKU
PSU physical SKU
RAM physical SKU
SSD physical SKU
serial numbers при необходимости
```

Это становится частью `KORSAC SYSTEM ID`.

Таким образом смена поставщика после заказа не меняет коммерческое обещание и не ломает историю.

## 20. MINI compatibility layer

Для MINI class-level compatibility недостаточно.

Нужен whitelist реально проверенных critical combinations.

Рекомендуемый HL-блок:

```text
KorsacValidatedBuild
```

Поля v0.1:

```text
UF_CODE
UF_MODEL_CODE
UF_REVISION
UF_ACTIVE
UF_CASE_SKU
UF_MB_SKU
UF_GPU_SKU
UF_PSU_SKU
UF_COOLER_SKU
UF_RAM_CLASS_XML_ID
UF_TEST_STATUS
UF_TESTED_AT
UF_NOTES
```

Это не обязательно полный BOM. Это compatibility-critical skeleton.

Пример:

```text
KP1440M_2026_1_COMBO_001

Case   = SKU_CASE_A_BLACK
MB     = SKU_MB_B850I_A
GPU    = SKU_GPU_RTX5070_A
PSU    = SKU_PSU_SFX750_A
Cooler = SKU_COOLER_A
RAM    = RAM_32_DDR5_6000_CL30
Status = APPROVED
```

Если RAM/SSD не влияют на физическую совместимость конкретной сборки, они остаются independent allowed options.

### 20.1. Почему whitelist, а не универсальный engine

На старте:

> tested whitelist > theoretical rules engine

Особенно для MINI, где nominal dimensions не всегда описывают:

- изгиб power cable;
- реальный clearance;
- конфликт радиатора и GPU;
- cable routing;
- влияние fan layout;
- температурное поведение.

Универсальные rules можно добавить позже поверх накопленных validated builds.

## 21. Выбор physical SKU при производстве

Production resolver получает:

```text
ordered component class
model revision
form factor
validated build restrictions
current stock / supplier offers
```

и выбирает physical SKU только из:

```text
APPROVED
+
соответствующий class
+
совместим с revision / validated combination
+
доступен
```

Алгоритм не должен выбирать SKU только потому, что он дешевле.

Дополнительный `UF_SORT`/priority позволяет предпочитать основную модель комплектующей и использовать substitute при отсутствии.

## 22. Статусы physical SKU

Рекомендуемый lifecycle:

```text
DRAFT       # добавлен, но ещё не разрешён к установке
APPROVED    # разрешён
SUSPENDED   # временно не использовать
EOL         # больше не использовать для новых сборок
```

Исторические SKU не удаляются, если они присутствуют в SYSTEM ID или заказах.

## 23. Что показывать покупателю

Публичный уровень зависит от типа комплектующей.

### Обычно abstract class

- motherboard;
- PSU;
- RAM;
- SSD;
- cooler;
- GPU vendor implementation.

Пример:

> B850 · Wi-Fi · 2.5 GbE

> 750W · 80+ Gold · ATX 3.1

### Обычно exact / visual product

- case;
- отдельные premium-компоненты, если их конкретная модель является частью ценности товара.

KORSAC должен гарантировать спецификацию, которую показывает покупателю.

## 24. Не делать на первом этапе

Не требуется сразу строить:

- универсальный экспертный compatibility engine;
- автоматический выбор cheapest supplier;
- динамическую замену component class по наличию;
- десятки CPU/GPU options;
- синхронизацию KORSAC HL один в один с King-Komp;
- удаление/рефакторинг текущих King-Komp HL;
- сложный MDM-сервис.

Первая версия должна быть простой и проверяемой.

## 25. Минимальный v0.1 для запуска

Для первой рабочей версии достаточно:

1. отдельные KORSAC class HL-блоки;
2. общие поля `UF_XML_ID`, `UF_PUBLIC_NAME`, `UF_ACTIVE`, `UF_SORT`, `UF_PRICE`;
3. основные class-specific характеристики;
4. catalog default / `_OPTIONS` properties;
5. `KorsacPhysicalSku`;
6. `KorsacValidatedBuild` для `PLAY 1440 MINI`;
7. order snapshot component classes;
8. production snapshot physical SKU;
9. server-side price validation.

`KorsacSupplierOffer` можно подключить сразу, если уже есть удобный источник supplier feed, либо вторым этапом.

## 26. Пример end-to-end: PLAY 1440 MINI

Каталог:

```text
KORSAC PLAY 1440 MINI

KK_GPU  = GPU_RTX_5070_12GB
KK_MB   = MB_B850_MINIITX_WIFI_2P5G
KK_RAM  = RAM_32_DDR5_6000_CL30
KK_SSD1 = SSD_1TB_NVME_PCIE4_TLC
KK_PSU  = PSU_750_GOLD_SFX_ATX31
KK_CASE = CASE_KORSAC_COMPACT_A_BLACK
```

Pricing:

```text
component classes
      ↓ UF_PRICE
pricing engine
      ↓
product BASE_PRICE
```

Заказ:

```text
GPU = GeForce RTX 5070 12 GB
PSU = 750W Gold SFX ATX 3.1
...
```

Production:

```text
component class
      ↓
approved SKUs
      ↓
validated MINI build
      ↓
stock/supplier availability
      ↓
physical SKU allocation
```

После сборки:

```text
KORSAC SYSTEM ID
      ↓
actual physical SKU snapshot
      ↓
benchmarks / thermal tests / serials
```

## 27. Направление дальнейшей реализации

Следующие технические шаги после утверждения схемы:

1. зафиксировать точные HL-block names и field types для Bitrix;
2. определить registry component types → class HL;
3. определить формат installer/migration для создания структуры;
4. адаптировать `kk.price-update` к KORSAC class HL и правилу default/options;
5. создать первую тестовую запись каждого class type;
6. создать первый `PLAY 1440` и `PLAY 1440 MINI` как тестовые товары;
7. реализовать `KorsacPhysicalSku` и production allocation;
8. после этого подключать supplier feeds и автоматизацию закупочных данных.

## 28. Открытые решения

Перед кодированием нужно отдельно утвердить:

- будет ли `UF_PRICE` включать только стоимость компонента или часть коммерческой маржи;
- нужен ли отдельный `UF_COST_REFERENCE`;
- будет ли supplier registry частью KORSAC или использовать существующий источник;
- какие serial numbers фиксируются в SYSTEM ID;
- должен ли покупатель заранее видеть точную модель GPU/SSD/RAM или только class;
- нужен ли отдельный production module или на первом этапе достаточно административного интерфейса KORSAC.

Эти вопросы не блокируют базовую HL-схему, но влияют на pricing и production workflow.