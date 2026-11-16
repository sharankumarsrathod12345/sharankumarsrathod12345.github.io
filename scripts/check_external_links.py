"""Check external links; 404/410 fail, blocked/rate-limited sites need manual review."""
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
import json, sys

ROOT = Path(__file__).resolve().parents[1]
links = set()
class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key not in ('href', 'src') or not value:
                continue
            parsed = urlsplit(value)
            if parsed.scheme == 'https' and parsed.hostname != 'sharankumarsrathod12345.github.io':
                links.add(urlunsplit(parsed._replace(fragment='')))
for path in ROOT.rglob('*.html'):
    Links().feed(path.read_text())
def check(url):
    try:
        request = Request(url, headers={'User-Agent': 'PortfolioLinkCheck/1.0'}, method='HEAD')
        try:
            with urlopen(request, timeout=15) as response:
                status = response.status
        except HTTPError as error:
            if error.code != 405:
                raise
            with urlopen(Request(url, headers={'User-Agent': 'PortfolioLinkCheck/1.0'}), timeout=15) as response:
                status = response.status
        return {'url': url, 'status': status, 'result': 'reachable'}
    except HTTPError as error:
        return {'url': url, 'status': error.code, 'result': 'broken' if error.code in (404, 410) else 'manual_review'}
    except (URLError, TimeoutError, OSError) as error:
        return {'url': url, 'result': 'manual_review', 'reason': str(error)}
with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(check, sorted(links)))
print(json.dumps({'links': results, 'note': 'Reachability does not validate destination content. Blocked requests are not treated as proof of a broken link.'}, indent=2))
sys.exit(any(item['result'] == 'broken' for item in results))
