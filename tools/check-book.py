"""Read-only checks for the book's LaTeX inclusion and citation graph.

This is a preflight, not a TeX or BibLaTeX parser. It intentionally leaves
the private manuscript and bibliography untouched.
"""

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")
BIB = re.compile(r"\\addbibresource(?:\[[^]]*\])?\s*\{([^}]+)\}")
CITE = re.compile(r"\\(?:auto|par|text|foot|full|smart)?cite\*?(?:\[[^]]*\])*\s*\{([^}]+)\}")
ENTRY = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)


def active_tex(path):
    lines = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        lines.append(re.split(r"(?<!\\)%", line, maxsplit=1)[0])
    return "\n".join(lines)


def resolve_input(name, source, main_dir):
    item = Path(name)
    variants = (item,) if item.suffix else (item.with_suffix(".lytex"), item.with_suffix(".tex"))
    for base in (source.parent, main_dir, ROOT / "style"):
        for variant in variants:
            candidate = base / variant
            if candidate.is_file():
                return candidate.resolve()
    return None


def check(main):
    errors, warnings, visited, citations, resources = [], [], set(), set(), set()
    main_dir = main.parent

    def walk(source):
        source = source.resolve()
        if source in visited:
            return
        visited.add(source)
        content = active_tex(source)
        for name in INPUT.findall(content):
            target = resolve_input(name, source, main_dir)
            if target is None:
                errors.append(f"include mancante: {source.relative_to(ROOT)} -> {name}")
            else:
                walk(target)
        for name in BIB.findall(content):
            candidates = (source.parent / name, main_dir / name, main_dir / "bib" / name)
            target = next((p.resolve() for p in candidates if p.is_file()), None)
            if target is None:
                errors.append(f"bibliografia mancante: {source.relative_to(ROOT)} -> {name}")
            else:
                resources.add(target)
        for group in CITE.findall(content):
            citations.update(key.strip() for key in group.split(",") if key.strip())

    walk(main)
    keys = set()
    for bib in sorted(resources):
        for key in ENTRY.findall(bib.read_text(encoding="utf-8-sig")):
            if key in keys:
                errors.append(f"citekey duplicata: {key}")
            keys.add(key)
    for key in sorted(citations - keys):
        errors.append(f"citazione senza voce bibliografica: {key}")
    if keys and not citations and main_dir.name == "manuscript":
        warnings.append("nessuna citekey usata: la bibliografia stampata resta vuota")
    chapter_dir = main_dir / "chapters"
    if chapter_dir.is_dir():
        for chapter in sorted(chapter_dir.glob("*.lytex")):
            if chapter.resolve() not in visited:
                warnings.append(f"capitolo non incluso nel main: {chapter.relative_to(ROOT)}")
    return errors, warnings, len(visited), len(keys), len(citations)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main", type=Path, help="sorgente principale, relativo alla radice")
    args = parser.parse_args()
    source = args.main or next((ROOT / p for p in (
        "manuscript/main.lytex", "manuscript/main.tex", "sample/main.lytex", "sample/main.tex"
    ) if (ROOT / p).is_file()), None)
    if source is None:
        parser.error("nessun main trovato")
    if not source.is_absolute():
        source = ROOT / source
    if not source.is_file():
        parser.error(f"file inesistente: {source}")
    errors, warnings, files, bib_keys, cited = check(source)
    print(f"Main: {source.relative_to(ROOT)}; sorgenti: {files}; voci bib: {bib_keys}; citekey usate: {cited}")
    for warning in warnings:
        print(f"AVVISO: {warning}")
    for error in errors:
        print(f"ERRORE: {error}")
    if not errors:
        print("Preflight: nessun collegamento rotto rilevato.")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
