---
generated-from-commit: 017b02a
generated-from-branch: main
generated-date: 2026-06-15
covers-paths:
  - scripts/**
  - style/**
  - sample/**
  - tools/**
  - .claude/skills/**
last-verified-commit: dd1c4d5
stato: in corso
---

# Lavoro in corso

> La fonte di verità su cosa è fatto resta `memory/index.md` e il work-log, non le spunte di
> questo file.

## Feature precedente (sostanzialmente conclusa): Bootstrap dell'ambiente e verifica della catena di build

Cosa faceva: rendere operativo lo stack deciso (ADR-003) installando l'ambiente e verificando che
la catena `lilypond-book` -> LuaLaTeX produca un PDF, prima di entrare nella stesura vera.

Definition of done:

- [x] Installato l'ambiente: `scripts/setup-tex.ps1` (TinyTeX + pacchetti) e LilyPond sotto Program Files
- [x] `scripts/build.ps1` compila `sample/main.lytex` -> `build/main.pdf` senza errori
- [x] Verificata la resa di un esempio LilyPond e della microtipografia nel PDF (sample ~40 KB)
- [x] Avviata la stesura: introduzione del libro stesa da `_notes/INTRO.docx`; struttura modulare attiva
- [ ] Primo commit eseguito dall'utente e `sync-context` lanciata per ancorare i `017b02a` (ancora
      pendente; nel frattempo l'HEAD reale e' avanzato di altri 4 commit non di stesura, vedi
      `memory/index.md`, nota drift)

Nota: la catena di build e' verificata su Windows. La parita' su Linux (`scripts/*.sh`) e'
implementata ma non ancora collaudata su una macchina Linux. Font definitivo (Libertinus) e stile
bibliografico (`authoryear`) restano da confermare alla prova del PDF con contenuto reale.

## Feature attiva: Bibliografia del libro e ricerca per la nuova tesi sul tritono

Cosa fa: due filoni distinti, entrambi avviati il 2026-07-16 su richiesta esplicita dell'utente.

**Filone 1, bibliografia da libri posseduti — sostanzialmente concluso**: `doc-ingest` +
`book-bib-extract` (entrambi in `tools/` e `.claude/skills/`, non ancora tracciati in git) hanno
popolato `manuscript/bib/references.bib` (83 voci `@book`) e il registro
`_notes/book-bib-registry.json` (152 voci: 86 verificate, 58 da-verificare con nota che documenta
il limite pratico raggiunto per ciascuna, 8 scartate). Dettagli completi in `memory/progress.md`
(voci del 2026-07-16) e ADR-005 in `memory/decisions.md`. Resta fuori scope la fase
`book-digest` (libro -> skill), mai iniziata.

**Filone 2, ricerca per la nuova tesi sul tritono — ricerca conclusa, in attesa della fonte primaria fisica**:
lo scope, chiarito dall'utente il 2026-07-17, era entrambe le vie: ricognizione sui libri già
posseduti e ricerca accademica esterna. Entrambe sono state condotte e fissate in note private:

- Ricognizione interna (29 libri del corpus `armonia-teoria`): scansione deterministica con
  `pdftotext` + lettura visiva mirata (via `pdftoppm`) dei 6 libri risultati scansioni senza testo
  nativo. Risultato in `_notes/tritono-ricognizione-interna.md`: trattazione storico-dialettica
  solida in Piston (*Harmony*, *Counterpoint*, *Armonia*-EDT, tutti con citazione diretta di
  "diabolus in musica") e trattazione indiretta in Schoenberg (*Structural Functions of Harmony*,
  via le "vagrant harmonies"); trattazione solo funzionale/jazz in Kostka, Levine, Berkman,
  Mulholland, Blatter, Beato, Wyatt&Schroeder; assente in Piston *Orchestration* e in un gruppo di
  manuali minori.
- Ricerca esterna (skill `deep-research`, poi verifica manuale mirata via `WebFetch` per
  contenere il costo dopo due rate-limit consecutivi dell'harness): risultato in
  `_notes/tritono-ricerca-esterna-stato.md`. Trovamento centrale: il "divieto ecclesiastico
  medievale del tritono come diabolus in musica" è un mito storiografico moderno, non un fatto
  medievale — l'espressione risale a Fux, *Gradus ad Parnassum* (1725), uso tecnico-pedagogico,
  poi retroattivamente attribuita al medioevo nell'Ottocento (Ambros, 1880); confermato con
  citazione diretta dal musicologo di Harvard Thomas Forest Kelly. Anche il confronto strutturale
  sesta-eccedente/sostituzione-di-tritono (Biamonte, *Music Theory Online* 14.2, 2008) è
  confermato con citazione diretta. Restano due dettagli minori non recuperati (Babbitt 1960,
  Vicentino 1555: fonte ResearchGate bloccata da un HTTP 403), a bassa priorità.

La fonte primaria del libro, "La dialettica del tritono" di Mariano Gaetani, è stata identificata
(ISBN 8869244857, editore probabile Edizioni Simple, anno probabile 2022 secondo un articolo del
*Resto del Carlino* su una presentazione pubblica — non ancora il colophon) e registrata in
`_notes/book-bib-registry.json` (voce `manual-isbn-8869244857`, citekey `gaetani2022`,
`bib_status: da-verificare`). L'utente non ha ancora consegnato il contenuto/appunti cartacei
annunciati: nessun contenuto su questa fonte è stato inventato, resta da trattare quando arriva.

File coinvolti finora (privati/ignorati, tranne i tre script e la skill):

```
tools/doc-ingest.py                          script di ingestione (istanziato da template)
tools/extract-titlepages.py                  estrazione standardizzata frontespizi (Poppler)
tools/render-bib-registry.py                 rigenera book-bib-registry.md dal JSON
.claude/skills/book-bib-extract/SKILL.md     skill di estrazione bibliografica (istanziata da template)
_notes/book-bib-registry.json                registro di stato (privato, 153 voci)
_notes/book-bib-registry.md                  tabella leggibile rigenerata dal registro (privato)
_notes/tritono-ricognizione-interna.md       nuovo, esito ricognizione sui libri posseduti (privato)
_notes/tritono-ricerca-esterna-stato.md      nuovo, esito ricerca esterna + lezione di costo (privato)
manuscript/bib/references.bib                bibliografia reale del libro (privato)
```

Domande aperte:

Se aggiornare la sezione "Precondizione" di `book-bib-extract/SKILL.md` per riflettere il metodo
di verifica visiva del colophon invece del mirror Markdown (ADR-005) — segnalato all'utente, non
ancora deciso. Se e quando riprendere le 58 voci `da-verificare` residue del filone 1 (limite
pratico raggiunto, non priorità immediata). Se e quando recuperare i due dettagli minori bloccati
su ResearchGate (Babbitt, Vicentino). Quando iniziare a scrivere la sezione/capitolo del libro sul
tritono: in attesa della fonte primaria fisica (Gaetani) o già con il materiale raccolto finora —
non ancora deciso con l'utente.

## Feature attiva aggiunta il 2026-07-24: stesura del capitolo sul tritono in prosa continua

Su richiesta dell'utente il capitolo sul tritono è stato riscritto dal formato report (indice più
otto punti numerati) al formato capitolo di libro continuo, senza sottotitoli, con voce "Marcato"
che rompe la quarta parete (lettore interpellato con "voi", confessione dell'autore-ingegnere) e con
l'ambizione dichiarata di costruire un impianto universale per leggere tutta l'armonia occidentale a
partire dal tritono. Bozza completa e validata movimento per movimento (arco A-I) in
`_notes/appunti-da-inserire-nel-libro/capitolo-tritono-continuo.md`. Il `.docx` sorgente resta
intatto come backup del report. Il 2026-07-24 il `.docx` continuo è stato assemblato con uno script
deterministico (`capitolo-tritono-continuo.docx`: prosa continua A-I, sei figure riusate ai segnaposto,
riferimenti [1]-[10] con la nuova voce web Springsteen verificata via oEmbed), e le sei figure sono state
rirenderizzate con le annotazioni in font Libertinus Sans (Emmentaler invariato per le note; sorgenti
`.ly` durevoli in `_notes/appunti-da-inserire-nel-libro/_ly-figure/`). Prossimo passo: trascrizione
fedele in `manuscript/chapters/NN-...lytex` con `\input` in `main.lytex` e build, quando l'utente dà il
via; resta in standby l'apertura biografica (Gaetani). Il quadro completo (voce, correzioni, direzioni
future, risorse pending) è in `_notes/RESUME-PROMPT.md`; i dettagli di tracciamento nelle voci del
2026-07-24 di `_notes/tracciamento-fonti-libro.md`; la risoluzione teorica frigio e le direzioni future
nella `_notes/cassaforte-capitolo-tritono.md`.

## Feature attiva aggiunta il 2026-07-29: la fase "libro -> skill", entrambe le accezioni

Su richiesta esplicita dell'utente si è affrontata la fase mai avviata "libro -> skill", che nel
progetto aveva due letture possibili. L'utente le ha volute entrambe, in quest'ordine, con un
obiettivo dichiarato oltre alla stesura: usare le skill risultanti anche per cercare fonti nuove
fuori dai libri posseduti, su forum, community, video e pareri di esperti. L'ordine non è arbitrario,
perché la dottrina del proprio libro definisce cosa cercare e rende mirata la seconda fase.

Prima accezione, conclusa: `.claude/skills/armonia-libro/`, il digest della dottrina del libro
dell'utente. Contiene `SKILL.md`, `tesi.md` (tritono identificatore, doppia eredità, lettura del
frigio, e le tre affermazioni dichiarate come intuizione e non teorema), `voce.md` (prosa continua,
voce Marcato, vincoli di stile e di intervento, flusso a quattro passi), `capitoli/01-tritono.md`
(arco A-I movimento per movimento), `fatti-verificati.md` (distingue confermato con citazione
diretta, confermato per voto, confutato e da non usare), `fonti.md` (mappa citekey e le due anomalie
da risolvere alla trascrizione in LaTeX) e `agenda-ricerca.md`.

Due anomalie bibliografiche emerse costruendo la skill e da risolvere prima della trascrizione in
LaTeX. Il riferimento [8] del capitolo continuo copre due fonti Sarti distinte, le slide
`sarti2018tonal` e la trascrizione della lezione CMRM2018, che non ha una voce propria nel registro:
in numerazione IEEE passa, con `biblatex` no. Il riferimento [10], la video-intervista di
Springsteen, non ha ancora voce né nel registro né nel `.bib`.

Seconda accezione, avviata con un pilota: installata la skill `book-digest` dal template, scritto
`tools/probe-pdf-text.py` e prodotta la triage dei 30 PDF di `ARMONIA E TEORIA` in
`_notes/corpus-digest-triage.md`. Digerito il primo libro, Berkman 2013, in
`.claude/skills/libro-berkman/`; la sua voce di registro è passata a `skill_status: done`. Restano
153 voci `pending`.

Decisione strutturale: ADR-007. Dentro `.claude/skills/` convivono tre classi, le skill di tooling
tracciate, `armonia-libro/` ignorata e `libro-*/` ignorate da glob, perché la dottrina è contenuto
del libro (ADR-004) e i digest sono materiale derivato da opere protette. Conseguenza operativa: le
due cartelle non hanno remoto git e vanno incluse nel backup su SSD portatile già in uso per
`manuscript/`.

Rilievo metodologico da conservare, perché correggeva un'ipotesi sbagliata: la qualità del testo
estraibile da un PDF non si misura né dal conteggio di caratteri né su un campione delle prime
pagine. I frontespizi sono tipografia decorativa che l'OCR rende male anche su volumi puliti, e
`Jazz Theory (1995, M.Levine).pdf` ne è il caso concreto, illeggibile in testa e integro a metà
volume. Lo strumento campiona quindi a metà libro e affianca all'indice di qualità la densità di
caratteri per pagina, che separa i libri di prosa da quelli di sola notazione.

Costo misurato del pilota, che serve a dimensionare il lotto successivo: 448 KB di testo, circa 112
mila token di sola lettura, per un libro di 215 pagine, con un digest risultante di 96 KB.

Domande aperte di questa feature. Quali libri digerire nel prossimo lotto, dato che la selezione per
rilevanza conta più della disponibilità: i candidati con testo pulito e alta rilevanza sono
Mulholland 2013, Blatter, Berklee Jazz Composition, Kostka e Levine 1995. Se e quando affrontare i
libri scansionati ad alta rilevanza, cioè i Piston e Schoenberg, che restano sulla via visiva mirata
di ADR-006 o richiedono una copia migliore del PDF, che l'utente si è offerto di procurare. Se
estendere il lavoro al corpus `CHITARRA`, 169 PDF, che è una decisione separata.

## Feature attiva aggiornata il 2026-08-03: maturazione del capitolo sul tritono

Il ciclo dal 2026-07-29 al 2026-08-03 ha portato il capitolo sul tritono da bozza validata a bozza
matura, e ha costruito attorno ad esso l'infrastruttura che serviva. Il quadro completo, con la guida
alla rilettura e l'elenco dei paragrafi cambiati, e in `_notes/STATO-CAPITOLO-TRITONO.md`; la storia
in `_notes/RESUME-PROMPT.md`, nota del 2026-08-03.

Il capitolo. Nove movimenti, 48314 caratteri, 90 paragrafi nel docx, sei figure, tredici riferimenti.
Markdown e docx allineati, con otto backup datati in `_backup/`. Proporzioni: i movimenti D ed E, che
sono il nucleo originale dell'autore, valgono il 38,9 per cento contro il 25 del 2026-07-31; il
movimento G, storico, e scesa al 13,3. Il movimento E, al 22 per cento, e ormai il piu lungo di
parecchio, e se crescera ancora conviene valutare se spezzarlo.

Che cosa e entrato nel capitolo, tutto su validazione esplicita dell'utente: Yavorsky nel movimento C,
che estende il precedente storico a una genealogia Choron-Fetis-Yavorsky; la dichiarazione al lettore
su dove l'autore ha compagnia e dove e solo, in apertura di D; la catena di quinte come chiave di
lettura e la tabella a sei operazioni in D, con la comparsa della napoletana; il test della doppia
eredita e il contatore dei tritoni in E; la testimonianza di Jacques de Liege sul semitritono nei
canti piani ecclesiastici in G, che porta quel movimento da un argomento per assenza a una
testimonianza contraria; e la chiusura sulle due dissonanze che fanno una consonanza.

L'infrastruttura. Tre skill nuove: `armonia-libro` e `libro-berkman`, ignorate da git per ADR-007
perche sono contenuto, e `fonte-nuova`, tracciata perche e procedura. Quattro strumenti Python
tracciati sotto `tools/`: `skill-freshness.py`, `probe-pdf-text.py`, `tritoni-scale.py`,
`derivazione-scale.py`. Due ADR nuovi: ADR-008 sui quattro livelli di verifica di una fonte, ADR-009
sugli strumenti che implementano il contenuto del libro e sul primato delle definizioni del libro.

La bibliografia. Da 91 a 101 voci in `manuscript/bib/references.bib`. Registro a 172 voci in
`_notes/book-bib-registry.json`, di cui 96 verificate. Tredici voci del corpus portano ora un campo
`skill_blocker` che dichiara perche non sono digeribili. Dieci PDF durevoli in `_notes/fonti-esterne/`.

Domande aperte di questa feature. Quando trascrivere il capitolo in `manuscript/chapters/`, che resta
il passo piu urgente. Se e come spezzare il movimento E. Quando aprire l'analisi del livello II della
macchina, calcolata e registrata nella voce 18 della cassaforte. Come sciogliere i due nodi
bibliografici prima di LaTeX, cioe il riferimento [8] su due fonti Sarti distinte e la fonte
Springsteen senza voce nel registro. E i sei ragionamenti ancora "da proporre" in
`_notes/ragionamenti-da-portare-nel-libro.md`.

In attesa dall'utente: il materiale privato sulla scala napoletana, annunciato e non consegnato, che
sblocchera l'espansione della tabella con armonizzazioni e riflessioni.

## Riconciliazione

Ultima verifica: 2026-08-03, ancorata a `dd1c4d5` a mano e non tramite `sync-context`. La quasi
totalita del lavoro di questo ciclo vive in file privati e ignorati, sotto `_notes/` e nelle due skill
di contenuto; la parte tracciata sono i quattro strumenti in `tools/`, la skill `fonte-nuova`, i due
ADR nuovi e queste schede. `covers-paths` e stata estesa a `tools/**` e `.claude/skills/**`, che prima
non erano coperte da nessuna scheda.
