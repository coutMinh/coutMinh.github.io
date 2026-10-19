"""Build the four static pages and the source-grounded project copy."""
from render_pages import ROOT, data, render

render()

lines = ['# Portfolio project copy', '', f'Prepared from CV_VinCAIR.pdf ({data["updated"]}), the linked papers, and original project repositories.', '', 'Titles and abstracts below are newly written portfolio copy. Formal paper titles are preserved separately. Review and publication labels follow the supplied CV; under-review work is not described as accepted.', '', '## Profile', '', 'Tran Ta Quang Minh (Trần Tạ Quang Minh) is an undergraduate AI researcher at the University of Science, VNU-HCM. His research focuses on trustworthy AI, retrieval-augmented generation, uncertainty quantification, and Vietnamese language understanding. He also develops applied computer-vision systems and mentors student projects at SEAS.', '']
for p in data['projects']:
    lines.extend([f'## {p["title"]}', '', f'**Subtitle:** {p["subtitle"]}', '', f'**Role:** {p["role"]}  ', f'**Status:** {p["status"]}', '', '**Abstract**', '', p['abstract'], '', '**Contribution / scope**', '', p['contribution'], ''])
    if p.get('paper_title'):
        lines.extend([f'**Formal paper title:** {p["paper_title"]}', ''])
    if p.get('image'):
        lines.extend([f'![{p["image_alt"]}](../{p["image"]})', '', f'**Figure credit:** {p["figure_credit"]}', '', f'[Original figure source]({p["figure_source"]})', ''])
    else:
        lines.extend([f'**Image:** {p["image_note"]}', ''])
    lines.extend([f'- [{link["label"]}]({link["url"]})' for link in p['links']])
    lines.append('')
lines.extend(['## Additional project drafts', '', 'These entries use only details documented in the CV. Expand them when team materials are available.', ''])
for p in data['other_projects']:
    lines.extend([f'### {p["title"]}', '', f'**Subtitle:** {p["subtitle"]}', '', f'**Status:** {p["status"]}', '', p['abstract'], '', f'[Project]({p["url"]})', ''])
lines.extend(['## Work in progress', '', '**When Unlearning Hurts: Adversarial Forgetting in Graph Neural Networks** — Investigating whether adversarial manipulation of machine-unlearning procedures can cause persistent degradation across sequential graph-learning tasks. Ongoing research; no results or public paper are claimed.', '', '**Adversarial Attacks on Video-Editing Models** — Investigating adversarial vulnerabilities in video-editing models with Thanh Le. Ongoing research; the supplied CV does not provide methods or results.', '', '## Asset provenance and editorial notes', '', '- URAG: original Figure 2 from arXiv:2603.19281v1, served with the paper HTML.', '- RAG robustness survey: original Figure 1 from arXiv:2608.24977v2, served with the paper HTML.', '- VialectBench: original Figure 2 from arXiv:2608.10414v1, served with the paper HTML.', '- EVENTA: original embedded Figure 2 extracted from page 3 of the 23Trinitrotoluen team manuscript linked by the official EVENTA 2025 challenge page. The public manuscript is anonymized. Association with this project and the award are supported by the CV; formal author names are not inferred.', '- Figures are reproduced as source assets, without AI generation or content alteration. The original authors retain their rights; source links accompany the website figures.', '- Portrait: the public SEAS staff profile, https://seas-cvn.com/staff/tran-ta-quang-minh-2026. No synthetic portrait is used.', '- Both SEAS entries describe mentored student work. No original project figure is present in either repository. These entries use text rather than an unrelated illustration or a diagram from the FishNet dataset paper.', '- Flood forecasts are described as a prototype, without claims of operational warning capability or measured accuracy. Real-time fish recognition and edge deployment remain project objectives unless project measurements are supplied.', '- Design references supplied in web.md: al-folio, Jon Barron, and academic-homepage. This is an original static implementation inspired by their academic structure, with no template code copied.', ''])
(ROOT / 'content').mkdir(exist_ok=True)
(ROOT / 'content/projects.md').write_text('\n'.join(lines), encoding='utf-8')
print(f'Rendered Home, Publications, Blog, Projects, and content/projects.md: {len(data["projects"])} full projects, {len(data["other_projects"])} additional drafts.')

