---
generated-from-commit: 017b02a
generated-from-branch: main
generated-date: 2026-06-15
covers-paths:
  - scripts/**
  - style/**
  - sample/**
  - tools/**
  - .claude/skills/**
last-verified-commit: 9acc2e0
stato: in corso
---

## 2026-10-09 - Collazione disponibile e recupero degli esemplari

Completata l'apertura delle 85 immagini disponibili della fonte guida, con calcoli e provenienze nel vault privato. Il livello resta L2: fotografia con continuazione assente e audit delle voci ancora aperti. Recuperato un PDF compresso tramite copia derivata verificata, originale immutato; acquisite tutte le 91 pagine. Risolto un collegamento a cartella senza eseguirlo: nove file censiti, sei documenti con anagrafiche verificate in coda distinta, una nuova lettura integrale attestata. Registro234, bibliografia163; diciassette unità chiuse nel ledger. Contenuti e dettagli bibliografici rimangono privati.

Corretto il rendering di schede con ancora non valida: output precedente conservato, errore ancora respinto, porzioni divise e ripresa dal checkpoint. La prova sul caso reale riproduce il vecchio KeyError e verifica che il dato malformato non venga accettato. Un breve segmento ASR può fornire evidenza inferiore a15 caratteri soltanto quando coincide con l'intero segmento non vuoto; una sottostringa breve di un passo lungo resta respinta. Nessuna promozione semantica automatica. Il lettore accetta corpora aggiuntivi privati e PDF derivati con verifica dei due hash e tracciamento della trasformazione.

Verificati 8/8 originali,104/104 voci originarie e157/157 precedenti all'import identici, preflight riuscito; collegamenti del vault controllati. Acquisizione/OCR e analisi GPU proseguono con stati/PID privati. R1/R2 richiedono ancora audit, revisione e ascolto; R3 conserva altri record e41 esemplari non collegati; R4segue originali e controesempi. La scrittura attende sintesi, indice e approvazione del testo esatto qui. Milestone e backup nel prompt privato; nessun Git add,commit,push o deploy eseguito.

# Lavoro in corso

Ripresa 2026-10-09 dopo crash: completata L1 di Walker (articolo pp. 33-47, tutte le 16 pagine PDF, note e bibliografia); digest `_notes/10-biblioteca/digest/walker1973galilei.md`, ledger e registro bibliografico aggiornati. Rimane aperta la discrepanza Cohen p. 223 / pp. 233-264 citata da Caleon. Prossimi passi: audit pentagrammi Gaetani p. 49 e tavole ancora aperte, quindi Field pp. 29-44 in *Music and Mathematics*. L’analizzatore automatico risulta ancora attivo; checkpoint 12:18:42Z: 108 grounded-unreviewed, 2.630 pending, 45 split. Non chiudere fonti sulla base delle schede automatiche.




## 2026-10-09 - Checkpoint conservato e riavvio della lettura

Un blocco multimediale breve, con 25 segmenti e 917 caratteri, ha superato il limite della risposta strutturata. Il controllo precedente divideva soltanto oltre 1.000 caratteri: corretto affinché divida anche più segmenti brevi. La prova sul checkpoint reale ricostruisce tutti i segmenti nelle due parti, conserva il padre e riproduce l'impedimento della vecchia guardia. Il batch è stato riavviato dal checkpoint; schede valide e risposte parziali rimangono conservate, livelli bibliografici invariati. Contatori vivi nei documenti privati; gli stati sottostanti sono fotografie successive del lavoro.

Snapshot successivo al recupero OCR verificato: 1020 file, 144162174 byte, CRC e SHA-256 di ogni membro verificati, database SQLite incluso tramite backup consistente. Percorso e hash nel prompt privato. Il nuovo riavvio, queste annotazioni e i risultati successivi allo snapshot rimangono nel progetto e non sono inclusi nello ZIP. La copia sul supporto distinto dell'ADR-004 rimane separata.


## 2026-10-09 - Recupero OCR concluso, lettura in prosecuzione

Recupero OCR completato: riacquisite tutte le 2.503 pagine dei 25 PDF riaperti, zero unità con il vecchio profilo. I nove esemplari prima vuoti hanno ora testo; il solo PDF non apribile rimane un impedimento di acquisizione. Tutti i 59 gruppi dei 65 file hanno esito tecnico, con collegamento e segnaposto ancora distinti da opere lette. Ricostruite 9.151 unità non vuote e 15.109.141 caratteri senza tagli o duplicazioni, ricerca FTS su 2.129 unità reali; integrità SQLite verificata.

Il batch automatico sulla GPU prosegue: le porzioni della prosa della fonte guida sono tutte passate al controllo meccanico, mentre interpretazioni e figure restano da revisionare; il livello della fonte guida rimane quello attestato prima. R1/R2 restano aperti per lettura e revisione del resto del corpus, pentagrammi, immagini, audio e rinvii. R3 comprende gli altri record e i 41 esemplari da collegare; R4 segue originali, allegati, versioni, conferme e controesempi. Registro 228, bibliografia 157 e contenuti del libro conservati. Le schede automatiche non sono chiusure di fonte.

Verifica di continuità: 8/8 originali, 104/104 voci originarie e 144/144 precedenti all'ultimo import identici; 601 wikilink in 123 note, zero mancanti; preflight del libro riuscito. Il mandato parallelo di registrazione GPU è stato versionato dall'utente al commit `f416586` e pubblicato sui due remoti verificati identici. Le annotazioni sotto conservano la diagnosi e il riavvio precedente; i contatori vivi rimangono nei checkpoint privati.

## Stato corrente: OCR riaperto e ricerca ancora in corso

La preparazione tecnica è stata riaperta per 25 PDF: 2.503 pagine avevano output OCR non validato. Nove esemplari apribili risultavano interamente senza testo acquisito. Il controllo su tre scansioni reali ha mostrato testo visibile e output scartato dal parser; corretto il formato, ora dichiarato esplicitamente e validato dall'intestazione TSV. La prova recupera parole osservabili in tutte e tre le pagine; reintrodotta la chiamata difettosa su una copia, la prova fallisce e il file operativo è identico. La precedente dicitura «preparazione conclusa» è superata: attestava unità tecniche presenti, non disponibilità corretta di tutto il testo.

OCR su questo PC e analisi semantica sulla GPU proseguono in parallelo. I risultati precedenti e le cache vecchie sono conservati; l'analizzatore attende la preparazione completa di ogni fonte. Corretto anche un blocco SQLite effettivamente osservato: la preparazione libera il writer dopo ogni pagina e prima di attendere altro OCR; schede valide già salvate vengono riusate con controllo di hash ed evidenze. Il servizio riprova disconnessioni SSH con limite; il supervisore distingue esecuzione incompleta e conclusa. La GPU è operativa, l'istanza resta temporanea con dati in RAM e risultati durevoli nel progetto.

Il primo lotto riguarda i 65 file locali, 59 identità tecniche. Per completare le fonti servono ancora batch e revisione di prosa, figure, pentagrammi, audio e trascrizioni, soluzione di un esemplare guasto e un collegamento, lettura degli altri record e acquisizione dei 41 esemplari non ancora collegati, seguito delle citazioni pertinenti. Registro 228, bibliografia 157 invariati; nessun livello o contenuto del manoscritto promosso. Stato dettagliato e contatori in `_notes/00-regia/FONTI-COSA-MANCA.md` e nei checkpoint del lettore. La scrittura segue sintesi, indice e approvazione qui del pezzo esatto.

## Incremento corrente: elaborazione locale riprendibile

Ripristino GPU concluso dall'autore: kernel `7.0.0-38-generic`, NVIDIA GeForce RTX 5060 Ti con 16.311 MiB, driver `595.99.02`. L'istanza temporanea ha caricato Qwen3 14B con contesto 16.384: `/api/ps` ha attestato 12.153.814.144 byte di modello interamente in VRAM. Il pilota reale ha prodotto schede con evidenze verificabili; il batch prosegue con checkpoint. I contatori correnti sono in `_notes/10-biblioteca/lettura-locale/STATO.md` e nei file di stato, non in un conteggio storico del diario.

Preparazione conclusa sui 59 gruppi tecnici dei 65 file obbligatori, con esito esplicito anche per esemplare non apribile, collegamento e segnaposto. Entrambi i video hanno trascrizioni complete indicizzate, ancora da revisionare. Il controllo ricostruisce senza tagli o duplicazioni 6.691 unità non vuote, 11.734.806 caratteri. Otto pagine native patologiche sono state riacquisite con OCR, conservando nativo e piani precedenti; corretti anche il controllo dei percorsi Windows estesi e la duplicazione dei piani al rilancio.

Il lettore seleziona identificativi dei passi; il programma copia dalla fonte evidenza, unità e intervallo di caratteri. Questo evita citazioni ricopiate male e localizzatori discordanti. Le schede fallite e i tentativi precedenti restano conservati; porzioni troppo dense o non valide vengono divise in parti contigue e riprovate. Le prove respingono evidenze inventate e ancore errate; una mutazione della guardia sulle unità contraddittorie ha fatto fallire il controllo, con sorgente operativo identico. Le interpretazioni e la completezza semantica richiedono revisione.

Tutti i risultati durevoli sono privati nel progetto. Landlock nega scritture sul disco dell'host GPU; temporanei in RAM, accesso ai dispositivi NVIDIA e metadati virtuali `/proc` necessari a CUDA. Modelli preesistenti in sola lettura, debug disattivato, log via SSH nel progetto, pulizia dei temporanei alla chiusura. Registro 228 e bibliografia 157 invariati; R1/R2 rimangono aperti per figure, pentagrammi, ascolto, esemplare guasto e destinazioni esterne. R3/R4 seguiranno questo lotto. Testo del libro e livelli bibliografici conservati; la scrittura riprende dopo sintesi e approvazione qui del singolo pezzo. Riferimento di lavoro `e0fca8c`, modifiche non committate; checkpoint Git storici distinti.

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

## Snapshot privato al termine del nuovo incremento

Creato e testato il nuovo archivio privato locale `harmony-private-20261008T131702Z.zip`: 329 file, 115.827.050 byte, manifest SHA-256 incluso. Percorso e hash completo sono nel prompt e nei metadati privati; il contenuto sostanziale è incluso, le annotazioni del ZIP sono successive. È una copia sullo stesso disco, distinta dal supporto fisicamente separato previsto dall’ADR-004. Nessun Git add, commit, push o deploy eseguito.

## Secondo blocco della fonte guida completato

Letto anche il blocco PDF 55-65, pp. stampate 52-62: undici immagini, otto trasformazioni e dodici strutture confrontate. Scheda e risultato sono privati in `_notes/20-ricerca/fonti-locali/gaetani2019/09-collazione-modulazioni-2026-10-08.md` e `verifica-modulazioni.json`, con script riproducibile. Totale dei due nuovi blocchi: 26 immagini; il volume resta L2 e le lacune dei pentagrammi rimangono esplicite. Prossimo blocco PDF 66-73, pp. 63-70, poi catalogo enarmonico. Nessuna prosa promossa.

Controlli conclusivi: otto file principali identici al primo snapshot, 104/104 voci precedenti identiche al backup preimportazione; 320 collegamenti risolti in 44 note di ricerca. Preflight del libro senza collegamenti rotti, due esclusioni legacy previste; Biber legge le 144 voci con otto avvisi esplicitamente conservati nel rapporto privato di qualità, senza inventare dati mancanti. Nessuna build completa necessaria per questo incremento: i capitoli e le due citazioni usate sono invariati.

## Ultimo incremento della fonte guida

Gaetani rimane L2: nuovo blocco visivo di quindici tavole PDF 38-52, pp. stampate 35-49, con nove mutazioni confrontate e 21 righe modali coerenti. PDF 51 taglia la continuazione inferiore di p. 48; il pentagramma p. 49 è aperto e ingrandito, ma la collazione completa delle singole voci resta da fare. Scheda `_notes/20-ricerca/fonti-locali/gaetani2019/08-collazione-famiglie-estese-2026-10-08.md` e script/JSON riproducibili. Il blocco PDF 55-65 è stato poi controllato nella scheda 09; il prossimo è PDF 66-73, pp. 63-70, prima del catalogo enarmonico.

## Mandato prioritario: lettura di tutto il corpus, 2026-10-08

Il nuovo messaggio dell'autore estende la ricerca alla lettura integrale di tutte le fonti, con informazioni durevoli nel vault e bibliografia aggiornata; roadmap, indice e scrittura seguono la ricerca. Il protocollo privato è `_notes/10-biblioteca/PROTOCOLLO.md`, il censimento `_notes/10-biblioteca/INDICE.md`; le attestazioni pregresse rimangono da riconciliare, non cancellate. Registro 215 record, 209 citekey, due senza chiave, quattro gruppi con chiave condivisa. Importate nel `.bib` reale 40 anagrafiche già verificate: bibliografia 144, zero verificate assenti e zero flag divergenti. Le 104 voci precedenti sono conservate identiche, con backup privato e report d'importazione. Il mandato autorizza questi aggiornamenti senza conferma per ogni voce.

Acquisizione tecnica: 171 PDF estratti, 20.956 pagine, 57.749.738 caratteri nativi; 13.421 pagine con poco testo richiedono immagini/OCR o identificazione come pagine bianche e spartiti. Un Pozzoli non si apre. Sono collegati file locali per 173 record, incluse sei copie recuperate nel progetto; 42 record non hanno ancora un esemplare locale collegato. L’estrazione non è lettura. Copie e testi estratti conservano hash e provenienza.

Tre letture integrali documentate nel nuovo ledger, con prosa, figure, note e riferimenti; schede e identità delle fonti restano nel vault privato. Sono chiusure effettive di questo incremento, non il totale delle letture pregresse; queste ultime si conservano e si riconciliano. Gli audit di dati, partiture originali e risultati sperimentali restano separati dalla lettura del paper. Le schede e la frontiera sono in `_notes/10-biblioteca/`; il piano comprende tutto il corpus, anche copie, scarti storici e opere senza chiave. Nessuna prosa del libro promossa. Il mandato e i conteggi in testa prevalgono sulle fotografie storiche sotto.

## Ripresa precedente: fonte guida Gaetani e provenienza del lavoro, 2026-10-08

Incremento successivo: due fonti locali Aebersold sono documentate in `_notes/20-ricerca/fonti-locali/aebersold/00-pratica-dorico-minore.md`, con contenuto L2 e limiti d'edizione. Il registro passa da 213 a 215; la bibliografia reale resta a 104 e le proposte esterne a 34. La selezione superiore J: copre 26 titoli e 11 aperture preliminari; inventario 891, percorsi collegati 156. La collazione visiva delle tavole selezionate di Gaetani è in `07-collazione-visiva-2026-10-08.md`, con risultato deterministico privato; restano aperti altri pentagrammi e tabelle. Il vault risolve 142 collegamenti nel nucleo controllato. Nessuna nuova prosa promossa; prossimo passo di ricerca: collazione delle altre armonizzazioni del volume guida e identificazione delle opere pertinenti nella frontiera delle citazioni.

Il facsimile del volume di Gaetani è stato fornito e il colophon conferma la prima edizione **dicembre 2019**, smentendo l'inferenza storica 2022 presente più sotto. Il registro privato usa ora `gaetani2019`, con anagrafica verificata e lettura contenutistica L2: OCR italiano 85/85 tavole e digest in `_notes/20-ricerca/fonti-locali/gaetani2019/`, con tabelle e pentagrammi ancora da collazionare integralmente. `.bib` reale 104 voci, registro 215 (213 prima dei due Aebersold), proposte esterne 34. La rettifica fondamentale, chiesta dall'autore: il suo appunto personale di lezione, par. 8, e la bozza continua D-E **contenevano già** dominante secondaria del II e doppio tritono; non attribuire al nuovo arrivo del PDF l'origine del ragionamento. La mappa privata `_notes/30-tesi/INTRECCIO-DELLE-TESI.md` e la collazione nella scheda della fonte conservano la provenienza. Freitas 2014 è propagato come L2 nel filone napoletana; cita Lewis 1939 e Lang 2009, il cui rapporto con Lang 1999 resta da verificare. Nessun movimento nuovo è stato aggiunto al manoscritto; prossimo incremento B01 dopo revisione. Il saggio sui modi resta obbligatorio nell'indice proposto. La sezione storica «fonte non ancora fornita» sotto è superata da questa nota.

> La fonte di verità su cosa è fatto resta `memory/index.md` e il work-log, non le spunte di questo file.

## Ripresa corrente: movimento B e vault privato, 2026-10-07

Crotch 1812 pp. 71-72 è stato verificato nel facsimile originale: `crotch1812` è la fonte primaria del nome della sesta napoletana citata da Lang 1999. Registro 208, proposte 29, `.bib` reale 103. La nota di Crotch sull'invenzione nazionale resta un'affermazione storica dell'autore, non una conclusione nostra; vedere `napoletana-confini.md`.

Dal commit utente `e0fca8c` il prossimo incremento del libro è diviso in B01, B02 e B03 sotto `_notes/40-libro/microstep/`. L'autore ha dato precedenza alla ricerca bibliografica estesa prima di rileggere i paragrafi. Il vault privato `_notes/` contiene ora protocollo, grafo di citazioni controllate, confronto delle pagine di cinque manuali locali e cassaforte delle nuove prove sotto `ricerca-estesa-2026-10-07/`. Il corpus J: è inventariato in sola lettura, 890 documenti nella fotografia iniziale; il registro ha **208 voci**, il `.bib` **103**. I PDF di Telesco e Gosden 2019 (e l'appendice di Gosden) e i passi decisivi di Persichetti 1961 sono stati letti a L2; l'XLSX Brown-Lee è riconciliato internamente, mentre partiture e MIDI restano da controllare per gli esempi destinati al libro. Il PDF locale di Fétis nominato “1844” è stato identificato dal frontespizio come nona edizione del 1867; la citazione 1844 è separata nel registro e resta da confrontare con l'originale. Il testo esatto di B01 aspetta la validazione dell'autore prescritta dalla regola di integrazione; nessuna nuova prosa è entrata nel `.lytex`. La bozza originale A-I e il saggio `modi_ionico_eolio_tonalita.docx`, destinato al libro, restano intatti. Le lacune della ricerca sono elencate nel protocollo privato, che guida la prossima sessione.

## Feature precedente (sostanzialmente conclusa): Bootstrap dell'ambiente e verifica della catena di build

Cosa faceva: rendere operativo lo stack deciso (ADR-003) installando l'ambiente e verificando che la catena `lilypond-book` -> LuaLaTeX produca un PDF, prima di entrare nella stesura vera.

Definition of done:

- [x] Installato l'ambiente: `scripts/setup-tex.ps1` (TinyTeX + pacchetti) e LilyPond sotto Program Files
- [x] `scripts/build.ps1` compila `sample/main.lytex` -> `build/main.pdf` senza errori
- [x] Verificata la resa di un esempio LilyPond e della microtipografia nel PDF (sample ~40 KB)
- [x] Avviata la stesura: introduzione del libro stesa da `_notes/40-libro/originali/INTRO.docx`; struttura modulare attiva
- [ ] Primo commit eseguito dall'utente e `sync-context` lanciata per ancorare i `017b02a` (ancora pendente; nel frattempo l'HEAD reale è avanzato di altri 4 commit non di stesura, vedi `memory/index.md`, nota drift)

Nota: la catena di build è verificata su Windows. La parità su Linux (`scripts/*.sh`) è implementata ma non ancora collaudata su una macchina Linux. Font definitivo (Libertinus) e stile bibliografico (`authoryear`) restano da confermare alla prova del PDF con contenuto reale.

## Feature attiva: Bibliografia del libro e ricerca per la nuova tesi sul tritono

Cosa fa: due filoni distinti, entrambi avviati il 2026-07-16 su richiesta esplicita dell'utente.

**Filone 1, bibliografia da libri posseduti - sostanzialmente concluso**: `doc-ingest` + `book-bib-extract` (entrambi in `tools/` e `.claude/skills/`, non ancora tracciati in git) hanno popolato `manuscript/bib/references.bib` (83 voci `@book`) e il registro `_notes/book-bib-registry.json` (152 voci: 86 verificate, 58 da-verificare con nota che documenta il limite pratico raggiunto per ciascuna, 8 scartate). Dettagli completi in `memory/progress.md` (voci del 2026-07-16) e ADR-005 in `memory/decisions.md`. Resta fuori scope la fase `book-digest` (libro -> skill), mai iniziata.

**Filone 2, ricerca per la nuova tesi sul tritono - ricerca conclusa, in attesa della fonte primaria fisica**: lo scope, chiarito dall'utente il 2026-07-17, era entrambe le vie: ricognizione sui libri già posseduti e ricerca accademica esterna. Entrambe sono state condotte e fissate in note private:

- Ricognizione interna (29 libri del corpus `armonia-teoria`): scansione deterministica con `pdftotext` + lettura visiva mirata (via `pdftoppm`) dei 6 libri risultati scansioni senza testo nativo. Risultato in `_notes/20-ricerca/ricognizioni/tritono-ricognizione-interna.md`: trattazione storico-dialettica solida in Piston (*Harmony*, *Counterpoint*, *Armonia*-EDT, tutti con citazione diretta di "diabolus in musica") e trattazione indiretta in Schoenberg (*Structural Functions of Harmony*, via le "vagrant harmonies"); trattazione solo funzionale/jazz in Kostka, Levine, Berkman, Mulholland, Blatter, Beato, Wyatt&Schroeder; assente in Piston *Orchestration* e in un gruppo di manuali minori.
- Ricerca esterna (skill `deep-research`, poi verifica manuale mirata via `WebFetch` per contenere il costo dopo due rate-limit consecutivi dell'harness): risultato in `_notes/20-ricerca/ricognizioni/tritono-ricerca-esterna-stato.md`. Trovamento centrale: il "divieto ecclesiastico medievale del tritono come diabolus in musica" è un mito storiografico moderno, non un fatto medievale - l'espressione risale a Fux, *Gradus ad Parnassum* (1725), uso tecnico-pedagogico, poi retroattivamente attribuita al medioevo nell'Ottocento (Ambros, 1880); confermato con citazione diretta dal musicologo di Harvard Thomas Forest Kelly. Anche il confronto strutturale sesta-eccedente/sostituzione-di-tritono (Biamonte, *Music Theory Online* 14.2, 2008) è confermato con citazione diretta. Restano due dettagli minori non recuperati (Babbitt 1960, Vicentino 1555: fonte ResearchGate bloccata da un HTTP 403), a bassa priorità.

La fonte primaria del libro, "La dialettica del tritono" di Mariano Gaetani, è stata identificata (ISBN 8869244857, editore probabile Edizioni Simple, anno probabile 2022 secondo un articolo del *Resto del Carlino* su una presentazione pubblica - non ancora il colophon) e registrata in `_notes/book-bib-registry.json` (voce `manual-isbn-8869244857`, citekey `gaetani2022`, `bib_status: da-verificare`). L'utente non ha ancora consegnato il contenuto/appunti cartacei annunciati: nessun contenuto su questa fonte è stato inventato, resta da trattare quando arriva.

File coinvolti finora (privati/ignorati, tranne i tre script e la skill):

```
tools/doc-ingest.py                          script di ingestione (istanziato da template)
tools/extract-titlepages.py                  estrazione standardizzata frontespizi (Poppler)
tools/render-bib-registry.py                 rigenera book-bib-registry.md dal JSON
.claude/skills/book-bib-extract/SKILL.md     skill di estrazione bibliografica (istanziata da template)
_notes/book-bib-registry.json                registro di stato (privato, 153 voci)
_notes/book-bib-registry.md                  tabella leggibile rigenerata dal registro (privato)
_notes/20-ricerca/ricognizioni/tritono-ricognizione-interna.md       nuovo, esito ricognizione sui libri posseduti (privato)
_notes/20-ricerca/ricognizioni/tritono-ricerca-esterna-stato.md      nuovo, esito ricerca esterna + lezione di costo (privato)
manuscript/bib/references.bib                bibliografia reale del libro (privato)
```

Domande aperte:

Se aggiornare la sezione "Precondizione" di `book-bib-extract/SKILL.md` per riflettere il metodo di verifica visiva del colophon invece del mirror Markdown (ADR-005) - segnalato all'utente, non ancora deciso. Se e quando riprendere le 58 voci `da-verificare` residue del filone 1 (limite pratico raggiunto, non priorità immediata). Se e quando recuperare i due dettagli minori bloccati su ResearchGate (Babbitt, Vicentino). Quando iniziare a scrivere la sezione/capitolo del libro sul tritono: in attesa della fonte primaria fisica (Gaetani) o già con il materiale raccolto finora - non ancora deciso con l'utente.

## Feature aggiunta il 2026-07-24: stesura del capitolo sul tritono in prosa continua (stato storico)

Su richiesta dell'utente il capitolo sul tritono è stato riscritto dal formato report (indice più otto punti numerati) al formato capitolo di libro continuo, senza sottotitoli, con voce "Marcato" che rompe la quarta parete (lettore interpellato con "voi", confessione dell'autore-ingegnere) e con l'ambizione dichiarata di costruire un impianto universale per leggere tutta l'armonia occidentale a partire dal tritono. Bozza completa e validata movimento per movimento (arco A-I) in `_notes/40-libro/bozze-autore/capitolo-tritono-continuo.md`. Il `.docx` sorgente resta intatto come backup del report. Il 2026-07-24 il `.docx` continuo è stato assemblato con uno script deterministico (`capitolo-tritono-continuo.docx`: prosa continua A-I, sei figure riusate ai segnaposto, riferimenti [1]-[10] con la nuova voce web Springsteen verificata via oEmbed), e le sei figure sono state rirenderizzate con le annotazioni in font Libertinus Sans (Emmentaler invariato per le note; sorgenti `.ly` durevoli in `_notes/40-libro/bozze-autore/_ly-figure/`). Prossimo passo: trascrizione fedele in `manuscript/chapters/NN-...lytex` con `\input` in `main.lytex` e build, quando l'utente dà il via; resta in standby l'apertura biografica (Gaetani). Il quadro completo (voce, correzioni, direzioni future, risorse pending) è in `_notes/RESUME-PROMPT.md`; i dettagli di tracciamento nelle voci del 2026-07-24 di `_notes/40-libro/tracciamento-fonti-libro.md`; la risoluzione teorica frigio e le direzioni future nella `_notes/30-tesi/cassaforte-capitolo-tritono.md`.

## Feature attiva aggiunta il 2026-07-29: la fase "libro -> skill", entrambe le accezioni

Su richiesta esplicita dell'utente si è affrontata la fase mai avviata "libro -> skill", che nel progetto aveva due letture possibili. L'utente le ha volute entrambe, in quest'ordine, con un obiettivo dichiarato oltre alla stesura: usare le skill risultanti anche per cercare fonti nuove fuori dai libri posseduti, su forum, community, video e pareri di esperti. L'ordine non è arbitrario, perché la dottrina del proprio libro definisce cosa cercare e rende mirata la seconda fase.

Prima accezione, conclusa: `.claude/skills/armonia-libro/`, il digest della dottrina del libro dell'utente. Contiene `SKILL.md`, `tesi.md` (tritono identificatore, doppia eredità, lettura del frigio, e le tre affermazioni dichiarate come intuizione e non teorema), `voce.md` (prosa continua, voce Marcato, vincoli di stile e di intervento, flusso a quattro passi), `capitoli/01-tritono.md` (arco A-I movimento per movimento), `fatti-verificati.md` (distingue confermato con citazione diretta, confermato per voto, confutato e da non usare), `fonti.md` (mappa citekey e le due anomalie da risolvere alla trascrizione in LaTeX) e `agenda-ricerca.md`.

Due anomalie bibliografiche emerse costruendo la skill: il riferimento [8] del capitolo continuo copre due fonti Sarti distinte, le slide `sarti2018tonal` e la trascrizione della lezione CMRM2018, che non ha una voce propria nel registro e va risolta prima dei movimenti G e H. Il riferimento [10], la video-intervista di Springsteen, mancava allora nel registro e nel `.bib`; è stato registrato nel 2026-10-07.

Seconda accezione, avviata con un pilota: installata la skill `book-digest` dal template, scritto `tools/probe-pdf-text.py` e prodotta la triage dei 30 PDF di `ARMONIA E TEORIA` in `_notes/20-ricerca/corpus-digest-triage.md`. Digerito il primo libro, Berkman 2013, in `.claude/skills/libro-berkman/`; la sua voce di registro è passata a `skill_status: done`. Restano 153 voci `pending`.

Decisione strutturale: ADR-007. Dentro `.claude/skills/` convivono tre classi, le skill di tooling tracciate, `armonia-libro/` ignorata e `libro-*/` ignorate da glob, perché la dottrina è contenuto del libro (ADR-004) e i digest sono materiale derivato da opere protette. Conseguenza operativa: le due cartelle non hanno remoto git e vanno incluse nel backup su SSD portatile già in uso per `manuscript/`.

Rilievo metodologico da conservare, perché correggeva un'ipotesi sbagliata: la qualità del testo estraibile da un PDF non si misura né dal conteggio di caratteri né su un campione delle prime pagine. I frontespizi sono tipografia decorativa che l'OCR rende male anche su volumi puliti, e `Jazz Theory (1995, M.Levine).pdf` ne è il caso concreto, illeggibile in testa e integro a metà volume. Lo strumento campiona quindi a metà libro e affianca all'indice di qualità la densità di caratteri per pagina, che separa i libri di prosa da quelli di sola notazione.

Costo misurato del pilota, che serve a dimensionare il lotto successivo: 448 KB di testo, circa 112 mila token di sola lettura, per un libro di 215 pagine, con un digest risultante di 96 KB.

Domande aperte di questa feature. Quali libri digerire nel prossimo lotto, dato che la selezione per rilevanza conta più della disponibilità: i candidati con testo pulito e alta rilevanza sono Mulholland 2013, Blatter, Berklee Jazz Composition, Kostka e Levine 1995. Se e quando affrontare i libri scansionati ad alta rilevanza, cioè i Piston e Schoenberg, che restano sulla via visiva mirata di ADR-006 o richiedono una copia migliore del PDF, che l'utente si è offerto di procurare. Se estendere il lavoro al corpus `CHITARRA`, 169 PDF, che è una decisione separata.

## Feature chiusa il 2026-08-05: rigenerazione di `armonia-libro` e sanatoria delle note stale

Ciclo breve, senza contenuto nuovo nel libro. `python tools/skill-freshness.py` segnalava una fonte cambiata per `armonia-libro`, e la segnalazione in se era rumore, perché l'utente aveva solo tolto degli a capo dalla cassaforte. Controllando le date e emerso il difetto vero, che è di procedura: il manifesto dichiarava `generated: 2026-08-03` mentre nessun file di contenuto della skill era stato riscritto dopo il 2026-07-31, perché `--update` era stato lanciato senza rigenerare. Sette fonti su tredici si erano mosse in mezzo, e la skill contraddiceva una fonte canonica, presentando ancora come intuizione la corrispondenza fra scale e coppie di tritoni che `tritoni-scale.py` aveva smentito.

Rigenerata la skill per intero salvo `voce.md`, riletta e confermata invariata. Aggiunti al manifesto `tools/tritoni-scale.py` e `tools/derivazione-scale.py`, perché la skill ne riporta i risultati come fatti calcolati e per ADR-009 le definizioni che implementano sono contenuto del libro. Scritto in `SKILL.md` e nel manifesto il vincolo d'ordine, cioè che `--update` si lancia solo dopo aver rigenerato. Verifica: `fresca: 15 fonti invariate`, exit code 0.

Sanata una discrepanza fra note canoniche. L'intestazione della voce 19 della cassaforte e `_notes/00-regia/STATO-CAPITOLO-TRITONO.md` dichiaravano ancora non applicato il quadro a sette gradi, mentre il capitolo lo contiene dall'ottavo passo del 2026-08-03. Corrette entrambe, con i tre addenda della voce 19 che portavano una classificazione a tre casi superata dalla correzione dell'utente a due. Riscritto `_notes/00-regia/COME-SI-USA.md` con i conteggi verificati e un quinto strato che mancava, cioè `.claude/`, più la precisazione che dieci skill su quattordici non sono invocabili dall'agente.

Nota per chi riprende: la sezione precedente di questa scheda dice che il quadro a sette gradi non è applicato. È stale, ed è superata da questa voce. Il capitolo lo contiene.

## Feature attiva aggiornata il 2026-08-03: maturazione del capitolo sul tritono

Il ciclo dal 2026-07-29 al 2026-08-03 ha portato il capitolo sul tritono da bozza validata a bozza matura, e ha costruito attorno ad esso l'infrastruttura che serviva. Il quadro completo, con la guida alla rilettura e l'elenco dei paragrafi cambiati, e in `_notes/00-regia/STATO-CAPITOLO-TRITONO.md`; la storia in `_notes/RESUME-PROMPT.md`, nota del 2026-08-03.

Il capitolo. Nove movimenti, 48314 caratteri, 90 paragrafi nel docx, sei figure, tredici riferimenti. Markdown e docx allineati, con otto backup datati in `_backup/`. Proporzioni: i movimenti D ed E, che sono il nucleo originale dell'autore, valgono il 38,9 per cento contro il 25 del 2026-07-31; il movimento G, storico, e scesa al 13,3. Il movimento E, al 22 per cento, e ormai il più lungo di parecchio, e se crescera ancora conviene valutare se spezzarlo.

Che cosa e entrato nel capitolo, tutto su validazione esplicita dell'utente: Yavorsky nel movimento C, che estende il precedente storico a una genealogia Choron-Fetis-Yavorsky; la dichiarazione al lettore su dove l'autore ha compagnia e dove e solo, in apertura di D; la catena di quinte come chiave di lettura e la tabella a sei operazioni in D, con la comparsa della napoletana; il test della doppia eredita e il contatore dei tritoni in E; la testimonianza di Jacques de Liege sul semitritono nei canti piani ecclesiastici in G, che porta quel movimento da un argomento per assenza a una testimonianza contraria; e la chiusura sulle due dissonanze che fanno una consonanza.

L'infrastruttura. Tre skill nuove: `armonia-libro` e `libro-berkman`, ignorate da git per ADR-007 perché sono contenuto, e `fonte-nuova`, tracciata perché e procedura. Quattro strumenti Python tracciati sotto `tools/`: `skill-freshness.py`, `probe-pdf-text.py`, `tritoni-scale.py`, `derivazione-scale.py`. Due ADR nuovi: ADR-008 sui quattro livelli di verifica di una fonte, ADR-009 sugli strumenti che implementano il contenuto del libro e sul primato delle definizioni del libro.

La bibliografia. Da 91 a 101 voci in `manuscript/bib/references.bib`. Registro a 172 voci in `_notes/book-bib-registry.json`, di cui 96 verificate. Tredici voci del corpus portano ora un campo `skill_blocker` che dichiara perché non sono digeribili. Dieci PDF durevoli in `_notes/20-ricerca/fonti-esterne/`.

Domande aperte di questa feature. Quando trascrivere il capitolo in `manuscript/chapters/`, che resta il passo più urgente. Se e come spezzare il movimento E, oggi al 22 per cento. Quando aprire l'analisi del livello II della macchina, calcolata e registrata nella voce 18 della cassaforte. Il risultato 4 della voce 14, cioè i tre tipi di coppia di tritoni, calcolato e mai proposto perché toccherebbe i movimenti F e H insieme. Come sciogliere i due nodi bibliografici prima di LaTeX, cioè il riferimento [8] su due fonti Sarti distinte e la fonte Springsteen senza voce nel registro. E i sei ragionamenti ancora "da proporre" in `_notes/30-tesi/ragionamenti-da-portare-nel-libro.md`.

In attesa dall'utente: il materiale privato sulla scala napoletana, annunciato e non consegnato, che sblocchera l'espansione della tabella con armonizzazioni e riflessioni.

## Ripresa operativa del 2026-10-07

Il movimento A della bozza continua sul tritono è ora incluso in `manuscript/chapters/01-tritono.lytex`, con `\input` nel main privato e due citazioni verificate nei sottotitoli dei video di Bennett e Springsteen. Le parafrasi sono state ristrette a ciò che i segmenti sostengono; l'originale Markdown e DOCX è intatto. Il prossimo pezzo è il movimento B, da confrontare con bozza, figure, citazioni e ragionamenti collegati. Sarti [8] riguarda G e H. La procedura è in `.claude/context/research-method.md` e il dettaglio in `_notes/20-ricerca/ricognizioni/ricerca-armonia-2026-10-07.md`. Il preflight trova 103 voci bibliografiche, due citekey usate e due capitoli non inclusi, uno scheletro e una introduzione legacy. I due studi percettivi e il controllo storiografico sono ancora nell'inbox, senza promozione nel `.bib`. L'indice privato `_notes/00-PERCORSO-LIBRO.md` ordina ora i materiali senza romperne i percorsi; `_notes/40-libro/percorso-libro/` contiene la scheda napoletana, lo stato aggiornato delle otto decisioni del dossier e il flusso editoriale. `modi_ionico_eolio_tonalita.docx` deve far parte del libro, ma la sua collocazione non è ancora decisa. Gli appunti cartacei dell'autore sulla napoletana sono ancora attesi.

## Riconciliazione

Ultima verifica: 2026-08-03, ancorata a `dd1c4d5` a mano e non tramite `sync-context`. La quasi totalita del lavoro di questo ciclo vive in file privati e ignorati, sotto `_notes/` e nelle due skill di contenuto; la parte tracciata sono i quattro strumenti in `tools/`, la skill `fonte-nuova`, i due ADR nuovi e queste schede. `covers-paths` e stata estesa a `tools/**` e `.claude/skills/**`, che prima non erano coperte da nessuna scheda.
