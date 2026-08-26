#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probe-pdf-text.py - Triage deterministica della qualità del testo estraibile da un corpus PDF.

Serve a decidere quali PDF si possono digerire leggendone il testo e quali no, prima di spendere
un solo token. Né il conteggio di caratteri né un campione preso dalle prime pagine bastano a
dire se un PDF è utilizzabile, e sbagliano in direzioni opposte.

Un PDF può portare uno strato di testo corposo ma inservibile, e allora il solo conteggio inganna
in eccesso. Al contrario, le prime pagine di un libro scansionato sono frontespizi con tipografia
decorativa, che qualunque OCR rende male anche quando il resto del volume è pulito: caso reale di
questo corpus, "Jazz Theory (1995, M.Levine).pdf" restituisce "J ll o THE A z z THE 0 Ry B0 0 K"
sul frontespizio ma prosa integra e leggibile a metà volume. Un campione preso in testa lo
scarterebbe a torto.

Per questo il campione si prende a metà libro, dove ci si aspetta prosa corrente, e la qualità
si misura con un indice invece che con un conteggio. L'indice combina tre segnali indipendenti, tutti
robusti rispetto alla lingua (il corpus è misto inglese/italiano) e insensibili al vocabolario:

  parole_lunghe  quota di token di almeno 4 lettere alfabetiche. L'OCR rotto frammenta le parole
                 in schegge di 1-2 caratteri, quindi questa quota crolla.
  alfabetico     quota di caratteri alfabetici sul totale dei non-spazi. Le scansioni di spartiti
                 producono pioggia di simboli e cifre.
  righe_prosa    quota di righe non vuote che sembrano prosa, cioè con almeno cinque parole e una
                 lunghezza media di parola plausibile.

Verdetto: alto (digeribile leggendo il testo), medio (utilizzabile con cautela, controllare a
campione), basso (strato di testo inservibile: serve una copia migliore del PDF o la lettura visiva
mirata di ADR-006), assente (nessuno strato di testo).

Dipendenze: pdftotext e pdfinfo (Poppler), già in uso nel progetto. Nessuna chiamata LLM.

Uso:
    python tools/probe-pdf-text.py "J:/.../ARMONIA E TEORIA"
    python tools/probe-pdf-text.py <cartella> --out _notes/corpus-digest-triage.md
    python tools/probe-pdf-text.py <cartella> --sample 6      # pagine campionate a metà libro
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

WORD = re.compile(r"[^\W\d_]+", re.UNICODE)

# Soglie dell'indice composito, tarate sui casi noti di questo corpus: Berkman 2013 (testo
# digitale nativo) e Levine 1995 (OCR buono a metà volume) devono finire in "alto"; i Piston,
# che non hanno alcuno strato di testo, in "assente".
SOGLIA_ALTO = 0.62
SOGLIA_MEDIO = 0.38

# Sotto questa soglia di caratteri sul campione, lo strato di testo si considera inesistente:
# poche decine di caratteri sono rumore del layer immagine, non testo. I Piston ne danno 4.
MIN_CHARS_TESTO = 200

# Densità minima di caratteri per pagina campionata perché valga la pena digerire il testo.
# Sopra questa soglia c'e' prosa corrente; sotto, il testo è leggibile ma la pagina è fatta
# di notazione musicale o di tabelle, e digerirla dal testo estratto non rende. Riferimenti di
# questo corpus: Berkman circa 1980, Levine circa 1550, Kostka circa 750, Beato circa 125.
MIN_DENSITA = 300


def run(cmd):
    try:
        return subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120
        )
    except (subprocess.TimeoutExpired, OSError):
        return None


def page_count(pdf):
    res = run(["pdfinfo", str(pdf)])
    if res is None or res.returncode != 0:
        return None
    for line in res.stdout.splitlines():
        if line.startswith("Pages:"):
            try:
                return int(line.split()[1])
            except (IndexError, ValueError):
                return None
    return None


def extract(pdf, first, last):
    res = run(["pdftotext", "-f", str(first), "-l", str(last), str(pdf), "-"])
    if res is None or res.returncode != 0:
        return ""
    return res.stdout


def quality(text):
    """Indice composito in [0,1] più i tre segnali che lo compongono."""
    tokens = text.split()
    if len(tokens) < 40:
        return 0.0, {"parole_lunghe": 0.0, "alfabetico": 0.0, "righe_prosa": 0.0}

    def run_alfabetico_piu_lungo(token):
        parti = WORD.findall(token)
        return max((len(p) for p in parti), default=0)

    lunghe = sum(1 for t in tokens if run_alfabetico_piu_lungo(t) >= 4)
    parole_lunghe = lunghe / len(tokens)

    non_spazi = [c for c in text if not c.isspace()]
    alfabetico = (sum(1 for c in non_spazi if c.isalpha()) / len(non_spazi)) if non_spazi else 0.0

    righe = [r for r in text.splitlines() if r.strip()]
    prosa = 0
    for r in righe:
        parole = r.split()
        if len(parole) < 5:
            continue
        media = sum(len(p) for p in parole) / len(parole)
        if 3.0 <= media <= 12.0:
            prosa += 1
    righe_prosa = (prosa / len(righe)) if righe else 0.0

    indice = 0.45 * parole_lunghe + 0.35 * alfabetico + 0.20 * righe_prosa
    return indice, {
        "parole_lunghe": parole_lunghe,
        "alfabetico": alfabetico,
        "righe_prosa": righe_prosa,
    }


def verdict(chars, indice, densita):
    if chars < MIN_CHARS_TESTO:
        return "assente"
    if densita < MIN_DENSITA:
        # Il testo che c'e' è leggibile, ma ce n'e' troppo poco: pagine di sola notazione o
        # di tabelle. Digerirle dal testo estratto non rende, a prescindere dall'indice.
        return "poco-testo"
    if indice >= SOGLIA_ALTO:
        return "alto"
    if indice >= SOGLIA_MEDIO:
        return "medio"
    return "basso"


def probe(pdf, sample):
    pages = page_count(pdf)
    if pages is None:
        return {
            "file": pdf,
            "pages": None,
            "chars": 0,
            "indice": 0.0,
            "segnali": {},
            "verdetto": "illeggibile",
        }

    # Campione a metà libro: lì c'e' prosa, non frontespizi né indici.
    start = max(1, pages // 2 - sample // 2)
    end = min(pages, start + sample - 1)
    text = extract(pdf, start, end)
    chars = len(text.replace(" ", "").replace("\n", ""))
    campionate = end - start + 1
    densita = chars / campionate if campionate else 0.0
    indice, segnali = quality(text)
    return {
        "file": pdf,
        "pages": pages,
        "range": (start, end),
        "chars": chars,
        "densita": densita,
        "indice": indice,
        "segnali": segnali,
        "verdetto": verdict(chars, indice, densita),
    }


ORDINE = ("alto", "medio", "basso", "poco-testo", "assente", "illeggibile")

GLOSSARIO = {
    "alto": "prosa corrente pulita: digeribile leggendo il testo estratto",
    "medio": "testo utilizzabile con cautela, controllare a campione prima di fidarsi",
    "basso": "strato di testo presente ma inservibile: serve una copia migliore",
    "poco-testo": "testo leggibile ma quasi assente: pagine di sola notazione o tabelle",
    "assente": "nessuno strato di testo, scansione pura",
    "illeggibile": "PDF non apribile da Poppler",
}


def render(rows, source):
    rank = {v: i for i, v in enumerate(ORDINE)}
    rows = sorted(rows, key=lambda r: (rank[r["verdetto"]], -r["indice"]))

    out = []
    out.append("# Triage della qualità del testo estraibile\n")
    out.append(
        "> Generato da `tools/probe-pdf-text.py`. Non modificare a mano: si rigenera a ogni corsa.\n"
        f"> Sorgente: `{source}`\n"
    )
    out.append(
        "\nIl campione si prende a metà libro, non in testa, perché i frontespizi sono tipografia "
        "decorativa che qualunque OCR rende male anche quando il resto del volume è pulito. "
        "L'indice combina la quota di parole di almeno 4 lettere, la quota di caratteri alfabetici "
        "e la quota di righe che sembrano prosa. La densità è il numero di caratteri per pagina "
        "campionata, e serve a distinguere un libro di prosa da uno fatto di notazione musicale, "
        "dove il testo che c'e' è leggibile ma non c'e' quasi testo.\n"
    )

    conteggi = {}
    for r in rows:
        conteggi[r["verdetto"]] = conteggi.get(r["verdetto"], 0) + 1
    out.append("\n## Riepilogo\n")
    for v in ORDINE:
        if v in conteggi:
            out.append(f"- {v} ({conteggi[v]}): {GLOSSARIO[v]}")
    out.append("")

    out.append("\n## Dettaglio\n")
    out.append("| Verdetto | Indice | Car./pag. | Pagine | Caratteri | File |")
    out.append("|---|---|---|---|---|---|")
    for r in rows:
        pages = r["pages"] if r["pages"] is not None else "?"
        out.append(
            f"| {r['verdetto']} | {r['indice']:.2f} | {r.get('densita', 0):.0f} | {pages} "
            f"| {r['chars']} | {r['file'].name} |"
        )

    sostituire = [
        r for r in rows if r["verdetto"] in ("basso", "assente", "illeggibile", "poco-testo")
    ]
    if sostituire:
        out.append("\n## Candidati a una copia migliore del PDF\n")
        out.append(
            "Questi file non si possono digerire leggendone il testo estratto. Nell'ordine: "
            "verificare se un'altra copia dello stesso titolo, già presente nel corpus, ha un "
            "verdetto migliore; altrimenti procurarsi una copia con testo nativo; altrimenti "
            "applicare la lettura visiva mirata di ADR-006 sulle sole pagine pertinenti.\n"
        )
        for r in sostituire:
            motivo = GLOSSARIO[r["verdetto"]]
            if r["verdetto"] == "basso":
                motivo += f" (indice {r['indice']:.2f})"
            if r["verdetto"] == "poco-testo":
                motivo += f" ({r.get('densita', 0):.0f} caratteri per pagina)"
            out.append(f"- `{r['file'].name}`: {motivo}")

    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[2])
    parser.add_argument("source", help="Cartella da scansionare ricorsivamente")
    parser.add_argument("--out", help="File Markdown da scrivere. Omesso: stampa a schermo.")
    parser.add_argument(
        "--sample", type=int, default=4, help="Pagine campionate a metà libro (default 4)"
    )
    args = parser.parse_args()

    source = Path(args.source)
    if not source.is_dir():
        print(f"[errore] {source} non è una cartella.")
        return 2

    pdfs = sorted(p for p in source.rglob("*") if p.suffix.lower() == ".pdf")
    if not pdfs:
        print(f"[errore] nessun PDF sotto {source}.")
        return 2

    rows = []
    for i, pdf in enumerate(pdfs, 1):
        print(f"[{i}/{len(pdfs)}] {pdf.name}", file=sys.stderr)
        rows.append(probe(pdf, args.sample))

    report = render(rows, source)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"[ok] scritto {out} ({len(rows)} PDF)")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
