#!/usr/bin/env python3
"""Census every local file, retaining exact provenance and separate reading coverage.

Does not change source files or assign reading levels. Document extraction and media
duration are technical information, never proof that the contents were read.
"""
import argparse
import collections
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / '_notes/10-biblioteca'
CACHE = ROOT / '_notes/99-cache/corpus-docx'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def load(path, default):
    return json.loads(path.read_text(encoding='utf-8-sig')) if path.is_file() else default

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def norm(path):
    return os.path.normcase(os.path.normpath(str(path)))

def docx(path, checksum):
    folder = CACHE / checksum
    folder.mkdir(parents=True, exist_ok=True)
    manifest_path = folder / 'manifest.json'
    if manifest_path.is_file():
        return load(manifest_path, {})
    parts, references, blocks = [], [], []
    with ZipFile(path) as archive:
        names = archive.namelist()
        component_names = sorted(n for n in names if n == 'word/document.xml' or n.startswith(('word/footnotes', 'word/endnotes', 'word/header', 'word/footer', 'word/comments')) and n.endswith('.xml'))
        for component in component_names:
            tree = ET.fromstring(archive.read(component))
            paragraphs = [''.join(t.text or '' for t in node.findall('.//w:t', NS)) for node in tree.findall('.//w:p', NS)]
            rows = [{'component': component, 'paragraph': i + 1, 'text': value} for i, value in enumerate(paragraphs)]
            native_path = folder / (Path(component).stem + '.json')
            native_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            bucket, size, chunk = [], 0, 0
            for row in rows:
                line = f"[{row['paragraph']}] {row['text']}\n"
                if bucket and size + len(line) > 16000:
                    chunk += 1
                    target = folder / f'{Path(component).stem}-{chunk:04d}.txt'
                    target.write_text(''.join(bucket), encoding='utf-8')
                    blocks.append({'file': target.relative_to(ROOT).as_posix(), 'component': component, 'first_paragraph': first, 'last_paragraph': row['paragraph'] - 1})
                    bucket, size = [], 0
                if not bucket:
                    first = row['paragraph']
                bucket.append(line)
                size += len(line)
            if bucket:
                chunk += 1
                target = folder / f'{Path(component).stem}-{chunk:04d}.txt'
                target.write_text(''.join(bucket), encoding='utf-8')
                blocks.append({'file': target.relative_to(ROOT).as_posix(), 'component': component, 'first_paragraph': first, 'last_paragraph': rows[-1]['paragraph']})
            parts.append({'component': component, 'paragraphs': len(rows), 'characters': sum(len(x) for x in paragraphs), 'native_json': native_path.relative_to(ROOT).as_posix()})
        for name in names:
            if name.startswith('word/') and name.endswith('.rels'):
                for node in ET.fromstring(archive.read(name)):
                    if node.get('TargetMode') == 'External':
                        references.append({'component': name, 'id': node.get('Id'), 'url': node.get('Target')})
        result = {'source': str(path), 'source_sha256': checksum, 'components': parts, 'chunks': blocks,
                  'external_relationships': references, 'embedded_media': [n for n in names if n.startswith('word/media/')],
                  'equations': sum(archive.read(n).count(b'<m:oMath') for n in component_names),
                  'read_by_agent': False, 'limitations': 'Native text excludes semantic interpretation of images, equations, layout and external linked content.'}
    manifest_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--name', required=True, help='Private output filename stem')
    args = parser.parse_args()
    if Path(args.name).name != args.name:
        parser.error('name must be a filename stem')
    root = args.root.resolve()
    if not root.is_dir():
        parser.error('Source directory does not exist')
    registry = load(ROOT / '_notes/book-bib-registry.json', {})
    ledger = load(LIBRARY / 'letture.json', {'records': {}})['records']
    extraction = load(LIBRARY / 'estrazione.json', {})
    by_path = collections.defaultdict(list)
    by_sha = collections.defaultdict(list)
    for record_id, record in registry.items():
        for field in ['source_path', 'source_path_duplicate']:
            if record.get(field):
                by_path[norm(record[field])].append(record_id)
        if len(record_id) == 64:
            by_sha[record_id].append(record_id)
    rows, groups = [], collections.defaultdict(list)
    ffprobe = shutil.which('ffprobe')
    for path in sorted((p for p in root.rglob('*') if p.is_file()), key=lambda p: str(p).casefold()):
        checksum = sha(path)
        ids = sorted(set(by_path[norm(path)] + by_sha[checksum]))
        suffix = path.suffix.lower()
        row = {'relative_path': path.relative_to(root).as_posix(), 'source_path': str(path),
               'bytes': path.stat().st_size, 'mtime_ns': path.stat().st_mtime_ns,
               'sha256': checksum, 'extension': suffix, 'record_ids': ids,
               'citekeys': sorted(set(registry[i].get('citekey') for i in ids if registry[i].get('citekey'))),
               'record_readings': [{'record_id': i, 'legacy': ledger.get(i, {}).get('attestazione_pregressa'),
                                    'level': ledger.get(i, {}).get('livello_attuale'),
                                    'integral_closed': ledger.get(i, {}).get('lettura_integrale_chiusa', False),
                                    'digest': ledger.get(i, {}).get('digest')} for i in ids],
               'queue_status': 'da-riconciliare-e-completare' if ids else 'da-identificare-e-leggere',
               'coverage_this_audit': 'Technical census only; no reading level assigned', 'technical': {}}
        if suffix == '.pdf':
            tech = next((x for x in extraction.values() if x.get('source_sha256') == checksum), None)
            if tech:
                row['technical'] = {'page_count': tech.get('page_count'), 'pages_low_native': tech.get('pages_needing_images_or_ocr'), 'existing_manifest': tech.get('manifest_path')}
            else:
                try:
                    import fitz
                    with fitz.open(path) as document:
                        row['technical'] = {'page_count': len(document), 'method': 'PDF structure only'}
                except Exception as error:
                    row['technical'] = {'error': str(error)}
                    row['queue_status'] = 'esemplare-non-apribile-da-recuperare'
        elif suffix == '.docx':
            info = docx(path, checksum)
            row['technical'] = {'manifest': (CACHE / checksum / 'manifest.json').relative_to(ROOT).as_posix(),
                                'characters': sum(p['characters'] for p in info['components']),
                                'paragraphs': sum(p['paragraphs'] for p in info['components']),
                                'chunks': len(info['chunks']), 'embedded_media': len(info['embedded_media']), 'external_links': len(info['external_relationships'])}
        elif suffix == '.txt':
            raw = path.read_bytes()
            try:
                text = raw.decode('utf-8-sig')
            except UnicodeDecodeError:
                text = raw.decode('cp1252')
            import re
            row['technical'] = {'characters': len(text), 'empty': not text.strip(), 'urls': re.findall(r'https?://[^\s<>]+', text)}
            if not text.strip():
                row['queue_status'] = 'segnaposto-vuoto-conservato'
        elif suffix in {'.mp3', '.m4v', '.mp4', '.wav'}:
            if ffprobe:
                run = subprocess.run([ffprobe, '-v', 'error', '-show_entries', 'format=duration:stream=codec_type', '-of', 'json', str(path)], capture_output=True, text=True, timeout=30, encoding='utf-8')
                row['technical'] = json.loads(run.stdout) if run.returncode == 0 else {'error': run.stderr}
            else:
                row['technical'] = {'error': 'ffprobe unavailable'}
            row['queue_status'] = 'da-ascoltare-o-trascrivere-e-collegare-agli-esempi'
        elif suffix == '.lnk':
            row['queue_status'] = 'collegamento-da-risolvere-senza-eseguirlo'
        groups[checksum].append(row['relative_path'])
        rows.append(row)
    stats = {'files': len(rows), 'extensions': dict(sorted(collections.Counter(x['extension'] for x in rows).items())),
             'distinct_sha256': len(groups), 'exact_duplicate_groups': sum(len(g) > 1 for g in groups.values()),
             'files_with_registry_match': sum(bool(x['record_ids']) for x in rows),
             'pdf_pages_openable_copies': sum(x['technical'].get('page_count') or 0 for x in rows if x['extension'] == '.pdf'),
             'pdf_errors': sum(bool(x['technical'].get('error')) for x in rows if x['extension'] == '.pdf'),
             'media_minutes': round(sum(float(x['technical'].get('format', {}).get('duration', 0)) for x in rows) / 60, 2),
             'empty_notes': sum(x['technical'].get('empty', False) for x in rows),
             'readings_closed_by_this_audit': 0}
    result = {'observed_utc': datetime.now(timezone.utc).isoformat(), 'root': str(root), 'scope': 'All files recursively; exact byte identity groups only.',
              'stats': stats, 'duplicates': {k: v for k, v in groups.items() if len(v) > 1}, 'files': rows}
    LIBRARY.mkdir(parents=True, exist_ok=True)
    output = LIBRARY / (args.name + '.json')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (LIBRARY / (args.name + '.csv')).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['path', 'type', 'citekeys', 'status', 'pages', 'duration_seconds', 'sha256'])
        for row in rows:
            writer.writerow([row['relative_path'], row['extension'], ';'.join(row['citekeys']), row['queue_status'], row['technical'].get('page_count', ''), row['technical'].get('format', {}).get('duration', ''), row['sha256']])
    print(json.dumps(stats, ensure_ascii=False))
    print(output)

if __name__ == '__main__':
    main()
