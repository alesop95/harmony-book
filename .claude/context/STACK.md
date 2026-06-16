---
generated-from-commit: PENDING-FIRST-COMMIT
generated-from-branch: main
generated-date: 2026-06-15
covers-paths:
  - style/**
  - scripts/**
  - sample/**
  - tex-packages.txt
  - .latexmkrc
  - .gitattributes
source-doc: transform-into-claude-md/devBook settings.docx
last-verified-commit: PENDING-FIRST-COMMIT
---

# Stack applicativo

> Documento di recupero più importante: tracciato. Derivato dalla ricerca in
> `transform-into-claude-md/` (handoff ignorato) e dalle decisioni ADR-003/ADR-004.

## Stack e runtime

Composizione in LaTeX con engine LuaLaTeX, fissato in `.latexmkrc` (`$pdf_mode = 4`). LuaLaTeX e'
scelto per Unicode nativo, font OpenType via `fontspec` e microtipografia completa di `microtype`
(espansione + protrusione), cioe' la resa editoriale che `pdflatex` non raggiunge. Classe del
libro: `memoir`. Lingua italiana via `babel`. Font: famiglia Libertinus (`libertinus-fonts`), con
`unicode-math` per la matematica coordinata.

Notazione musicale: LilyPond integrato tramite il preprocessore `lilypond-book`, che produce esempi
vettoriali di qualita' editoriale dentro il LaTeX. I sorgenti che contengono musica usano estensione
`.lytex`; gli spartiti stanno in file `.ly`. LilyPond e' un binario esterno, non un pacchetto TeX:
va installato a parte e messo sul PATH (`lilypond`, `lilypond-book`).

Bibliografia: `biblatex` + `biber` (export Zotero -> BetterBibTeX nel `.bib`). Indice analitico:
`imakeidx`. Glossario dei termini: `glossaries`. Riferimenti incrociati: `cleveref` (dopo
`hyperref`). Figure vettoriali (cerchio delle quinte, schemi tonali): `tikz`/`pgfplots`.

Ambiente riproducibile: TinyTeX user-local, descritto dal manifesto `tex-packages.txt` e installato
dagli script `scripts/setup-tex.{ps1,sh}` (sezione 13 di `PROJECT-SYSTEM.md`); la distribuzione TeX
materializzata non e' versionata. Build a un comando con `scripts/build.{ps1,sh}`, che esegue la
passata `lilypond-book` (per i `.lytex`) e poi `latexmk -lualatex`, con output in `build/` (ignorata).
Portabilita' Windows 11 / Linux garantita dalla coppia di script `.ps1`/`.sh` e da `.gitattributes`
che forza LF. La procedura e' incapsulata nella skill `latex-build`.

## Alternative deliberatamente escluse

Quarto + Pandoc come front-end di authoring (sorgente `.qmd`, output multiplo PDF/EPUB/HTML
interattivo): valutato (era il centro della ricerca) e rimandato a una Fase 2, non adottato ora.
Motivo: aggiunge un layer di toolchain e una resa tipografica meno controllabile, mentre l'obiettivo
immediato e' scrivere il libro con la massima qualita' editoriale del PDF e diff git puliti; le
sorgenti LaTeX+LilyPond restano riusabili da Quarto se l'edizione web diventera' un'esigenza.

Docker + GitHub Actions (ambiente containerizzato e build CI multi-formato): rimandato a una Fase 3.
Motivo: l'ambiente nativo TinyTeX + manifesto e' gia' riproducibile e portabile senza il peso di
Docker; la CI ha senso quando esistera' un'edizione web da pubblicare.

`pdflatex` come engine: escluso per i limiti su font moderni, Unicode e microtipografia.
`musixtex` come notazione full-LaTeX: escluso a favore di LilyPond per qualita' e ergonomia.

## Flussi di codice e ruolo architetturale dei file

Il preambolo condiviso `style/preamble.tex` (pubblico) carica pacchetti e impostazioni tipografiche;
`style/harmony-macros.sty` raccoglie le macro di notazione armonica. I file principali fanno
`\documentclass{memoir}` seguito da `\input{preamble}`. Il contenuto reale vive in `manuscript/`
(ignorato): `main.lytex` include i capitoli `chapters/*.lytex`, gli esempi `music/*.ly` e la
bibliografia `bib/references.bib`. `sample/main.lytex` (pubblico) e' un documento minimo che esercita
l'intera catena per verificarla senza esporre contenuto. Gli script di build risolvono i percorsi via
`TEXINPUTS`/`BIBINPUTS` impostati per includere `style/` e la cartella sorgente, e scelgono
`manuscript/main.lytex` se presente, altrimenti `sample/main.lytex`.

## Riferimenti a snippet

- `.latexmkrc` — engine LuaLaTeX e pulizia ausiliari.
- `style/preamble.tex` — pacchetti e tipografia.
- `style/harmony-macros.sty:\grado` — macro di notazione armonica.
- `scripts/build.ps1` / `scripts/build.sh` — passata `lilypond-book` + `latexmk -lualatex`.
- `tex-packages.txt` — manifesto riproducibile dell'ambiente TeX.
- Riferimento esterno: `transform-into-claude-md/latex4musicians.pdf` (cap. 4, LilyPond+LaTeX).
