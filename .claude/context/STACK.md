---
generated-from-commit: 017b02a
generated-from-branch: main
generated-date: 2026-06-15
covers-paths:
  - style/**
  - scripts/**
  - sample/**
  - tools/**
  - tex-packages.txt
  - .latexmkrc
  - .gitattributes
source-doc: transform-into-claude-md/devBook settings.docx
last-verified-commit: 9acc2e0
---

# Stack applicativo

> Documento di recupero più importante: tracciato. Derivato dalla ricerca in `transform-into-claude-md/` (handoff ignorato) e dalle decisioni ADR-003/ADR-004.

## Stack e runtime

Composizione in LaTeX con engine LuaLaTeX, fissato in `.latexmkrc` (`$pdf_mode = 4`). LuaLaTeX e' scelto per Unicode nativo, font OpenType via `fontspec` e microtipografia completa di `microtype` (espansione + protrusione), cioe' la resa editoriale che `pdflatex` non raggiunge. Classe del libro: `memoir`. Lingua italiana via `babel`. Font: famiglia Libertinus (`libertinus-fonts`), con `unicode-math` per la matematica coordinata.

Notazione musicale: LilyPond integrato tramite il preprocessore `lilypond-book`, che produce esempi vettoriali di qualita' editoriale dentro il LaTeX. I sorgenti che contengono musica usano estensione `.lytex`; gli spartiti stanno in file `.ly`. LilyPond e' un binario esterno, non un pacchetto TeX: va installato a parte e messo sul PATH (`lilypond`, `lilypond-book`).

Bibliografia: `biblatex` + `biber` (export Zotero -> BetterBibTeX nel `.bib`). Indice analitico: `imakeidx`. Glossario dei termini: `glossaries`. Riferimenti incrociati: `cleveref` (dopo `hyperref`). Figure vettoriali (cerchio delle quinte, schemi tonali): `tikz`/`pgfplots`.

Ambiente riproducibile: TinyTeX user-local, descritto dal manifesto `tex-packages.txt` e installato dagli script `scripts/setup-tex.{ps1,sh}` (sezione 13 di `PROJECT-SYSTEM.md`); la distribuzione TeX materializzata non e' versionata. Build a un comando con `scripts/build.{ps1,sh}`, che esegue la passata `lilypond-book` (per i `.lytex`) e poi `latexmk -lualatex`, con output in `build/` (ignorata). Portabilita' Windows 11 / Linux garantita dalla coppia di script `.ps1`/`.sh` e da `.gitattributes` che forza LF. La procedura e' incapsulata nella skill `latex-build`.

## Alternative deliberatamente escluse

Quarto + Pandoc come front-end di authoring (sorgente `.qmd`, output multiplo PDF/EPUB/HTML interattivo): valutato (era il centro della ricerca) e rimandato a una Fase 2, non adottato ora. Motivo: aggiunge un layer di toolchain e una resa tipografica meno controllabile, mentre l'obiettivo immediato e' scrivere il libro con la massima qualita' editoriale del PDF e diff git puliti; le sorgenti LaTeX+LilyPond restano riusabili da Quarto se l'edizione web diventera' un'esigenza.

Docker + GitHub Actions (ambiente containerizzato e build CI multi-formato): rimandato a una Fase 3. Motivo: l'ambiente nativo TinyTeX + manifesto e' gia' riproducibile e portabile senza il peso di Docker; la CI ha senso quando esistera' un'edizione web da pubblicare.

`pdflatex` come engine: escluso per i limiti su font moderni, Unicode e microtipografia. `musixtex` come notazione full-LaTeX: escluso a favore di LilyPond per qualita' e ergonomia.

## Flussi di codice e ruolo architetturale dei file

Il preambolo condiviso `style/preamble.tex` (pubblico) carica pacchetti e impostazioni tipografiche; `style/harmony-macros.sty` raccoglie le macro di notazione armonica. I file principali fanno `\documentclass{memoir}` seguito da `\input{preamble}`. Il contenuto reale vive in `manuscript/` (ignorato): `main.lytex` include i capitoli `chapters/*.lytex`, gli esempi `music/*.ly` e la bibliografia `bib/references.bib`. `sample/main.lytex` (pubblico) e' un documento minimo che esercita l'intera catena per verificarla senza esporre contenuto. Gli script di build risolvono i percorsi via `TEXINPUTS`/`BIBINPUTS` impostati per includere `style/` e la cartella sorgente, e scelgono `manuscript/main.lytex` se presente, altrimenti `sample/main.lytex`.

## Gli strumenti sotto `tools/`

Sezione aggiunta il 2026-08-06 insieme a `tools/**` nelle `covers-paths`, che prima mancava: fino a quel giorno un cambiamento sotto `tools/` non veniva confrontato con questa scheda, quindi il drift sugli script era per costruzione invisibile a `sync-context` da questo lato. Gli script sono undici, nove Python, uno Node e uno PowerShell, più il `README.md` della cartella. La scheda `current-work.md` copriva `tools/**` dal 2026-08-03, ma descrive il lavoro in corso, non lo stack: il posto dove questi strumenti vanno descritti è qui.

Il criterio con cui questi strumenti esistono è quello di `.claude/rules/token-economy.md`, cioè spingere su codice deterministico tutto ciò che non richiede comprensione semantica, e quello di ADR-009 per i due che implementano affermazioni del libro: le definizioni che usano sono quelle del libro, non quelle scolastiche, e un cambio di definizione è un cambio di contenuto, non un refactor.

Due strumenti implementano il contenuto del libro invece di documentarlo, e sono registrati come fonti nel manifesto della skill `armonia-libro` proprio per questo. `tritoni-scale.py` calcola il contenuto di tritoni delle scale rappresentate come insiemi di classi di altezza modulo dodici, esamina la corrispondenza fra una scala e la sua coppia di tritoni, ed è lo strumento che ha smentito l'intuizione della corrispondenza biunivoca sostituendola con il risultato due a uno e i due teoremi. `derivazione-scale.py` implementa la macchina delle dominanti secondarie ai due livelli fissati dall'utente il 2026-08-03: il primo livello sono le scale ottenute alterando una sola nota rispetto alla tonalità diatonica di partenza, il secondo quelle ottenute applicando la stessa operazione a ciascuna scala di primo livello.

Due strumenti tengono in pari gli artefatti derivati. `skill-freshness.py` rileva la deriva fra una skill e le sue fonti ricalcolando gli sha256 registrati nel manifesto `.sources.json`, e porta il vincolo d'ordine che è costato un ciclo di deriva invisibile: `--update` riallinea gli hash senza toccare il contenuto, quindi si lancia solo dopo aver rigenerato la skill. `render-bib-registry.py` rigenera `_notes/book-bib-registry.md` dal JSON del registro, leggendo il titolo dal `.bib` reale quando la voce è già scritta e usando il nome del file sorgente come segnaposto quando non lo è.

Tre strumenti servono l'ingestione documentale e la disciplina bibliografica. `doc-ingest.py` converte un corpus di `.pdf`, `.docx`, `.pptx`, `.xlsx` e `.html` in una cache Markdown locale con manifest a content-hash per non riconvertire l'invariato, e rigenera l'`_INDEX.md` che è lo scheletro di Livello 1 della disclosure progressiva. `probe-pdf-text.py` fa il triage deterministico della qualità del testo estraibile da un PDF, perché né il conteggio dei caratteri né un campione dalle prime pagine bastano a decidere se un libro si può digerire, e sbagliano in direzioni opposte. `extract-titlepages.py` estrae come PNG le pagine di frontespizio e colophon per la verifica visiva richiesta da `book-bib-extract`, fissando DPI e numero di pagine che nelle sessioni manuali cambiavano ogni volta.

Due strumenti presidiano la convenzione della sorgente Markdown fissata in `.claude/rules/interaction-style.md` e il formato dei comandi di `git-commands-format.md`. `md-unwrap.py` srotola i paragrafi con a capo interni unendo i pezzi con un singolo spazio, e non normalizza nient'altro: marcatori di lista, tabelle, stili di titolo, escaping e ordine restano come sono; quando `markdown-it-py` è importabile ogni file passa da un oracolo di rendering che pretende un HTML normalizzato identico, e in caso di divergenza il file non viene scritto. `lint-md-commands.py` copre l'angolo che il primo per contratto non tocca, cioè il contenuto dei blocchi recintati: cerca i comandi non copiabili in una riga sola, cioè continuazioni di riga con backslash, backtick o caret, heredoc multi-riga e comandi git che proseguono sulla riga seguente, riconosce un blocco come shell dalla sua info string o dal contenuto quando l'info string manca, è in sola lettura ed esce con codice 1 se trova qualcosa, così si usa come gate.

Restano due strumenti di servizio. `render-diagrams.mjs` rende i diagrammi Mermaid di `.claude/context/diagrams/*.mmd` nei corrispondenti `.svg` riusando il browser Chromium-based di sistema senza scaricare il Chromium di Puppeteer. `latest-screenshot.ps1`, scritto il 2026-08-06, restituisce il percorso e l'età dell'immagine più recente nella cartella di cattura, ed è lo strumento che `.claude/rules/manual-screenshots.md` presuppone quando un passo dello sviluppo è visibile solo all'utente.

Nessuno di questi strumenti entra nella catena di build del libro: `scripts/build.{ps1,sh}` non li invoca, e il PDF si compila senza di essi. Vivono accanto al libro come strumenti di verifica e di manutenzione, e per questo sono tracciati mentre il contenuto che verificano non lo è.

## Riferimenti a snippet

- `.latexmkrc` — engine LuaLaTeX e pulizia ausiliari.
- `style/preamble.tex` — pacchetti e tipografia.
- `style/harmony-macros.sty:\grado` — macro di notazione armonica.
- `style/harmony-macros.sty:apertura` — ambiente per il brano introduttivo in corsivo, rientrato e staccato dal resto (usato per l'introduzione/abstract del libro).
- `scripts/build.ps1` / `scripts/build.sh` — passata `lilypond-book` + `latexmk -lualatex`.
- `tex-packages.txt` — manifesto riproducibile dell'ambiente TeX.
- `tools/tritoni-scale.py` / `tools/derivazione-scale.py` — implementano affermazioni del libro (ADR-009).
- `tools/skill-freshness.py` — deriva fra skill e fonti; `--update` solo dopo la rigenerazione.
- `tools/latest-screenshot.ps1` — percorso ed età dell'ultimo screenshot, per `manual-screenshots.md`.
- Riferimenti esterni su LilyPond+LaTeX e autopubblicazione: vedi `README.md`, sezione "Risorse e riferimenti".
