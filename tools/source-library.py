"""Inventory and extract the registered corpus without claiming to have read it.

Generated data and texts are private. Existing authored reading records are kept.
Run from the project root:
    python tools/source-library.py audit
    python tools/source-library.py extract
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / '_notes/book-bib-registry.json'
BIB = ROOT / 'manuscript/bib/references.bib'
LIBRARY = ROOT / '_notes/10-biblioteca'
CACHE = ROOT / '_notes/99-cache/doc-ingest/source-library'


def json_read(path, fallback):
    return json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else fallback


def json_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def bib_entries(text):
    """Read balanced, brace-delimited entries; preserve each original body."""
    entries = {}
    for match in re.finditer(r'(?m)^\s*@([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,', text):
        start = match.start()
        opening = text.index('{', match.start())
        depth, quoted, escaped, end = 1, False, False, opening + 1
        while end < len(text) and depth:
            char = text[end]
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"' and depth == 1:
                quoted = not quoted
            elif not quoted and char == '{':
                depth += 1
            elif not quoted and char == '}':
                depth -= 1
            end += 1
        if depth:
            raise ValueError(f'Unclosed BibLaTeX entry: {match.group(2)}')
        key = match.group(2)
        if key in entries:
            raise ValueError(f'Duplicate BibLaTeX key: {key}')
        entries[key] = text[start:end].strip()
    return entries


def bib_title(entry):
    match = re.search(r'\btitle\s*=\s*\{(.*?)\}\s*[,\n]', entry, re.S | re.I)
    return ' '.join(match.group(1).split()) if match else None


def legacy_level(record):
    field = record.get('bib_verified_by') or ''
    explicit = re.search(r'(?:livello\s*|\bL)([1-4])\b', field, re.I)
    # Retain only explicit labels; do not infer reading from bibliographic status.
    return f'L{explicit.group(1)}' if explicit else None


def links_from_notes(record):
    return list(dict.fromkeys(re.findall(r'https?://[^\s<>]+', record.get('notes') or '')))


def audit():
    registry = json_read(REGISTRY, {})
    entries = bib_entries(BIB.read_text(encoding='utf-8'))
    ledger_path = LIBRARY / 'letture.json'
    ledger = json_read(ledger_path, {'schema': 1, 'records': {}})
    extraction = json_read(LIBRARY / 'estrazione.json', {})
    groups = defaultdict(list)
    rows = []
    for record_id, record in registry.items():
        key = record.get('citekey')
        groups[key or f'senza-chiave:{record_id}'].append(record_id)
        original_source = Path(record['source_path']) if record.get('source_path') else None
        title = record.get('title') or bib_title(entries.get(key, '')) or (original_source.stem if original_source else key or record_id)
        if record_id not in ledger['records']:
            ledger['records'][record_id] = {
                'citekey': key,
                'stato': 'da-leggere-o-riconciliare',
                'livello_pregresso_esplicito': legacy_level(record),
                'attestazione_pregressa': record.get('bib_verified_by'),
                'lettura_integrale_chiusa': False,
                'pagine_testo_lette': [],
                'pagine_immagini_lette': [],
                'digest': None,
                'note': 'Il censimento non annulla le letture pregresse; la loro copertura va riconciliata con le schede esistenti.',
            }
        reading = ledger['records'][record_id]
        source = original_source
        if not (source and source.is_file()) and reading.get('local_copy_path'):
            source = ROOT / reading['local_copy_path']
        row = {
            'record_id': record_id, 'citekey': key, 'title': title,
            'corpus': record.get('corpus'), 'bib_status': record.get('bib_status'),
            'in_bib': bool(key and key in entries),
            'flag_bib_written': record.get('bib_entry_written'),
            'source_path': str(source) if source else None,
            'original_source_path': str(original_source) if original_source else None,
            'local_copy_path': reading.get('local_copy_path'),
            'local_exists': source.is_file() if source else False,
            'url_candidates': links_from_notes(record),
            'legacy_level': reading.get('livello_pregresso_esplicito'),
            'legacy_attestation': reading.get('attestazione_pregressa'),
            'registry_content_level': legacy_level(record),
            'reading_state': reading['stato'],
            'integral_reading_closed': reading['lettura_integrale_chiusa'],
            'digest': reading.get('digest'),
            'extraction': extraction.get(record_id),
        }
        rows.append(row)
    stats = {
        'records': len(rows), 'citekeys': len({row['citekey'] for row in rows if row['citekey']}),
        'without_citekey': sum(not row['citekey'] for row in rows),
        'operational_groups': len(groups), 'bib_entries': len(entries),
        'metadata_status': dict(Counter(row['bib_status'] for row in rows)),
        'local_files': sum(row['local_exists'] for row in rows),
        'original_local_paths': sum(bool(row['original_source_path']) for row in rows),
        'no_local_file': sum(not row['local_exists'] for row in rows),
        'integral_readings_closed_in_new_ledger': sum(row['integral_reading_closed'] for row in rows),
        'explicit_legacy_content_levels': dict(Counter(row['legacy_level'] or 'non-esplicito' for row in rows)),
        'explicit_registry_content_levels': dict(Counter(row['registry_content_level'] or 'non-esplicito' for row in rows)),
        'verified_missing_bib': len({row['citekey'] for row in rows if row['bib_status'] == 'verificata' and row['citekey'] and not row['in_bib']}),
        'flag_mismatches': sum(bool(row['flag_bib_written']) != row['in_bib'] for row in rows),
        'extracted_pdfs': sum('page_count' in item for item in extraction.values()),
        'extraction_errors': sum('error' in item for item in extraction.values()),
        'extracted_pdf_pages': sum(item.get('page_count', 0) for item in extraction.values()),
        'pages_with_little_native_text': sum(item.get('pages_needing_images_or_ocr', 0) for item in extraction.values()),
        'extracted_native_characters': sum(item.get('native_characters', 0) for item in extraction.values()),
    }
    result = {
        'generated_utc': datetime.now(timezone.utc).isoformat(), 'stats': stats,
        'groups_with_shared_citekey': {k: v for k, v in groups.items() if len(v) > 1},
        'records': rows,
    }
    json_write(ledger_path, ledger)
    json_write(LIBRARY / 'inventario.json', result)
    lines = [
        '# Biblioteca di progetto · censimento e letture', '',
        'Questo indice è generato da `tools/source-library.py audit`. Tutti i record sono conservati, comprese copie, edizioni, voci senza chiave e precedenti scarti. Una citekey comune è un gruppo da riconciliare, non prova di identità degli esemplari.', '',
        f"Registro: {stats['records']} record; {stats['citekeys']} citekey; {stats['without_citekey']} senza chiave; {stats['operational_groups']} gruppi operativi. Bibliografia: {stats['bib_entries']} voci. File locali accessibili: {stats['local_files']}; record senza file locale: {stats['no_local_file']}.", '',
        f"Chiusure integrali registrate nel nuovo protocollo: {stats['integral_readings_closed_in_new_ledger']}. Questo numero non riclassifica come non lette le fonti già lette in passato: quelle attestazioni sono conservate e vanno riconciliate. Estrazione automatica e lettura restano separate.", '',
        f"Acquisizione tecnica: {stats['extracted_pdfs']} PDF estratti, {stats['extraction_errors']} errori; {stats['extracted_pdf_pages']} pagine PDF, {stats['pages_with_little_native_text']} con poco testo nativo, {stats['extracted_native_characters']} caratteri. Le pagine con poco testo richiedono apertura dell'immagine e, se utile, OCR; la soglia automatica non distingue una pagina bianca da una scansione o una partitura.", '',
        'Lo stato autorato vive in `letture.json`, i dati derivati in `inventario.json`, le estrazioni tecniche in `estrazione.json`. I testi estratti sono nella cache privata `_notes/99-cache/doc-ingest/source-library/`; i digest e le informazioni durevoli si scrivono in `10-biblioteca/digest/` o nelle schede private già esistenti.', '',
        '| citekey / record | Fonte | Anagrafica | File locale | Nel .bib | Lettura nel protocollo |',
        '|---|---|---|---|---|---|',
    ]
    for row in sorted(rows, key=lambda value: (value['corpus'] or '', value['citekey'] or '', value['record_id'])):
        cell = lambda text: str(text).replace('|', '\\|').replace('\n', ' ')
        label = row['citekey'] or row['record_id']
        if row['digest']:
            target = str(row['digest']).removeprefix('_notes/').removesuffix('.md')
            label = f'[[{target}|{label}]]'
        lines.append('| ' + ' | '.join(map(cell, [label, row['title'], row['bib_status'], 'sì' if row['local_exists'] else 'no', 'sì' if row['in_bib'] else 'no', row['reading_state']])) + ' |')
    (LIBRARY / 'INDICE.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(stats, ensure_ascii=False))
    return result


def extract(limit=None, retry_errors=False):
    import fitz
    fitz.TOOLS.mupdf_display_errors(False)
    fitz.TOOLS.mupdf_display_warnings(False)
    registry = json_read(REGISTRY, {})
    ledger = json_read(LIBRARY / 'letture.json', {'records': {}})
    manifest_path = LIBRARY / 'estrazione.json'
    manifest = json_read(manifest_path, {})
    total = 0
    failures = 0
    for record_id, record in registry.items():
        source_name = record.get('source_path')
        if not source_name or not (ROOT / source_name).is_file():
            source_name = ledger['records'].get(record_id, {}).get('local_copy_path')
        if not source_name:
            continue
        source = ROOT / source_name
        if not source.is_file() or source.suffix.lower() != '.pdf':
            continue
        stat = source.stat()
        previous = manifest.get(record_id, {})
        if previous.get('error') and not retry_errors and previous.get('source_bytes') == stat.st_size and previous.get('source_mtime_ns') == stat.st_mtime_ns:
            continue
        if previous.get('source_bytes') == stat.st_size and previous.get('source_mtime_ns') == stat.st_mtime_ns and (ROOT / previous.get('manifest_path', '_missing')).is_file():
            continue
        if limit is not None and total >= limit:
            break
        try:
            with source.open('rb') as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            target = CACHE / digest
            target.mkdir(parents=True, exist_ok=True)
            page_manifest = target / 'pages.json'
            if not page_manifest.exists():
                with fitz.open(source) as doc:
                    pages = []
                    for number, page in enumerate(doc, 1):
                        text = page.get_text(sort=True)
                        destination = target / f'pdf-{number:04d}.txt'
                        destination.write_text(text, encoding='utf-8')
                        alphabetic = sum(char.isalpha() for char in text)
                        pages.append({
                            'pdf_page': number, 'native_characters': len(text.strip()),
                            'alphabetic_characters': alphabetic,
                            'text_file': destination.relative_to(ROOT).as_posix(),
                            'needs_image_reading_or_ocr': alphabetic < 80,
                        })
                    json_write(page_manifest, {'sha256': digest, 'page_count': len(pages), 'pages': pages, 'source_metadata': doc.metadata, 'read_by_agent': False})
            pages_data = json_read(page_manifest, {})
            manifest[record_id] = {
                'source_bytes': stat.st_size, 'source_mtime_ns': stat.st_mtime_ns,
                'source_sha256': digest, 'manifest_path': page_manifest.relative_to(ROOT).as_posix(),
                'page_count': pages_data['page_count'],
                'pages_needing_images_or_ocr': sum(p['needs_image_reading_or_ocr'] for p in pages_data['pages']),
                'native_characters': sum(p['native_characters'] for p in pages_data['pages']),
                'read_by_agent': False,
            }
            total += 1
            print(f"extracted {record.get('citekey') or record_id}: {pages_data['page_count']} pages", flush=True)
            json_write(manifest_path, manifest)
        except Exception as error:
            failures += 1
            manifest[record_id] = {'error': str(error), 'source_path': str(source), 'source_bytes': stat.st_size, 'source_mtime_ns': stat.st_mtime_ns, 'read_by_agent': False}
            json_write(manifest_path, manifest)
            print(f"error {record.get('citekey') or record_id}: {error}", flush=True)
    print(f'extractions completed: {total}; errors: {failures}', flush=True)
    audit()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['audit', 'extract'])
    parser.add_argument('--limit', type=int)
    parser.add_argument('--retry-errors', action='store_true')
    args = parser.parse_args()
    if args.command == 'audit':
        audit()
    else:
        extract(args.limit, args.retry_errors)


if __name__ == '__main__':
    main()
