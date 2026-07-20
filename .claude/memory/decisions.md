# Registro delle decisioni architetturali

> Convenzione ADR-lite, append-only. Ogni decisione architetturale non ovvia entra come voce
> numerata con data, stato, contesto, decisione, motivazione e conseguenze. Una decisione non si
> cancella e non si riscrive: quando viene superata, si aggiunge una nuova voce che dichiara di
> superare la precedente e ne cita il numero. Le inferenze non confermate si marcano come da
> verificare e si promuovono a decisione solo quando una fonte le conferma.

## ADR-001 — Adozione del sistema di progetto portabile

Data: 2026-06-15
Stato: accettata
Contesto: il progetto necessita di uno stato interamente recuperabile da un clone e di
documentazione che resti allineata al codice senza rilettura integrale a ogni sessione.
Decisione: adottare il sistema descritto in `.claude/PROJECT-SYSTEM.md`, con motore di
riconciliazione ancorato ai commit e doppio livello documentale tracciato/ignorato.
Motivazione: persistenza strutturale su disco indipendente dalla sessione di chat, e controllo
umano sul versionamento.
Conseguenze: ogni passo significativo aggiorna schede, `last-verified-commit`, snapshot e
work-log; commit e push restano manuali.

## ADR-002 — Scelta dello stack rimandata alla sessione ripresa

Data: 2026-06-15
Stato: accettata
Contesto: il progetto è un libro di armonia che deve essere portabile in scrittura sia su Windows 11
sia su Linux, dove il version control funge di fatto da stato di avanzamento del libro. Una ricerca
personale dello stack tecnico esiste già nella cartella ignorata `transform-into-claude-md/`, ma va
letta e discussa con l'utente prima di fissare la tecnologia, e la sessione corrente si chiude per
uno switch di account Claude.
Decisione: completare in questa sessione solo lo scaffold strutturale del sistema di progetto, e
rimandare alla sessione ripresa la lettura di `transform-into-claude-md/`, la decisione condivisa
dello stack (LaTeX e notazione musicale) e il conseguente popolamento delle schede.
Motivazione: non inventare contenuto in fase di init come prescrive `PROJECT-SYSTEM.md`, e non
perdere la discussione sullo stack alla chiusura della sessione per cambio account.
Conseguenze: le schede di `context/` restano col solo frontmatter ancorato a `PENDING-FIRST-COMMIT`;
il pacchetto LaTeX di `.claude/templates/latex/` resta da attivare; la guida operativa della ripresa
vive in `_notes/RESUME-PROMPT.md`.

## ADR-003 — Stack: LaTeX-nativo (LuaLaTeX + memoir + LilyPond via lilypond-book)

Data: 2026-06-15
Stato: accettata
Contesto: serve scrivere un libro di armonia di qualita' editoriale, portabile tra Windows 11 e
Linux, con esempi musicali e diff git puliti (il version control e' lo stato di avanzamento). La
ricerca in `transform-into-claude-md/devBook settings.docx` proponeva uno stack Quarto + Pandoc +
LuaLaTeX + LilyPond + Docker + GitHub Actions multi-formato.
Decisione: adottare un core LaTeX-nativo: engine LuaLaTeX (fissato in `.latexmkrc`), classe `memoir`,
font Libertinus via `fontspec`, `microtype` completo, `babel` italiano, `biblatex`+`biber`,
`imakeidx`, `glossaries`, `cleveref`, `tikz`/`pgfplots`; notazione musicale LilyPond integrata via il
preprocessore `lilypond-book`. Ambiente riproducibile TinyTeX user-local + manifesto
`tex-packages.txt` + `latexmk`, con script `.ps1`/`.sh` e la skill `latex-build`.
Motivazione: massimo controllo tipografico e diff testuali puliti, portabilita' senza Docker,
coerenza con la filosofia del sistema (partire minimale). Quarto/HTML/EPUB/interattivita' e
Docker/CI sono rimandati a Fase 2 e Fase 3, innestabili senza rilavoro perche' le sorgenti
LaTeX+LilyPond si riusano.
Conseguenze: il pacchetto LaTeX del bundle e' stato istanziato e adattato (engine LuaLaTeX, passata
`lilypond-book`, sorgente da `manuscript/` con fallback `sample/`). LilyPond resta un binario esterno
da installare a parte. La scheda `STACK.md` e' popolata.

## ADR-004 — Privacy del contenuto: split tooling pubblico / manoscritto privato

Data: 2026-06-15
Stato: accettata
Contesto: il contenuto del libro non deve mai essere visibile su una repo pubblica, altrimenti se ne
comprometterebbe la vendita; al tempo stesso si vuole che il version control rifletta l'avanzamento.
Decisione: separare nettamente tooling/struttura da contenuto. Il repository pubblico
`alesop95/harmony-book` traccia solo metodo e struttura (`.claude/`, `style/`, `scripts/`, `sample/`,
manifesti, configurazioni); il contenuto vendibile vive in `manuscript/`, ignorata da git. Per ora i
capitoli restano locali e il backup avviene per copia da SSD a SSD portatile, non via remoto git.
`manuscript/` e' un sottoalbero autonomo: in futuro vi si potra' fare `git init` con un remoto
privato (Opzione 2 piena) senza ristrutturare. Forzato LF via `.gitattributes` per coerenza
Windows/Linux.
Motivazione: garantire che la prosa non sia mai pubblica, conservando un version control pubblico
dell'avanzamento di struttura e metodo.
Conseguenze: `.gitignore` esclude `manuscript/` e `build/`; il repository pubblico non compila il
libro reale (compila `sample/`), il libro reale si compila in locale dove `manuscript/` esiste. La
storia git della prosa, finche' resta locale, dipende dal backup SSD dell'utente.

## ADR-005 — Bibliografia da libri scansionati: verifica visiva del colophon, non OCR/mirror Markdown

Data: 2026-07-16 (decisione emersa nella pratica il 2026-07-15, formalizzata qui il 2026-07-16)
Stato: accettata
Contesto: il pacchetto `doc-ingest` (via `markitdown`) produce un mirror Markdown testuale di ogni
PDF ingerito, ed è il percorso che la skill `book-bib-extract/SKILL.md` dichiara come precondizione
("legge il mirror Markdown già in cache"). In pratica, la maggior parte dei libri di chitarra/armonia
posseduti dall'utente sono PDF scansionati senza livello di testo nativo: l'unico run reale di
`doc-ingest.py` su un campione (5 PDF Piston) ha prodotto mirror Markdown a 0 parole, perché il ramo
OCR (`pytesseract`+`pdf2image`) non era stato attivato.
Decisione: per l'estrazione bibliografica di libri scansionati, il percorso effettivo è l'estrazione
di un piccolo numero di pagine di frontespizio/colophon come immagini PNG (via `pdftoppm`/Poppler,
ora standardizzata in `tools/extract-titlepages.py` con DPI e range pagine fissi), lette
visivamente pagina per pagina. Il mirror Markdown di `doc-ingest.py` resta il percorso valido solo
per PDF con testo nativo estraibile.
Motivazione: l'OCR testuale su scansioni di libri didattici di chitarra (spesso fotocopie di bassa
qualità) è inaffidabile o assente nel pacchetto attuale; la lettura visiva diretta della pagina è più
economica in token (poche pagine mirate, mai il libro intero) e più affidabile per dati strutturati
come anno/editore/ISBN, che vanno citati esattamente o dichiarati assenti, mai dedotti da OCR
rumoroso.
Conseguenze: `book-bib-extract/SKILL.md` descrive ancora la precondizione originaria (mirror
Markdown); resta da aggiornare la sua sezione "Precondizione" per riflettere questa prassi, cosa
segnalata ma non ancora eseguita per non modificare un pacchetto condiviso senza conferma esplicita.
Per un buon numero di libri (soprattutto europei/didattici classici, o copie con difetti di
scansione che omettono la pagina di copyright) anche il controllo esteso a 6-15 pagine non trova
alcun anno: sono casi di limite pratico del metodo, non di ricerca insufficiente, e restano
`da-verificare` a tempo indeterminato salvo accesso alla copia fisica.

## ADR-006 — Ricerca di contenuto nei libri scansionati: estrazione testuale prima, lettura visiva mirata solo sui match

Data: 2026-07-20
Stato: accettata
Contesto: ADR-005 aveva fissato il metodo per l'estrazione bibliografica (colophon) da libri
scansionati senza OCR affidabile: lettura visiva delle sole pagine di frontespizio. La ricerca sul
tritono nel filone 2 ha posto un problema affine ma diverso: non estrarre un'anagrafica da poche
pagine fisse, ma trovare in quali punti di un corpo di 29 libri, spesso di centinaia di pagine,
compaia un argomento specifico, senza aprire ogni libro pagina per pagina.
Decisione: per la ricerca di contenuto (non di anagrafica) nei libri già ingeriti, il primo passo è
sempre un'estrazione testuale deterministica con `pdftotext` (Poppler, già in uso) e una ricerca
per parola chiave con numero di pagina ricavato dai salti di modulo; la lettura visiva pagina per
pagina (`pdftoppm`, come in ADR-005) si riserva solo ai file dove questa estrazione risulta vuota
(scansione senza testo nativo) o insufficiente, e anche in quel caso solo sulle pagine dell'indice
analitico e quelle effettivamente segnalate come pertinenti, mai sul libro intero.
Motivazione: coerenza con il principio deterministico-prima-del-linguistico di
`token-economy.md`: `pdftotext` costa CPU locale e nessun token, e su un corpus di 27 file distinti
ha risolto in pochi secondi la maggioranza dei casi (i libri con testo nativo), lasciando la lettura
visiva, più costosa, a un sottoinsieme piccolo e noto in anticipo (6 libri su 29 nel caso concreto).
Conseguenze: il metodo è riusabile per qualunque ricerca di contenuto futura sullo stesso corpus
(`_notes/book-bib-registry.json`), non solo per il tritono. Non sostituisce ADR-005 per l'anagrafica
bibliografica, che resta sul solo colophon; i due metodi coesistono per scopi diversi sullo stesso
insieme di file.

<!-- ADR-007 — <titolo>
Data: <YYYY-MM-DD>
Stato: <proposta / accettata / superata da ADR-NNN>
Contesto: ...
Decisione: ...
Motivazione: ...
Conseguenze: ... -->
