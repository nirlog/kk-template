"""Negative review fixtures prevent assortment and shared-product identity drift."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from monitor_curation_audit import audit

ROOT = Path(__file__).resolve().parents[1]


class MonitorCurationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.page = self.root / 'prototype/monitors.html'
        self.page.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / 'prototype/monitors.html', self.page)
        self.review = self.root / 'docs/frontend/review'
        self.review.mkdir(parents=True)
        for name in ('equipment-product-sources.json', 'equipment-media-sources.json'):
            shutil.copyfile(ROOT / 'docs/frontend/review' / name, self.review / name)
        shutil.copytree(ROOT / 'prototype/assets/images/equipment', self.root / 'prototype/assets/images/equipment')

    def products(self, change):
        path = self.review / 'equipment-product-sources.json'
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def errors(self):
        return '\n'.join(audit(self.root)['errors'])

    def test_current_review_is_complete_and_deterministic(self):
        report = audit(self.root)
        self.assertEqual(report, audit(self.root))
        self.assertEqual(report['unique_products'], 10)
        self.assertEqual(report['family_counts'], {'PLAY': 4, 'CREATE': 4, 'WORK': 5})
        self.assertEqual(report['errors'], [])

    def test_family_structure_and_choice_cannot_collapse(self):
        original = self.page.read_text()
        self.page.write_text(original.replace('data-monitor-family="CREATE"', 'data-monitor-family="PLAY"'))
        self.assertIn('ordered PLAY, CREATE, WORK', self.errors())
        # Two recommendations cannot silently satisfy a curated family.
        self.page.write_text(original.replace('data-monitor-card', 'data-removed-card', 2))
        self.assertIn('PLAY requires 3–6', self.errors())
        self.products(lambda p: p.__delitem__(slice(8, None)))
        self.assertIn('9–12 unique', self.errors())

    def test_shared_models_cannot_become_duplicate_entities(self):
        self.products(lambda p: p.append(dict(p[4])))
        self.assertIn('unique stable product IDs', self.errors())
        self.assertIn('must not duplicate a product entity/source URL', self.errors())

    def test_each_appearance_keeps_its_verified_identity_and_url(self):
        original = self.page.read_text()
        # Alter only one appearance of the shared LG model.
        self.page.write_text(original.replace('LG 27U631A-B</h3>', 'LG Fictional Model</h3>', 1))
        self.assertIn('name differs', self.errors())
        self.page.write_text(original.replace('href="https://www.king-komp.com/catalog/monitory/259632/"', 'href="monitors.html?family=CREATE"', 1))
        self.assertIn('query facet', self.errors())
        self.page.write_text(original.replace('data-monitor-product="lg-27u631a-b"', 'data-monitor-product="unverified"', 1))
        self.assertIn('Unverified product', self.errors())

    def test_facts_prices_and_editorial_relationships_cannot_drift(self):
        original = self.page.read_text()
        self.page.write_text(original.replace('<dd>до 240 Гц · DisplayPort</dd>', '<dd>до 999 Гц · DisplayPort</dd>', 1))
        self.assertIn('specifications differ', self.errors())
        self.page.write_text(original.replace('22 050 ₽', '99 999 ₽', 1))
        self.assertIn('price example differs', self.errors())
        self.page.write_text(original)
        self.products(lambda p: p[4]['families']['WORK'].pop('editorial_reason'))
        self.assertIn('editorial relationship', self.errors())

    def test_original_media_cannot_be_swapped_or_modified(self):
        original = self.page.read_text()
        self.page.write_text(original.replace('assets/images/equipment/lg-01.webp', 'assets/images/equipment/msi-mag-01.webp', 1))
        self.assertIn('photograph/attributes differ', self.errors())
        self.page.write_text(original)
        media = self.root / 'prototype/assets/images/equipment/lg-01.webp'
        media.write_bytes(b'substitute image')
        self.assertIn('Original media bytes differ', self.errors())

    def test_source_verification_cannot_be_removed(self):
        self.products(lambda p: p[0].update(http_status=404, catalog_html_sha256='', displayed_facts={}))
        self.assertIn('verified source facts required', self.errors())
        self.assertIn('source hash required', self.errors())


if __name__ == '__main__':
    unittest.main()
