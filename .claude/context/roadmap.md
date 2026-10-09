---
generated-from-commit: 017b02a
generated-from-branch: main
generated-date: 2026-06-15
covers-paths: []
last-verified-commit: 017b02a
---

# Roadmap

## Incremento corrente: corpus completo e riordino del vault

Ricerca completa prima della sintesi editoriale e della scrittura. Registro 228, bibliografia reale 157; sedici chiusure del nuovo ledger comprendono tre testi e tredici commenti esatti, con unità e limiti dichiarati. Il corpus locale obbligatorio è censito su tutti i formati: 65 file, di cui 31 PDF, tre DOCX, undici note testuali, diciannove media e un collegamento. Le pagine PDF distintamente apribili sono 6.268; un esemplare non si apre. Il censimento e le estrazioni non attestano lettura completa. Dettagli, identità e contenuti rimangono privati.

Il vault è organizzato in otto sezioni numerate: regia, biblioteca, ricerca, tesi, libro, strumenti, archivio e cache. Ingresso `_notes/HOME.md`, roadmap privata `_notes/00-regia/ROADMAP-LETTURA-COMPLETA.md`, inventario completo `_notes/10-biblioteca/CORPUS-ARMONIA.md`. I percorsi precedenti hanno un manifest; originali e storia sono conservati. Cinque copie di cache identiche agli esemplari durevoli sono rimosse, 28.725.939 byte; ventitré materiali unici o storici sono conservati fuori dalla cache. Otto file principali e tutte le 104 voci originarie restano identici; anche le 144 voci precedenti all’ultimo import sono identiche. I collegamenti correnti risolvono; ledger e bibliografia non hanno flag divergenti. I conteggi nei blocchi successivi sono fotografie precedenti.

Conferma dell’autore conservata verbatim: terminata ricerca, sintesi e indice, ogni pezzo viene proposto e approvato qui in chat prima di inserirlo nel manoscritto. Si conserva il testo esatto approvato insieme ai ragionamenti, alle obiezioni e ai legami fra concetti. Nessuna nuova prosa promossa in questo giro; nessun Git add, commit, push o deploy. Il punto di ripresa privato nomina una sola coda corrente.

## Incremento corrente: lettore d’archivio e nuove unità bibliografiche

Usato il lettore `community-sources` già istanziato nel progetto, dopo il rifiuto dell’accesso diretto. Acquisiti e letti tredici snapshot con 493 record di commento, tre corpi assenti dichiarati. Tredici unità di commento hanno attribuzione e permalink verificati, copie private e lettura L1 limitata alla propria unità. Registro 228, bibliografia reale 157; sedici chiusure nel ledger distinguono tre fonti accademiche/didattiche e tredici commenti. Il mandato sul corpus completo rimane aperto; nessuna pretesa di completezza del sito vivo o del grafo esterno. Esiti, correzioni, frontiera e provenienze sono nel vault privato `_notes/20-ricerca/reddit-musictheory/`; prompt e collegamenti aggiornati. Le 104 voci originarie e le bozze restano conservate. La fonte guida resta L2 con 58 immagini nelle nuove schede. I blocchi sottostanti sono fotografie precedenti.

## Stato corrente: altra collazione e nuovo ramo di ricerca

Letti e confrontati altri quindici facsimili della fonte guida, con 21 righe modali e 35 strutture accordali. Schede 08-12: 58 immagini attestate; livello complessivo ancora L2, coda e lacune nel ledger privato. La richiesta successiva dell'autore aggiunge un commento web e una selezione di dodici discussioni: tredici nuovi record candidati, anagrafiche e testi ancora da acquisire direttamente, nessuna promozione bibliografica. Registro 228, bibliografia reale 144, tre nuove chiusure integrali documentate. Dettagli privati in `_notes/20-ricerca/reddit-musictheory/00-ricerca-e-fonti.md` e nella scheda 12 della fonte guida. Bozze conservate; prompt, concetti, ricerca e archivio dei messaggi aggiornati. I blocchi sottostanti sono fotografie precedenti.

## Stato corrente: catalogo finale della fonte guida

Lettura e collazione di PDF 66-82, pp. stampate 63-79: diciassette immagini, 47 coppie complessive e quattro righe modali, con controllo riproducibile. Dettagli e calcoli restano privati nelle schede 10-11 sotto `_notes/20-ricerca/fonti-locali/gaetani2019/`. Le schede 08-11 attestano 43 immagini; la fonte rimane L2 perché le figure precedenti e le lacune dichiarate non sono tutte chiuse. Registro 215, bibliografia reale 144, tre nuove chiusure integrali documentate; bozze e manoscritto intatti. Proseguire con l'audit delle figure iniziali e delle lacune, poi con il documento principale e l'appendice del prossimo paper nella coda privata. Prompt, ledger, concetti e archivio dei messaggi disponibili aggiornati nello stesso giro. Le note sottostanti sono fotografie precedenti, non la coda attuale.

> Direzione e priorità del progetto. Tracciata. Non è il work-log: qui sta dove si va, non cosa è già stato fatto.

## Direzione

Scrivere un libro di armonia di qualità editoriale, portabile tra Windows 11 e Linux. Stack deciso (ADR-003): LaTeX-nativo LuaLaTeX + memoir + LilyPond via lilypond-book. Contenuto privato (ADR-004): `manuscript/` ignorata, backup SSD; repo pubblico solo per metodo e struttura.

## Priorità

Dal mandato del 2026-10-08 la sequenza attiva è: lettura completa del corpus con bibliografia aggiornata, sintesi critica, consolidamento di roadmap e indice del libro, poi nuova scrittura per microstep. Il piano di ricerca è privato in `_notes/10-biblioteca/PIANO-LETTURE.md`; l'indice precedente resta una proposta. Questo ordine supera la precedente indicazione di continuare la stesura contemporaneamente alla ricerca selettiva. Il testo già scritto e i ragionamenti restano conservati; le attestazioni pregresse si riconciliano.

1. Fase 1 (in corso): bootstrap ambiente, verifica della catena di build su `sample/`, poi stesura dei capitoli in `manuscript/`. Definire struttura del libro e convenzioni di notazione armonica.
2. Primo commit e ancoraggio del sistema (`sync-context`).
3. Fase 2 (futura, da valutare): front-end Quarto per edizione web HTML/EPUB interattiva (YouTube, audio) riusando le sorgenti LaTeX+LilyPond. Solo se l'edizione web diventa un obiettivo reale.
4. Fase 3 (futura, opzionale): Docker + GitHub Actions per build CI multi-formato e pubblicazione; Git LFS per asset audio/immagini pesanti.

## Idee e ipotesi da verificare

Font e stile bibliografico definitivi alla prova del PDF (da verificare). Promozione di `manuscript/` a repository privato separato se servirà storia/backup remoti della prosa (ADR-004).

## Prossimo incremento editoriale, fissato il 2026-10-07

La priorità attiva è portare nel manoscritto il capitolo continuo sul tritono, un movimento alla volta. Il movimento A è in `manuscript/chapters/01-tritono.lytex`, con attribuzioni Bennett e Springsteen verificate sui sottotitoli e due citazioni bibliografiche. Il prossimo incremento è il movimento B; Sarti riguarda G e H. Prima di ogni incremento si legge la bozza privata e il registro dei ragionamenti; dopo si confrontano testo, figure, citazioni e indice delle pendenze. La ricerca esterna segue i nodi concettuali della scheda `research-method.md` e non sospende la stesura dove i claim sono già sostenuti. Le due verifiche storiche urgenti riguardano la divergenza fra Fétis e Yavorsky e la formulazione della storia del «diabolus»; i nuovi studi percettivi restano candidati finché non sono letti e registrati.

Il saggio privato `modi_ionico_eolio_tonalita.docx` è destinato al libro e resta un filone distinto con cassaforte chiusa; dopo la priorità attiva sul tritono va pianificata la sua collocazione e trascrizione. Per il filone delle scale derivate la prima scheda è `_notes/40-libro/percorso-libro/01-napoletana.md`: il calcolo interno è disponibile, mentre gli appunti cartacei dell'autore e il perimetro degli esempi sono ancora in attesa. Le otto decisioni del dossier hanno stato aggiornato in `_notes/40-libro/percorso-libro/02-decisioni.md`.

Il movimento B ha ora tre unità in `_notes/40-libro/microstep/B00-mappa.md`, con proposte e prove separate per B01 (accordi), B02 (prassi del minore) e B03 (centro e sensibile). L'ingresso del vault Obsidian privato è `_notes/HOME.md`; l'audit J: e la ricerca aggiuntiva sono collegati da lì. La prossima consegna editoriale è la validazione del testo esatto di B01 prevista dalla regola del progetto, seguita da figura, citazione se usata, trascrizione, build e tracciamento. B02 e B03 seguono uno alla volta. Il dato storico su Bach è ora documentato ma non va trasformato in una tesi sull'origine della scala.
