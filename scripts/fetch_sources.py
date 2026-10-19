"""Cache the public sources cited by the supplied CV for portfolio preparation."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import base64
import json
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.research'
CACHE.mkdir(exist_ok=True)


def fetch(url, dest):
    dest = CACHE / dest
    if dest.exists() and dest.stat().st_size:
        return dest.read_bytes()
    request = urllib.request.Request(url, headers={'User-Agent': 'AcademicPortfolio/1.0'})
    with urllib.request.urlopen(request, timeout=40) as response:
        data = response.read()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    print(f'Saved {dest.relative_to(ROOT)} ({len(data)} bytes)', flush=True)
    return data


def paper(slug, arxiv):
    fetch(f'https://arxiv.org/pdf/{arxiv}', f'{slug}.pdf')
    fetch(f'https://arxiv.org/html/{arxiv}', f'{slug}.html')


def repository(owner, name, slug):
    api = f'https://api.github.com/repos/{owner}/{name}'
    meta = json.loads(fetch(api, f'{slug}/metadata.json'))
    branch = meta['default_branch']
    tree = json.loads(fetch(f'{api}/git/trees/{branch}?recursive=1', f'{slug}/tree.json'))
    try:
        readme = json.loads(fetch(f'{api}/readme', f'{slug}/readme.json'))
        (CACHE / slug / 'README.md').write_bytes(base64.b64decode(readme['content']))
    except Exception as error:
        print(f'{slug} README: {error}', flush=True)
    for item in tree.get('tree', []):
        path = item['path']
        if item['type'] == 'blob' and not path.startswith('database/') and path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg', '.pdf')) and item.get('size', 0) < 8_000_000:
            try:
                fetch(f'https://raw.githubusercontent.com/{owner}/{name}/{branch}/{urllib.parse.quote(path)}', f'{slug}/media/{path}')
            except Exception as error:
                print(f'{slug}/{path}: {error}', flush=True)


jobs = [
    (paper, ('urag', '2603.19281')),
    (paper, ('rag-security', '2608.24977')),
    (paper, ('vialectbench', '2608.10414')),
    (repository, ('coutMinh', 'EVENT-Event-Based-Image-Retrieval', 'eventa')),
    (repository, ('SEAS-CVN', 'SEAS-Flood-Prediction', 'seas-flood')),
    (repository, ('SEAS-CVN', 'fast-fish-identification', 'seas-fish')),
    (repository, ('coutMinh', 'AII_2024', 'ai-glasses')),
    (fetch, ('https://seas-cvn.com/staff/tran-ta-quang-minh-2026', 'seas-profile.html')),
    (fetch, ('https://seas-cvn.com/images/team/2026/tran-ta-quang-minh-2026.jpg', 'portrait.jpg')),
    (fetch, ('https://arxiv.org/html/2603.19281v1/Dataset_construct_pipeline.png', 'urag-pipeline.png')),
    (fetch, ('https://arxiv.org/html/2608.24977v2/thumbnail.png', 'rag-security-overview.png')),
    (fetch, ('https://arxiv.org/html/2608.10414v1/vialect_annotation_pipeline.png', 'vialectbench-pipeline.png')),
    (fetch, ('https://arxiv.org/html/2608.10414v1/dialects_thumb.png', 'vialectbench-thumbnail.png')),
    (fetch, ('https://ltnghia.github.io/eventa/eventa-2025', 'eventa-challenge.html')),
    (fetch, ('https://drive.google.com/uc?export=download&id=1z1emGFeWblzfZNHfj7KFqWS6QIZnkWvt', 'eventa-paper.pdf')),
]
with ThreadPoolExecutor(max_workers=6) as pool:
    futures = [pool.submit(fn, *args) for fn, args in jobs]
    for (fn, args), future in zip(jobs, futures):
        try:
            future.result()
        except Exception as error:
            print(f'FAILED {args}: {error}', flush=True)
