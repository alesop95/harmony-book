#!/usr/bin/env python3
"""Inventory a local music corpus without changing its files or the bibliography.

Example:
    python tools/audit-local-sources.py --root "J:\\MAIN\\MUSIC\\THEORY and INSTRUMENTS" \
        --snapshot _notes/10-biblioteca/cataloghi/catalogo-locale-2026-10-07.json

A later run may pass --previous with an earlier snapshot to distinguish newly
arrived files from files that simply lack a bibliography record.
"""

import argparse
import collections
import datetime as dt
import json
import os
from pathlib import Path


EXTENSIONS = {".pdf", ".epub", ".docx"}
PATH_FIELDS = ("source_path", "source_path_duplicate")


def norm(path):
    return os.path.normcase(os.path.normpath(str(path)))


def registered_paths(registry_path):
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Il registro deve essere un oggetto JSON")
    return {
        norm(entry[field])
        for entry in data.values()
        if isinstance(entry, dict)
        for field in PATH_FIELDS
        if entry.get(field)
    }


def scan(root, known, all_files=False):
    rows = []
    for directory, _, filenames in os.walk(root):
        for filename in filenames:
            path = Path(directory) / filename
            if not all_files and path.suffix.lower() not in EXTENSIONS:
                continue
            rel = path.relative_to(root)
            info = path.stat()
            rows.append({
                "relative_path": str(rel),
                "group": rel.parts[0],
                "bytes": info.st_size,
                "mtime_ns": info.st_mtime_ns,
                "path_in_registry": norm(path) in known,
            })
    return sorted(rows, key=lambda row: row["relative_path"].casefold())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--registry", type=Path, default=Path("_notes/book-bib-registry.json"))
    parser.add_argument("--snapshot", type=Path, help="Scrive una fotografia privata JSON")
    parser.add_argument("--previous", type=Path, help="Confronta con una fotografia precedente")
    parser.add_argument("--all-files", action="store_true", help="Include appunti, collegamenti e media oltre ai documenti")
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"Cartella inesistente: {root}")
    known = registered_paths(args.registry)
    rows = scan(root, known, args.all_files)
    counts = collections.Counter((row["group"], row["path_in_registry"]) for row in rows)
    print(f"Documenti: {len(rows)}; percorsi nel registro: {sum(row['path_in_registry'] for row in rows)}")
    for group in sorted({row["group"] for row in rows}, key=str.casefold):
        print(f"{group}: {counts[(group, True)]} nel registro, {counts[(group, False)]} senza percorso")

    if args.previous:
        old = json.loads(args.previous.read_text(encoding="utf-8"))
        prior = {row["relative_path"].casefold(): row for row in old["files"]}
        current = {row["relative_path"].casefold(): row for row in rows}
        added = sorted(current.keys() - prior.keys())
        missing = sorted(prior.keys() - current.keys())
        changed = sorted(k for k in current.keys() & prior.keys()
                         if (current[k]["bytes"], current[k]["mtime_ns"])
                         != (prior[k]["bytes"], prior[k]["mtime_ns"]))
        print(f"Dalla fotografia precedente: {len(added)} aggiunti, {len(missing)} assenti, {len(changed)} con dimensione o data diversa")
        for label, keys, source in (("AGGIUNTO", added, current), ("ASSENTE", missing, prior), ("CAMBIATO", changed, current)):
            for key in keys:
                print(f"{label}: {source[key]['relative_path']}")

    if args.snapshot:
        args.snapshot.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "observed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "root": str(root),
            "extensions": "all" if args.all_files else sorted(EXTENSIONS),
            "matching_rule": "Percorso esatto in source_path o source_path_duplicate; non prova anagrafica o lettura",
            "files": rows,
        }
        args.snapshot.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Fotografia: {args.snapshot}")


if __name__ == "__main__":
    main()
