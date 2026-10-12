#!/usr/bin/env python3
"""Cross-page static architecture audit. No network, browser or backend claims."""
import argparse
from collections import Counter
from dataclasses import dataclass, field
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from seo_audit import ACCOUNT_PAGES, Page, audit as seo_audit, schema_nodes

# Concrete review mappings. IA owns production policy; FINAL-AUDIT owns mapping.
ROUTES = {
    'index.html': ('/', 'Homepage', ('Organization', 'WebSite')),
    'computers.html': ('/computers/', 'Computer hub', ('CollectionPage', 'BreadcrumbList')),
    'catalog.html': ('/computers/play/', 'PLAY family', ('CollectionPage', 'BreadcrumbList')),
    'create.html': ('/computers/create/', 'CREATE family', ('CollectionPage', 'BreadcrumbList')),
    'work.html': ('/computers/work/', 'WORK family', ('CollectionPage', 'BreadcrumbList')),
    'product.html': ('/computers/play/1440/', 'Computer model', ('Product', 'BreadcrumbList')),
    'projects.html': ('/projects/', 'Projects archive', ('CollectionPage', 'BreadcrumbList')),
    'project.html': ('/projects/{approved-slug}/', 'Historical project', ('Article', 'BreadcrumbList')),
    'equipment.html': ('/equipment/', 'Equipment hub', ('CollectionPage', 'BreadcrumbList')),
    'monitors.html': ('/equipment/monitors/', 'Curated category', ('CollectionPage', 'BreadcrumbList')),
    'monitor.html': ('/equipment/monitors/{approved-slug}/', 'Ordinary product', ('Product', 'BreadcrumbList')),
    'cart.html': ('/cart/', 'Transactional cart', ()),
    'checkout.html': ('/checkout/', 'Transactional checkout', ()),
    'order-success.html': ('/order-success/', 'Transactional result', ()),
    'contacts.html': ('/contacts/', 'Contacts', ('ContactPage', 'BreadcrumbList')),
    'passport.html': ('/passport/{PUBLIC_ID}/', 'Active public System projection', ()),
    'passport-pending.html': ('/passport/{PUBLIC_ID}/', 'Pending public System projection', ()),
    'account-login.html': ('/account/login/', 'Authentication', ()),
    'account-register.html': ('/account/register/', 'Registration', ()),
    'account-forgot-password.html': ('/account/forgot-password/', 'Recovery', ()),
    'account-orders.html': ('/account/orders/', 'Private Orders', ()),
    'account-order.html': ('/account/orders/{id}/', 'Private Order snapshot', ()),
    'account-systems.html': ('/account/systems/', 'Private current Systems', ()),
    'account-inquiries.html': ('/account/inquiries/', 'Private inquiries', ()),
    'account-profile.html': ('/account/profile/', 'Private profile', ()),
    '404.html': ('REQUESTED URL; HTTP 404', 'Error response', ()),
    '500.html': ('REQUESTED URL; HTTP 500', 'Resilient error response', ()),
    '503.html': ('REQUESTED URL; HTTP 503', 'Resilient error response', ()),
    'system-workflow.html': ('NO PUBLIC ROUTE', 'Disposable Bitrix Admin review', ()),
    'ui.html': ('NO PUBLIC ROUTE', 'UI Kit review', ()),
    'review.html': ('NO PUBLIC ROUTE', 'Review navigation', ()),
}
PRIMARY_NAV = ('Компьютеры', 'Конфигуратор', 'Для бизнеса', 'Поддержка', 'О KORSAC')
PRIMARY_HREFS = ('computers.html', 'product.html#configurator', 'work.html', 'product.html#warranty', 'index.html#why')
INTRO_PAGES = {name for name, (_, kind, _) in ROUTES.items() if kind in (
    'Homepage', 'Computer hub', 'PLAY family', 'CREATE family', 'WORK family',
    'Computer model', 'Projects archive', 'Historical project', 'Equipment hub',
    'Curated category', 'Ordinary product')}
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def all(self, tag=None, attr=None, cls=None):
        found = []
        for child in self.children:
            if isinstance(child, Node):
                if (tag is None or child.tag == tag) and (attr is None or attr in child.attrs) and (cls is None or cls in child.attrs.get('class', '').split()):
                    found.append(child)
                found.extend(child.all(tag, attr, cls))
        return found

    @property
    def text(self):
        return ' '.join(' '.join(c.text if isinstance(c, Node) else c for c in self.children).split())


class Document(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.root = Node('document')
        self.stack = [self.root]
        self.errors = []
        self.feed(raw)
        self.close()
        if len(self.stack) != 1:
            self.errors.append('Unclosed HTML elements')

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if len(self.stack) == 1 or self.stack[-1].tag != tag:
            self.errors.append(f'Misnested HTML closing tag: {tag}')
        else:
            self.stack.pop()

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def markdown_anchors(raw):
    anchors, counts, fenced = set(), Counter(), False
    for line in raw.splitlines():
        if line.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
        if fenced:
            continue
        heading = re.match(r'^#{1,6}\s+(.+?)\s*#*$', line)
        if heading:
            slug = re.sub(r'[^\w -]', '', heading[1].lower()).replace(' ', '-')
            index = counts[slug]
            counts[slug] += 1
            anchors.add(slug + (f'-{index}' if index else ''))
    return anchors


def link_errors(path, ref, root, pages):
    """Local file/fragment validation with repository containment, no HTTP fetching."""
    url = urlsplit(ref)
    if url.scheme or url.netloc:
        return []
    target = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
    if not target.is_relative_to(root.resolve()):
        return [f'Local resource escapes repository: {ref}']
    if not target.is_file():
        return [f'Missing local resource: {ref}']
    if url.fragment and target.suffix == '.html':
        page = pages.get(target) or Page(target)
        if unquote(url.fragment) not in page.ids:
            return [f'Missing local anchor: {ref}']
    if url.fragment and target.suffix == '.md' and unquote(url.fragment) not in markdown_anchors(target.read_text()):
        return [f'Missing Markdown anchor: {ref}']
    return []


def parsed_schema(page):
    nodes = []
    for raw in page.jsonld:
        try:
            nodes.extend(schema_nodes(json.loads(raw)))
        except json.JSONDecodeError:
            pass  # The underlying SEO audit reports malformed JSON-LD.
    return nodes


def breadcrumb_sync(page, doc):
    nodes = [n for n in parsed_schema(page) if n.get('@type') == 'BreadcrumbList']
    crumbs = doc.all('nav', cls='k-breadcrumb')
    if not nodes and not crumbs:
        return []
    if len(nodes) != 1 or len(crumbs) != 1:
        return ['Expected one matching visible and structured breadcrumb trail']
    visible = crumbs[0].all('li')
    items = nodes[0].get('itemListElement', [])
    if len(visible) != len(items):
        return ['Visible/schema breadcrumb lengths differ']
    errors = []
    for index, (li, item) in enumerate(zip(visible, items), 1):
        if not isinstance(item, dict) or item.get('position') != index or item.get('name') != li.text:
            errors.append(f'Breadcrumb name/position mismatch at {index}')
            continue
        links = li.all('a')
        schema_url = item.get('item')
        if isinstance(schema_url, dict):
            schema_url = schema_url.get('@id')
        if index < len(items):
            if len(links) != 1 or schema_url != links[0].attrs.get('href'):
                errors.append(f'Breadcrumb ancestor URL mismatch at {index}')
        elif not li.all(attr='aria-current'):
            errors.append('Final visible breadcrumb requires aria-current')
    return errors


def page_contract(page, doc):
    errors = []
    name = page.path.name
    graph = parsed_schema(page)
    types = {n['@type'] for n in graph if isinstance(n.get('@type'), str)}
    expected = set(ROUTES[name][2])
    # Brand/ListItem are nested descriptive types, never independent page entities.
    if types - {'Brand', 'ListItem'} != expected:
        errors.append(f'Schema page-type mismatch: expected {sorted(expected)}, got {sorted(types)}')
    if not expected and page.jsonld:
        errors.append('Utility/private/admin pages require no structured data')
    if page.meta.get('og:url'):
        errors.append('Prototype must not invent production og:url')
    errors.extend(breadcrumb_sync(page, doc))
    for nav in doc.all('nav', cls='k-site-nav'):
        links = nav.all('a')
        if tuple(a.text for a in links) != PRIMARY_NAV or tuple(a.attrs.get('href') for a in links) != PRIMARY_HREFS:
            errors.append('Public primary menu must retain five approved native routes')
    for a in doc.all('a'):
        href = a.attrs.get('href', '')
        if urlsplit(href).path == 'system-workflow.html' and name != 'review.html':
            errors.append('Internal Admin workflow is accessible outside review materials')
        if a.attrs.get('aria-label') == 'KORSAC — главная' and href != 'index.html':
            errors.append('Logo must lead to Homepage')
        if a.text == 'Личный кабинет' or a.attrs.get('aria-label') in ('Личный кабинет', 'Войти в личный кабинет'):
            if href != 'account-login.html' or 'data-dialog-open' in a.attrs:
                errors.append('Public Account utility must be a native Login link, including drawer')
    scope = [n for n in doc.all() if n.attrs.get('id') == 'scope-dialog']
    if scope and 'личный кабинет появ' in scope[0].text.lower():
        errors.append('Scope dialog must not present implemented Account review as a missing concept')
    if name not in ACCOUNT_PAGES:
        for footer in doc.all('footer'):
            for a in footer.all('a'):
                if urlsplit(a.attrs.get('href', '')).path in ACCOUNT_PAGES | {'passport.html', 'passport-pending.html', 'system-workflow.html'}:
                    errors.append('Public footer must not expose private/Passport/internal routes')
    intro = 'src="assets/js/brand-intro.js"' in page.raw
    if intro != (name in INTRO_PAGES):
        errors.append('Brand Intro participation differs from approved public-page policy')
    if name not in ('system-workflow.html', 'ui.html', 'review.html'):
        if re.search(r'(?i)\bUSER[_ -]?ID\b|\bSECRET[_ -]?CODE\b|DEMO-SN|\bS\s*/\s*N\b|OwnershipHistory|data-internal-workflow', page.raw):
            errors.append('Customer/public source exposes protected internal/credential markers')
        if re.search(r'(?<![\w-])\d{4}-\d{4}(?![\w-])', page.raw):
            errors.append('Customer/public source exposes a physical secret-code value')
    if name == 'product.html':
        for token in ('data-passport-output', 'data-public-passport', 'data-transfer-date', 'data-warranty-end'):
            if token in page.raw:
                errors.append(f'Product must not carry a physical System projection/output: {token}')
        example = [n for n in doc.all() if n.attrs.get('id') == 'system-passport-info']
        if len(example) != 1 or 'Пример паспорта' not in example[0].text or not any(a.attrs.get('href') == 'passport.html' for a in example[0].all('a')):
            errors.append('Product requires independently labelled static Passport example')
        if not any(a.attrs.get('href') == 'cart.html' and 'пример корзины' in a.text for a in doc.all('a')):
            errors.append('Product requires honest native static Cart continuation')
    if name == 'monitor.html':
        if doc.all(attr='data-product-experience') or doc.all(attr='data-prototype-config') or doc.all(attr='data-system-id'):
            errors.append('Ordinary monitor must not become a configured PC/System')
        if not any(a.attrs.get('href') == 'cart.html#cart-monitor' for a in doc.all('a')):
            errors.append('Ordinary product requires its own native cart-line destination')
    ids = set(page.ids)
    if len(doc.all('main')) != 1 or not any(a.attrs.get('href') == '#main' for a in doc.all('a')):
        errors.append('Page requires one main landmark and native skip link')
    for label in doc.all('label'):
        if label.attrs.get('for') and label.attrs['for'] not in ids:
            errors.append(f'Label refers to missing control: {label.attrs["for"]}')
    for tag, attrs in page.elements:
        for key in ('src', 'href'):
            if tag in ('script', 'link', 'iframe', 'video', 'audio', 'source') and attrs.get(key) and urlsplit(attrs[key]).netloc:
                errors.append('Prototype runtime/media dependencies must be local')
    for img in page.images:
        if any(urlsplit(img.get(k, '')).netloc for k in ('src',)):
            errors.append('Prototype media must be local, not hotlinked')
        if not all(img.get(k, '').isdigit() and int(img[k]) > 0 for k in ('width', 'height')):
            errors.append(f'Media requires positive dimensions: {img.get("src")}')
    if 'product.html#product-passport' in page.links:
        errors.append('Stale Product Passport anchor')
    return sorted(set(errors))


def amount(text):
    return int(re.sub(r'[^0-9]', '', text.split('₽')[0])) * 100


def commerce_errors(docs):
    errors = []
    cart = docs['cart.html']
    lines = cart.all('article', attr='data-demo-cart-line')
    kinds = Counter(n.attrs.get('data-cart-line-type') for n in lines)
    if kinds != Counter({'system': 2, 'product': 1}):
        errors.append('Mixed Cart requires two configured PC lines and one ordinary product')
    total = sum(int(n.attrs['data-demo-unit-price-minor']) * int(n.all(attr='data-demo-quantity')[0].text) for n in lines)
    for n in lines:
        if n.attrs.get('data-cart-line-type') == 'product' and ('data-cart-config' in n.attrs or 'CONFIG /' in n.text or n.all(attr='data-system-id')):
            errors.append('Ordinary cart product must not carry CONFIG/System identity')
    expected = [n.attrs['data-cart-label'].split(', CONFIG /')[0] for n in lines]
    for filename in ('checkout.html', 'order-success.html'):
        lists = docs[filename].all('ul', cls='k-order-lines')
        if len(lists) != 1:
            errors.append(f'{filename}: expected one authored Order summary')
            continue
        order_lines = lists[0].all('li')
        if Counter(n.attrs.get('data-order-line-type') for n in order_lines) != kinds:
            errors.append(f'{filename}: mixed line kinds differ from source Cart')
        names = [n.all('strong')[0].text.split(' CONFIG /')[0] for n in order_lines]
        if names != expected:
            errors.append(f'{filename}: ordered identities differ from source Cart')
        rendered_total = 0
        for n in order_lines:
            spans = n.all('span')
            price = spans[-1].text if spans else ''
            if '×' in price:
                qty, unit = price.split('×', 1)
                rendered_total += int(qty.strip()) * amount(unit)
        if rendered_total != total:
            errors.append(f'{filename}: saved line amounts disagree with source Cart')
        for block in docs[filename].all(cls='k-submit-total'):
            if amount(block.all('strong')[0].text) != total:
                errors.append(f'{filename}: submission total mismatch')
        for n in docs[filename].all(attr='data-demo-total') + docs[filename].all(attr='data-demo-subtotal'):
            if amount(n.text) != total:
                errors.append(f'{filename}: source total mismatch')
    for n in cart.all(attr='data-demo-total') + cart.all(attr='data-demo-subtotal'):
        if amount(n.text) != total:
            errors.append('Cart source total mismatch')
    return sorted(set(errors))


def repository_errors(root, pages):
    errors = []
    refs = 0
    # Markdown destinations and stable GitHub documents, not historical commit/PR URLs.
    paths = [root / 'README.md', *sorted((root / 'docs').rglob('*.md'))]
    paths += list((root / 'prototype').glob('*.html'))
    for p in paths:
        raw = p.read_text()
        for url in re.findall(r'https://github\.com/nirlog/kk-template/(?:blob|tree)/([^\s"<>)]*)', raw):
            if not url.startswith('main/') and not re.match(r'^[a-f0-9]{40}/', url):
                errors.append(f'{p.relative_to(root)}: unstable feature-branch document URL')
            elif url.startswith('main/'):
                relative = urlsplit(url).path.removeprefix('main/')
                if not (root / unquote(relative)).is_file() and '/blob/' in raw:
                    errors.append(f'{p.relative_to(root)}: missing stable GitHub document: {relative}')
        if p.suffix == '.md':
            for ref in re.findall(r'\]\(([^)\n]+)\)', raw):
                ref = ref.strip('<>')
                refs += 1
                errors.extend(f'{p.relative_to(root)}: {e}' for e in link_errors(p, ref, root, pages))
    report = root / 'docs/frontend/KORSAC-FINAL-AUDIT.md'
    if report.is_file():
        mapping = {}
        for line in report.read_text().splitlines():
            cells = [cell.strip().strip('`') for cell in line.split('|')]
            if len(cells) >= 4 and cells[1].startswith('prototype/'):
                mapping[cells[1].removeprefix('prototype/')] = cells[2]
        if mapping != {name: row[0] for name, row in ROUTES.items()}:
            errors.append('Authoritative final report route mapping differs from audited inventory')
    else:
        errors.append('Missing authoritative final report route mapping')
    for p in (root / 'prototype/assets/css').glob('*.css'):
        for ref in re.findall(r'url\(\s*["\']?([^"\')\s]+)', p.read_text()):
            errors.extend(f'{p.relative_to(root)}: {e}' for e in link_errors(p, ref, root, pages))
    for p in (root / 'prototype/assets/js').glob('*.js'):
        if 'data-passport-output' in p.read_text():
            errors.append(f'{p.name}: stale configurator/Passport output coupling')
    for p in (root / 'prototype').rglob('*'):
        if p.is_file() and 'fancybox' in p.name.lower():
            errors.append('Deferred Fancybox/Media Viewer must not be installed')
    for p in list((root / 'prototype').rglob('*.js')) + list((root / 'prototype').rglob('*.html')):
        if re.search(r'Fancybox\.(?:bind|show)|new\s+Fancybox|@fancyapps/', p.read_text()):
            errors.append(f'{p.relative_to(root)}: deferred Media Viewer is active')
    return sorted(set(errors)), refs


def media_errors(root):
    errors, count = [], 0
    for name in ('projects-media-sources.json', 'equipment-media-sources.json'):
        ledger = json.loads((root / 'docs/frontend/review' / name).read_text())
        for row in ledger:
            count += 1
            p = root / 'prototype' / row['file']
            if not p.is_file() or len(p.read_bytes()) != row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
                errors.append(f'Media source bytes/hash mismatch: {row["file"]}')
    return errors, count


def audit(root):
    root = root.resolve()
    seo = seo_audit(root)
    seo_by_page = {row['page']: row['errors'] for row in seo['pages']}
    pages = {p.resolve(): Page(p) for p in sorted((root / 'prototype').glob('*.html'))}
    names = {p.name for p in pages}
    errors = []
    if names != set(ROUTES):
        errors.append(f'Unreviewed route inventory: missing={sorted(set(ROUTES)-names)}; extra={sorted(names-set(ROUTES))}')
    docs, results = {}, []
    for path, page in pages.items():
        d = Document(page.raw)
        docs[path.name] = d.root
        issues = d.errors[:] + ['SEO: ' + e for e in seo_by_page.get('prototype/' + path.name, [])]
        issues.extend(page_contract(page, d.root) if path.name in ROUTES else [])
        for tag, attrs in page.elements:
            for key in ('action', 'poster', 'data'):
                if attrs.get(key) and tag in ('form', 'video', 'object'):
                    issues.extend(link_errors(path, attrs[key], root, pages))
        results.append({'page': 'prototype/' + path.name, 'production': ROUTES.get(path.name, ('UNREVIEWED',))[0], 'page_type': ROUTES.get(path.name, ('', 'UNREVIEWED'))[1], 'errors': sorted(set(issues))})
    if all(p in docs for p in ('cart.html', 'checkout.html', 'order-success.html')):
        errors.extend(commerce_errors(docs))
    repo_errors, refs = repository_errors(root, pages)
    errors.extend(repo_errors)
    media, media_count = media_errors(root)
    errors.extend(media)
    return {'pages': results, 'repository_errors': sorted(set(errors)), 'seo_errors': seo['errors'], 'seo_review_warnings': seo['warnings'], 'checked_markdown_destinations': refs, 'verified_source_media': media_count, 'errors': len(set(errors)) + sum(len(r['errors']) for r in results), 'limitations': ['Static source checks do not prove backend authorization, lifecycle transactions, email delivery, live commercial state or production HTTP/SEO behavior.', 'Browser layout/accessibility/motion and human visual review are separate evidence.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    result = audit(args.root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for row in result['pages']:
            for e in row['errors']:
                print(f'{row["page"]}: {e}')
        for e in result['repository_errors']:
            print(e)
        print(f'{len(result["pages"])} pages; {result["errors"]} errors; {result["verified_source_media"]} source media verified')
    return int(result['errors'] > 0)


if __name__ == '__main__':
    raise SystemExit(main())
