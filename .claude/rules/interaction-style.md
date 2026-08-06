# Stile di interazione e di documentazione tecnica

> Regola modulare, da caricare sempre. Codifica lo stile descritto nella sezione 8 di `PROJECT-SYSTEM.md`, così da renderlo vincolante per ogni sessione invece di affidarlo alla memoria. Vale per la documentazione prodotta e per il modo di rispondere.

## Destinatario e registro

La comunicazione si rivolge a un lettore tecnico esperto e va scritta come ci si rivolgerebbe a un responsabile tecnico: diretta, chiara, esaustiva, senza ridondanza. Si preferisce spiegare una cosa una volta sola, in modo descrittivo, senza dare per scontato nemmeno il semplice, e senza ripeterla altrove.

## Impianto del testo

L'impianto è discorsivo. I concetti vengono prima inquadrati architetturalmente, poi approfonditi con estratti di codice annotati, infine collegati ai flussi con paragrafi di raccordo. Non si usano elenchi puntati nella prosa, non si usano emoji, non si usa il grassetto nella prosa. I termini chiave densi si marcano in corsivo. Le keyword di codice dentro i blocchi sintattici si marcano in grassetto. I frammenti di codice e di configurazione stanno in blocchi monospazio. Gli alberi del filesystem si mantengono come blocchi preformattati con indentazione.

## Convenzioni tipografiche

Gli acronimi si spiegano in note a piè di pagina numerate, per non interrompere il discorso con parentesi inline. Non si usano i trattini lunghi: sono ammessi solo i trattini brevi.

## Convenzione della sorgente Markdown

Ogni paragrafo sta su una sola riga sorgente, senza andare a capo a una colonna fissa: la riga finisce dove finisce il paragrafo, e sono i paragrafi a essere separati da una riga vuota. Vale per tutti i file Markdown tracciati del progetto, ed è stata applicata all'intero albero dal commit `9f5420b` del 2026-08-06; la regola è scritta qui il giorno stesso, perché fino a quel momento viveva solo nel messaggio di commit e sarebbe stata dimenticata alla sessione successiva, producendo un albero misto e diff di sola riformattazione.

Le due ragioni. Un diff diventa leggibile per paragrafo invece di frammentarsi su righe arbitrarie, così si vede che cosa è cambiato nel discorso e non dove si è spostato un a capo. E una modifica puntuale a un paragrafo non richiede di reimpaginare quelli vicini, che è la causa tipica dei diff enormi e vuoti.

Restano fuori dalla convenzione, perché la riga vi è significativa, i blocchi di codice e preformattati, gli alberi del filesystem, le righe di tabella e gli elementi di elenco di un file che li usa già. I file `.md` sotto `_notes/` sono materiale di lavoro storico e non si riformattano in blocco: si adegua il testo nuovo e si lascia stare il resto.

La convenzione non si applica a mano: lo strumento è `tools/md-unwrap.py`, che toglie gli a capo interni a un blocco di testo unendo i pezzi con un singolo spazio e non normalizza nient'altro, con `--check` e `--diff` per vedere cosa farebbe prima di scrivere. Quando la libreria `markdown-it-py` è disponibile, ogni file passa da un oracolo di rendering che pretende un HTML normalizzato identico prima e dopo, e se divergono il file non viene scritto. I blocchi recintati restano intatti per contratto, ed è la ragione per cui il formato dei comandi di shell ha un controllo separato, `tools/lint-md-commands.py`, descritto in `git-commands-format.md`.

## Onestà del contenuto

Non si presenta mai come fatto un contenuto inferito, speculativo o non verificato. Ciò che non è verificabile va etichettato come tale, e ciò che non si conosce va dichiarato invece di essere riempito per ipotesi. Le inferenze non confermate si marcano esplicitamente come da verificare e si promuovono a fatto solo quando una fonte le conferma.
