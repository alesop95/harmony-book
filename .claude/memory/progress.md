# Work-log

> Append-only, in ordine cronologico inverso (la voce più recente in alto). Ogni passo
> significativo di codice e ogni intervento manuale rilevante lascia una voce con data, file
> toccati, motivo e commit di riferimento. Qui confluisce anche il log di riconciliazione dei
> documenti `.docx`, con il nome del documento sorgente e l'esito, così la data di allineamento
> sopravvive a un clone.

## 2026-07-17/20 — Ricerca sul tritono: fonte primaria registrata, ricognizione interna ed esterna concluse

Commit: nessuno (lavoro privato/ignorato, salvo l'entrata già coperta dalla voce del 2026-07-17
sotto per la parte di sync-context).
File toccati: `_notes/book-bib-registry.json` (nuova voce `manual-isbn-8869244857` per la fonte
primaria, poi corretta da citekey `gaetani2019` a `gaetani2022`), `_notes/book-bib-registry.md`
(rigenerata, 153 voci), `_notes/tritono-ricognizione-interna.md` (nuovo), `_notes/tritono-ricerca-esterna-stato.md`
(nuovo), `.claude/context/current-work.md` (sezione "Feature attiva" aggiornata).
Motivo: ripresa del filone 2 (tesi sul tritono) dopo il riavvio forzato che aveva interrotto la
sessione precedente; scope chiarito dall'utente il 2026-07-17 come "entrambe le vie" (ricognizione
interna + ricerca esterna).
Fonte primaria: l'utente ha fornito il link Amazon del libro annunciato come riferimento
"più importante di tutti", "La dialettica del tritono" di Mariano Gaetani (ISBN 8869244857).
Registrato nel registro bibliografico con `bib_status: da-verificare` (non è stato visto il
colophon fisico). Editore e anno aggiornati in corso di sessione da un primo indizio debole
(sintesi di ricerca web, "2019") a uno più solido (articolo del *Resto del Carlino* del
2022-07-26 su una presentazione pubblica del libro, "Editore: Edizioni Simple", anno 2022):
citekey corretto di conseguenza.
Ricognizione interna: scansione deterministica (`pdftotext` + ricerca per parola chiave) dei 29
libri del corpus `armonia-teoria`, poi lettura visiva mirata (`pdftoppm`, via 6 agenti paralleli
più due retry per errori transitori 529) dei 6 libri risultati scansioni senza testo nativo
(Piston *Harmony*, *Counterpoint*, *Orchestration*, *Armonia*-EDT; Schoenberg; Wyatt&Schroeder).
Trovamenti principali: sezione dedicata "The Tritone" con citazione diretta di "diabolus in musica"
in tre volumi di Piston; trattazione indiretta in Schoenberg tramite le "vagrant harmonies";
assente in Piston *Orchestration* (fuori tema) e in un gruppo di manuali minori/solfeggio. Un file
(`Pozzoli - Corso Facile Di Solfeggio.pdf`) non estraibile con `pdftotext`, non indagato oltre
(priorità bassa). Esito completo con citekey/pagina/citazione in `_notes/tritono-ricognizione-interna.md`.
Ricerca esterna: la skill `deep-research` (harness `Workflow`, verifica adversariale a 3 voti per
affermazione) è stata lanciata due volte sulla stessa domanda ed entrambe le volte ha esaurito il
limite di sessione nella fase di verifica (fino a ~130 chiamate per 41-43 affermazioni estratte),
senza mai completare la sintesi finale. Per chiudere lo step senza un terzo giro costoso, le
affermazioni più rilevanti rimaste in sospeso sono state verificate a mano con 3 chiamate `WebFetch`
mirate. Trovamento centrale, confermato con citazione diretta (Thomas Forest Kelly, Harvard): il
"divieto ecclesiastico medievale del tritono come diabolus in musica" è un mito storiografico
moderno; l'espressione risale a Fux (*Gradus ad Parnassum*, 1725, uso tecnico-pedagogico), poi
attribuita al medioevo nell'Ottocento (Ambros, 1880). Confermato anche il confronto strutturale
sesta-eccedente/sostituzione-di-tritono (Biamonte, *Music Theory Online* 14.2, 2008). Lezione
operativa per sessioni future: l'harness `deep-research` con molte affermazioni da verificare è
troppo costoso per un limite di sessione in un colpo solo; preferire una domanda più stretta per
lancio, oppure la verifica manuale mirata via `WebFetch` sulle sole fonti primarie già trovate,
oppure un resume mirato (`resumeFromRunId`) a inizio sessione quando il limite è fresco. Dettagli
completi, incluse le affermazioni confutate e quelle non ancora recuperabili (Babbitt 1960,
Vicentino 1555, bloccate da un 403 su ResearchGate), in `_notes/tritono-ricerca-esterna-stato.md`.
Fuori scope per ora: avvio della stesura vera e propria della sezione/capitolo sul tritono (in
attesa di decidere con l'utente se aspettare la fonte primaria fisica).

## 2026-07-17 — Riconciliazione del drift con sync-context, ripresa dopo riavvio forzato

Commit: `4942de1` (nuovo commit di riferimento delle schede)
File toccati: `.claude/context/STACK.md` (aggiunto riferimento all'ambiente `apertura` in
`style/harmony-macros.sty:73-76`, bump `last-verified-commit`), `.claude/context/design-and-security.md`
(solo bump `last-verified-commit`, contenuto già coerente), `.claude/context/current-work.md`
(solo bump `last-verified-commit`, ri-ancorata a un commit reale), `.claude/memory/index.md`
(tabella di stato aggiornata, nota drift chiusa).
Motivo: dopo un riavvio forzato del PC, ripresa di sessione secondo la procedura di
`CLAUDE.md`. Il drift segnalato nella sessione precedente (quattro commit di template/skill mai
riconciliati) è stato chiuso lanciando `sync-context`: l'unico cambiamento sostanziale nelle aree
coperte dalle schede era l'ambiente `apertura` (introdotto in `f3a6c45`), ora documentato; i
diagrammi di `design-and-security.md` erano già corretti nel contenuto. `deployment.md`,
`dev-testing.md` e `roadmap.md` non hanno `covers-paths` popolati e restano esclusi dal confronto,
senza modifiche.
Prossimo passo, per richiesta esplicita dell'utente: procedere sul filone 2 (ricerca bibliografica
per la tesi sul tritono), scope chiarito come ricognizione interna + ricerca esterna, con la fonte
primaria "La dialettica del tritono" (ISBN 8869244857) identificata ma non ancora consegnata.

## 2026-07-16 — Chiusura del lotto di ingestione libri interrotto, bibliografia consolidata

Commit: (pendente; i file toccati sono privati/ignorati salvo i tre script sotto `tools/` e la
skill `.claude/skills/book-bib-extract/`, che sono nuovi e non ancora tracciati)
File toccati: `tools/render-bib-registry.py` (nuovo, rigenera `_notes/book-bib-registry.md` dal
JSON in modo deterministico), `tools/extract-titlepages.py` (nuovo, estrazione standardizzata dei
frontespizi via `pdftoppm`/Poppler con DPI e range pagine fissi, sostituisce comandi ad-hoc mai
salvati nella sessione precedente), `_notes/book-bib-registry.json` e `manuscript/bib/references.bib`
(privati, ignorati).
Motivo: una sessione precedente (vedi voce retroattiva sotto) si era interrotta per esaurimento
token durante l'ingestione di libri di chitarra/armonia in bibliografia, lasciando un lotto a
metà (corpus `chitarra-books-folders`, 16 file di frontespizio senza voci di registro) e due gap
strutturali (tabella `.md` del registro mai rigenerata; meccanismo di generazione PNG dei
frontespizi non tracciato). Questa sessione ha chiuso il lotto interrotto (15 libri distinti,
`fabbri4` era una quarta pagina dello stesso libro `fabbri`, non un sedicesimo libro), poi ha
esteso il controllo del colophon a un lotto ampio delle voci `da-verificare` preesistenti tramite
agenti paralleli (istruzione esplicita dell'utente per quel giro) più un piccolo lotto manuale di
verifica.
Esito bibliografia: `manuscript/bib/references.bib` passato da 58 a 83 voci `@book` (integrità
verificata: parentesi bilanciate, nessuna citekey duplicata). Registro `_notes/book-bib-registry.json`
a 152 voci totali: 86 verificate, 58 da-verificare (ciascuna con nota che documenta perché l'anno
manca — difetto di scansione o colophon genuinamente assente — per non ripetere il lavoro a vuoto
in una sessione futura), 8 scartate (inclusa una voce riclassificata da "da-verificare" a
"scartata" perché non è un libro, solo un estratto di rivista di 4 pagine).
Pulizia: rimossi due PDF di lavoro dimenticati (~40 MB) da `_notes/.tmp-doc-cache/`.
Fuori scope, per decisione esplicita dell'utente: le 58 voci rimaste senza colophon (limite
pratico raggiunto per questa via) e la fase `book-digest` (libro -> skill), mai iniziata — tutte
le 152 voci hanno ancora `skill_status: pending`.

## 2026-07-15/16 — Avvio dell'ingestione libri e della bibliografia (voce retroattiva, ricostruita)

Commit: nessuno (lavoro mai committato, file coinvolti privati/ignorati o non ancora tracciati)
File toccati: `tools/doc-ingest.py` (istanziato dal template), `.claude/skills/book-bib-extract/SKILL.md`
(istanziata), `_notes/book-bib-registry.json`, `manuscript/bib/references.bib`,
`_notes/.tmp-doc-cache/**` (cache di lavoro, PNG di frontespizio e mirror Markdown).
Motivo: NON verificabile con certezza dai soli file su disco, perché questa sessione non ha
lasciato una voce di log né un `RESUME-PROMPT.md` aggiornato prima di interrompersi per
esaurimento token — questa voce è ricostruita da un'esplorazione dei file `_notes/` e delle
timestamp all'inizio della sessione del 2026-07-16 (vedi sopra), non da un resoconto diretto.
Nella sessione (o sessioni) del 15-16 luglio è stata popolata la bibliografia di tre corpus di
libri posseduti (`armonia-teoria`, `chitarra-books-root`, `chitarra-libri-gianluca`), arrivando a
137 voci nel registro prima dell'interruzione (60 verificate, 71 da-verificare, 6 scartate), con
58 voci `@book` reali già scritte in `manuscript/bib/references.bib`. Il lavoro di verifica
bibliografica è stato condotto leggendo pagine di frontespizio renderizzate come PNG (non il
mirror Markdown di `doc-ingest.py`, che per questi PDF scansionati risulta vuoto senza OCR), con
un meccanismo di generazione PNG mai salvato su disco come script.

## 2026-06-16 — Stesura dell'introduzione del libro (da INTRO.docx)

Commit: (pendente; il contenuto NON entra in git)
File toccati (privati, ignorati): `manuscript/chapters/00-introduzione.lytex`.
Motivo: l'utente ha fornito `_notes/INTRO.docx` come introduzione/abstract del libro. Ingestione con
la strategia della sezione 5 (estrazione in `_notes/.tmp-docx-intro/`, lettura mirata) e trascrizione
fedele nel capitolo di introduzione, senza inventare. Compilazione verificata: `build/main.pdf`
(~41 KB), zero glyph mancanti (caratteri tipografici Unicode resi da Libertinus via LuaLaTeX).
Riconciliazione documento sorgente: `_notes/INTRO.docx` (privato), esito = introduzione stesa.

## 2026-06-16 — Pulizia handoff, strumento diagrammi e diagrammi di flusso

Commit: (pendente, da committare)
File toccati: rimossa `transform-into-claude-md/` (handoff, era ignorata) dopo aver travasato i
riferimenti pubblici in `README.md` (sezione "Risorse e riferimenti") e quelli personali in
`_notes/RESOCONTO.md`; `STACK.md` (riferimento esterno aggiornato); `tools/render-diagrams.mjs` e
`tools/README.md` istanziati dal bundle; tre diagrammi Mermaid in `.claude/context/diagrams/`
(`flusso-scrittura`, `struttura-progetto`, `pipeline-build`) come `.mmd` + `.svg`; `README.md`
(sezione "Diagrammi del flusso di lavoro"); `design-and-security.md` (tabella diagrammi registrata,
`covers-paths` su `.claude/context/diagrams/**`).
Motivo: pulizia post-decisione e documentazione visuale dell'uso del progetto. SVG generati con
`node tools/render-diagrams.mjs` (Edge di sistema, nessun Chromium scaricato).

## 2026-06-16 — Ancoraggio al primo commit (sync-context)

Commit: 017b02a
File toccati: frontmatter di tutte le schede `context/*.md`, `memory/index.md`, work-log.
Motivo: eseguito il primo ancoraggio dopo il primo commit reale dell'utente. Sostituito il
segnaposto `PENDING-FIRST-COMMIT` con l'hash di HEAD (`017b02a`) in `generated-from-commit` e
`last-verified-commit` di STACK/current-work/roadmap/deployment/design-and-security/dev-testing e
nel commit di riferimento di `memory/index.md`. Le menzioni descrittive del segnaposto in
`PROJECT-SYSTEM.md`, nelle skill, nei template e negli ADR restano invariate (storico). Da qui il
drift si gestisce normalmente con `sync-context`.

## 2026-06-16 — Ambiente installato e catena di build verificata

Commit: 017b02a
File toccati: `tex-packages.txt`, `.latexmkrc`, `scripts/setup-tex.ps1`, `scripts/build.ps1`,
`scripts/build.sh`, `manuscript/main.lytex` (ignorato).
Motivo: reso operativo lo stack di ADR-003. TinyTeX, `lualatex` e `latexmk` erano gia' presenti;
`scripts/setup-tex.ps1` ha installato i pacchetti del manifesto. LilyPond e' stato installato
manualmente dall'utente sotto `C:\Program Files\lilypond-2.26.0-mingw-x86_64\...\bin`; gli script lo
rilevano li' (o via `LILYPOND_BIN`) senza percorsi hardcoded di macchina.
Correzioni emerse dalla verifica, ora parte del progetto:
- Manifesto: `tabularx` -> `tools`, rimosso `graphicx` (coperto da `graphics`), aggiunti `xpatch`
  (dipendenza di memoir) e `makeindex` (binario non incluso nel TinyTeX minimale).
- `build.ps1`: su Windows `lilypond-book` e' un `.py`; invocato esplicitamente col `python.exe`
  incluso in LilyPond, mai via associazione di sistema del `.py` (che su questa macchina puntava a
  un'app Electron). `BIBINPUTS` include anche la cartella sorgente.
- `.latexmkrc`: aggiunto il supporto `glossaries` (cus_dep `makeglossaries`); l'indice via
  `makeindex` e' nativo di latexmk.
Esito verifica (test manuale, vedi `_notes/TEST-CHECKLIST.md`): `scripts/build.ps1 -Main
sample\main.lytex` produce `build/main.pdf` (catena lilypond-book -> LuaLaTeX -> biber -> makeindex,
~40 KB, con esempi musicali); il build di default sullo scheletro `manuscript/` produce un PDF
pulito (~10 KB). Lo scheletro del manoscritto e' stato reso minimo: glossario/indice/bibliografia e
`\include` dei capitoli restano come blocchi commentati da attivare quando esistono voci reali,
perche' attivati a vuoto mandavano latexmk in stallo.

## 2026-06-16 — Decisione dello stack, privacy del contenuto e attivazione del pacchetto LaTeX

Commit: 017b02a
File toccati: `STACK.md`, `current-work.md`, `roadmap.md`, `decisions.md` (ADR-003, ADR-004),
`.latexmkrc`, `tex-packages.txt`, `scripts/{setup-tex,build}.{ps1,sh}`,
`.claude/skills/latex-build/SKILL.md`, `style/{preamble.tex,harmony-macros.sty}`,
`sample/`, `manuscript/` (ignorata), `README.md`, `.gitattributes`, `.gitignore`.
Motivo: ingestione dell'handoff `transform-into-claude-md/` (sezione 5: estrazione del `.docx` in
`_notes/.tmp-docx-devbook/`, lettura mirata) e decisione condivisa con l'utente. Stack: LaTeX-nativo
LuaLaTeX + memoir + LilyPond via lilypond-book (ADR-003), pacchetto LaTeX del bundle istanziato e
adattato (engine lualatex, passata lilypond-book, sorgente manuscript/ con fallback sample/).
Privacy: split tooling pubblico / `manuscript/` privata ignorata, backup SSD, promovibile a repo
privato (ADR-004). Schede STACK/current-work/roadmap popolate. Ambiente non ancora installato e
catena non ancora compilata (richiede TinyTeX + LilyPond): e' la Definition of Done corrente.
Riconciliazione handoff: documento sorgente `transform-into-claude-md/devBook settings.docx`, esito
= stack fissato (ADR-003/004). Cartella handoff ignorata, non committata.

## 2026-06-15 — Inizializzazione del sistema di progetto

Commit: 017b02a
File toccati: anatomia di `.claude` (settings.json, memory/, context/, rules/, skills/, templates/),
`CLAUDE.md`, `CLAUDE.local.md`, `.gitignore`, `_notes/`.
Motivo: installazione del sistema portabile di contesto, documentazione e version control descritto
in `.claude/PROJECT-SYSTEM.md`, eseguita in modalità greenfield. Repo git inizializzato su branch
`main` con identità locale `alesop95 <alessio.sopranzi.95@gmail.com>` e remoto
`git@github-personal:alesop95/harmony-book.git` (vedi `.claude/rules/git-identity-and-repo.md`).
Protezione globale `user.useConfigOnly` già attiva sulla macchina, non modificata. Schede di
`context/` create con sola struttura e frontmatter (segnaposto `PENDING-FIRST-COMMIT`), da popolare
nelle sessioni successive senza inventare contenuto.

Decisioni di processo registrate in questa sessione:
- Stack non ancora deciso: la lettura di `transform-into-claude-md/` (handoff ignorato) e la scelta
  dello stack per il libro di armonia sono rimandate alla sessione ripresa, da svolgere insieme
  all'utente. Vedi `_notes/RESUME-PROMPT.md`.
- MCP non configurato: nessun `.mcp.json` né cartella `mcp/`. Resta istanziabile in seguito dal
  template `.claude/templates/mcp.json` rieseguendo il passo MCP della skill `init-project-system`.
- Pacchetto LaTeX non ancora attivato: resta istanziabile da `.claude/templates/latex/` quando lo
  stack lo confermerà.
