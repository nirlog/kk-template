"""Negative fixtures exercise the staging guard, independent of production markup."""
import json
from pathlib import Path
import tempfile
import unittest
from seo_audit import audit

GOOD = '''<!doctype html><html lang="ru"><head><title>Fixture</title>
<meta name="description" content="Fixture description">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta property="og:title" content="Fixture"><meta property="og:description" content="Fixture description">
<meta property="og:site_name" content="KORSAC"><meta property="og:type" content="website">
</head><body><main id="main"><h1>Fixture</h1><a href="#main">Main</a></main></body></html>'''


class AuditGuardTests(unittest.TestCase):
    def check_fixture(self, html=GOOD, extra=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'prototype').mkdir()
            (root / 'prototype/product.html').write_text(html, encoding='utf-8')
            for name, contents in (extra or {}).items():
                (root / 'prototype' / name).write_text(contents, encoding='utf-8')
            result = audit(root)
            self.assertEqual(result, audit(root), 'Audit output must be deterministic')
            return result

    def errors(self, html, extra=None):
        return '\n'.join(error for page in self.check_fixture(html, extra)['pages'] for error in page['errors'])

    def test_good_fixture_and_empty_directory(self):
        self.assertEqual(self.check_fixture()['errors'], 0)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(audit(Path(tmp))['errors'], 1)

    def test_staging_indexing_and_canonical(self):
        self.assertIn('robots must', self.errors(GOOD.replace('noindex, nofollow, noarchive', 'index, follow')))
        self.assertIn('canonical', self.errors(GOOD.replace('</head>', '<link rel="canonical" href="https://example.com/"></head>')))

    def test_metadata_and_h1(self):
        for changed, message in [(GOOD.replace('lang="ru"', ''), 'lang'), (GOOD.replace('lang="ru"', 'lang'), 'lang'), (GOOD.replace('<title>Fixture</title>', '<title> </title>'), 'title'), (GOOD.replace('content="Fixture description"', 'content=""', 1), 'description'), (GOOD.replace('<h1>Fixture</h1>', ''), 'H1'), (GOOD.replace('</main>', '<h1>Another</h1></main>'), 'H1')]:
            with self.subTest(message=message):
                self.assertIn(message, self.errors(changed))
        self.assertIn('Duplicate page title', self.errors(GOOD, {'duplicate.html': GOOD}))
        self.assertIn('Duplicate page description', self.errors(GOOD, {'duplicate.html': GOOD}))

    def test_ids_links_images(self):
        for markup, message in [('<p id="main">duplicate</p>', 'Duplicate HTML ID'), ('<a href="missing.html">missing</a>', 'Broken local link'), ('<a href="#gone">missing</a>', 'Broken HTML fragment'), ('<a href="other.html#gone">missing</a>', 'Broken HTML fragment'), ('<img src="pixel.svg">', 'Missing image alt')]:
            with self.subTest(message=message):
                self.assertIn(message, self.errors(GOOD.replace('</main>', markup + '</main>'), {'pixel.svg': '<svg/>', 'other.html': GOOD.replace('Fixture', 'Other')}))
        report = self.check_fixture(GOOD.replace('</main>', '<img src="pixel.svg" alt=""></main>'), {'pixel.svg': '<svg/>'})
        self.assertTrue(any('dimensions' in w for p in report['pages'] for w in p['warnings']))

    def test_implicit_offer_and_rating_properties(self):
        for key, value in [('offers', {'price': 179900}), ('aggregateRating', {'ratingValue': 5}), ('review', {'reviewBody': 'Dummy'})]:
            graph = {'@type': 'Product', key: value}
            self.assertGreater(self.check_fixture(GOOD.replace('</head>', '<script type="application/ld+json">' + json.dumps(graph) + '</script></head>'))['errors'], 0)

    def test_invalid_and_unsafe_schema(self):
        self.assertIn('Invalid JSON-LD', self.errors(GOOD.replace('</head>', '<script type="application/ld+json">{bad}</script></head>')))
        for node, message in [({'@type': 'Offer', 'price': '179900'}, 'Offer'), ({'@type': 'AggregateOffer', 'lowPrice': '179900'}, 'AggregateOffer'), ({'@type': 'AggregateRating', 'ratingValue': 5}, 'AggregateRating'), ({'@type': 'Review', 'reviewBody': 'Dummy'}, 'Review')]:
            with self.subTest(type=node['@type']):
                graph = {'@context': 'https://schema.org', '@graph': [{'@type': 'Product', 'offers': [node]}]}
                self.assertIn(message, self.errors(GOOD.replace('</head>', '<script type="application/ld+json">' + json.dumps(graph) + '</script></head>')))


if __name__ == '__main__':
    unittest.main()
