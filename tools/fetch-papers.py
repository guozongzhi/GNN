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


def download(row, previous=None):
    from pypdf import PdfReader
    item = dict(row)
    previous = previous or {}
    path = ROOT / 'source' / 'papers' / (row['id'] + '.pdf')
    item['retrieved_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if not row['pdf_url']:
        item.update(status='unavailable', reason='Publisher/institutional record found; no open original PDF obtained.')
        return item
    try:
        request = urllib.request.Request(row['pdf_url'], headers={'User-Agent': 'GNN-study-materials/1.0'})
        if path.exists():
            data = path.read_bytes()
            item['retrieved_at'] = previous.get('retrieved_at')
            if previous.get('resolved_url'):
                item['resolved_url'] = previous['resolved_url']
            item['cache_reused'] = True
        else:
            with urllib.request.urlopen(request, timeout=50) as response:
                data = response.read()
                item['resolved_url'] = response.url
        digest = hashlib.sha256(data).hexdigest()
        if previous.get('sha256') and digest != previous['sha256']:
            raise ValueError('SHA-256 mismatch with recorded original; file and manifest are not replaced')
        if not data.startswith(b'%PDF-'):
            raise ValueError('Response is not a PDF')
        reader = PdfReader(io.BytesIO(data))
        first = reader.pages[0].extract_text() or ''
        if len(first.strip()) < 40:
            raise ValueError('First page text too short for identity verification')
        item.update(status='downloaded', file=str(path.relative_to(ROOT)), bytes=len(data),
                    sha256=digest, pages=len(reader.pages),
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
    manifest = ROOT / 'source/manifest.json'
    previous = {r['id']: r for r in json.loads(manifest.read_text())} if manifest.exists() else {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda row: download(row, previous.get(row['id'])), rows))
    if any(row['status'] == 'failed' for row in results):
        destination = ROOT / 'tmp/download-report.json'
        destination.parent.mkdir(exist_ok=True)
    else:
        destination = manifest
    destination.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    for row in results:
        print(row['id'], row['status'], row.get('pages', ''), row.get('reason', ''))
    if any(row['status'] == 'failed' for row in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
