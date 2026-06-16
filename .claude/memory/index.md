# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di
> riferimento e mappa ogni scheda al suo stato di verifica. È la fonte di verità su cosa è fatto,
> non le spunte del diario.

## Stato

```
Branch attivo:        main
Commit di riferimento: PENDING-FIRST-COMMIT
Data snapshot:        2026-06-16
```

## Stato di verifica delle schede

| Scheda | last-verified | Stato |
|---|---|---|
| STACK.md | PENDING-FIRST-COMMIT | popolata (ADR-003) |
| design-and-security.md | PENDING-FIRST-COMMIT | da popolare |
| deployment.md | PENDING-FIRST-COMMIT | da popolare |
| dev-testing.md | PENDING-FIRST-COMMIT | da popolare |
| current-work.md | PENDING-FIRST-COMMIT | popolata (Fase 1) |
| roadmap.md | PENDING-FIRST-COMMIT | popolata |

## Punto di ripresa

Stack deciso (ADR-003) e privacy decisa (ADR-004). Ambiente installato e catena di build VERIFICATA
su Windows: `scripts/build.ps1` compila `sample/main.lytex` (lilypond-book -> LuaLaTeX -> biber ->
makeindex) e lo scheletro `manuscript/`. Prossima azione concreta: avviare la stesura del capitolo 1
in `manuscript/` (privato, ignorato), e far eseguire all'utente il PRIMO COMMIT, dopo il quale
lanciare `sync-context` per sostituire ogni `PENDING-FIRST-COMMIT` con l'hash di HEAD. Da collaudare
ancora la parita' Linux degli script `.sh`. Vedi `context/current-work.md`.
