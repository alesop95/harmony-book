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


## GPU e ancoraggi del lettore locale

Il servizio isolato usa ora la GPU ripristinata. Qwen3 14B è interamente in VRAM con contesto 16.384, misurato dall'API. Il formato locale v3 chiede solo id di ancora per gli elementi: evidenze e localizzatori vengono derivati dalle unità integrali dal programma. La suddivisione conserva i genitori e riprova figli contigui dopo saturazione o fallimento della validazione. Landlock permette la directory RAM, i dispositivi effettivi NVIDIA e le scritture dei metadati virtuali `/proc` richieste da CUDA; il disco del server rimane non scrivibile. Stato, schede e dettagli di esecuzione rimangono privati.

## Lettore semantico locale e corpus integrale

`tools/local-reading.py` orchestra OCR, unità documentali, trascrizioni, indice SQLite FTS5 e schede locali in JSON/Markdown. Le porzioni conservano ogni carattere del testo preparato; le evidenze sono validate nell'unità d'origine. Temi, glossario, relazioni e frontiera sono derivati non revisionati, distinti dal ledger delle letture. La configurazione e tutti gli artefatti sono privati sotto `_notes/`; modelli, endpoint e percorsi reali non sono nel codice pubblico.

`tools/start-local-reading.ps1` separa preparazione, trascrizioni, servizio, pilota e supervisione in processi Windows nascosti, con PID e log nel progetto. `tools/isolated-ollama-host.py` viene eseguito in memoria attraverso SSH; Landlock nega scritture sul filesystem remoto e consente soltanto temporanei in RAM e dispositivi, con pulizia al termine del canale. Pesi già installati, nessun pull o installazione remota. L'analizzatore usa output strutturati di Ollama e checkpoint dello stream; la supervisione prosegue dopo il pilota ancorato e arresta il servizio dedicato alla fine o all'errore. La disponibilità GPU è una misura d'esecuzione, non un requisito presunto. Procedura e copertura nella guida privata `_notes/00-regia/LETTURA-LOCALE.md`.

## Recupero di fonti di comunità

Il lettore già presente `.claude/templates/community-sources/tools/fetch-reddit.py` usa Arctic Shift e conserva post, albero dei commenti, metadati, mappa dei rinvii e stato della corsa sotto `_notes/20-ricerca/acquisizioni-community/`. `--radice` indica la destinazione del progetto; `post` acquisisce un seme, `riprendi` continua uno stato con tetti dichiarati. Non richiede credenziali e non apre il browser personale. Prima si applica `fonti-non-recuperabili`; poi il testo ottenuto viene letto, attribuito e collegato nel vault. Acquisizione, copertura e lettura sono attestazioni distinte.

> Documento di recupero più importante: tracciato. Derivato dalla ricerca in `transform-into-claude-md/` (handoff ignorato) e dalle decisioni ADR-003/ADR-004.

## Stack e runtime

Composizione in LaTeX con engine LuaLaTeX, fissato in `.latexmkrc` (`$pdf_mode = 4`). LuaLaTeX è scelto per Unicode nativo, font OpenType via `fontspec` e microtipografia completa di `microtype` (espansione + protrusione), cioè la resa editoriale che `pdflatex` non raggiunge. Classe del libro: `memoir`. Lingua italiana via `babel`. Font: famiglia Libertinus (`libertinus-fonts`), con `unicode-math` per la matematica coordinata.

Notazione musicale: LilyPond integrato tramite il preprocessore `lilypond-book`, che produce esempi vettoriali di qualità editoriale dentro il LaTeX. I sorgenti che contengono musica usano estensione `.lytex`; gli spartiti stanno in file `.ly`. LilyPond è un binario esterno, non un pacchetto TeX: va installato a parte e messo sul PATH (`lilypond`, `lilypond-book`).

Bibliografia: `biblatex` + `biber` (export Zotero -> BetterBibTeX nel `.bib`). Indice analitico: `imakeidx`. Glossario dei termini: `glossaries`. Riferimenti incrociati: `cleveref` (dopo `hyperref`). Figure vettoriali (cerchio delle quinte, schemi tonali): `tikz`/`pgfplots`.

Ambiente riproducibile: TinyTeX user-local, descritto dal manifesto `tex-packages.txt` e installato dagli script `scripts/setup-tex.{ps1,sh}` (sezione 13 di `PROJECT-SYSTEM.md`); la distribuzione TeX materializzata non è versionata. Build a un comando con `scripts/build.{ps1,sh}`, che esegue la passata `lilypond-book` (per i `.lytex`) e poi `latexmk -lualatex`, con output in `build/` (ignorata). La coppia di script `.ps1`/`.sh` e `.gitattributes` che forza LF preparano la portabilità Windows 11 / Linux; la build è stata provata su Windows, non ancora su Linux. La procedura è incapsulata nella skill `latex-build`.

## Alternative deliberatamente escluse

Quarto + Pandoc come front-end di authoring (sorgente `.qmd`, output multiplo PDF/EPUB/HTML interattivo): valutato (era il centro della ricerca) e rimandato a una Fase 2, non adottato ora. Motivo: aggiunge un layer di toolchain e una resa tipografica meno controllabile, mentre l'obiettivo immediato è scrivere il libro con la massima qualità editoriale del PDF e diff git puliti; le sorgenti LaTeX+LilyPond restano riusabili da Quarto se l'edizione web diventerà un'esigenza.

Docker + GitHub Actions (ambiente containerizzato e build CI multi-formato): rimandato a una Fase 3. Motivo: l'ambiente nativo TinyTeX + manifesto è già riproducibile e portabile senza il peso di Docker; la CI ha senso quando esisterà un'edizione web da pubblicare.

`pdflatex` come engine: escluso per i limiti su font moderni, Unicode e microtipografia. `musixtex` come notazione full-LaTeX: escluso a favore di LilyPond per qualità e ergonomia.

## Flussi di codice e ruolo architetturale dei file

Il preambolo condiviso `style/preamble.tex` (pubblico) carica pacchetti e impostazioni tipografiche; `style/harmony-macros.sty` raccoglie le macro di notazione armonica. I file principali fanno `\documentclass{memoir}` seguito da `\input{preamble}`. Il contenuto reale vive in `manuscript/` (ignorato): `main.lytex` include i capitoli `chapters/*.lytex`, gli esempi `music/*.ly` e la bibliografia `bib/references.bib`. `sample/main.lytex` (pubblico) è un documento minimo che esercita l'intera catena per verificarla senza esporre contenuto. Gli script di build risolvono i percorsi via `TEXINPUTS`/`BIBINPUTS` impostati per includere `style/` e la cartella sorgente, e scelgono `manuscript/main.lytex` se presente, altrimenti `sample/main.lytex`.

## Gli strumenti sotto `tools/`

Sezione aggiunta il 2026-08-06 insieme a `tools/**` nelle `covers-paths`, che prima mancava: fino a quel giorno un cambiamento sotto `tools/` non veniva confrontato con questa scheda, quindi il drift sugli script era per costruzione invisibile a `sync-context` da questo lato. Al 2026-10-07 gli script sono diciassette, quindici Python, uno Node e uno PowerShell, più il `README.md` e un file di esclusioni della cartella; la descrizione sotto copre i flussi principali. La scheda `current-work.md` copriva `tools/**` dal 2026-08-03, ma descrive il lavoro in corso, non lo stack: il posto dove questi strumenti vanno descritti è qui.

Il criterio con cui questi strumenti esistono è quello di `.claude/rules/token-economy.md`, cioè spingere su codice deterministico tutto ciò che non richiede comprensione semantica, e quello di ADR-009 per i due che implementano affermazioni del libro: le definizioni che usano sono quelle del libro, non quelle scolastiche, e un cambio di definizione è un cambio di contenuto, non un refactor.

Due strumenti implementano il contenuto del libro invece di documentarlo, e sono registrati come fonti nel manifesto della skill `armonia-libro` proprio per questo. `tritoni-scale.py` calcola il contenuto di tritoni delle scale rappresentate come insiemi di classi di altezza modulo dodici, esamina la corrispondenza fra una scala e la sua coppia di tritoni, ed è lo strumento che ha smentito l'intuizione della corrispondenza biunivoca sostituendola con il risultato due a uno e i due teoremi. `derivazione-scale.py` implementa la macchina delle dominanti secondarie ai due livelli fissati dall'utente il 2026-08-03: il primo livello sono le scale ottenute alterando una sola nota rispetto alla tonalità diatonica di partenza, il secondo quelle ottenute applicando la stessa operazione a ciascuna scala di primo livello.

Due strumenti tengono in pari gli artefatti derivati. `skill-freshness.py` rileva la deriva fra una skill e le sue fonti ricalcolando gli sha256 registrati nel manifesto `.sources.json`, e porta il vincolo d'ordine che è costato un ciclo di deriva invisibile: `--update` riallinea gli hash senza toccare il contenuto, quindi si lancia solo dopo aver rigenerato la skill. `render-bib-registry.py` rigenera `_notes/book-bib-registry.md` dal JSON del registro, leggendo il titolo dal `.bib` reale quando la voce è già scritta e usando il nome del file sorgente come segnaposto quando non lo è.

Tre strumenti servono l'ingestione documentale e la disciplina bibliografica. `doc-ingest.py` converte un corpus di `.pdf`, `.docx`, `.pptx`, `.xlsx` e `.html` in una cache Markdown locale con manifest a content-hash per non riconvertire l'invariato, e rigenera l'`_INDEX.md` che è lo scheletro di Livello 1 della disclosure progressiva. `probe-pdf-text.py` fa il triage deterministico della qualità del testo estraibile da un PDF, perché né il conteggio dei caratteri né un campione dalle prime pagine bastano a decidere se un libro si può digerire, e sbagliano in direzioni opposte. `extract-titlepages.py` estrae come PNG le pagine di frontespizio e colophon per la verifica visiva richiesta da `book-bib-extract`, fissando DPI e numero di pagine che nelle sessioni manuali cambiavano ogni volta.

Due strumenti presidiano la convenzione della sorgente Markdown fissata in `.claude/rules/interaction-style.md` e il formato dei comandi di `git-commands-format.md`. `md-unwrap.py` srotola i paragrafi con a capo interni unendo i pezzi con un singolo spazio, e non normalizza nient'altro: marcatori di lista, tabelle, stili di titolo, escaping e ordine restano come sono; quando `markdown-it-py` è importabile ogni file passa da un oracolo di rendering che pretende un HTML normalizzato identico, e in caso di divergenza il file non viene scritto. `lint-md-commands.py` copre l'angolo che il primo per contratto non tocca, cioè il contenuto dei blocchi recintati: cerca i comandi non copiabili in una riga sola, cioè continuazioni di riga con backslash, backtick o caret, heredoc multi-riga e comandi git che proseguono sulla riga seguente, riconosce un blocco come shell dalla sua info string o dal contenuto quando l'info string manca, è in sola lettura ed esce con codice 1 se trova qualcosa, così si usa come gate.

Restano due strumenti di servizio. `render-diagrams.mjs` rende i diagrammi Mermaid di `.claude/context/diagrams/*.mmd` nei corrispondenti `.svg` riusando il browser Chromium-based di sistema senza scaricare il Chromium di Puppeteer. `latest-screenshot.ps1`, scritto il 2026-08-06, restituisce il percorso e l'età dell'immagine più recente nella cartella di cattura, ed è lo strumento che `.claude/rules/manual-screenshots.md` presuppone quando un passo dello sviluppo è visibile solo all'utente.

Nessuno di questi strumenti entra nella catena di build del libro: `scripts/build.{ps1,sh}` non li invoca, e il PDF si compila senza di essi. Vivono accanto al libro come strumenti di verifica e di manutenzione, e per questo sono tracciati mentre il contenuto che verificano non lo è.

`check-book.py`, aggiunto il 2026-10-07, controlla in sola lettura il grafo degli `\input`, le risorse bibliografiche, le citekey citate e gli eventuali capitoli non inclusi. Non interpreta l'intero linguaggio TeX e non sostituisce la build. Gli script di build passano ora esplicitamente `.latexmkrc` a `latexmk`, perché la compilazione dei `.lytex` avviene dalla directory `build/`, dalla quale la configurazione di radice non veniva caricata automaticamente. Il preambolo nasconde in stampa il campo `note` delle voci bibliografiche: contiene lo stato interno di verifica e non è testo per il lettore. Metadati necessari al riferimento editoriale vanno quindi nei campi bibliografici appropriati, non soltanto in `note`.

`audit-local-sources.py`, aggiunto nello stesso ciclo, cataloga senza modificarli i PDF, EPUB e DOCX di una radice esterna, associa i percorsi esatti a quelli del registro e confronta fotografie successive per trovare arrivi o cambiamenti. La prima fotografia del corpus J: è privata in `_notes/`; un percorso non registrato non è automaticamente una fonte nuova. `render-bib-registry.py` mostra ora il titolo già verificato nel JSON per una fonte candidata non ancora nel `.bib`, quando quel campo è disponibile.

Il programma di lettura completa usa tre strumenti di manutenzione aggiunti il 2026-10-08. `source-library.py` separa censimento, acquisizione tecnica per pagina e ledger autorato delle letture, conservando le attestazioni pregresse; l'estrazione nativa non prova lettura. `sync-book-bib.py` confronta proposte e bibliografia reale, importa soltanto anagrafiche verificate se la sessione lo autorizza, salva un backup e riconcilia i flag senza sovrascrivere voci esistenti. `fetch-source-files.py` acquisisce documenti accessibili con URL, data e hash, senza superare controlli di accesso. I dati reali e i digest stanno nel vault privato. Nessuno dei tre entra nella build LaTeX.

## Riferimenti a snippet

- `.latexmkrc` - engine LuaLaTeX e pulizia ausiliari.
- `style/preamble.tex` - pacchetti e tipografia.
- `style/harmony-macros.sty:\grado` - macro di notazione armonica.
- `style/harmony-macros.sty:apertura` - ambiente per il brano introduttivo in corsivo, rientrato e staccato dal resto (usato per l'introduzione/abstract del libro).
- `scripts/build.ps1` / `scripts/build.sh` - passata `lilypond-book` + `latexmk -lualatex`.
- `tex-packages.txt` - manifesto riproducibile dell'ambiente TeX.
- `tools/tritoni-scale.py` / `tools/derivazione-scale.py` - implementano affermazioni del libro (ADR-009).
- `tools/skill-freshness.py` - deriva fra skill e fonti; `--update` solo dopo la rigenerazione.
- `tools/latest-screenshot.ps1` - percorso ed età dell'ultimo screenshot, per `manual-screenshots.md`.
- Riferimenti esterni su LilyPond+LaTeX e autopubblicazione: vedi `README.md`, sezione "Risorse e riferimenti".

## Censimento completo e destinazioni dopo il riordino

`audit-local-sources.py --all-files` estende il censimento oltre PDF/EPUB/DOCX; l’uso senza il flag mantiene il perimetro precedente. `audit-reading-corpus.py --root <cartella> --name <nome>` censisce tutti i file in sola lettura, conserva hash, corrispondenze bibliografiche e metadati tecnici, estrae i DOCX in porzioni private e misura i media con ffprobe. Richiede Python e PyMuPDF per i PDF non già censiti; ffprobe è facoltativo, e se manca lo segnala. Non assegna livelli di lettura.

`source-library.py` usa `_notes/10-biblioteca/` e `_notes/99-cache/doc-ingest/source-library/`. Il registro centrale conserva il percorso `_notes/book-bib-registry.json`; `sync-book-bib.py` conserva i propri report nella biblioteca riorganizzata. `fetch-community.py` delega al lettore vendorizzato, mantenendolo intatto, e indirizza le nuove acquisizioni verso `_notes/20-ricerca/acquisizioni-community/`. `post` e `riprendi` mantengono i comandi del template; l’help e la destinazione sono verificati senza acquisizione di nuovi contenuti in questo giro.

Le procedure private attuali sono in `_notes/80-strumenti/`; gli script di lavorazioni precedenti sono archiviati e non vanno rieseguiti come aggiornamenti correnti. La procedura di snapshot esclude l’intera cache e i propri ZIP. La migrazione conserva hash, percorsi precedenti e copie delle note anteriori al riallineamento dei link; le validazioni distinguono file autoriali immutati da documentazione operativa aggiornata.
