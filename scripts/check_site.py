"""Validate every rendered page, including cross-page anchors and local assets."""
from html.parser import HTMLParser
from pathlib import Path
from string import Template
from urllib.parse import unquote, urlsplit
import json

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index.html', 'publications.html', 'blog.html', 'projects.html']


class Site(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.images = []
        self.current = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for attr in ('href', 'src', 'data-source'):
            if attrs.get(attr):
                self.links.append(attrs[attr])
        if tag == 'img' and attrs.get('src'):
            self.images.append(attrs)
        if attrs.get('aria-current') == 'page':
            self.current.append(attrs.get('href'))


documents = {}
errors = []
for filename in PAGES:
    html = (ROOT / filename).read_text(encoding='utf-8')
    site = Site()
    site.feed(html)
    documents[filename] = site
    if len(site.ids) != len(set(site.ids)):
        errors.append(f'{filename}: duplicate HTML IDs')
    if site.current != [filename]:
        errors.append(f'{filename}: incorrect active navigation')
    if Template(html).get_identifiers():
        errors.append(f'{filename}: unresolved template placeholders')
    for marker in ('TODO', 'Lorem ipsum', 'Your Name'):
        if marker in html:
            errors.append(f'{filename}: unresolved placeholder {marker}')

for filename, site in documents.items():
    for link in site.links:
        parts = urlsplit(link)
        if parts.scheme or parts.netloc:
            continue
        path = unquote(parts.path) if parts.path else filename
        target = (ROOT / path).resolve()
        if parts.path.startswith('/') or not target.is_relative_to(ROOT) or not target.is_file():
            errors.append(f'{filename}: invalid or missing local resource {link}')
            continue
        # Windows is case-insensitive; deployed GitHub Pages paths are not.
        actual = ROOT
        for part in Path(path).parts:
            if part not in {p.name for p in actual.iterdir()}:
                errors.append(f'{filename}: incorrect path casing {link}')
                break
            actual /= part
        if parts.fragment and target.name in documents and parts.fragment not in documents[target.name].ids:
            errors.append(f'{filename}: missing anchor {link}')
    for image in site.images:
        if not image.get('alt'):
            errors.append(f'{filename}: missing image description {image["src"]}')
        if urlsplit(image['src']).scheme:
            errors.append(f'{filename}: image depends on an external host')

copy = (ROOT / 'content/projects.md').read_text(encoding='utf-8')
data = json.loads((ROOT / 'data/portfolio.json').read_text(encoding='utf-8'))
profile = json.loads((ROOT / 'data/profile.json').read_text(encoding='utf-8'))
for project in data['projects'] + data['other_projects']:
    destination = 'publications.html' if project['category'] == 'research' else 'projects.html'
    if project['id'] not in documents[destination].ids:
        errors.append(f'{destination}: missing project {project["id"]}')
    if project['title'] not in copy or project['abstract'] not in copy:
        errors.append(f'Missing project copy: {project["id"]}')
    if project['category'] == 'mentored' and 'mentor' not in project['role'].lower():
        errors.append(f'Missing mentor attribution: {project["id"]}')
    if project.get('image'):
        if not project.get('figure_source') or not project.get('figure_credit'):
            errors.append(f'Missing figure provenance: {project["id"]}')
        path = ROOT / project['image']
        if not path.is_file() or path.stat().st_size < 1000:
            errors.append(f'Invalid figure: {project["id"]}')
for award in profile['honors']:
    if award['id'] not in documents['index.html'].ids:
        errors.append(f'Missing honor: {award["id"]}')
if not (ROOT / '.nojekyll').is_file():
    errors.append('Missing .nojekyll')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(PAGES)} pages; {sum(len(s.links) for s in documents.values())} resource/anchor links; {len(profile["honors"])} honors; local images, cross-page anchors, roles, and figure sources verified.')
