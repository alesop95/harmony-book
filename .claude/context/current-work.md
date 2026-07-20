---
generated-from-commit: 017b02a
generated-from-branch: main
generated-date: 2026-06-15
covers-paths:
  - scripts/**
  - style/**
  - sample/**
last-verified-commit: 4942de1
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

## Riconciliazione

Ultima verifica: 2026-07-20, non ancora ancorata a un commit reale (il lavoro di questa sessione
vive in file privati/ignorati o non ancora tracciati, salvo la parte di sync-context su commit
reali già riflessa in `memory/index.md`).
