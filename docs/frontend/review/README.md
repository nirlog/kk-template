# Материалы визуального и motion-ревью KORSAC

## Interactive Product Experience v3

[Запись взаимодействий — MP4](interactive-v3.mp4) показывает реальный native
wheel-scroll через пять контекстов Explorer (примерно 0–5 s), ручные кнопки
и memory hotspot (5–8 s), смену корпусов, RAM/SSD/SSD2 и manifest (8–15 s),
этапы сборки и соответствующую validation-сцену (15–21 s).
RAM и второй SSD переключаются нативными стрелками клавиатуры.
Запись сделана с normal motion, без замедления и без программного управления
scroll position: Chromium 151, viewport 1440×1080 px, видео 960×720 px /
25 fps, 21,16 s, около 1,0 MiB, H.264. Это только review asset.

Снимки v3:

- [PLAY 1440 — desktop](product-v3-desktop.png), 1440×1080 px.
- [PLAY 1440 — mobile](product-v3-mobile.png), 375×1000 px.
- [System Explorer — desktop](explorer-v3-desktop.png), 1440×1080 px.
- [System Explorer — mobile](explorer-v3-mobile.png), 375×1200 px.
- [Конфигуратор и сцена](configurator-stage-v3.png), 1440×1440 px:
  North, 64 ГБ DDR5, основной 2 ТБ и второй SSD 1 ТБ.
- [Interactive Product Primitives](interactive-primitives-v3.png),
  1440×1200 px: scoped playground и отдельный native fixture.

PNG сняты в Chromium с reduced motion. Предыдущие материалы v1/v2/v2.1
сохранены под исходными именами. Wireframe в новых снимках — условная схема,
не фотография и не точная компоновка выбранного корпуса.

[Архитектура и live checklist v3](../KORSAC-INTERACTIVE-PRODUCT-EXPERIENCE.md)
описывают ручной выбор, priority после прокрутки, tablet/mobile fallback,
no-JS/reduced-motion и будущие media/kk.korsac adapters.
Человеческое live-ревью остаётся acceptance gate: запись и автоматические
проверки не подтверждают visual/motion acceptance.

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
