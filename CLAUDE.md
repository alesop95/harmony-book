# harmony-book

> Istruzioni di team, versionate. Questo file è l'indice del progetto: indicizza i soli file satellite tracciati e descrive la procedura di ripresa. Le preferenze personali vivono in `CLAUDE.local.md`, ignorato da git, non qui.

## Cos'è questo progetto

Un libro di armonia. La scrittura deve restare portabile sia su Windows 11 sia su Linux. Lo stack è LuaLaTeX, `memoir` e LilyPond; vedi `.claude/context/STACK.md`. Il repository pubblico versiona il metodo, mentre il manoscritto e le note sostanziali sono privati e ignorati da git: il loro avanzamento va conservato anche nel backup privato.

## Procedura di ripresa in una sessione nuova

Lo stato documentato e presente su questo disco si recupera seguendo un percorso fisso; gli appunti cartacei non ancora consegnati restano esterni. Si legge per primo `.claude/memory/index.md`, che dà branch, commit di riferimento, stato di verifica di ogni scheda e punto di ripresa. Si legge poi `.claude/context/current-work.md` per la feature attiva e `_notes/00-PERCORSO-LIBRO.md` per la mappa sequenziale dei materiali privati. Si invoca la skill `sync-context` per verificare il drift tra schede e codice, e si leggono solo le schede pertinenti al task. Il work-log `.claude/memory/progress.md` e il registro `.claude/memory/decisions.md` forniscono la storia e le decisioni quando servono. Il materiale grezzo sotto `_notes/` si apre per verificare un requisito originale o un passaggio da promuovere nel libro.

## Indice dei file satellite tracciati

Memoria e meta-stato, sotto `.claude/memory/`, letti sempre a inizio sessione.

```
.claude/memory/index.md       snapshot e tabella di sincronizzazione, da leggere per primo
.claude/memory/progress.md    work-log append-only di passi e riconciliazioni
.claude/memory/decisions.md   registro ADR-lite delle decisioni architetturali
```

Schede tecniche, sotto `.claude/context/`, con frontmatter di riconciliazione.

```
.claude/context/STACK.md                stack, flussi di codice, ruolo architetturale dei file
.claude/context/design-and-security.md  paradigmi di design e sicurezza applicativa
.claude/context/deployment.md           livelli build e pubblicazione, comandi
.claude/context/dev-testing.md          controlli di qualità, runner, hook
.claude/context/current-work.md         feature attiva, definition of done, domande aperte
.claude/context/roadmap.md              direzione e priorità
.claude/context/research-method.md       protocollo di ricerca per i claim del libro
```

Regole modulari caricate su necessità, sotto `.claude/rules/`, e skill richiamabili, sotto `.claude/skills/`. Lo standard di sistema completo è in `.claude/PROJECT-SYSTEM.md`.

Norme caricate su richiesta, una riga per situazione con le parole con cui si presenta, così che il caricamento non dipenda dal ricordare che la norma esista.

- `git worktree list` mostra più di un albero, se ne crea o se ne rimuove uno, si deve decidere da dove leggere la memoria versionata: skill `alberi-di-lavoro`.
- Un recupero web fallisce con 403 o con una pagina di verifica anti-bot, la fonte sta su Reddit o su Discord, serve la trascrizione di un video, si sta per annotare una fonte non letta: skill `fonti-non-recuperabili`.
- Si scrive o si valuta una prova automatica, si chiude un difetto, una verifica manuale smentisce una suite verde, si sta per dichiarare completo un intervento il cui scopo era un effetto misurabile: skill `prove-che-misurano`.
- Si inizializza o si allinea il progetto, oppure cambia il modo in cui si prova e si rilascia, e va deciso come separare test e produzione: skill `separazione-ambienti`.

## Vincoli di team

Le operazioni di `git add`, commit e push restano sempre manuali dell'utente: l'agente prepara i file, non committa. L'identità git e il remoto sono configurati a livello locale del repository secondo `.claude/rules/git-identity-and-repo.md`; i valori reali restano fuori dai file tracciati. Lo stile di documentazione e di interazione è quello di `.claude/rules/interaction-style.md`. I file di memoria e di contesto si aggiornano nello stesso giro di lavoro sostanziale, come prescrive `.claude/rules/chat-non-e-memoria.md`; il controllo del versionamento resta umano.
