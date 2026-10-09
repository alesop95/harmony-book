"""Import prepared, verified bibliography entries and reconcile registry flags.

Preview by default. Use --apply only when the session authorizes bibliography
updates. Existing entries are never replaced by an import. Source contents and
the import report remain private; this tool does not assert full-text reading.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('source_library', ROOT / 'tools/source-library.py')
library = importlib.util.module_from_spec(spec)
spec.loader.exec_module(library)


def synchronize(proposals, apply=False):
    registry_path = ROOT / '_notes/book-bib-registry.json'
    bib_path = ROOT / 'manuscript/bib/references.bib'
    original = bib_path.read_bytes()
    text = original.decode('utf-8-sig')
    existing = library.bib_entries(text)
    registry = library.json_read(registry_path, {})
    candidates = {}
    for proposal in proposals:
        for key, entry in library.bib_entries(proposal.read_text(encoding='utf-8-sig')).items():
            if key in candidates and entry != candidates[key]:
                raise ValueError(f'Conflicting proposals: {key}')
            candidates[key] = entry
    new = {key: entry for key, entry in candidates.items() if key not in existing}
    for key in new:
        matches = [record for record in registry.values() if record.get('citekey') == key]
        if not any(record.get('bib_status') == 'verificata' for record in matches):
            raise ValueError(f'Metadata not verified in registry: {key}')
        if len(matches) > 1:
            raise ValueError(f'Reconcile shared citekey before importing: {key}')
    eol = '\r\n' if b'\r\n' in original else '\n'
    appended = text
    if new:
        addition = '\n\n'.join(new.values()).replace('\r\n', '\n').replace('\n', eol)
        appended = text.rstrip() + eol + eol + '% Importazione di voci verificate: ' + datetime.now(timezone.utc).date().isoformat() + eol + addition + eol
    final = library.bib_entries(appended)
    for key, entry in existing.items():
        if final.get(key) != entry:
            raise ValueError(f'Existing entry changed: {key}')
    flag_changes = []
    for record_id, record in registry.items():
        in_bib = record.get('citekey') in final
        if bool(record.get('bib_entry_written')) != in_bib:
            flag_changes.append(record_id)
        record['bib_entry_written'] = in_bib
        if in_bib:
            record['bib_file'] = 'manuscript/bib/references.bib'
    report = {
        'generated_utc': datetime.now(timezone.utc).isoformat(),
        'applied': apply,
        'before': len(existing), 'after': len(final),
        'added': list(new),
        'already_present': [key for key in candidates if key in existing],
        'flag_changes': flag_changes,
        'previous_bib_sha256': hashlib.sha256(original).hexdigest(),
    }
    if apply:
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup = ROOT / '_notes/10-biblioteca/backup-bib' / ('references-' + stamp + '.bib')
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(original)
        payload = appended.encode('utf-8')
        if original.startswith(b'\xef\xbb\xbf'):
            payload = b'\xef\xbb\xbf' + payload
        bib_path.write_bytes(payload)
        library.json_write(registry_path, registry)
        report['backup'] = backup.relative_to(ROOT).as_posix()
        report['result_bib_sha256'] = hashlib.sha256(payload).hexdigest()
        archive = ROOT / '_notes/10-biblioteca/importazioni' / ('sync-' + stamp + '.json')
        report['archive'] = archive.relative_to(ROOT).as_posix()
        library.json_write(archive, report)
        library.json_write(ROOT / '_notes/10-biblioteca/ultimo-sync-bib.json', report)
    print(json.dumps(report, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--proposals', nargs='+', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    synchronize(args.proposals, args.apply)


if __name__ == '__main__':
    main()
