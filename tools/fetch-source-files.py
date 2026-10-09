"""Acquire an accessible source with URL, date and file hash in a private manifest.

This command downloads one document. It does not bypass access controls and
does not change the reading level or the bibliographic metadata.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / '_notes'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if not args.url.startswith(('https://', 'http://')):
        raise ValueError('Only HTTP(S) source URLs are supported')
    args.out = (ROOT / args.out).resolve()
    if not args.out.is_relative_to(PRIVATE.resolve()):
        raise ValueError('Source files and provenance must stay in the private _notes directory')
    if args.out.exists() or args.out.with_suffix(args.out.suffix + '.source.json').exists():
        raise FileExistsError(f'Preserve existing source: {args.out}')
    request = urllib.request.Request(args.url, headers={'User-Agent': 'harmony-book-source-research/1.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
        metadata = {
            'requested_url': args.url, 'resolved_url': response.url,
            'retrieved_utc': datetime.now(timezone.utc).isoformat(),
            'content_type': response.headers.get('Content-Type'),
            'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'read_by_agent': False,
        }
    if args.out.suffix.lower() == '.pdf' and not data.lstrip().startswith(b'%PDF-'):
        raise ValueError('Response is not a PDF; source not written')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(data)
    args.out.with_suffix(args.out.suffix + '.source.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(metadata, ensure_ascii=False))


if __name__ == '__main__':
    main()
