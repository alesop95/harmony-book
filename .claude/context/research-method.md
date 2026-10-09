# Ricerca accademica per il libro di armonia

## Analisi locale e attestazione della lettura

Il lettore `tools/local-reading.py` preserva unità integrali e localizzatori, propone digest, glossario, archi fra concetti e riferimenti attraverso un modello locale e controlla che le evidenze esistano nella specifica unità. Le schede automatiche sono esplicitamente non revisionate: un ancoraggio letterale non verifica ogni interpretazione, completezza, attribuzione storica o notazione. OCR, trascrizioni e digest non promuovono livelli di lettura. La revisione torna ai facsimili, agli esempi ascoltati e ai passi completi; i riferimenti estratti alimentano una frontiera, senza attestare lettura delle destinazioni. Risultati e configurazione rimangono nel livello privato del progetto; il vincolo sui residui dell'host di inferenza è verificato prima dell'invio dei testi.

## Fonti di comunità: accesso e unità di citazione

Al primo 403 caricare `fonti-non-recuperabili` e consultare il pacchetto `community-sources` già istanziato; il lettore è `.claude/templates/community-sources/tools/fetch-reddit.py`. Il comando `python tools/fetch-community.py post <URL-o-ID>` conserva testo e albero d’archivio nel livello privato. Un fallimento dell’accesso diretto non esaurisce la via d’archivio. Annotare autore, permalink, date di pubblicazione e cattura disponibili, data di download, hash e lacune. Il download non certifica lettura; la completezza dello snapshot non certifica il sito vivo o i rinvii.

Una voce di forum individua il commento che viene citato; L1 si riferisce a quella unità precisa. Il contesto e le risposte contrarie si conservano insieme, e ogni diversa attribuzione richiede il proprio localizzatore. Il testo del forum documenta una testimonianza o un argomento: le conclusioni storiche, teoriche, percettive e le frequenze richiedono fonti o verifiche autonome. Rinvii a paper e libri alimentano la frontiera, senza attestare la loro lettura. I dettagli del corpus e le informazioni personali restano privati.

## Estensione del mandato, 2026-10-08

L'autore richiede ora lettura integrale di tutte le fonti, disponibilità durevole delle informazioni e bibliografia sempre aggiornata; roadmap, indice e nuova scrittura seguono la sintesi della ricerca. Il perimetro, il protocollo e la coda di lettura sono privati in `_notes/10-biblioteca/`. La lettura mirata per claim descritta sotto rimane utile per ordinare e collegare il lavoro, ma non esaurisce il nuovo mandato. L'estrazione tecnica non conta come lettura; le attestazioni pregresse restano conservate. L'autorizzazione corrente copre l'inserimento delle anagrafiche verificate nel `.bib`, senza conferma per ciascuna voce. Fonti soltanto segnalate e metadati incerti restano candidati; nessun contenuto viene attribuito a una fonte non letta.

Questa è una revisione narrativa mirata ai problemi del libro. Il corpus già posseduto viene esaminato prima di cercare all'esterno. Ogni nuova ricerca parte da una proposizione formulata con precisione, dal punto del manoscritto che ne dipende e dal limite delle fonti già registrate. La ricerca non si dichiara sistematica né esaustiva senza un perimetro, uno screening completo e un criterio di arresto documentati.

## Unità di lavoro

Si lavora su un nodo concettuale alla volta. La scheda privata del nodo registra: domanda; proposizione del libro; definizioni operative; evidenza interna; query e data; candidati inclusi, esclusi e sospesi con motivo; pagine effettivamente lette; controesempi; legami con gli altri nodi; conseguenza editoriale; stato. La risposta di una fonte a una domanda diversa non viene trasferita automaticamente alla proposizione in esame.

La distinzione fondamentale è fra identità intervallare, funzione armonica, condotta delle voci, provenienza storica e risposta percettiva. Due accordi possono condividere le stesse classi di altezze e avere funzioni diverse nel contesto. Una dimostrazione combinatoria può stabilire quali strutture siano possibili nel modello scelto; non dimostra da sola frequenza nel repertorio, udibilità o priorità storica.

## Catena della prova

`_notes/book-bib-registry.json` resta il registro anagrafico con il grado di verifica; `manuscript/bib/references.bib` resta l'export tipografico privato. La procedura `fonte-nuova` governa l'ingresso di una fonte e la sua conferma prima del `.bib`. Le schede private conservano il passaggio fonte-pagina-proposizione-limite; `_notes/30-tesi/ragionamenti-da-portare-nel-libro.md` conserva le inferenze originali e il loro stato; le cassaforti conservano la relazione con il capitolo. Un indice di stato deve riportare anche l'esito di ogni passaggio, non solo un rimando al dettaglio.

Per storia della teoria si cerca il testo originale quando la datazione o la paternità è parte della tesi. Per analisi armonica si confrontano definizioni, riduzioni e casi musicali reali. Per la tesi di derivazione si dichiarano le ipotesi della macchina, si generano tutti i casi entro il perimetro e si cercano casi che la smentiscano. Per le asserzioni percettive si distinguono studi sperimentali e analisi teoriche, annotando stimoli, partecipanti, compiti e stile musicale. Una fonte di psicologia dell'ascolto non prova automaticamente una genealogia teorica.

## Scrittura e conservazione

La conferma corrente dell'autore fissa la sequenza: completare la lettura del corpus e dei riferimenti pertinenti, sintetizzare e consolidare roadmap e indice, poi riprendere la scrittura. Ogni pezzo viene proposto e approvato nel suo testo esatto qui in chat prima di inserirlo nel manoscritto. Il messaggio originale, le decisioni e i ragionamenti rimangono conservati nel livello privato insieme alle relazioni tra concetti. La roadmap corrente è `_notes/00-regia/ROADMAP-LETTURA-COMPLETA.md`; il censimento locale comprende tutti i formati e si legge in `_notes/10-biblioteca/CORPUS-ARMONIA.md`.

Il capitolo usa una voce continua e accessibile. La profondità scientifica sta nelle distinzioni verificabili, negli esempi notati e nelle cautele locali, senza trasformare la prosa in un rapporto di ricerca. Il materiale che non è ancora pronto resta in una scheda con stato esplicito; la promozione in `manuscript/` avviene per un movimento o un nodo alla volta e lascia una traccia dalla bozza, dalle fonti e dai ragionamenti al testo finale. Prima e dopo ogni promozione si confrontano struttura, figure, citazioni e pendenze. Nessuna bozza viene eliminata come effetto collaterale della trascrizione.

Il controllo `python tools/check-book.py` verifica collegamenti `\input`, file `.bib`, citekey duplicate e citazioni nei sorgenti inclusi; segnala i capitoli non inclusi. È un controllo preliminare: la build e la lettura del PDF restano necessarie, e un capitolo ancora in Markdown non risulta presente nel libro per questo solo fatto.


## Lettore: recuperi e corpora aggiuntivi, 2026-10-09

Configurazione privata `additional_corpora` per accodare inventari con lo stesso schema; gli hash mantengono le identità. `source_overrides.processing_pdf` indica una copia derivata privata, il suo SHA-256 e il manifest di trasformazione: hash derivato e originale verificati prima dell'acquisizione, provenienza nelle unità. Un collegamento può avere una cartella risolta e verificata; non viene eseguito né dichiarato letto il suo contenuto.

Il rendering conserva schede non valide senza eccezione su localizzatori mancanti e mostra gli errori. La prova privata `verify-reader-recovery-2026-10-09.py` usa una scheda fallita reale, riproduce il vecchio arresto, conserva SHA-256/output e verifica che l'ancora inesistente resti respinta. Per segmenti ASR molto brevi l'evidenza può coincidere con l'intero segmento non vuoto anche sotto15 caratteri; la sottostringa breve di un testo lungo rimane non valida. Sono controlli di provenienza letterale, non di validità dell'interpretazione. La revisione di fonte, figure, notazione e ascolto rimane necessaria.
