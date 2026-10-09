#!/usr/bin/env python3
"""Deterministic, dependency-free checks for the staging prototype, not a search validator."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

POLICY = 'noindex, nofollow, noarchive'
FAMILY_PAGES = {'computers.html', 'catalog.html', 'create.html', 'work.html'}
PROJECT_PAGES = {'projects.html': 'CollectionPage', 'project.html': 'Article'}


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.lang = ''
        self.titles = []
        self.meta = {}
        self.meta_counts = Counter()
        self.ids = []
        self.links = []
        self.images = []
        self.project_records = []
        self.project_covers = []
        self.project_galleries = []
        self._project_record = None
        self._project_cover = False
        self._project_gallery = None
        self.h1 = 0
        self.canonical = False
        self.jsonld = []
        self._title = None
        self._ld = None
        self.feed(path.read_text(encoding='utf-8'))
        self.close()

    def handle_starttag(self, tag, attrs):
        a = {key: value or '' for key, value in attrs}
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'html':
            self.lang = a.get('lang', '')
        if tag == 'title':
            self._title = ''
        if tag == 'h1':
            self.h1 += 1
        if tag == 'meta':
            key = a.get('name', a.get('property', '')).lower()
            self.meta[key] = a.get('content', '').strip()
            self.meta_counts[key] += 1
        if tag == 'link' and 'canonical' in a.get('rel', '').split():
            self.canonical = True
        if tag in ('a', 'link') and 'href' in a:
            self.links.append(a['href'])
        if 'src' in a:
            self.links.append(a['src'])
        if 'srcset' in a:
            self.links.extend(item.strip().split()[0] for item in a['srcset'].split(',') if item.strip())
        if tag == 'article' and 'k-project-entry' in a.get('class', '').split():
            self._project_record = []
            self.project_records.append(self._project_record)
        if tag == 'figure' and 'data-project-cover' in a:
            self._project_cover = True
        if tag == 'ul' and 'data-project-gallery' in a:
            self._project_gallery = []
            self.project_galleries.append(self._project_gallery)
        if tag == 'img':
            self.images.append(a)
            if 'data-project-image' in a:
                if self._project_record is not None:
                    self._project_record.append(a)
                if self._project_cover:
                    self.project_covers.append(a)
                if self._project_gallery is not None:
                    self._project_gallery.append(a)
        if tag == 'script' and a.get('type', '').lower() == 'application/ld+json':
            self._ld = ''

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        if self._title is not None:
            self._title += data
        if self._ld is not None:
            self._ld += data

    def handle_endtag(self, tag):
        if tag == 'article':
            self._project_record = None
        if tag == 'figure':
            self._project_cover = False
        if tag == 'ul':
            self._project_gallery = None
        if tag == 'title' and self._title is not None:
            self.titles.append(self._title.strip())
            self._title = None
        if tag == 'script' and self._ld is not None:
            self.jsonld.append(self._ld)
            self._ld = None


def schema_nodes(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from schema_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from schema_nodes(child)


def valid_breadcrumb_url(value):
    """Accept review paths or HTTP(S) page URLs, also via item: {"@id": URL}."""
    if isinstance(value, dict):
        value = value.get('@id')
    if not isinstance(value, str) or not value or any(c.isspace() for c in value):
        return False
    if any(ord(c) < 32 or c in '<>"{}\\' for c in value):
        return False
    try:
        url = urlsplit(value)
        if url.scheme:
            # Accessing port also rejects malformed/out-of-range authorities.
            url.port
            return url.scheme.lower() in ('http', 'https') and bool(url.hostname)
        return not url.netloc and bool(url.path) and not value.startswith('//')
    except ValueError:
        return False


def breadcrumb_errors(node):
    items = node.get('itemListElement')
    if not isinstance(items, list) or not items:
        return ['BreadcrumbList requires a non-empty itemListElement list']
    errors = []
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            errors.append(f'BreadcrumbList ListItem #{index} must be an object')
        elif index < len(items) or 'item' in item:
            if not valid_breadcrumb_url(item.get('item')):
                errors.append(f'BreadcrumbList ListItem #{index} requires a valid item URL or item.@id; only the final item may omit item')
    return errors


def project_media_errors(page, prototype):
    """Check authored review media presence/attributes, not photographic authenticity."""
    errors = []
    photos = [img for img in page.images if 'data-project-image' in img]
    if page.path.name == 'projects.html':
        if not page.project_records:
            errors.append('Projects list requires authored project records with media')
        for index, images in enumerate(page.project_records, 1):
            if not images:
                errors.append(f'Projects record #{index} requires a project image')
    if page.path.name == 'project.html':
        if not page.project_covers:
            errors.append('Project detail requires a project cover image')
        if not any(page.project_galleries):
            errors.append('Project detail requires visible gallery images in base HTML')
    for img in photos:
        src = img.get('src', '')
        url = urlsplit(src)
        target = (page.path.parent / unquote(url.path)).resolve()
        directory = (prototype / 'assets/images/projects').resolve()
        if url.scheme or url.netloc or not target.is_relative_to(directory) or target.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp', '.avif'):
            errors.append(f'Project image must be a local project photograph: {src}')
        elif not target.is_file():
            errors.append(f'Missing local project image: {src}')
        if not img.get('alt', '').strip():
            errors.append(f'Project image requires non-empty alt: {src}')
        if not all(img.get(k, '').isdigit() and int(img[k]) > 0 for k in ('width', 'height')):
            errors.append(f'Project image requires explicit positive width/height: {src}')
    return errors


def article_image_urls(value):
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, dict):
        return article_image_urls(value.get('url', value.get('contentUrl')))
    if isinstance(value, list):
        groups = [article_image_urls(child) for child in value]
        return [url for group in groups for url in group] if groups and all(groups) else []
    return []


def audit(root):
    prototype = root / 'prototype'
    files = sorted(prototype.glob('*.html'))
    pages = {p.resolve(): Page(p) for p in files}
    results = []
    title_counts = Counter(title for p in pages.values() for title in p.titles if title)
    desc_counts = Counter(p.meta.get('description') for p in pages.values() if p.meta.get('description'))
    for path, page in list(pages.items()):
        errors, warnings, types = [], [], set()
        if not page.lang.strip():
            errors.append('Missing HTML lang')
        elif page.lang != 'ru':
            errors.append('Expected HTML lang=ru')
        if len(page.titles) != 1 or not page.titles[0]:
            errors.append('Expected one non-empty title')
        elif title_counts[page.titles[0]] > 1:
            errors.append('Duplicate page title')
        if not page.meta.get('description'):
            errors.append('Missing non-empty meta description')
        elif desc_counts[page.meta['description']] > 1:
            errors.append('Duplicate page description')
        for key in ('description', 'robots', 'viewport', 'og:title', 'og:description', 'og:site_name', 'og:type'):
            if page.meta_counts[key] != 1 or not page.meta.get(key):
                errors.append(f'Expected one non-empty {key} meta')
        if page.meta.get('robots', '').lower() != POLICY:
            errors.append('Prototype robots must be noindex, nofollow, noarchive')
        if page.h1 != 1:
            errors.append(f'Expected one H1, found {page.h1}')
        for ident, count in sorted(Counter(page.ids).items()):
            if count > 1:
                errors.append(f'Duplicate HTML ID: {ident}')
        if page.canonical:
            errors.append('Prototype must not publish a production canonical')
        for src in sorted(set(page.links)):
            url = urlsplit(src)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.is_relative_to(root.resolve()):
                errors.append(f'Local link escapes repository: {src}')
                continue
            if not target.is_file():
                errors.append(f'Broken local link: {src}')
                continue
            if url.fragment and target.suffix == '.html':
                if target not in pages:
                    pages[target] = Page(target)
                if unquote(url.fragment) not in pages[target].ids:
                    errors.append(f'Broken HTML fragment: {src}')
        for img in page.images:
            if 'alt' not in img:
                errors.append(f'Missing image alt: {img.get("src", "(no src)")}')
            dimensions = (img.get('width', ''), img.get('height', ''))
            if not all(v.isdigit() and int(v) > 0 for v in dimensions):
                warnings.append(f'Review image dimensions/aspect ratio: {img.get("src", "(no src)")}')
        for index, raw in enumerate(page.jsonld, 1):
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f'Invalid JSON-LD #{index}: {exc.msg} at line {exc.lineno}')
                continue
            for node in schema_nodes(data):
                node_types = node.get('@type', [])
                if isinstance(node_types, str):
                    node_types = [node_types]
                if not isinstance(node_types, list) or not all(isinstance(t, str) for t in node_types):
                    errors.append('Invalid schema @type value')
                    continue
                types.update(node_types)
                if path.name == 'project.html' and 'Article' in node_types and 'image' in node:
                    image_urls = article_image_urls(node['image'])
                    visible = {img.get('src') for img in page.images if 'data-project-image' in img}
                    if not image_urls or any(url not in visible for url in image_urls):
                        errors.append('Article.image must refer to an actual visible local project image')
                if 'BreadcrumbList' in node_types:
                    errors.extend(breadcrumb_errors(node))
                for t in node_types:
                    if t in ('Offer', 'AggregateOffer'):
                        errors.append(f'Prototype schema must not claim authoritative {t} (including sample Offer.price)')
                    if t in ('Review', 'AggregateRating'):
                        errors.append(f'Prototype has no authoritative {t} data')
                if 'offers' in node:
                    errors.append('Prototype must not carry offers, including implicit sample Offer.price')
                if 'aggregateRating' in node or 'review' in node:
                    errors.append('Prototype has no authoritative review/rating data')
                for key in ('@id', 'url', 'logo', 'item'):
                    value = node.get(key)
                    if isinstance(value, str):
                        try:
                            if not urlsplit(value).scheme:
                                warnings.append('Relative schema URLs/IDs are semantic-review only; production needs absolute canonical URLs')
                        except ValueError:
                            errors.append(f'Invalid schema URL in {key}')
        if path.name in ('404.html', '500.html', '503.html') and types:
            errors.append('Error templates must not carry content structured data')
        if path.name in FAMILY_PAGES:
            for required in ('CollectionPage', 'BreadcrumbList'):
                if required not in types:
                    errors.append(f'Computer hub/family requires {required} schema')
            if 'Product' in types:
                errors.append('Computer hub/family landing must not claim Product schema')
        if path.name in PROJECT_PAGES:
            errors.extend(project_media_errors(page, prototype))
            for required in (PROJECT_PAGES[path.name], 'BreadcrumbList'):
                if required not in types:
                    errors.append(f'Projects page requires {required} schema')
            if 'Product' in types:
                errors.append('Project case/list must not claim Product schema')
        warnings.extend(['Prototype canonical/og:url intentionally omitted; production follows page-type policy and approved host', 'No approved og:image; production social artwork remains pending'])
        results.append({'page': path.relative_to(root.resolve()).as_posix(), 'title': page.titles[0] if page.titles else '', 'schema_types': sorted(types), 'errors': sorted(set(errors)), 'warnings': sorted(set(warnings))})
    if not files:
        return {'pages': [], 'errors': 1, 'warnings': 0, 'failure': 'No prototype/*.html files found'}
    return {'pages': results, 'errors': sum(len(p['errors']) for p in results), 'warnings': sum(len(p['warnings']) for p in results)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1], help='Repository containing prototype/')
    parser.add_argument('--json', action='store_true', help='Emit machine-readable deterministic report')
    args = parser.parse_args()
    result = audit(args.root.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for page in result['pages']:
            print(f'{page["page"]}: schema={", ".join(page["schema_types"]) or "none"}; errors={len(page["errors"])}; warnings={len(page["warnings"])}')
            for issue in page['errors']:
                print(f'  ERROR {issue}')
            for issue in page['warnings']:
                print(f'  WARN  {issue}')
        if 'failure' in result:
            print(f'ERROR {result["failure"]}')
        print(f'{len(result["pages"])} pages; {result["errors"]} errors; {result["warnings"]} intentional/review warnings')
    return int(result['errors'] > 0)


if __name__ == '__main__':
    raise SystemExit(main())
