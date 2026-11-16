"""Render case-study summaries from one editable file. --check detects drift."""
from pathlib import Path
from html import escape
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
records = json.loads((ROOT / 'content/projects.json').read_text())
seen = set()
changed = []
for item in records:
    slug = item['slug']
    if not re.fullmatch(r'[a-z0-9-]+', slug) or slug in seen:
        raise SystemExit(f'Invalid or duplicate project slug: {slug}')
    seen.add(slug)
    path = ROOT / 'projects' / slug / 'index.html'
    text = path.read_text()
    fields = [('THE DECISION', 'decision'), ('BUSINESS TAKEAWAY', 'takeaway'), ('NEXT BUSINESS STEP', 'next_step')]
    block = '<section class="project-brief" aria-label="Project at a glance">'
    for label, key in fields:
        block += f'<div><span>{label}</span><p>{escape(item[key])}</p></div>'
    block += f'<a href="/evidence/#{slug}">Sources &amp; validation →</a></section>'
    updated, count = re.subn(r'<section class="project-brief".*?</section>', lambda _: block, text, flags=re.S)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one summary block')
    if updated != text:
        changed.append(str(path.relative_to(ROOT)))
        if '--check' not in sys.argv:
            path.write_text(updated)
if seen != {p.parent.name for p in (ROOT / 'projects').glob('*/index.html')}:
    raise SystemExit('Project content does not match case-study folders')
if changed and '--check' in sys.argv:
    raise SystemExit('Run python scripts/sync_projects.py to update: ' + ', '.join(changed))
print(f'{len(records)} project summaries checked; {len(changed)} updated.')
