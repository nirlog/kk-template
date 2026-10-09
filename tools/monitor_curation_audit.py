#!/usr/bin/env python3
"""Review-only curation/source contract; does not infer product suitability or stock."""
import argparse
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit


class Selection(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.sections = []
        self.family = None
        self.card = None
        self.field = None
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'section' and 'data-monitor-family' in a:
            self.family = {'name': a['data-monitor-family'], 'cards': []}
            self.sections.append(self.family)
        if tag == 'article' and 'data-monitor-card' in a:
            self.card = {'id': a.get('data-monitor-product', ''), 'name': '', 'url': '', 'image': {}, 'specs': [], 'price': ''}
            if self.family is not None:
                self.family['cards'].append(self.card)
        if self.card is not None:
            if tag == 'img' and 'data-monitor-image' in a:
                self.card['image'] = a
            if tag == 'a' and 'data-monitor-link' in a:
                self.card['url'] = a.get('href', '')
            if tag in ('h3', 'dt', 'dd', 'strong'):
                self.field = tag
                if tag in ('dt', 'dd'):
                    self.card['specs'].append('')

    def handle_data(self, data):
        if self.card is not None:
            if self.field == 'h3':
                self.card['name'] += data
            elif self.field == 'strong':
                self.card['price'] += data
            elif self.field in ('dt', 'dd'):
                self.card['specs'][-1] += data

    def handle_endtag(self, tag):
        if tag == self.field:
            self.field = None
        if tag == 'article':
            self.card = None
        if tag == 'section':
            self.family = None


def audit(root):
    review = root / 'docs/frontend/review'
    products = json.loads((review / 'equipment-product-sources.json').read_text())
    media = json.loads((review / 'equipment-media-sources.json').read_text())
    selection = Selection((root / 'prototype/monitors.html').read_text())
    errors = []
    ids = [p.get('product_id') for p in products]
    if len(set(ids)) != len(ids) or None in ids:
        errors.append('Product ledger requires unique stable product IDs')
    if len({p['catalog_source'] for p in products}) != len(products):
        errors.append('Family assignments must not duplicate a product entity/source URL')
    if not 9 <= len(products) <= 12:
        errors.append('Review assortment requires 9–12 unique products')
    if [s['name'] for s in selection.sections] != ['PLAY', 'CREATE', 'WORK']:
        errors.append('Category requires ordered PLAY, CREATE, WORK sections')
    appearances = Counter()
    lookup = {p.get('product_id'): p for p in products}
    for section in selection.sections:
        family = section['name']
        cards = section['cards']
        if not 3 <= len(cards) <= 6:
            errors.append(f'{family} requires 3–6 recommendations')
        if len({c['id'] for c in cards}) != len(cards):
            errors.append(f'{family} repeats a product within the same section')
        for card in cards:
            key = card['id']
            appearances[(key, family)] += 1
            product = lookup.get(key)
            if product is None:
                errors.append(f'Unverified product: {key}')
                continue
            relation = product.get('families', {}).get(family, {})
            if not relation.get('editorial_reason') or not relation.get('selection_label'):
                errors.append(f'{key}/{family} requires an editorial relationship')
            if card['name'].strip() != product['name']:
                errors.append(f'{key}: name differs from its product entity')
            if card['url'] != product['review_url'] or urlsplit(card['url']).query:
                errors.append(f'{key}: canonical review link differs or creates a query facet')
            specs = [s.strip() for s in card['specs']]
            if specs != [v for pair in product['card_specifications'] for v in pair]:
                errors.append(f'{key}: displayed specifications differ from source ledger')
            if re.sub(r'\D', '', card['price']) != str(product['review_price_rub']):
                errors.append(f'{key}: price example differs from source snapshot')
            cover = next((m for m in media if m['product'] == product['media_key'] and m['source_gallery_position'] == 1), None)
            img = card['image']
            if cover is None or any(str(img.get(k, '')) != str(cover[v]) for k, v in [('src', 'file'), ('width', 'width'), ('height', 'height'), ('alt', 'alt')]):
                errors.append(f'{key}: photograph/attributes differ from source manifest')
    for p in products:
        for family in p.get('families', {}):
            if appearances[(p.get('product_id'), family)] != 1:
                errors.append(f'{p.get("product_id")}/{family}: ledger relationship must appear exactly once')
        if p.get('http_status') != 200 or not p.get('displayed_facts'):
            errors.append(f'{p.get("product_id")}: verified source facts required')
        for field in ('catalog_source', 'specification_source'):
            u = urlsplit(p[field])
            if u.scheme != 'https' or not u.hostname:
                errors.append(f'{p.get("product_id")}: invalid HTTPS source')
        for field in ('catalog_html_sha256', 'specification_html_sha256'):
            if not re.fullmatch('[0-9a-f]{64}', p.get(field, '')):
                errors.append(f'{p.get("product_id")}: source hash required')
    for m in media:
        path = root / 'prototype' / m['file']
        if not path.resolve().is_relative_to((root / 'prototype/assets/images/equipment').resolve()) or not path.is_file():
            errors.append(f'Missing/local media path: {m["file"]}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != m['sha256'] or path.stat().st_size != m['bytes']:
            errors.append(f'Original media bytes differ: {m["file"]}')
    return {'unique_products': len(products), 'family_counts': {s['name']: len(s['cards']) for s in selection.sections}, 'errors': sorted(set(errors))}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = audit(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['errors']))
