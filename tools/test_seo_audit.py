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
    def check_fixture(self, html=GOOD, extra=None, page_name='product.html'):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'prototype').mkdir()
            media = root / 'prototype/assets/images/projects/fixture.jpg'
            media.parent.mkdir(parents=True)
            media.write_bytes(b'fixture: audit checks presence, source authenticity is reviewed separately')
            (root / 'prototype' / page_name).write_text(html, encoding='utf-8')
            for name, contents in (extra or {}).items():
                target = root / 'prototype' / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(contents, encoding='utf-8')
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

    def breadcrumb_fixture(self, items):
        graph = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}
        return GOOD.replace('</head>', '<script type="application/ld+json">' + json.dumps(graph) + '</script></head>')

    def test_breadcrumb_non_final_items_required(self):
        items = [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'index.html'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Computers', 'item': '/computers/'},
            {'@type': 'ListItem', 'position': 3, 'name': 'PLAY'},
        ]
        for index in (0, 1):
            with self.subTest(index=index):
                broken = [dict(item) for item in items]
                broken[index].pop('item')
                # The ListItem's own identity cannot replace the target page.
                broken[index]['@id'] = '/computers/'
                self.assertIn(f'ListItem #{index + 1} requires a valid item', self.errors(self.breadcrumb_fixture(broken)))

    def test_breadcrumb_valid_representations_and_final_omission(self):
        for value in ('index.html', '/computers/', 'https://example.com/computers/', {'@id': '/computers/'}, {'@id': 'https://example.com/computers/'}):
            with self.subTest(value=value):
                items = [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Ancestor', 'item': value},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Current'},
                ]
                self.assertEqual(self.check_fixture(self.breadcrumb_fixture(items))['errors'], 0)
                items[-1]['item'] = {'@id': 'product.html'}
                self.assertEqual(self.check_fixture(self.breadcrumb_fixture(items))['errors'], 0)

    def test_breadcrumb_invalid_items_and_list_shape(self):
        for value in (None, '', 'not a URL', '#', 'javascript:alert(1)', 'data:text/html,test', 'https://', 'https://[broken', 42, {}, {'@id': ''}, {'@id': 42}, {'url': '/computers/'}):
            with self.subTest(value=value):
                items = [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Ancestor', 'item': value},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Current'},
                ]
                self.assertIn('requires a valid item', self.errors(self.breadcrumb_fixture(items)))
        for items in (None, [], {}, ['invalid']):
            with self.subTest(items=items):
                self.assertIn('BreadcrumbList', self.errors(self.breadcrumb_fixture(items)))
        self.assertIn('requires a valid item', self.errors(self.breadcrumb_fixture([
            {'@type': 'ListItem', 'position': 1, 'name': 'Current', 'item': ''},
        ])))

    def test_invalid_and_unsafe_schema(self):
        self.assertIn('Invalid JSON-LD', self.errors(GOOD.replace('</head>', '<script type="application/ld+json">{bad}</script></head>')))
        for node, message in [({'@type': 'Offer', 'price': '179900'}, 'Offer'), ({'@type': 'AggregateOffer', 'lowPrice': '179900'}, 'AggregateOffer'), ({'@type': 'AggregateRating', 'ratingValue': 5}, 'AggregateRating'), ({'@type': 'Review', 'reviewBody': 'Dummy'}, 'Review')]:
            with self.subTest(type=node['@type']):
                graph = {'@context': 'https://schema.org', '@graph': [{'@type': 'Product', 'offers': [node]}]}
                self.assertIn(message, self.errors(GOOD.replace('</head>', '<script type="application/ld+json">' + json.dumps(graph) + '</script></head>')))

    def test_family_pages_require_collection_not_product(self):
        breadcrumb = {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'index.html'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Family'},
        ]}
        for name in ('computers.html', 'catalog.html', 'create.html', 'work.html'):
            for page_type, expected in [('CollectionPage', 0), ('Product', 2)]:
                with self.subTest(page=name, type=page_type):
                    graph = {'@context': 'https://schema.org', '@graph': [{'@type': page_type}, breadcrumb]}
                    markup = GOOD.replace('</head>', '<script type="application/ld+json">' + json.dumps(graph) + '</script></head>')
                    self.assertEqual(self.check_fixture(markup, page_name=name)['errors'], expected)
            missing = self.check_fixture(GOOD, page_name=name)
            self.assertTrue(any('requires BreadcrumbList' in e for e in missing['pages'][0]['errors']))

    def test_new_families_are_discovered_and_keep_all_staging_guards(self):
        extras = {}
        for name in ('computers', 'create', 'work'):
            graph = {'@context': 'https://schema.org', '@graph': [
                {'@type': 'CollectionPage'},
                {'@type': 'BreadcrumbList', 'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'product.html'},
                    {'@type': 'ListItem', 'position': 2, 'name': name},
                ]},
            ]}
            markup = GOOD.replace('Fixture', name).replace('</head>', '<script type="application/ld+json">' + json.dumps(graph) + '</script></head>')
            extras[name + '.html'] = markup
        good = self.check_fixture(extra=extras)
        self.assertEqual(len(good['pages']), 4)
        self.assertEqual(good['errors'], 0)
        for name in extras:
            for mutation, message in [
                (extras[name].replace('noindex, nofollow, noarchive', 'index, follow'), 'robots must'),
                (extras[name].replace('</main>', '<p id="main">duplicate</p></main>'), 'Duplicate HTML ID'),
                (extras[name].replace('</main>', '<a href="missing.html">missing</a></main>'), 'Broken local link'),
                (extras[name].replace('</main>', '<h1>Duplicate</h1></main>'), 'Expected one H1'),
            ]:
                with self.subTest(page=name, guard=message):
                    broken = dict(extras, **{name: mutation})
                    self.assertIn(message, '\n'.join(e for p in self.check_fixture(extra=broken)['pages'] for e in p['errors']))

    def project_markup(self, page_type, extra_nodes=None):
        graph = {'@context': 'https://schema.org', '@graph': [
            {'@type': page_type, 'headline' if page_type == 'Article' else 'name': 'Fixture'},
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'product.html'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Project'},
            ]},
        ] + (extra_nodes or [])}
        markup = GOOD.replace('</head>', '<script type="application/ld+json">' + json.dumps(graph) + '</script></head>')
        photo = '<img data-project-image src="assets/images/projects/fixture.jpg" alt="Fixture computer" width="600" height="480">'
        # Both media containers are valid; a schema mutation must still expose media.
        media = '<article class="k-project-entry"><figure data-project-cover>' + photo + '</figure></article><ul data-project-gallery><li>' + photo + '</li></ul>'
        return markup.replace('</main>', media + '</main>')

    def test_projects_schema_requires_article_or_collection_and_breadcrumb(self):
        for name, required in [('projects.html', 'CollectionPage'), ('project.html', 'Article')]:
            with self.subTest(page=name):
                valid = self.project_markup(required)
                self.assertEqual(self.check_fixture(valid, page_name=name)['errors'], 0)
                for wrong in ['Product', 'WebPage', 'Article' if required == 'CollectionPage' else 'CollectionPage']:
                    errors = self.check_fixture(self.project_markup(wrong), page_name=name)['pages'][0]['errors']
                    self.assertTrue(any(f'requires {required}' in e for e in errors))
                    if wrong == 'Product':
                        self.assertIn('Project case/list must not claim Product schema', errors)
                # Required list semantics cannot disappear while entity type remains correct.
                no_crumb = self.project_markup(required).replace('"BreadcrumbList"', '"ItemList"')
                self.assertIn('Projects page requires BreadcrumbList schema', self.check_fixture(no_crumb, page_name=name)['pages'][0]['errors'])
                # A valid Article/Collection must not conceal an extra Product entity.
                product = self.project_markup(required, [{'@type': 'Product'}])
                self.assertIn('Project case/list must not claim Product schema', self.check_fixture(product, page_name=name)['pages'][0]['errors'])

    def test_projects_reject_commercial_and_review_schema(self):
        for name, required in [('projects.html', 'CollectionPage'), ('project.html', 'Article')]:
            for prohibited in ['Offer', 'AggregateOffer', 'Review', 'AggregateRating']:
                with self.subTest(page=name, prohibited=prohibited):
                    markup = self.project_markup(required, [{'@type': prohibited}])
                    errors = self.check_fixture(markup, page_name=name)['pages'][0]['errors']
                    self.assertTrue(any(prohibited in e for e in errors))
            for key in ['offers', 'review', 'aggregateRating']:
                markup = self.project_markup(required, [{key: {}}])
                self.assertGreater(self.check_fixture(markup, page_name=name)['errors'], 0)

    def test_projects_discovery_and_existing_guards(self):
        extras = {
            name: self.project_markup(required).replace('Fixture', name)
            for name, required in [('projects.html', 'CollectionPage'), ('project.html', 'Article')]
        }
        report = self.check_fixture(extra=extras)
        self.assertEqual(len(report['pages']), 3)
        self.assertEqual(report['errors'], 0)
        for name in extras:
            for mutation, message in [
                (extras[name].replace('noindex, nofollow, noarchive', 'index, follow'), 'robots must'),
                (extras[name].replace('</main>', '<p id="main">duplicate</p></main>'), 'Duplicate HTML ID'),
                (extras[name].replace('</main>', '<a href="gone.html">gone</a></main>'), 'Broken local link'),
                (extras[name].replace('</main>', '<h1>Extra</h1></main>'), 'Expected one H1'),
                (extras[name].replace('"item": "product.html"', '"item": ""'), 'requires a valid item'),
                (extras[name].replace('</head>', '<link rel="canonical" href="https://example.com"></head>'), 'canonical'),
                (extras[name].replace('</main>', '<img src="pixel.svg"></main>'), 'Missing image alt'),
            ]:
                with self.subTest(page=name, guard=message):
                    broken = dict(extras, **{name: mutation, 'pixel.svg': '<svg/>'})
                    errors = '\n'.join(e for p in self.check_fixture(extra=broken)['pages'] for e in p['errors'])
                    self.assertIn(message, errors)

    def test_project_media_presence_and_local_resources(self):
        for name, required in [('projects.html', 'CollectionPage'), ('project.html', 'Article')]:
            valid = self.project_markup(required)
            with self.subTest(page=name):
                self.assertEqual(self.check_fixture(valid, page_name=name)['errors'], 0)
                no_media = valid.replace('data-project-image', 'data-other-image')
                errors = self.check_fixture(no_media, page_name=name)['pages'][0]['errors']
                self.assertTrue(any('requires a project' in e for e in errors))
                for src, message in [
                    ('assets/images/projects/missing.jpg', 'Missing local project image'),
                    ('https://www.king-komp.com/upload/photo.jpg', 'must be a local project photograph'),
                    ('assets/images/brand/logo.svg', 'must be a local project photograph'),
                ]:
                    changed = valid.replace('assets/images/projects/fixture.jpg', src)
                    self.assertTrue(any(message in e for e in self.check_fixture(changed, page_name=name)['pages'][0]['errors']))
        # It is not enough for some other record to have an image.
        extra_record = self.project_markup('CollectionPage').replace('</main>', '<article class="k-project-entry"><h2>Missing cover</h2></article></main>')
        self.assertIn('Projects record #2 requires a project image', self.check_fixture(extra_record, page_name='projects.html')['pages'][0]['errors'])
        no_gallery = self.project_markup('Article').replace('data-project-gallery', 'data-other-gallery')
        self.assertIn('Project detail requires visible gallery images in base HTML', self.check_fixture(no_gallery, page_name='project.html')['pages'][0]['errors'])

    def test_project_photos_need_alt_and_dimensions(self):
        for name, required in [('projects.html', 'CollectionPage'), ('project.html', 'Article')]:
            valid = self.project_markup(required)
            for mutation, message in [
                (valid.replace('alt="Fixture computer"', ''), 'requires non-empty alt'),
                (valid.replace('alt="Fixture computer"', 'alt=" "'), 'requires non-empty alt'),
                (valid.replace('width="600"', ''), 'requires explicit positive width/height'),
                (valid.replace('height="480"', 'height="0"'), 'requires explicit positive width/height'),
            ]:
                with self.subTest(page=name, guard=message):
                    self.assertTrue(any(message in e for e in self.check_fixture(mutation, page_name=name)['pages'][0]['errors']))

    def test_article_image_must_be_visible_project_media(self):
        valid = self.project_markup('Article')
        for image in ['assets/images/projects/fixture.jpg', ['assets/images/projects/fixture.jpg'], {'@type': 'ImageObject', 'url': 'assets/images/projects/fixture.jpg'}]:
            changed = valid.replace('"headline": "Fixture"', '"headline": "Fixture", "image": ' + json.dumps(image))
            self.assertEqual(self.check_fixture(changed, page_name='project.html')['errors'], 0)
        for image in [['assets/images/projects/fixture.jpg', ''], '', 'assets/images/projects/hidden.jpg', 'https://example.com/photo.jpg', {'url': ''}]:
            changed = valid.replace('"headline": "Fixture"', '"headline": "Fixture", "image": ' + json.dumps(image))
            self.assertIn('Article.image must refer to an actual visible local project image', self.check_fixture(changed, page_name='project.html')['pages'][0]['errors'])


if __name__ == '__main__':
    unittest.main()
