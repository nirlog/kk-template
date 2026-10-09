# KORSAC — Contacts & Error Pages v1

[Production architecture](KORSAC-INFORMATION-ARCHITECTURE.md) и
[SEO source contract](KORSAC-SEO-FOUNDATION.md) определяют дальнейший перенос.
Новые страницы не добавляют commerce/backend, отправку данных или motion.

## Contacts

`prototype/contacts.html` → `/contacts/` в production. Публичные sticky header,
footer, native enhanced drawer и no-JS navigation сохранены. Header не получил
новых пунктов; Contacts доступен из public footer и compact transaction footer.
Main: breadcrumbs, H1, спокойный intro, телефон/email/время работы, B2B/support,
небольшой адресный slot без карты. Полей формы нет, нечего отправлять/сохранять.
Настоящие channel links будут добавлены только вместе с утверждёнными данными.
Неподтверждённые значения — текстовые slots, не fake tel/mailto/адрес/часы.

В будущем единые settings владеют телефон/email/адрес/hours/brand organization;
Header/Footer/Contacts/ContactPage JSON-LD получают одинаковые данные.
B2B и support могут использовать отдельные подтверждённые каналы из тех же
settings. Location/map появляется с согласованным адресом, не как декоративный
вымышленный объект. Future contact form имеет backend/API обработку и privacy
контракт; success/error не создают crawlable SEO URL.

Contacts indexable только в production, self-canonical и ContactPage +
BreadcrumbList. В prototype noindex и sparse schema, без ContactPoint.
Спокойная informational page не включает Brand Intro: нет boot/overlay/
controller, timestamp не читается и не меняется. Это такое же ограничение
шаблона, как у transactional pages; policy существующих Home/Catalog/Product
не изменена. Декоративной entry animation или новой interaction нет.

## Error states

| Review file | Сообщение                   | Действия                             | Production response owner                                 |
| ----------- | --------------------------- | ------------------------------------ | --------------------------------------------------------- |
| `404.html`  | Страница не найдена.        | Главная, выбрать компьютер, контакты | Router: actual `404 Not Found`                            |
| `500.html`  | Что-то пошло не так.        | Главная, контакты                    | Server error handler: actual `500 Internal Server Error`  |
| `503.html`  | KORSAC временно недоступен. | Попробовать позже, контакты          | Server maintenance gate: actual `503 Service Unavailable` |

404 сохраняет approved public brand/nav, sticky background и native fallback
menu. Utility Cart/Account/Search отсутствуют. 500/503 — reduced resilient shell:
одна standalone `error-resilient.css` без imports и локальный static logo.
Не требуются shared tokens, app CSS/JS/API/Bitrix или external assets.
Локальный failure stylesheet намеренно повторяет минимальные approved colors;
это автономный fallback, не второе полноценное design system.

Все ошибки показываются немедленно, без Brand Intro/Hero motion.
Нет debug/stack/PHP/database/Bitrix paths/request IDs. Нет автоматического
redirect/reload, обещанного времени восстановления, реального поиска.
«Попробовать позже» в static 503 вручную открывает `503.html`; production
адаптер связывает её с текущим запрошенным URL для повторной попытки.
При общей недоступности Contacts тоже может быть недоступен — локальный logo
и сообщение не зависят от успешного перехода по этой ссылке.

## HTTP и deployment

Static file opening/http.server не умеют выразить HTTP error contract:
именованный файл возвращается как обычный **200**. Это visual review, не
проверка настоящих статусов. Ответ отсутствующего production URL обязан
содержать template **и 404**, без canonical на missing URL, без перенаправления
на Home. Намеренно удалённый контент без замены может иметь 410, отдельный
дизайн сейчас не нужен. 403 оставлен до реального public use case.

Unexpected server exception возвращает 500 без утечки technical internals;
безопасный fallback отдается по возможности самим сервером. Maintenance gate
передаёт 503 вне неисправного Bitrix-приложения. Retry-After имеет смысл только
при известной оценке — seconds или HTTP date; выдуманного срока и заголовка нет.
Production fallback HTML/CSS/logo должны быть доступны web server до запуска
приложения. Если даже static assets недоступны, HTML сообщение остаётся
readable; это проверено с blocked CSS/logo в браузере.

### Пути production fallback не зависят от глубины запроса

Error template рендерится для **исходного requested URL**, а не по адресу
`/404.html`, `/500.html` или `/503.html`. Например, при запросе
`/computers/play/1440/missing/` относительное `assets/css/error-resilient.css`
разрешилось бы внутри этого пути и сломало fallback. Production CSS/logo URLs
обязаны быть **origin-root-absolute** (начинаться с `/`) или формироваться
сервером как абсолютные asset URLs независимо от request depth. Их реальные
пути определяет deployment/template asset resolver, не браузерный JS и не
неисправный Bitrix component. Они доступны web server до запуска приложения.

Home action использует `/`, Contacts — `/contacts/`, без file-relative
`index.html`/`contacts.html`. 503 retry сохраняет исходный requested URL
(включая необходимый request context), а не ведёт на fixed `503.html` или Home;
никакого auto-reload. Production integration проверяет ответы на глубоко
вложенных URL: actual status, загрузку CSS/logo, Home/Contacts и ручной retry.
Static prototype сохраняет относительные пути для HTTP/file review; это
не deployment-ready пути production error templates.

Все ошибки noindex, вне sitemap и публичного меню. В prototype policy полнее:
`noindex, nofollow, noarchive`. Нет Product/Article schema; errors без JSON-LD,
canonical и social-image fiction. Review hub перечисляет их как visual states.

## Accessibility / review

Один H1, skip link, landmarks, настоящий link text и видимый focus.
Код не заменяет сообщение. 320px не занят giant decorative mark: code,
сообщение и primary action в первом practical viewport. 404 normal hover
использует существующий reduced timing; 500/503 не анимируют содержимое.
Контакты сканируются по каналам, B2B/support имеют отдельные headings.

Снимки и фактические проверки: [Review](review/README.md),
[SEO report](review/seo-foundation-v1.md). Новых interactions не введено,
поэтому отдельный MP4 не требуется. Human visual acceptance остаётся review
снимков/живого browser; production HTTP/Bitrix integration не реализована.
