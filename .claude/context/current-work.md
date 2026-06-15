---
generated-from-commit: PENDING-FIRST-COMMIT
generated-from-branch: main
generated-date: 2026-06-15
covers-paths: []
last-verified-commit: PENDING-FIRST-COMMIT
stato: in pianificazione
---

# Lavoro in corso

> La fonte di verità su cosa è fatto resta `memory/index.md` e il work-log, non le spunte di
> questo file. Ogni feature si descrive con lo schema fisso sotto, così il lavoro pendente è
> leggibile senza ricostruire il contesto da capo.

## Feature: Decisione dello stack e bootstrap della scrittura

Cosa fa: definisce con quale stack tecnico si scrive il libro di armonia (motore di composizione e
notazione musicale), portabile su Windows 11 e Linux, e prepara lo scheletro delle sorgenti.

File da creare:

```
<da definire dopo la scelta dello stack, es. sorgenti del libro e manifesto di build>
```

File da modificare:

```
.claude/context/STACK.md   popolare con lo stack scelto e le alternative escluse
```

Definition of done:

- [ ] Letto `transform-into-claude-md/` e discusso lo stack con l'utente
- [ ] Stack deciso e registrato come ADR in `memory/decisions.md`
- [ ] Pacchetto LaTeX attivato da `.claude/templates/latex/` se lo stack lo richiede
- [ ] Schede di `context/` popolate leggendo le scelte
- [ ] Primo commit eseguito dall'utente e `sync-context` lanciata per ancorare i `PENDING-FIRST-COMMIT`

Domande aperte:

Quale stack di composizione e quale sistema di notazione musicale offrono il miglior compromesso
tra qualità tipografica, portabilità Windows/Linux e diff leggibili in git per il version control
come stato di avanzamento. Da risolvere leggendo l'handoff e discutendo con l'utente.

## Riconciliazione

Ultima verifica: 2026-06-15 al commit PENDING-FIRST-COMMIT.
