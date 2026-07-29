# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di
> riferimento e mappa ogni scheda al suo stato di verifica. È la fonte di verità su cosa è fatto,
> non le spunte del diario.

## Stato

```
Branch attivo:        main
Commit di riferimento: 4942de1 (schede riconciliate con sync-context il 2026-07-17)
Data snapshot:        2026-07-17
```

## Stato di verifica delle schede

| Scheda | last-verified | Stato |
|---|---|---|
| STACK.md | 4942de1 | aggiornata (aggiunto riferimento all'ambiente `apertura` in `harmony-macros.sty`) |
| design-and-security.md | 4942de1 | diagrammi registrati e riconciliati; paradigmi da popolare |
| deployment.md | 017b02a | da popolare (covers-paths vuoto, nessun confronto di drift applicabile) |
| dev-testing.md | 017b02a | da popolare (covers-paths vuoto, nessun confronto di drift applicabile) |
| current-work.md | 4942de1 | aggiornata e ri-ancorata a un commit reale |
| roadmap.md | 017b02a | aggiornata (covers-paths vuoto, nessun confronto di drift applicabile) |

**Drift chiuso il 2026-07-17**: i quattro commit intercorsi (`f3a6c45`, `f2d8d9c`, `bb78fca`,
`2c49269`, `4942de1`) sono stati riconciliati con `sync-context`. L'unico cambiamento sostanziale
nelle aree coperte era l'ambiente `apertura` aggiunto a `style/harmony-macros.sty` (introdotto in
`f3a6c45`), ora documentato in `STACK.md`; i diagrammi in `design-and-security.md` erano già
corretti nel contenuto, solo l'ancoraggio era stale. `deployment.md`, `dev-testing.md` e
`roadmap.md` non hanno `covers-paths` popolati e restano fuori da questo confronto.

## Punto di ripresa

Ambiente e catena di build LaTeX/LilyPond verificati (ADR-003), stesura del libro non ancora
avviata oltre l'introduzione. In parallelo, sessioni non tracciate in git (15-20 luglio 2026,
vedi `memory/progress.md`) hanno costruito una bibliografia sostanziale in
`manuscript/bib/references.bib` (83 voci `@book`) a partire da libri posseduti, con un registro
di stato in `_notes/book-bib-registry.json` (153 voci: 86 verificate, 58 da-verificare, 8
scartate, 1 fonte primaria fuori schema `da-verificare`). La fase "libro -> skill" (`book-digest`)
non è mai partita.

La ricerca bibliografica per la nuova tesi sul tritono (avviata il 2026-07-16, scope chiarito il
2026-07-17 come "entrambe le vie") è conclusa: ricognizione sui libri posseduti e ricerca esterna
sono entrambe fissate in `_notes/tritono-ricognizione-interna.md` e
`_notes/tritono-ricerca-esterna-stato.md` (vedi `context/current-work.md` per la sintesi e ADR-006
per il metodo). Trovamento principale: il presunto divieto ecclesiastico medievale del tritono
("diabolus in musica") è un mito storiografico moderno, non un fatto medievale. La fonte primaria
annunciata dall'utente è stata identificata ("La dialettica del tritono" di Mariano Gaetani, ISBN
8869244857) ma il contenuto/appunti cartacei non sono ancora stati consegnati — non inventare
contenuto su questa fonte finché non arriva. Prossima decisione aperta con l'utente: se iniziare
già la stesura della sezione/capitolo sul tritono con il materiale raccolto, o attendere la fonte
primaria fisica.

Il 2026-07-24 è stato riscritto il capitolo sul tritono dal formato report al formato capitolo di
libro continuo (voce "Marcato", rottura della quarta parete, ambizione del framework universale):
bozza completa e validata in `_notes/appunti-da-inserire-nel-libro/capitolo-tritono-continuo.md`,
il `.docx` report resta intatto come backup. Nella stessa data il `.docx` continuo è stato assemblato
(`capitolo-tritono-continuo.docx`: arco A-I, sei figure riusate ai segnaposto, riferimenti [1]-[10] con
la nuova voce web Springsteen), e le sei figure sono state rirenderizzate con le annotazioni in font
Libertinus Sans (sorgenti `.ly` durevoli in `_notes/appunti-da-inserire-nel-libro/_ly-figure/`).
Prossimo passo: trascrizione fedele in `manuscript/chapters/NN-...lytex` quando l'utente dà il via, con
l'apertura biografica ancora in standby. Handoff completo di questa sessione in `_notes/RESUME-PROMPT.md`:
è il primo file da leggere alla ripresa, insieme a questo. La correzione teorica del minore armonico
(lettura del frigio, non dell'eolio) e le direzioni future del libro sono in
`_notes/cassaforte-capitolo-tritono.md`.

Il 2026-07-29 è stata affrontata la fase "libro -> skill", mai avviata prima, nelle sue due accezioni
e in quest'ordine deciso dall'utente. È nata `.claude/skills/armonia-libro/`, che digerisce la
dottrina del libro (tesi, voce, fatti verificati con il loro grado di verifica, mappa delle fonti,
agenda di ricerca) da circa 120 KB di note private a 59 KB, di cui 5 KB in contesto
all'invocazione. È poi partito `book-digest`: installata la skill dal template, prodotta la triage
del corpus `ARMONIA E TEORIA` in `_notes/corpus-digest-triage.md` con il nuovo
`tools/probe-pdf-text.py`, e digerito il primo libro, Berkman 2013, in
`.claude/skills/libro-berkman/`. ADR-007 fissa che la dottrina e i digest di opere di terzi non si
versionano: le due cartelle sono ignorate e dipendono dal backup su SSD, non da git. Nuovo
`tools/skill-freshness.py` per rilevare la deriva fra skill e fonti a costo zero di token.

Correzione di un dato riportato finora sia qui sia in `context/current-work.md`: il registro
bibliografico ha 161 voci, non 153. La ripartizione (94 verificate, 59 da-verificare, 8 scartate) era
corretta, era il totale a essere stale. Della coda `book-digest`, 153 voci restano `pending`, 1 è
`done` e 7 non hanno il campo.

A ogni avanzamento significativo sulla stesura vera e propria: aggiornare le schede impattate e
il work-log, poi l'utente committa e si rilancia `sync-context` per bumpare `last-verified-commit`.
Da collaudare ancora la parità Linux degli script `.sh`.
