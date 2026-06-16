# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di
> riferimento e mappa ogni scheda al suo stato di verifica. È la fonte di verità su cosa è fatto,
> non le spunte del diario.

## Stato

```
Branch attivo:        main
Commit di riferimento: 017b02a
Data snapshot:        2026-06-16
```

## Stato di verifica delle schede

| Scheda | last-verified | Stato |
|---|---|---|
| STACK.md | 017b02a | aggiornata |
| design-and-security.md | 017b02a | diagrammi registrati; paradigmi da popolare |
| deployment.md | 017b02a | da popolare |
| dev-testing.md | 017b02a | da popolare |
| current-work.md | 017b02a | aggiornata |
| roadmap.md | 017b02a | aggiornata |

## Punto di ripresa

Sistema ancorato al primo commit `017b02a` (branch `main`). Ambiente e catena di build verificati.
Prossima azione concreta: iniziare la stesura in `manuscript/` (privato, ignorato) — copertina,
introduzione e capitolo 1 — compilando con `scripts/build.ps1` per controllare la resa. A ogni
avanzamento significativo: aggiornare le schede impattate e il work-log, poi l'utente committa e si
rilancia `sync-context` per bumpare `last-verified-commit`. Da collaudare ancora la parità Linux
degli script `.sh`.
