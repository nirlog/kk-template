"""Public projection/privacy and static domain fixture guards; no fake automation tests."""
import json
from pathlib import Path
import re
import unittest
from seo_audit import Page, audit
import test_seo_audit as seo_fixtures
GOOD = seo_fixtures.GOOD

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = GOOD.replace('<main id="main">', '<main id="main" data-public-passport="active">').replace('</main>', '''
<p data-system-id>KS-2610-0012</p>
<section data-passport-components><dl><div data-passport-component><dt>CPU</dt><dd>Review CPU</dd></div></dl></section>
<div data-passport-warranty><time data-transfer-date datetime="2026-10-07">07.10.2026</time><time data-warranty-end datetime="2029-10-07">07.10.2029</time></div>
<a href="#inquiry" data-inquiry-cta>Задать вопрос</a><div data-inquiry-context>KS-2610-0012 / review system</div><form id="inquiry" data-passport-inquiry method="dialog"><button type="button">Check</button></form></main>''')
PENDING = GOOD.replace('<main id="main">', '<main id="main" data-public-passport="pending">').replace('</main>', '<p data-system-id>KS-2610-0013</p><p data-passport-pending>Паспорт ещё не активирован</p></main>')


class PublicPassportTests(unittest.TestCase):
    def report(self, html, name='passport.html'):
        return seo_fixtures.AuditGuardTests().check_fixture(html, page_name=name)

    def errors(self, html, name='passport.html'):
        return '\n'.join(e for p in self.report(html, name)['pages'] for e in p['errors'])

    def test_active_pending_and_current_repository(self):
        self.assertEqual(self.report(ACTIVE)['errors'], 0)
        self.assertEqual(self.report(PENDING, 'passport-pending.html')['errors'], 0)
        self.assertEqual(audit(ROOT)['errors'], 0)

    def test_staging_metadata_and_system_id_shape(self):
        self.assertIn('robots must', self.errors(ACTIVE.replace('noindex, nofollow, noarchive', 'index, follow')))
        for value in ('KS-26-001284', 'KS-2613-0012', 'KS-2600-0012', 'KS-2610-0000', 'ORDER-0012', ''):
            with self.subTest(value=value):
                self.assertIn('readable SYSTEM ID', self.errors(ACTIVE.replace('KS-2610-0012', value)))
        self.assertIn('generic', self.errors(ACTIVE.replace('<title>Fixture</title>', '<title>KS-2610-0012</title>')))
        self.assertIn('public active projection', self.errors(ACTIVE.replace('data-public-passport="active"', 'data-public-passport="pending"')))

    def test_system_passport_is_not_product_or_article_schema(self):
        for kind in ('Product', 'Offer', 'AggregateOffer', 'Review', 'AggregateRating', 'Article'):
            for markup, name in ((ACTIVE, 'passport.html'), (PENDING, 'passport-pending.html')):
                with self.subTest(kind=kind, page=name):
                    script = '<script type="application/ld+json">' + json.dumps({'@type': kind}) + '</script>'
                    self.assertIn(f'must not claim {kind}', self.errors(markup.replace('</head>', script + '</head>'), name))

    def test_serials_and_internal_context_cannot_hide_in_public_source(self):
        for fragment in ('<p>S/N: PRIVATE</p>', '<!-- serial_number=PRIVATE -->', '<input name="ORDER_ID" value="1">', '<script type="application/json">{"CUSTOMER_ID":1}</script>', '<div data-service-history>notes</div>', '<p>DEMO-SN-01</p>', '<input name="SYSTEM_INTERNAL_ID">', '<input name="COMPONENT_ID">', '<div data-supplier>internal</div>', '<p>RMA: private</p>'):
            with self.subTest(fragment=fragment):
                self.assertTrue(self.errors(ACTIVE.replace('</main>', fragment + '</main>')))
        self.assertIn('hidden identity', self.errors(ACTIVE.replace('</form>', '<input type="hidden" name="context" value="123"></form>')))
        self.assertIn('prefill customer', self.errors(ACTIVE.replace('</form>', '<input name="contact" value="private-contact"></form>')))

    def test_active_context_cannot_be_removed(self):
        for marker in ('data-passport-components', 'data-passport-component', 'data-passport-warranty', 'data-transfer-date', 'data-warranty-end', 'data-inquiry-cta', 'data-inquiry-context', 'data-passport-inquiry'):
            with self.subTest(marker=marker):
                self.assertIn('requires '+marker, self.errors(ACTIVE.replace(marker, 'data-removed-marker')))
        self.assertIn('time snapshot', self.errors(ACTIVE.replace('datetime="2029-10-07"', 'datetime="calculated-later"')))

    def test_secret_credential_is_private_in_active_and_pending_source(self):
        fragments = ('<p>SECRET_CODE</p>', '<!-- secretCode: 1234-5678 -->',
                     '<meta name="secret-code" content="1234-5678">',
                     '<script type="application/json">{"SECRET_CODE":"1234-5678"}</script>',
                     '<div hidden>1234-5678</div>', '<p>Код системы</p>')
        for markup, name in ((ACTIVE, 'passport.html'), (PENDING, 'passport-pending.html')):
            for fragment in fragments:
                with self.subTest(page=name, fragment=fragment):
                    self.assertIn('secret-code', self.errors(markup.replace('</head>', fragment + '</head>'), name))

    def test_account_and_ownership_data_cannot_hide_in_public_projection(self):
        fragments = ('<p>USER_ID 52002</p>', '<meta name="current-user-id" content="52002">',
                     '<!-- System.USER_ID = 52002 -->',
                     '<script type="application/json">{"SystemOwnershipHistory":[]}</script>',
                     '<div hidden data-ownership-history>old account</div>',
                     '<p>История смены владельца</p>',
                     '<script type="application/json">{"SystemOwnershipRequest":{"REQUEST_USER_ID":52003}}</script>',
                     '<div hidden data-ownership-request>PENDING</div>', '<p>Заявка на смену владельца</p>',
                     '<input name="SECRET_VERIFIED" value="true">', '<p>OLD_USER_ID / NEW_USER_ID</p>',
                     '<p>PROCESSED_BY / PROCESSED_AT</p>', '<p>USER_UNLINK</p>')
        for markup, name in ((ACTIVE, 'passport.html'), (PENDING, 'passport-pending.html')):
            for fragment in fragments:
                with self.subTest(page=name, fragment=fragment):
                    self.assertIn('ownership', self.errors(markup.replace('</main>', fragment + '</main>'), name))

    def test_pending_cannot_carry_active_data_even_hidden(self):
        for fragment in ('<section data-passport-components hidden>hidden</section>', '<p data-passport-warranty hidden>hidden</p>', '<p>GPU — GeForce RTX 5070</p>', '<time datetime="2026-10-07">date</time>', '<p>Гарантия до 2029</p>'):
            with self.subTest(fragment=fragment):
                self.assertIn('must not contain', self.errors(PENDING.replace('</main>', fragment + '</main>'), 'passport-pending.html'))
        self.assertIn('textual not-activated state', self.errors(PENDING.replace('Паспорт ещё не активирован', 'Loading'), 'passport-pending.html'))

    def test_passport_never_boots_brand_intro(self):
        self.assertIn('Brand Intro', self.errors(ACTIVE.replace('</head>', '<script src="assets/js/brand-intro.js"></script></head>')))
        for name in ('passport.html', 'passport-pending.html'):
            raw = (ROOT / 'prototype' / name).read_text()
            self.assertNotIn('korsac:brand-intro', raw)
            self.assertNotIn('data-brand-intro', raw)
            self.assertNotIn('system-workflow.js', raw)

    def test_product_example_is_explicit_and_has_no_configurator_coupling(self):
        product = (ROOT / 'prototype/product.html').read_text()
        example = re.search(r'<article\b[^>]*id="system-passport-info"[^>]*>(.*?)</article>', product, re.S).group(1)
        self.assertEqual(re.findall(r'KS-\d{4}-\d{4}', product), ['KS-2610-0012'])
        self.assertNotIn('KS-26-001284', product)
        self.assertIn('data-passport-example', example)
        self.assertIn('Пример паспорта', example)
        self.assertIn('не означает, что такая', example)
        self.assertIn('система уже существует', example)
        self.assertIn('после сборки', example)
        self.assertIn('передачи владельцу', example)
        self.assertIn('href="passport.html"', example)
        self.assertIn('Посмотреть пример паспорта', example)
        self.assertEqual(Page(ROOT / 'prototype/product.html').links.count('passport.html'), 1)
        self.assertNotRegex(example, r'data-(?:summary|stage|passports?)-output|data-motion|data-public-passport')
        self.assertNotIn('data-passport-output', product)
        controller = (ROOT / 'prototype/assets/js/product-experience.js').read_text()
        self.assertNotIn('data-passport-output', controller)
        self.assertNotIn('data-passport-example', controller)
        self.assertNotIn('system-passport-info', controller)
        for path in (ROOT / 'prototype').glob('*.html'):
            self.assertNotIn('product.html#product-passport', path.read_text(), path.name)

    def test_internal_workflow_has_no_public_navigation_entry(self):
        for path in (ROOT / 'prototype').glob('*.html'):
            if path.name in ('review.html', 'system-workflow.html'):
                continue
            page = Page(path)
            self.assertNotIn('system-workflow.html', page.links, path.name)
            if path.name not in ('passport.html', 'passport-pending.html'):
                if path.name not in ('product.html', 'account-systems.html', 'account-inquiries.html'):
                    self.assertNotIn('passport.html', page.links, path.name)
                for shell in re.findall(r'<(?:header|footer)\b[^>]*>.*?</(?:header|footer)>', page.raw, re.S):
                    self.assertNotIn('passport.html', shell, path.name)
                drawer = re.search(r'<dialog\b[^>]*id="menu-drawer"[^>]*>(.*?)</dialog>', page.raw, re.S)
                if drawer:
                    self.assertNotIn('passport.html', drawer.group(1), path.name)
                self.assertNotIn('passport-pending.html', page.links, path.name)
        self.assertIn('system-workflow.html', Page(ROOT / 'prototype/review.html').links)
        workflow = (ROOT / 'prototype/system-workflow.html').read_text()
        self.assertIn('Bitrix Admin workflow concept / review only', workflow)
        self.assertIn('S/N: DEMO-SN-', workflow)
        self.assertNotIn('Принудительно активировать', workflow)
        internal = Page(ROOT / 'prototype/system-workflow.html')
        records = {a['data-system-component-id'] for _, a in internal.elements if 'data-system-component-id' in a}
        choices = [a['value'] for _, a in internal.elements if 'data-replacement-choice' in a]
        self.assertEqual(len(records), 9)
        self.assertEqual(set(choices), records)
        self.assertEqual(len(choices), 2 * len(records), 'Upgrade and repair each select the same current records once')

    def test_workflow_is_disposable_admin_concept_with_related_order_systems(self):
        workflow = (ROOT / 'prototype/system-workflow.html').read_text()
        text = ' '.join(re.sub(r'<[^>]+>', ' ', workflow).split())
        page = Page(ROOT / 'prototype/system-workflow.html')
        for public_asset in ('k-site-header', 'k-passport-shell', 'k-passport-brand', 'brand-intro', 'shell.js', 'brand.css'):
            self.assertNotIn(public_asset, workflow)
        self.assertNotIn('index.html', page.links)
        self.assertIn('k-admin-review-bar', workflow)
        self.assertIn('одноразовый', workflow.lower())
        self.assertIn('не приложение для клиента', text)
        self.assertIn('Systems · Ownership Requests · Inquiries · Statuses · Settings', text)
        self.assertIn('Main · Components · Passport · Service · Ownership · History', text)
        self.assertIn('Системы KORSAC · карточка заказа Bitrix', text)
        self.assertIn('Полные данные System не переносятся в свойства заказа', text)
        self.assertIn('ORDER_ID + ORDER_BASKET_ID + ORDER_UNIT_INDEX', text)
        self.assertIn('Обычный product · System не создаётся', text)

    def test_admin_ownership_review_shows_evidence_without_secret_or_takeover(self):
        page = Page(ROOT / 'prototype/system-workflow.html')
        raw = page.raw
        self.assertIn('data-ownership-review', raw)
        self.assertIn('data-current-owner', raw)
        self.assertIn('data-secret-verified', raw)
        self.assertIn('С прошлой смены владельца прошло менее 7 дней', ' '.join(raw.split()))
        for operation in ('approveOwnership', 'rejectOwnership'):
            buttons = [a for tag, a in page.elements if tag == 'button' and a.get('data-workflow-action') == operation]
            self.assertEqual(len(buttons), 1)
            self.assertNotIn('disabled', buttons[0], 'Recent change is a warning, not a block')
            self.assertEqual(buttons[0]['type'], 'button')
        self.assertIn('data-workflow-form="ownership-transfer"', raw)
        self.assertIn('INITIAL_ORDER', raw)
        self.assertIn('ADMIN_TRANSFER', raw)
        self.assertIn('USER_UNLINK', raw)
        self.assertNotIn('SECRET_CODE', raw)
        self.assertNotRegex(raw, r'(?<![\w-])\d{4}-\d{4}(?![\w-])')
        self.assertFalse(any(tag == 'input' and re.search(r'secret|code', a.get('name', '') + a.get('id', ''), re.I) for tag, a in page.elements))
        fixture = json.loads((ROOT / 'docs/frontend/review/system-passport-fixture.json').read_text())['internal_ownership_review']
        self.assertIn(str(fixture['system_user_id']) + ' · DEMO-ACCOUNT-B', raw)
        self.assertIn(str(fixture['request']['request_user_id']) + ' · DEMO-ACCOUNT-C', raw)
        self.assertEqual(fixture['history'][-1]['new_user_id'], fixture['system_user_id'])
        self.assertEqual(fixture['history'][0]['new_user_id'], fixture['initial_order_user_id'])
        self.assertTrue(fixture['request']['secret_verified'])
        self.assertTrue(fixture['recent_change_warning'])
        self.assertNotIn('secret_code', json.dumps(fixture).lower())
        script = (ROOT / 'prototype/assets/js/system-workflow.js').read_text()
        self.assertNotRegex(script, r'\b(?:fetch|XMLHttpRequest|localStorage|sessionStorage|randomUUID|randomBytes)\b')

    def test_fixture_projection_uses_variable_slots_and_authored_snapshots(self):
        fixture = json.loads((ROOT / 'docs/frontend/review/system-passport-fixture.json').read_text())
        page = Page(ROOT / 'prototype/passport.html')
        self.assertEqual(page.system_ids, [fixture['system_id']])
        slots = [a['data-component-slot'] for _, a in page.elements if 'data-passport-component' in a]
        self.assertEqual(slots, [c['slot_key'] for c in fixture['components'] if c['status'] == 'ACTIVE'])
        self.assertEqual(len(slots), len(set(slots)))
        self.assertIn('SSD_1', slots)
        self.assertIn('SSD_2', slots)
        for marker, key in (('data-transfer-date', 'transfer_date'), ('data-warranty-end', 'warranty_end')):
            self.assertEqual([a['datetime'] for _, a in page.elements if marker in a], [fixture[key]])
        public = (ROOT / 'prototype/passport.html').read_text()
        pending = (ROOT / 'prototype/passport-pending.html').read_text()
        self.assertNotIn('8f9ab671c60345244f08ed310f912b8d', public + pending)
        self.assertEqual(Page(ROOT / 'prototype/passport-pending.html').system_ids, [fixture['pending_system_id']])
        self.assertNotEqual(fixture['pending_system_id'], fixture['secondary_system_id'])
        inquiry = (ROOT / 'prototype/assets/js/passport-inquiry.js').read_text()
        self.assertNotRegex(inquiry, r'\b(?:fetch|XMLHttpRequest|localStorage|sessionStorage|randomBytes|randomUUID)\b')


if __name__ == '__main__':
    unittest.main()
