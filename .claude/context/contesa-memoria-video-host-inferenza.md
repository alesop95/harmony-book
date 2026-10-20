---
generated-date: 2026-10-20
covers-paths: []
related-paths:
  - tools/isolated-ollama-host.py
  - tools/local-reading.py
last-verified-commit: 9480ad1
verification-scope: segnalazione esterna, nessuna verifica del codice o dell'host
---

# L'host di inferenza ha ripreso a usare la scheda, e ora la memoria video si contende

> Scheda aggiunta il 2026-10-20 da una sessione di un altro progetto, su richiesta del proprietario. Non contiene contenuti di questo progetto e non tocca i suoi strumenti: riporta un cambiamento dell'host condiviso che cambia le condizioni in cui il servizio isolato parte.

## Che cosa è cambiato

Dal riavvio della macchina del 15/10/2026 alle 12:20 il servizio di inferenza sempre acceso dell'host, quello che ascolta sulla rete, serviva sul processore: era partito prima che lo stack del driver fosse pronto e, poiché interroga le schede una volta sola all'avvio, aveva tenuto quella scelta per cinque giorni. Il 20/10/2026 alle 10:49 è stato riavviato ed è stato aggiunto alla sua configurazione un passo di attesa dello stack del driver, perché la corsa non si ripeta. La misura prima e dopo, su un modello denso da 14,8 miliardi di parametri: da 1,91 a 43,99 parole al secondo, caricamento da 105,89 a 3,99 secondi, memoria video occupata da zero a 10,12 GB.

## Perché riguarda il servizio isolato di questo progetto

Finché il servizio condiviso macinava sul processore non occupava memoria video, e un'istanza isolata trovava la scheda libera. Da oggi non è più così: la scheda ha circa 16 GB, un modello denso da quattordici miliardi ne occupa 10,12, e il servizio condiviso tiene il modello residente per cinque minuti dopo l'ultima richiesta, che è il valore predefinito della sua configurazione. Due modelli di quella taglia non ci stanno insieme.

Ne discende che un avvio dell'istanza isolata può trovare memoria insufficiente e ripiegare sul processore senza dichiararlo, cioè esattamente la condizione che la disciplina di questo progetto chiede di misurare invece di presumere. La verifica già prevista, cioè leggere la memoria video occupata dopo il caricamento, resta quindi necessaria e diventa discriminante: un modello caricato con memoria video a zero significa che si sta lavorando sul processore.

Due mitigazioni, entrambe dal lato di chi chiama e nessuna delle quali tocca servizi condivisi, cosa che la decisione del 2026-10-14 vieta. La prima è passare esplicitamente la durata di permanenza nella richiesta invece di lasciare il valore predefinito, così la memoria si libera subito dopo l'uso. La seconda è verificare la memoria video libera prima di avviare l'istanza isolata, e rinviare invece di partire in una condizione che poi degrada in silenzio.

## Che cosa non cambia

Il motivo per cui questo progetto usa un'istanza propria non era l'accesso alla scheda ma l'assenza di tracce, stabilita dalla decisione del 2026-10-14. Quel motivo resta intatto: anche con il servizio condiviso ora accelerato, passarci il contenuto significherebbe lasciare metadata di richiesta nel giornale dell'host e rinunciare alle garanzie di cgroup, inibitore di sonno e temporanei in memoria che l'istanza isolata verifica prima di partire.
