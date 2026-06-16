---
generated-from-commit: PENDING-FIRST-COMMIT
generated-from-branch: main
generated-date: 2026-06-15
covers-paths: []
last-verified-commit: PENDING-FIRST-COMMIT
---

# Roadmap

> Direzione e priorità del progetto. Tracciata. Non è il work-log: qui sta dove si va, non cosa è
> già stato fatto.

## Direzione

Scrivere un libro di armonia di qualità editoriale, portabile tra Windows 11 e Linux. Stack deciso
(ADR-003): LaTeX-nativo LuaLaTeX + memoir + LilyPond via lilypond-book. Contenuto privato (ADR-004):
`manuscript/` ignorata, backup SSD; repo pubblico solo per metodo e struttura.

## Priorità

1. Fase 1 (in corso): bootstrap ambiente, verifica della catena di build su `sample/`, poi stesura
   dei capitoli in `manuscript/`. Definire struttura del libro e convenzioni di notazione armonica.
2. Primo commit e ancoraggio del sistema (`sync-context`).
3. Fase 2 (futura, da valutare): front-end Quarto per edizione web HTML/EPUB interattiva (YouTube,
   audio) riusando le sorgenti LaTeX+LilyPond. Solo se l'edizione web diventa un obiettivo reale.
4. Fase 3 (futura, opzionale): Docker + GitHub Actions per build CI multi-formato e pubblicazione;
   Git LFS per asset audio/immagini pesanti.

## Idee e ipotesi da verificare

Font e stile bibliografico definitivi alla prova del PDF (da verificare). Promozione di
`manuscript/` a repository privato separato se servira' storia/backup remoti della prosa (ADR-004).
