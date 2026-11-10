"""Download unchanged originals; record hashes and failures, never pass HTML as PDF."""
import concurrent.futures
import datetime
import hashlib
import io
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def download(row):
    from pypdf import PdfReader
    item = dict(row)
    path = ROOT / 'source' / 'papers' / (row['id'] + '.pdf')
    item['retrieved_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if not row['pdf_url']:
        item.update(status='unavailable', reason='Publisher/institutional record found; no open original PDF obtained.')
        return item
    try:
        request = urllib.request.Request(row['pdf_url'], headers={'User-Agent': 'GNN-study-materials/1.0'})
        if path.exists():
            data = path.read_bytes()
            item['retrieved_at'] = datetime.datetime.fromtimestamp(path.stat().st_mtime, datetime.timezone.utc).isoformat()
            item['cache_reused'] = True
        else:
            with urllib.request.urlopen(request, timeout=50) as response:
                data = response.read()
                item['resolved_url'] = response.url
        if not data.startswith(b'%PDF-'):
            raise ValueError('Response is not a PDF')
        reader = PdfReader(io.BytesIO(data))
        first = reader.pages[0].extract_text() or ''
        if len(first.strip()) < 40:
            raise ValueError('First page text too short for identity verification')
        item.update(status='downloaded', file=str(path.relative_to(ROOT)), bytes=len(data),
                    sha256=hashlib.sha256(data).hexdigest(), pages=len(reader.pages),
                    pdf_title=str((reader.metadata or {}).get('/Title', '')),
                    first_page_excerpt=re.sub(r'\s+', ' ', first)[:1000])
        version = re.search(r'\d{4}\.\d{4,5}v\d+', first)
        item['pdf_version_marker'] = version.group(0) if version else None
        if not path.exists():
            path.write_bytes(data)
        return item
    except Exception as exc:
        item.update(status='failed', reason=str(exc))
        return item


def main():
    rows = json.loads((ROOT / 'source/catalog.json').read_text())
    (ROOT / 'source/papers').mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(download, rows))
    (ROOT / 'source/manifest.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    for row in results:
        print(row['id'], row['status'], row.get('pages', ''), row.get('reason', ''))
    if any(row['status'] == 'failed' for row in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
