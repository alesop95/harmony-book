#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill-freshness.py - Rileva la deriva fra una skill derivata e le sue fonti.

Una skill prodotta digerendo altri file (la dottrina del libro da _notes/, un libro di
riferimento da un PDF) è un artefatto derivato: le fonti restano canoniche e continuano a
cambiare, la skill no. Senza un controllo, la deriva è silenziosa e ci si accorge che la
skill è vecchia solo quando risponde con qualcosa che non vale più.

Ogni skill derivata porta un manifesto `.sources.json` con lo sha256 di ciascuna fonte al
momento della digestione. Questo script ricalcola gli hash e dice quali fonti sono cambiate.
Costa CPU locale e nessun token, secondo il principio deterministico-prima-del-linguistico di
.claude/rules/token-economy.md.

Uso:
    python tools/skill-freshness.py                       # controlla tutte le skill con manifesto
    python tools/skill-freshness.py .claude/skills/armonia-libro
    python tools/skill-freshness.py <skill> --update      # riscrive il manifesto agli hash attuali

Codici di uscita: 0 tutto fresco, 1 almeno una fonte cambiata o mancante, 2 errore d'uso.
"""

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

MANIFEST_NAME = ".sources.json"
SKILLS_DIR = Path(".claude/skills")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def repo_root():
    """Radice del repo: la cartella che contiene .claude/, risalendo dal cwd."""
    here = Path.cwd().resolve()
    for candidate in [here, *here.parents]:
        if (candidate / ".claude").is_dir():
            return candidate
    return here


def resolve(root, recorded):
    """Le fonti dentro il repo si registrano relative alla radice; quelle fuori, per esempio su un
    disco esterno, si registrano assolute, perche su Windows i drive non stanno in un albero unico
    e un percorso relativo non puo attraversarli."""
    p = Path(recorded)
    return p if p.is_absolute() else root / p


def load_manifest(skill_dir):
    path = skill_dir / MANIFEST_NAME
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check(skill_dir, root):
    """Confronta gli hash registrati con quelli attuali. Ritorna (fresche, cambiate, mancanti)."""
    manifest = load_manifest(skill_dir)
    if manifest is None:
        return None
    fresh, changed, missing = [], [], []
    for rel, recorded in sorted(manifest.get("sources", {}).items()):
        target = resolve(root, rel)
        if not target.exists():
            missing.append(rel)
        elif sha256_of(target) == recorded:
            fresh.append(rel)
        else:
            changed.append(rel)
    return manifest, fresh, changed, missing


def update(skill_dir, root):
    manifest = load_manifest(skill_dir)
    if manifest is None:
        print(f"[errore] nessun {MANIFEST_NAME} in {skill_dir}: crealo prima, anche a mano.")
        return 2
    sources = {}
    for rel in sorted(manifest.get("sources", {})):
        target = resolve(root, rel)
        if not target.exists():
            print(f"[attenzione] fonte sparita, la tengo nel manifesto senza hash: {rel}")
            sources[rel] = None
            continue
        sources[rel] = sha256_of(target)
    manifest["sources"] = sources
    manifest["generated"] = date.today().isoformat()
    with open(skill_dir / MANIFEST_NAME, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"[ok] manifesto riallineato: {skill_dir / MANIFEST_NAME} ({len(sources)} fonti)")
    return 0


def report(skill_dir, result):
    manifest, fresh, changed, missing = result
    generated = manifest.get("generated", "data ignota")
    print(f"\n=== {skill_dir}  (digerita il {generated}) ===")
    for rel in changed:
        print(f"  CAMBIATA  {rel}")
    for rel in missing:
        print(f"  MANCANTE  {rel}")
    if not changed and not missing:
        print(f"  fresca: {len(fresh)} fonti invariate")
    else:
        print(f"  invariate: {len(fresh)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[2])
    parser.add_argument(
        "skill",
        nargs="?",
        help="Cartella della skill da controllare. Omesso: tutte quelle con un manifesto.",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Riscrive il manifesto con gli hash attuali, dopo aver rigenerato la skill.",
    )
    args = parser.parse_args()

    root = repo_root()

    if args.skill:
        targets = [Path(args.skill)]
    else:
        base = root / SKILLS_DIR
        if not base.is_dir():
            print(f"[errore] {base} non esiste.")
            return 2
        targets = sorted(d for d in base.iterdir() if (d / MANIFEST_NAME).exists())
        if not targets:
            print("Nessuna skill con manifesto .sources.json.")
            return 0

    if args.update:
        if not args.skill:
            print("[errore] --update richiede una skill esplicita, per non riallinearle tutte.")
            return 2
        return update(targets[0], root)

    stale = False
    for skill_dir in targets:
        result = check(skill_dir, root)
        if result is None:
            print(f"[errore] nessun {MANIFEST_NAME} in {skill_dir}.")
            return 2
        report(skill_dir, result)
        if result[2] or result[3]:
            stale = True

    if stale:
        print(
            "\nAlmeno una fonte è cambiata. Rigenera le parti di skill interessate, poi\n"
            "riallinea con: python tools/skill-freshness.py <skill> --update"
        )
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
