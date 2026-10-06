# KORSAC / kk-template

Документация бренда и продуктовой архитектуры KORSAC, а также статическая
визуальная основа будущего сайта.

## Prototype

Прототип на HTML5, CSS и обычном JavaScript работает без установки пакетов,
сборки, Bitrix и внешних ресурсов. Откройте HTML-файл прямо в браузере:

- [prototype/index.html](prototype/index.html) — навигация для дизайнеров и разработчиков.
- [prototype/ui.html](prototype/ui.html) — токены, компоненты и состояния.
- [prototype/product.html](prototype/product.html) — PLAY 1440 и макет конфигуратора.

Для проверки через HTTP из корня репозитория:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory prototype
```

Откройте локальный порт 8000 в браузере. Сервер необязателен; файлы также
работают через `file://`. Цены, статусы, паспорт и сервисные опции — примеры.
Поиск, корзина, API и расчёт цены не реализованы.

[Описание системы и план переноса в Bitrix](docs/frontend/KORSAC-STATIC-PROTOTYPE.md).
