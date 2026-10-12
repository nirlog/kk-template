"""Negative architecture fixtures exercise cross-page guards, not backend behavior."""
from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile
import unittest

from final_audit import Document, ROUTES, audit

ROOT = Path(__file__).resolve().parents[1]


class FinalAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.root = Path(cls.directory.name)
        for name in ('prototype', 'docs'):
            shutil.copytree(ROOT / name, cls.root / name)
        shutil.copy(ROOT / 'README.md', cls.root / 'README.md')

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    @contextmanager
    def changed(self, relative, before, after):
        path = self.root / relative
        original = path.read_text()
        self.assertIn(before, original)
        path.write_text(original.replace(before, after, 1))
        try:
            yield audit(self.root)
        finally:
            path.write_text(original)

    def messages(self, result):
        return result['repository_errors'] + [error for p in result['pages'] for error in p['errors']]

    def test_current_complete_inventory(self):
        result = audit(ROOT)
        self.assertEqual(result['errors'], 0, self.messages(result))
        self.assertEqual(len(result['pages']), 31)
        self.assertEqual(result['verified_source_media'], 23)
        self.assertEqual({p.name for p in (ROOT / 'prototype').glob('account*.html')}, {n for n in ROUTES if n.startswith('account-')})

    def test_unapproved_account_dashboard_is_detected(self):
        p = self.root / 'prototype/account.html'
        shutil.copy(self.root / 'prototype/account-orders.html', p)
        try:
            self.assertTrue(any('extra=' in e and 'account.html' in e for e in audit(self.root)['repository_errors']))
        finally:
            p.unlink()

    def test_missing_links_fragments_and_css_assets(self):
        for before, after in [('href="computers.html"', 'href="missing.html"'), ('href="product.html#configurator"', 'href="product.html#missing-anchor"')]:
            with self.subTest(after=after), self.changed('prototype/index.html', before, after) as result:
                self.assertGreater(result['seo_errors'], 0)
        with self.changed('prototype/assets/css/account.css', '.k-account-container', '.k-account-container') as _:
            p = self.root / 'prototype/assets/css/account.css'
            p.write_text(p.read_text() + '\n.test {background:url(missing.png)}')
            self.assertTrue(any('Missing local resource' in e for e in self.messages(audit(self.root))))

    def test_feature_branch_and_dead_document_links(self):
        with self.changed('prototype/review.html', 'blob/main/', 'blob/feat/dead-branch/') as r:
            self.assertTrue(any('unstable feature-branch' in e for e in self.messages(r)))
        with self.changed('prototype/review.html', 'blob/main/docs/frontend/KORSAC-INFORMATION-ARCHITECTURE.md', 'blob/main/docs/frontend/missing.md') as r:
            self.assertTrue(any('missing stable GitHub document' in e for e in self.messages(r)))
        with self.changed('README.md', '(prototype/index.html)', '(prototype/missing.html)') as r:
            self.assertTrue(any('Missing local resource' in e for e in self.messages(r)))

    def test_breadcrumb_urls_labels_positions_remain_synchronized(self):
        for before, after in [('"item": "computers.html"', '"item": "catalog.html"'), ('"name": "Компьютеры"', '"name": "Other entity"'), ('"position": 2', '"position": 8')]:
            with self.subTest(after=after), self.changed('prototype/product.html', before, after) as r:
                self.assertTrue(any('Breadcrumb' in e for e in self.messages(r)))

    def test_schema_page_type_contract_all_types(self):
        for name, before, after in [('index', '"@type": "WebSite"', '"@type": "Product"'), ('product', '"@type": "Product"', '"@type": "Article"'), ('project', '"@type": "Article"', '"@type": "Product"'), ('contacts', '"@type": "ContactPage"', '"@type": "Article"')]:
            with self.subTest(name=name), self.changed(f'prototype/{name}.html', before, after) as r:
                self.assertTrue(any('Schema page-type mismatch' in e for e in self.messages(r)))
        with self.changed('prototype/index.html', '</head>', '<meta property="og:url" content="https://fake.invalid/"></head>') as r:
            self.assertTrue(any('invent production og:url' in e for e in self.messages(r)))
        with self.changed('prototype/cart.html', '</head>', '<script type="application/ld+json">{"@type":"Product"}</script></head>') as r:
            self.assertTrue(any('Utility/private/admin' in e for e in self.messages(r)))

    def test_internal_review_and_private_footer_are_not_public_navigation(self):
        with self.changed('prototype/index.html', 'href="contacts.html"', 'href="system-workflow.html"') as r:
            self.assertTrue(any('Internal Admin workflow' in e for e in self.messages(r)))
        with self.changed('prototype/index.html', 'href="contacts.html"', 'href="account-systems.html"') as r:
            self.assertTrue(any('Public footer' in e for e in self.messages(r)))

    def test_primary_nav_no_sixth_entry_and_account_drawer_is_native(self):
        with self.changed('prototype/index.html', '<nav class="k-site-nav" aria-label="Основная навигация">', '<nav class="k-site-nav" aria-label="Основная навигация"><a href="account-login.html">Аккаунт</a>') as r:
            self.assertTrue(any('five approved' in e for e in self.messages(r)))
        with self.changed('prototype/index.html', 'href="account-login.html"', 'href="#site-prototype"') as r:
            self.assertTrue(any('native Login link' in e for e in self.messages(r)))

        with self.changed('prototype/index.html', 'Поиск появится при подключении магазина.', 'Поиск и личный кабинет появятся при подключении магазина.') as r:
            self.assertTrue(any('missing concept' in e for e in self.messages(r)))

    def test_product_example_does_not_follow_configuration(self):
        with self.changed('prototype/product.html', 'data-passport-example', 'data-passport-example data-passport-output="ram"') as r:
            self.assertTrue(any('physical System projection/output' in e for e in self.messages(r)))
        with self.changed('prototype/assets/js/prototype.js', '"use strict";', '"use strict"; // data-passport-output') as r:
            self.assertTrue(any('stale configurator/Passport' in e for e in self.messages(r)))

    def test_protected_data_cannot_enter_customer_or_public_source(self):
        for name in ('index', 'product', 'monitor', 'cart', 'checkout', 'account-order', 'passport', 'passport-pending'):
            for field in ('USER_ID', 'SECRET_CODE', 'DEMO-SN', 'OwnershipHistory'):
                with self.subTest(page=name, field=field), self.changed(f'prototype/{name}.html', '</head>', f'<!-- {field} --></head>') as r:
                    self.assertTrue(any('protected internal/credential' in e for e in self.messages(r)))

    def test_mixed_commerce_identity_type_and_source_amounts(self):
        for filename in ('checkout', 'order-success'):
            for before, after in [('data-order-line-type="product"', 'data-order-line-type="system"'), ('381 850 ₽', '359 800 ₽'), ('1 × 22 050 ₽', '1 × 22 051 ₽'), ('MSI MAG 274QF X24', 'Invented product')]:
                with self.subTest(page=filename, after=after), self.changed(f'prototype/{filename}.html', before, after) as r:
                    self.assertTrue(any(filename + '.html' in e for e in r['repository_errors']), self.messages(r))
        with self.changed('prototype/product.html', '</head>', '<!-- 1234-5678 --></head>') as r:
            self.assertTrue(any('physical secret-code value' in e for e in self.messages(r)))
        with self.changed('prototype/cart.html', 'data-cart-line-type="product"', 'data-cart-line-type="product" data-cart-config="03"') as r:
            self.assertTrue(any('Ordinary cart product' in e for e in self.messages(r)))

    def test_monitor_remains_ordinary_product(self):
        with self.changed('prototype/monitor.html', '<main', '<main data-product-experience') as r:
            self.assertTrue(any('Ordinary monitor' in e for e in self.messages(r)))

    def test_brand_intro_excludes_private_and_utility_pages(self):
        with self.changed('prototype/account-orders.html', '</head>', '<script src="assets/js/brand-intro.js"></script></head>') as r:
            self.assertTrue(any('Brand Intro participation' in e for e in self.messages(r)))

    def test_deferred_media_viewer_and_source_bytes(self):
        with self.changed('prototype/index.html', '</head>', '<script src="https://cdn.example.invalid/viewer.js"></script></head>') as r:
            self.assertTrue(any('runtime/media dependencies must be local' in e for e in self.messages(r)))
        with self.changed('prototype/assets/js/prototype.js', '"use strict";', '"use strict"; Fancybox.bind("[data-gallery]");') as r:
            self.assertTrue(any('deferred Media Viewer' in e for e in self.messages(r)))
        p = self.root / 'prototype/assets/images/projects/white-i5-01.jpg'
        data = p.read_bytes()
        try:
            p.write_bytes(data + b'corruption')
            self.assertTrue(any('Media source bytes/hash mismatch' in e for e in self.messages(audit(self.root))))
        finally:
            p.write_bytes(data)

    def test_malformed_jsonld_is_reported_without_crashing(self):
        with self.changed('prototype/index.html', '"@context": "https://schema.org"', 'invalid-json') as r:
            self.assertGreater(r['seo_errors'], 0)

    def test_stale_markdown_review_anchor_is_detected(self):
        with self.changed('README.md', '(docs/frontend/KORSAC-FINAL-AUDIT.md)', '(docs/frontend/KORSAC-FINAL-AUDIT.md#nonexistent-section)') as r:
            self.assertTrue(any('Missing Markdown anchor' in e for e in self.messages(r)))

    def test_authoritative_mapping_cannot_drift(self):
        with self.changed('docs/frontend/KORSAC-FINAL-AUDIT.md', '`/computers/play/1440/`', '`/wrong/`') as r:
            self.assertTrue(any('route mapping differs' in e for e in self.messages(r)))

    def test_tree_parser_handles_nested_labels_and_semantics(self):
        valid = Document('<main><a href="x"><svg><path /></svg> Text <span>value</span></a><input></main>')
        self.assertEqual(valid.errors, [])
        self.assertEqual(valid.root.all('a')[0].text, 'Text value')
        self.assertTrue(Document('<main><nav></main></nav>').errors)


if __name__ == '__main__':
    unittest.main()
