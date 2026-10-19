# Tran Ta Quang Minh — academic website

A static academic website with four separate pages:

- **Home** (`index.html`): a white introduction panel with biography, supervisors, portrait, and profile links; a separate white panel for Education, Teaching & Mentorship, and all 11 Honors & Awards; and a selected-publications panel. Teaching entries expand to reveal their full descriptions.
- **Publications** (`publications.html`): three papers with author lists, publication/review labels, and abstracts. Original paper figures remain expandable; captions below thumbnails and the ongoing-research/status-note sections have been removed.
- **Blog** (`blog.html`): a dedicated writing page, currently showing an honest empty state because no posts have been supplied.
- **Projects** (`projects.html`): five equally sized cards for EVENTA, AI Assistant Glasses, AquaSafe, and the two mentored SEAS projects. All cards use coordinated conceptual covers, with no category filters. The grid has three columns on desktop, two on tablet, and one on phones.

The design takes structural inspiration from [Gia Huy Thai's academic homepage](https://oxyzgiahuy.github.io/). Its biography, claims, and project content are specific to Minh. Existing original-paper thumbnails are preserved. The shared footer has been removed from every page.

No installation, framework, backend, or build is required to view or host the generated HTML. Open `index.html` in a browser, or preview over HTTP:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Visit `http://127.0.0.1:8000`. All page and asset paths are relative and support both user sites and repository subpaths on GitHub Pages.

## Edit content

- `data/profile.json`: exact CV profile links, education, teaching, organization links and logo provenance, honors/certificate links, and ongoing research.
- `data/portfolio.json`: publications, author lists, project descriptions, roles, links, and image provenance.
- `templates/home.html`: the biography and Home layout. Update supervisor/project prose here.
- `templates/publications.html`, `templates/projects.html`, `templates/blog.html`: each page's layout and introductory copy. Add actual blog content in the Blog template when ready.
- `templates/base.html`: shared navigation, metadata, and image dialog.
- `assets/style.css`: responsive layout and light/dark themes.
- `assets/site.js`: optional theme controls and enlarged publication figures.
- `assets/images/project-covers/`: five generated conceptual project-cover images.
- `content/project-cover-prompts.md`: the exact prompts used with the built-in Imagegen tool.

After changing data or templates, regenerate the four HTML pages and the project copy document:

```powershell
python scripts/build.py
python scripts/check_site.py
```

Both scripts use only the Python standard library. `scripts/render_pages.py` supplies the page renderer used by the build script. Commit the generated HTML alongside the source files; GitHub does not need to run Python.

## GitHub Pages

For a personal site, create a public repository named `<username>.github.io`. Place the generated HTML files, `assets/`, `CV_VinCAIR.pdf`, `content/`, and `.nojekyll` at the repository root. Keeping `data/`, `templates/`, and `scripts/` in the repository lets you edit and rebuild later.

In **Settings → Pages**, select **Deploy from a branch → main → / (root)**. `.nojekyll` disables Jekyll processing. Do not upload `.qa/`, `.research/`, or Python caches. `.gitignore` excludes these when using Git; browser uploads must exclude them manually.

To refresh the upload archive after rebuilding:

```powershell
python scripts/package_site.py
```

This refreshes `portfolio-upload.zip` and copies the current site and editable sources into `UPLOAD-TO-GITHUB/`. Upload the contents of that folder, including the complete `assets/` folder and other subfolders. Drag the folders onto GitHub's upload area to preserve their hierarchy. `index.html` must be at the repository root, and `assets/style.css` must stay inside `assets/`; uploading only the top-level files leaves the site unstyled. Do not upload the ZIP itself as the website. Packaging does not publish or push anything.

## Content and sources

Profile links, supervisors, academic results, awards, certificate links, and publication/review labels follow `CV_VinCAIR.pdf`, dated September 2026. The high-school entry follows the owner's additional information: Lương Văn Chánh High School for the Gifted, Tuy Hòa, specialized in Physics. No high-school dates or HUST camp date were supplied, so none are invented.

Home lists all nine recognitions in the CV's Projects & Awards section, plus Excellent Student recognition from Education and the excellent-mentorship recognition from Teaching & Mentorship. The two top-3% academic years are separate entries; HUST selection and the presentation award share one entry.

URAG, Retrieved But Not Reliable, and VialectBench retain the existing original publication figures. Figure source links and credits remain in the enlarged-image dialog, and `content/projects.md` records their provenance. The original EVENTA figure is preserved in the source assets and copy document; its Projects cover now uses conceptual artwork. The public EVENTA manuscript is anonymized, so the site does not infer a formal author list. Mentored work is explicitly attributed as mentoring.

The five Projects covers were generated with the built-in Imagegen tool at the owner's request. They are conceptual illustrations, not screenshots, original paper figures, deployed systems, or measured results. Prompts and saved asset paths are recorded in `content/project-cover-prompts.md`. Lifelog Retrieval App and Real-time Monitoring Surveillance System have been removed from Projects; the related CV award entries remain on Home.

The original portrait comes from the public SEAS staff profile. The optional `scripts/fetch_sources.py` caches source materials into the ignored `.research/` directory; the website itself does not fetch external papers or third-party images.

Organization icons are stored locally in `assets/images/organizations/`. Lương Văn Chánh High School and Science Lab use the avatars supplied by the Open Graph metadata of their linked Facebook pages. SEAS uses its official website logo. The University of Science crest matches the supplied university artwork and was downloaded from the reference homepage's institution badge. Each asset's source is recorded in `data/profile.json`; the icons link to the relevant school or organization. Facebook avatars are a downloaded snapshot, so displaying the site does not require Facebook requests or expiring CDN URLs.

## Validation

`scripts/check_site.py` checks all four pages, local resources with case-sensitive filenames, cross-page anchors, active navigation, project coverage, honors, and figure provenance.

Browser checks covered all four pages at 1440, 768, 390, and 320 pixels; root and repository-subpath hosting; exact CV profile links; white Home panels; removal of captions, footer, and publication notes; five equal project cards/covers in a responsive 3/2/1-column grid; native abstract expansion; image dialogs and Escape/focus restoration; theme persistence across pages; reduced motion; and reading without JavaScript. No horizontal overflow or browser errors were observed. Screenshots and local browser-check tooling live in the ignored `.qa/` directory.
