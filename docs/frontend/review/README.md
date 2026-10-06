# Снимки визуального ревью KORSAC

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

Захват v2: Chromium 151, reduced motion, desktop 1440×1080 px, mobile
375×1000 px. Дополнительные desktop-фрагменты сняты при 1440×1440 px,
чтобы в кадр помещались длинный manifest и все пять motion-примеров.

Статические снимки используются для сравнения композиции и состояний.
Последовательности движения нужно смотреть в разделе Motion на
[`prototype/ui.html`](../../../prototype/ui.html): hero, validation,
selection, SYSTEM ID и section index повторяются отдельными кнопками.
Параметры захвата и фактические результаты проверок фиксируются в PR.

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
