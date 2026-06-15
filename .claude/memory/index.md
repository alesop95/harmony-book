# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di
> riferimento e mappa ogni scheda al suo stato di verifica. È la fonte di verità su cosa è fatto,
> non le spunte del diario.

## Stato

```
Branch attivo:        main
Commit di riferimento: PENDING-FIRST-COMMIT
Data snapshot:        2026-06-15
```

## Stato di verifica delle schede

| Scheda | last-verified | Stato |
|---|---|---|
| STACK.md | PENDING-FIRST-COMMIT | da popolare |
| design-and-security.md | PENDING-FIRST-COMMIT | da popolare |
| deployment.md | PENDING-FIRST-COMMIT | da popolare |
| dev-testing.md | PENDING-FIRST-COMMIT | da popolare |
| current-work.md | PENDING-FIRST-COMMIT | da popolare |
| roadmap.md | PENDING-FIRST-COMMIT | da popolare |

## Punto di ripresa

Progetto appena inizializzato in greenfield sotto account Claude `.claude-account2`. Lo stack non
è ancora deciso: il primo task della sessione ripresa è leggere `_notes/RESUME-PROMPT.md`, poi
`transform-into-claude-md/` (cartella ignorata, handoff di ricerca), decidere con l'utente lo stack
per scrivere un libro di armonia, attivare se scelto il pacchetto LaTeX da `.claude/templates/latex/`,
popolare le schede di `context/` leggendo le scelte, e infine far eseguire all'utente il primo
commit e lanciare la skill `sync-context` per ancorare ogni `PENDING-FIRST-COMMIT` a `HEAD`.
