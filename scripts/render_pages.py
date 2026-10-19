"""Render the four static pages with relative, GitHub Pages-compatible URLs."""
from html import escape
from pathlib import Path
from string import Template
import json

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/portfolio.json').read_text(encoding='utf-8'))
profile = json.loads((ROOT / 'data/profile.json').read_text(encoding='utf-8'))


def e(value):
    return escape(str(value), quote=True)


def icon(paths, cls=''):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'


ICONS = {
    'Email': icon('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>'),
    'Google Scholar': icon('<path d="m2 9 10-6 10 6-10 6-10-6Z"/><path d="M6 12v5c4 3 8 3 12 0v-5M22 9v8"/>'),
    'GitHub': icon('<path d="M9 19c-4 1-4-2-6-2m12 5v-4c0-1-.4-2-1-2 4-.5 6-2 6-6 0-1-.3-2-1-3 .3-1 .3-3 0-4-2 0-3 1-4 2a14 14 0 0 0-6 0C8 4 7 3 5 3c-.3 1-.3 3 0 4-.7 1-1 2-1 3 0 4 2 5.5 6 6-.6 0-1 1-1 2v4"/>'),
    'LinkedIn': icon('<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7M7 7h.01M11 17v-7m0 3c0-4 6-4 6 0v4"/>'),
    'location': icon('<path d="M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>'),
    'document': icon('<path d="M14 2H5v20h14V7l-5-5Zm0 0v5h5M8 12h8M8 16h6"/>'),
    'notebook': icon('<path d="M5 3h14v18H5zM3 7h4M3 12h4M3 17h4M10 8h5M10 12h5M10 16h3"/>'),
    'theme': icon('<path d="M20.3 15.2A8.5 8.5 0 0 1 8.8 3.7a8.5 8.5 0 1 0 11.5 11.5Z"/>', 'moon-icon') + icon('<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>', 'sun-icon')
}


def external(url, label, cls=''):
    return f'<a class="{cls}" href="{e(url)}" target="_blank" rel="noopener">{label}</a>'


def resource_links(project):
    return ''.join(external(link['url'], e(link['label']) + ' <span aria-hidden="true">↗</span>') for link in project['links'])


def figure(project):
    return f'''<figure class="paper-figure"><a class="figure-link" href="{e(project['image'])}" data-figure-title="{e(project['title'])}" data-credit="{e(project['figure_credit'])}" data-source="{e(project['figure_source'])}" aria-label="Enlarge the original {e(project['title'])} figure"><img src="{e(project['image'])}" alt="{e(project['image_alt'])}" loading="lazy"><span class="figure-enlarge" aria-hidden="true">↗</span></a><figcaption>{external(project['figure_source'], 'Original paper figure ↗')}</figcaption></figure>'''


def abstract(project):
    return f'<details class="abstract"><summary>Abstract <span aria-hidden="true">+</span></summary><p>{e(project["abstract"])}</p></details>'


def publication(project, selected=False):
    authors = e(project['authors']).replace('Minh Tran', '<strong>Minh Tran</strong>')
    # Contribution labels stay beside the citation; full abstracts remain on Publications.
    title = f'<a href="publications.html#{e(project["id"])}">{e(project["paper_title"])}</a>' if selected else e(project['paper_title'])
    accepted = ' accepted' if project['id'] == 'rag-security' else ''
    return f'''<article id="{e(project['id'])}" class="publication-item">{figure(project)}<div class="paper-content"><div class="paper-meta"><span class="status{accepted}">{e(project['status'])}</span><span class="contribution">{e(project['role'])}</span></div><h3>{title}</h3><p class="authors">{authors}</p><p class="paper-summary">{e(project['summary'])}</p><div class="paper-links">{resource_links(project)}</div>{'' if selected else abstract(project)}</div></article>'''


def project_card(project):
    media = figure(project) if project.get('image') else ''
    category = project['category']
    manuscript = f'<p class="manuscript-title">{e(project["paper_title"])}</p>' if project.get('paper_title') else ''
    return f'''<article id="{e(project['id'])}" class="project-card{' has-figure' if media else ''}" data-category="{e(category)}">{media}<div class="project-content"><div class="paper-meta"><span class="status{' accepted' if project['id']=='ai-glasses' else ''}">{e(project['status'])}</span><span class="contribution">{e(project['role'])}</span></div><h2>{e(project['title'])}</h2><p class="project-subtitle">{e(project['subtitle'])}</p><p>{e(project['summary'])}</p>{manuscript}<div class="tags">{''.join(f'<span>{e(tag)}</span>' for tag in project['tags'])}</div>{abstract(project)}<div class="paper-links">{resource_links(project)}</div></div></article>'''


def institution_logo(item):
    image = f'<img src="{e(item["logo"])}" alt="{e(item["institution"])} logo" width="36" height="36" loading="lazy">'
    return external(item['url'], image, 'institution-logo')


def education():
    rows = []
    for item in profile['education']:
        detail = f'<p class="education-detail">{e(item["detail"])}</p>' if item['detail'] else ''
        title = external(item['url'], e(item['institution']))
        rows.append(f'<article class="background-item">{institution_logo(item)}<div><h3>{title}</h3><p>{e(item["qualification"])}</p><p class="item-date">{e(item["period"])}</p>{detail}</div></article>')
    return ''.join(rows)


def teaching():
    rows = []
    for item in profile['teaching']:
        title = external(item['url'], e(item.get('display_name', item['institution'])))
        rows.append(f'<article class="teaching-item">{institution_logo(item)}<div><h3>{title}</h3><p class="teaching-role">{e(item["role"])}</p><p class="item-date">{e(item["period"])}</p><details class="teaching-details"><summary>Details <span aria-hidden="true">+</span></summary><p class="teaching-detail">{e(item["detail"])}</p></details></div></article>')
    return ''.join(rows)


def honors():
    rows = []
    for item in profile['honors']:
        title = external(item['url'], e(item['title']) + ' <span class="award-arrow" aria-hidden="true">↗</span>') if item.get('url') else e(item['title'])
        date = f'<span class="award-date">{e(item["date"])} · </span>' if item['date'] else ''
        rows.append(f'<li id="{e(item["id"])}"><span class="award-dot" aria-hidden="true"></span><div><h3>{title}</h3><p>{date}{e(item["detail"])}</p></div></li>')
    return ''.join(rows)


def ongoing():
    return ''.join(f'<article class="ongoing-item"><span class="ongoing-dot" aria-hidden="true"></span><div><h3>{e(item["title"])}</h3><p>{e(item["description"])}</p><p class="supervisors">With {e(item["supervisors"])}</p>{external(item["url"], "Research slides ↗") if item.get("url") else ""}</div></article>' for item in profile['ongoing'])


def render():
    research = [p for p in data['projects'] if p['category'] == 'research']
    projects = [p for p in data['projects'] if p['category'] != 'research']
    for item in data['other_projects']:
        link = {'label': 'Live demo' if item['id']=='aquasafe' else 'Code', 'url': item['url']}
        projects.append({**item, 'links': [link]})
    # Put built systems together, followed by the clearly attributed mentoring work.
    projects.sort(key=lambda p: p['category'] == 'mentored')
    social = ''.join(f'<a href="{e(item["url"])}"' + ('' if item['label']=='Email' else ' target="_blank" rel="noopener"') + f'>{ICONS[item["label"]]}<span>{e(item["label"])}</span></a>' for item in profile['links'])
    values = {'profile_links': social, 'location_icon': ICONS['location'], 'document_icon': ICONS['document'], 'notebook_icon': ICONS['notebook'], 'selected_publications': ''.join(publication(p, True) for p in research), 'education': education(), 'teaching': teaching(), 'honors': honors(), 'publications': ''.join(publication(p) for p in research), 'ongoing': ongoing(), 'projects': ''.join(project_card(p) for p in projects), 'scholar_url': e(next(p['url'] for p in profile['links'] if p['label']=='Google Scholar'))}
    pages = [('Home','index.html','home.html','Undergraduate AI researcher at VNU-HCM. Work in trustworthy AI, retrieval-augmented generation, and Vietnamese language understanding.'), ('Publications','publications.html','publications.html','Publications by Tran Ta Quang Minh on RAG robustness, uncertainty quantification, and Vietnamese dialects.'), ('Blog','blog.html','blog.html','Research notes and writing by Tran Ta Quang Minh.'), ('Projects','projects.html','projects.html','Applied AI projects and mentored student work by Tran Ta Quang Minh.')]
    base = Template((ROOT/'templates/base.html').read_text(encoding='utf-8'))
    for name, filename, template, description in pages:
        body = Template((ROOT/'templates'/template).read_text(encoding='utf-8')).substitute(values)
        navigation = ''.join(f'<a href="{path}"' + (' aria-current="page"' if label==name else '') + f'>{label}</a>' for label, path, _, _ in pages)
        html = base.substitute(title=e('Tran Ta Quang Minh' if name=='Home' else f'{name} · Tran Ta Quang Minh'), description=e(description), body=body, navigation=navigation, theme_icon=ICONS['theme'], page_class=f'{name.lower()}-page', updated=e(profile['content_updated']))
        (ROOT/filename).write_text(html, encoding='utf-8')
