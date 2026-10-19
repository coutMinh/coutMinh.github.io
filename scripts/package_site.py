"""Package the current GitHub Pages files and editable sources, excluding QA/cache data."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import shutil

ROOT = Path(__file__).resolve().parents[1]
FILES = ['index.html', 'publications.html', 'blog.html', 'projects.html',
         'CV_VinCAIR.pdf', 'README.md', '.nojekyll', '.gitignore']
DIRECTORIES = ['assets', 'content', 'data', 'templates', 'scripts']


def package():
    files = [ROOT / name for name in FILES]
    for name in DIRECTORIES:
        files.extend(p for p in (ROOT / name).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts
                     and p.suffix != '.pyc')
    target = ROOT / 'portfolio-upload.zip'
    target.parent.mkdir(exist_ok=True)
    with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
        for path in sorted(files):
            archive.write(path, path.relative_to(ROOT).as_posix())
    upload_directory = ROOT / 'UPLOAD-TO-GITHUB'
    if not upload_directory.resolve().is_relative_to(ROOT):
        raise SystemExit('Upload destination must stay within the workspace')
    for path in files:
        destination = upload_directory / path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    print(f'Packaged {len(files)} files: {target.relative_to(ROOT).as_posix()}')
    print(f'Refreshed upload folder: {upload_directory.relative_to(ROOT).as_posix()}')


if __name__ == '__main__':
    package()
