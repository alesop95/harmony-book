---
generated-from-commit: 017b02a
generated-from-branch: main
generated-date: 2026-06-15
covers-paths:
  - scripts/**
  - style/**
  - sample/**
last-verified-commit: 017b02a
stato: in corso
---

# Lavoro in corso

> La fonte di verità su cosa è fatto resta `memory/index.md` e il work-log, non le spunte di
> questo file.

## Feature: Bootstrap dell'ambiente e verifica della catena di build

Cosa fa: rende operativo lo stack deciso (ADR-003) installando l'ambiente e verificando che la
catena `lilypond-book` -> LuaLaTeX produca un PDF, prima di entrare nella stesura vera.

File da creare:

```
manuscript/chapters/*.lytex   capitoli reali del libro (privati, ignorati)
```

File da modificare:

```
tex-packages.txt          aggiungere pacchetti se il preambolo evolve
style/preamble.tex        rifinire tipografia e macro armoniche
```

Definition of done:

- [x] Installato l'ambiente: `scripts/setup-tex.ps1` (TinyTeX + pacchetti) e LilyPond sotto Program Files
- [x] `scripts/build.ps1` compila `sample/main.lytex` -> `build/main.pdf` senza errori
- [x] Verificata la resa di un esempio LilyPond e della microtipografia nel PDF (sample ~40 KB)
- [ ] Avviata la stesura del capitolo 1 in `manuscript/`
- [ ] Primo commit eseguito dall'utente e `sync-context` lanciata per ancorare i `017b02a`

Nota: la catena di build e' verificata su Windows. La parita' su Linux (`scripts/*.sh`) e'
implementata ma non ancora collaudata su una macchina Linux.

Domande aperte:

Scelta del font definitivo (Libertinus e' il default proposto) e dello stile bibliografico
(`authoryear` di default) da confermare alla prova del PDF. La struttura dei capitoli e delle
convenzioni di notazione armonica si affina con la stesura.

## Riconciliazione

Ultima verifica: 2026-06-15 al commit 017b02a.
