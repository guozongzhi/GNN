"""Verify archived source bytes without network access or changing the manifests."""
import argparse
import hashlib
import json
from pathlib import Path


def verify(root):
    root = Path(root).resolve()
    count, unavailable = 0, 0
    for manifest in ('manifest.json', 'web-manifest.json'):
        for row in json.loads((root / 'source' / manifest).read_text()):
            if row['status'] != 'downloaded':
                unavailable += 1
                continue
            path = root / row['file'] if manifest == 'manifest.json' else root / 'source' / row['file']
            if not path.resolve().is_relative_to(root):
                raise ValueError(f"Source path escapes repository: {row['id']}")
            data = path.read_bytes()
            if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
                raise ValueError(f"Source checksum mismatch: {row['id']}")
            count += 1
    return count, unavailable


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    verified, unavailable = verify(args.root)
    print(f'{verified} original files verified; {unavailable} explicitly unavailable records')
