---
generated-from-commit: 017b02a
generated-from-branch: main
generated-date: 2026-06-15
covers-paths:
  - .claude/context/diagrams/**
last-verified-commit: 4942de1
---

# Design e sicurezza applicativa

> Popolare leggendo le scelte effettive. I diagrammi referenziati vivono in `diagrams/` in
> corrispondenza uno a uno con i componenti descritti (sezione 7 di `PROJECT-SYSTEM.md`).

## Paradigmi di software design

<organizzazione delle sorgenti del libro, separazione capitoli/preambolo/esempi, contratti tra file>

## Sicurezza applicativa

<gestione di eventuali segreti di build o pubblicazione, superfici esposte e mitigazioni; per un
libro tipicamente minima, da dichiarare esplicitamente quando definita>

## Diagrammi

| Diagramma | Sorgente | Componenti rappresentati |
|---|---|---|
| flusso-scrittura.svg | flusso-scrittura.mmd | ciclo scrivi → build → rivedi → commit → sync-context, con backup SSD |
| struttura-progetto.svg | struttura-progetto.mmd | split pubblico (style, scripts, sample, .claude) / privato locale (manuscript, build) |
| pipeline-build.svg | pipeline-build.mmd | lilypond-book → lualatex → biber/makeindex/makeglossaries → build/main.pdf |
