# Материалы визуального и motion-ревью KORSAC

## Catalog & Product Family Experience v1

[Каталог: короткая запись — MP4](catalog-v1.mp4) показывает normal motion:
примерно 0–9 s — PLAY 1440 → PRO → MINI → 4K → 1080 → 1440,
keyboard focus/selection карточки MINI, отметки 1440/PRO и comparison dialog;
примерно 9–14,5 s — mobile touch selector PRO → MINI → 1440 с местным
видимым обновлением preview и обычной короткой прокруткой к CTA.

Захват: Chromium 151, desktop viewport 1440×1080 и touch-emulated mobile
375×800. MP4 H.264: 960×720 / 25 fps, **14,48 s**, около **1,02 MiB**.
Mobile-фрагмент расположен по центру общего кадра. Нет замедления,
автопереключения Navigator или fake performance/price calculation.

PNG с reduced motion:

- [Каталог desktop](catalog-v1-desktop.png), 1440×1200: семейства, четыре ступени,
  отдельная MINI-ветка и выбранный PLAY 1440 целиком.
- [Каталог mobile](catalog-v1-mobile.png), 375×1440: компактный selector,
  выбранная модель, пример цены и CTA.
- [Вся линейка PLAY](catalog-range-v1.png), 1440×1900: все пять source cards,
  чуть больший приоритет PLAY 1440, рабочие classes и неизвестные цены.
- [Сравнение 1440 / PRO](catalog-compare-v1.png), 1440×1080: product columns
  и семь фактических строк, без численных performance claims.
- [Catalog Primitives](catalog-primitives-v1.png), 1344×2267: component capture
  из UI Kit — family switch, ladder item, MINI marker, выбранная карточка,
  независимый Navigator и comparison row.

[Документ каталога](../KORSAC-CATALOG-EXPERIENCE.md) описывает single HTML data
source, MAX3 comparison, mobile/no-JS/reduced-motion и future Bitrix mapping.
На 320/375/430 px карточки примерно 543–602 px; без horizontal overflow.
Высота preview стабильна при переключении пяти моделей на контрольных ширинах.
Review assets не загружаются страницами. Материалы продукта v3.1 ниже остаются
актуальной отдельной основой; каталог не меняет Product Explorer.

Human acceptance остаётся открытым: быстро ли читается ladder/MINI-ветка,
ясно ли назначение PRO, понятны ли сравнение и мобильный путь в карточку,
соответствует ли короткий resolve KORSAC. Запись и tests не заменяют эту оценку.

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
