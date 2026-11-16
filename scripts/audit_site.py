"""Dependency-free structural, accessibility and asset-budget checks for the site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,subprocess,tempfile,sys,re
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=[];self.links=[];self.images=[];self.headings=[];self.lang=None;self.viewport=False;self.title=False;self.scripts=[];self.in_script=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='html':self.lang=a.get('lang')
  if tag=='title':self.title=True
  if tag=='meta' and a.get('name')=='viewport':self.viewport=True
  if tag=='img':self.images.append(a)
  if a.get('srcset'):
   self.links.extend(part.strip().split()[0] for part in a['srcset'].split(',') if part.strip())
  if tag in ['h1','h2','h3']:self.headings.append(tag)
  for key in ['src','href']:
   if a.get(key):self.links.append(a[key])
  if tag=='script':self.in_script=not a.get('src')
 def handle_endtag(self,tag):
  if tag=='script':self.in_script=False
 def handle_data(self,s):
  if self.in_script:self.scripts.append(s)
def ratio(a,b):
 def lum(h):
  rgb=[int(h[i:i+2],16)/255 for i in [0,2,4]]
  return sum((x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4)*w for x,w in zip(rgb,[.2126,.7152,.0722]))
 x,y=sorted([lum(a),lum(b)]);return (y+.05)/(x+.05)
paths=sorted(ROOT.rglob('*.html'))
parsed={};errors=[];report={'pages':[],'contrast':{},'asset_bytes':{}}
for p in paths:
 q=Page();q.feed(p.read_text());parsed[p]=q
 if not q.lang or not q.viewport or not q.title:errors.append(f'{p}: missing document metadata')
 if q.headings.count('h1')!=1:errors.append(f'{p}: expected one h1')
 if len(q.ids)!=len(set(q.ids)):errors.append(f'{p}: duplicate IDs')
 for img in q.images:
  if not img.get('alt'):errors.append(f'{p}: image without descriptive alt: {img.get("src")}')
 for script in q.scripts:
  with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as f:
   f.write(script);f.flush();result=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
   if result.returncode:errors.append(f'{p}: inline JavaScript syntax error: {result.stderr}')
 report['pages'].append({'path':p.relative_to(ROOT).as_posix(),'h1':q.headings.count('h1'),'images':len(q.images),'unique_ids':len(set(q.ids))})
for p,q in parsed.items():
 for link in q.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(ROOT/unquote(u.path).lstrip('/')) if u.path.startswith('/') else p.parent/unquote(u.path)
  if not u.path:target=p
  if target.is_dir():target=target/'index.html'
  target=target.resolve()
  if not target.exists():errors.append(f'{p.relative_to(ROOT)}: missing {link}');continue
  if u.fragment and target in parsed and u.fragment not in parsed[target].ids:errors.append(f'{p.relative_to(ROOT)}: missing fragment {link}')
# Resolve assets referenced by CSS and by the JavaScript preview galleries.
for asset in (ROOT/'assets').glob('*'):
 if asset.suffix not in ('.css','.js'):continue
 text=asset.read_text()
 if asset.suffix=='.js':
  result=subprocess.run(['node','--check',str(asset)],capture_output=True,text=True)
  if result.returncode:errors.append(f'{asset.name}: JavaScript syntax error: {result.stderr}')
 refs=re.findall(r"[\"'](?:/assets/)?([a-zA-Z0-9_-]+\.(?:png|jpg|jpeg|webp|svg))[\"']",text)
 for ref in refs:
  if not (ROOT/'assets'/ref).is_file():errors.append(f'{asset.name}: missing dynamic asset {ref}')
 if asset.suffix=='.css':
  for ref in re.findall(r'url\([\"\']?([^\)\"\']+)',text):
   if ref.startswith(('data:','http:','https:','#')):continue
   target=ROOT/ref.lstrip('/') if ref.startswith('/') else asset.parent/ref
   if not target.is_file():errors.append(f'{asset.name}: missing CSS asset {ref}')
for label,fg,bg in [('light body','202b26','f6f5f0'),('light muted','59635c','fffefa'),('light link','286549','fffefa'),('dark body','edf4ec','0c1714'),('dark muted','b4c3b9','15251f'),('dark link','a8ddbb','15251f')]:
 value=ratio(fg,bg);report['contrast'][label]=round(value,2)
 if value<4.5:errors.append(f'{label}: contrast {value:.2f} below 4.5')
for file in ['assets/experience.js','assets/experience.css','assets/site.css','assets/sales-dashboard-hero.webp']:
 p=ROOT/file;report['asset_bytes'][file]=p.stat().st_size
 if p.stat().st_size>180000:errors.append(f'{file}: exceeds 180KB single-file budget')
for p in (ROOT/'assets').glob('*-small.webp'):
 if p.stat().st_size>80000:errors.append(f'{p.name}: mobile cover exceeds 80KB budget')
report['checked_dynamic_assets']=True
report['checked_srcset']=True
report['limits']='Structural checks and selected color pairs only; not a complete WCAG conformance or Lighthouse performance score. Browser interaction and layout checks are recorded separately.'
report['errors']=errors;report['status']='passed' if not errors else 'failed'
print(json.dumps(report,indent=2));sys.exit(bool(errors))
