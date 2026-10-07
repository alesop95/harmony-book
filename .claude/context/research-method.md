# Ricerca accademica per il libro di armonia

Questa è una revisione narrativa mirata ai problemi del libro. Il corpus già posseduto viene esaminato prima di cercare all'esterno. Ogni nuova ricerca parte da una proposizione formulata con precisione, dal punto del manoscritto che ne dipende e dal limite delle fonti già registrate. La ricerca non si dichiara sistematica né esaustiva senza un perimetro, uno screening completo e un criterio di arresto documentati.

## Unità di lavoro

Si lavora su un nodo concettuale alla volta. La scheda privata del nodo registra: domanda; proposizione del libro; definizioni operative; evidenza interna; query e data; candidati inclusi, esclusi e sospesi con motivo; pagine effettivamente lette; controesempi; legami con gli altri nodi; conseguenza editoriale; stato. La risposta di una fonte a una domanda diversa non viene trasferita automaticamente alla proposizione in esame.

La distinzione fondamentale è fra identità intervallare, funzione armonica, condotta delle voci, provenienza storica e risposta percettiva. Due accordi possono condividere le stesse classi di altezze e avere funzioni diverse nel contesto. Una dimostrazione combinatoria può stabilire quali strutture siano possibili nel modello scelto; non dimostra da sola frequenza nel repertorio, udibilità o priorità storica.

## Catena della prova

`_notes/book-bib-registry.json` resta il registro anagrafico con il grado di verifica; `manuscript/bib/references.bib` resta l'export tipografico privato. La procedura `fonte-nuova` governa l'ingresso di una fonte e la sua conferma prima del `.bib`. Le schede private conservano il passaggio fonte-pagina-proposizione-limite; `_notes/ragionamenti-da-portare-nel-libro.md` conserva le inferenze originali e il loro stato; le cassaforti conservano la relazione con il capitolo. Un indice di stato deve riportare anche l'esito di ogni passaggio, non solo un rimando al dettaglio.

Per storia della teoria si cerca il testo originale quando la datazione o la paternità è parte della tesi. Per analisi armonica si confrontano definizioni, riduzioni e casi musicali reali. Per la tesi di derivazione si dichiarano le ipotesi della macchina, si generano tutti i casi entro il perimetro e si cercano casi che la smentiscano. Per le asserzioni percettive si distinguono studi sperimentali e analisi teoriche, annotando stimoli, partecipanti, compiti e stile musicale. Una fonte di psicologia dell'ascolto non prova automaticamente una genealogia teorica.

## Scrittura e conservazione

Il capitolo usa una voce continua e accessibile. La profondità scientifica sta nelle distinzioni verificabili, negli esempi notati e nelle cautele locali, senza trasformare la prosa in un rapporto di ricerca. Il materiale che non è ancora pronto resta in una scheda con stato esplicito; la promozione in `manuscript/` avviene per un movimento o un nodo alla volta e lascia una traccia dalla bozza, dalle fonti e dai ragionamenti al testo finale. Prima e dopo ogni promozione si confrontano struttura, figure, citazioni e pendenze. Nessuna bozza viene eliminata come effetto collaterale della trascrizione.

Il controllo `python tools/check-book.py` verifica collegamenti `\input`, file `.bib`, citekey duplicate e citazioni nei sorgenti inclusi; segnala i capitoli non inclusi. È un controllo preliminare: la build e la lettura del PDF restano necessarie, e un capitolo ancora in Markdown non risulta presente nel libro per questo solo fatto.
