---
generated-from-commit: 017b02a
generated-from-branch: main
generated-date: 2026-06-15
covers-paths: []
last-verified-commit: 017b02a
---

# Roadmap

> Direzione e priorità del progetto. Tracciata. Non è il work-log: qui sta dove si va, non cosa è già stato fatto.

## Direzione

Scrivere un libro di armonia di qualità editoriale, portabile tra Windows 11 e Linux. Stack deciso (ADR-003): LaTeX-nativo LuaLaTeX + memoir + LilyPond via lilypond-book. Contenuto privato (ADR-004): `manuscript/` ignorata, backup SSD; repo pubblico solo per metodo e struttura.

## Priorità

1. Fase 1 (in corso): bootstrap ambiente, verifica della catena di build su `sample/`, poi stesura dei capitoli in `manuscript/`. Definire struttura del libro e convenzioni di notazione armonica.
2. Primo commit e ancoraggio del sistema (`sync-context`).
3. Fase 2 (futura, da valutare): front-end Quarto per edizione web HTML/EPUB interattiva (YouTube, audio) riusando le sorgenti LaTeX+LilyPond. Solo se l'edizione web diventa un obiettivo reale.
4. Fase 3 (futura, opzionale): Docker + GitHub Actions per build CI multi-formato e pubblicazione; Git LFS per asset audio/immagini pesanti.

## Idee e ipotesi da verificare

Font e stile bibliografico definitivi alla prova del PDF (da verificare). Promozione di `manuscript/` a repository privato separato se servirà storia/backup remoti della prosa (ADR-004).

## Prossimo incremento editoriale, fissato il 2026-10-07

La priorità attiva è portare nel manoscritto il capitolo continuo sul tritono, un movimento alla volta. Il movimento A è in `manuscript/chapters/01-tritono.lytex`, con attribuzioni Bennett e Springsteen verificate sui sottotitoli e due citazioni bibliografiche. Il prossimo incremento è il movimento B; Sarti riguarda G e H. Prima di ogni incremento si legge la bozza privata e il registro dei ragionamenti; dopo si confrontano testo, figure, citazioni e indice delle pendenze. La ricerca esterna segue i nodi concettuali della scheda `research-method.md` e non sospende la stesura dove i claim sono già sostenuti. Le due verifiche storiche urgenti riguardano la divergenza fra Fétis e Yavorsky e la formulazione della storia del «diabolus»; i nuovi studi percettivi restano candidati finché non sono letti e registrati.

Il saggio privato `modi_ionico_eolio_tonalita.docx` è destinato al libro e resta un filone distinto con cassaforte chiusa; dopo la priorità attiva sul tritono va pianificata la sua collocazione e trascrizione. Per il filone delle scale derivate la prima scheda è `_notes/percorso-libro/01-napoletana.md`: il calcolo interno è disponibile, mentre gli appunti cartacei dell'autore e il perimetro degli esempi sono ancora in attesa. Le otto decisioni del dossier hanno stato aggiornato in `_notes/percorso-libro/02-decisioni.md`.
