---
generated-from-commit: 017b02a
generated-from-branch: main
generated-date: 2026-06-15
covers-paths: []
last-verified-commit: 017b02a
---

# Test di sviluppo

## Risposta strutturata su segmenti brevi, 2026-10-09

Osservato un superamento del limite di risposta su 25 segmenti ASR per soli 917 caratteri. La guardia basata soltanto sulla lunghezza lasciava il blocco indivisibile e fermava il batch. La prova sul checkpoint reale divide in 12 e 13 segmenti, conserva il padre e ricostruisce tutti i frammenti nell'ordine originale; la vecchia condizione riproduce l'impedimento. Il riavvio effettivo ha prodotto una nuova scheda valida su una delle parti, mentre prosegue sull'altra. Output limitato o interrotto non viene accettato come scheda; livelli di lettura e interpretazioni restano da revisionare. Checkpoint e prova dettagliata rimangono privati.



## Difetti osservati nell’acquisizione, 2026-10-09

Tre scansioni reali leggibili producevano zero parole nel lettore: ora la prova recupera termini visibili e il ritorno al formato difettoso su una copia la fa fallire. Intestazione TSV verificata, profilo di cache versionato e pagine vecchie riacquisite. È stata inoltre osservata una conclusione falsa dopo interruzione del trasporto: il checkpoint con errori e porzioni pendenti ora restituisce stato incompleto, e la mutazione del controllo riproduce la falsa conclusione. SQLite è stato rilasciato per pagina dopo un lock reale, prima di attendere processi OCR esterni; il modello riusa solo schede con hash ed evidenze ancora validi. Misure e casi sono privati in `00-regia/lettura-locale/`.

## Controllo reale degli ancoraggi e della copertura

Verificato il corpus preparato: ricostruite 6.691 unità non vuote e 11.734.806 caratteri da tutte le porzioni foglia, senza lacune o duplicazioni; ricerca FTS con 1.370 unità effettivamente trovate. Il test del formato v3 seleziona un passo reale, verifica copia letterale e provenienza derivata, poi rifiuta id inesistente e unità contraddittoria. Rimossa la guardia su una copia: il test fallisce sull'unità errata e il file operativo conserva lo stesso SHA-256. Il pilota reale conserva tentativi e schede; questi controlli attestano copertura tecnica e provenienza, mentre interpretazioni, figure, ascolto e completezza semantica restano da revisionare.

## Verifica del lettore locale

Il controllo privato `_notes/80-strumenti/verify-local-reading.py` esercita citazioni esatte e inventate, identificativi mancanti e pagina sbagliata, poi ricostruisce le unità reali dalle porzioni e interroga l'indice FTS. La mutazione su una copia del lettore ha tolto il controllo della presenza letterale: il test è fallito sull'evidenza inventata; hash operativo invariato. Le prove non certificano interpretazioni, completezza semantica o trascrizione musicale. Il pilota sul modello reale conserva output, errori e verifiche nel progetto; i livelli del ledger non sono promossi. Per la continuità, controllati otto originali e le 104/144 voci pregresse identici, insieme al preflight del libro. Nessuna build completa richiesta quando prosa, notazione e citazioni del manoscritto sono invariati.

> Popolare leggendo la configurazione reale dei controlli. La checklist operativa locale dei test manuali vive invece in `_notes/00-regia/TEST-CHECKLIST.md`, ignorata da git.

## Test runner e comandi

<controlli di qualità del libro, es. compilazione senza errori, controllo riferimenti, dove girano>

## Rotte e dati mockati

<eventuali fixture o esempi finti usati durante la stesura; per un libro tipicamente non applicabile>

## Hook e controlli di qualità

<controlli eseguiti prima del commit, es. build pulita, assenza di warning critici>


## Lettore: recuperi e corpora aggiuntivi, 2026-10-09

Configurazione privata `additional_corpora` per accodare inventari con lo stesso schema; gli hash mantengono le identità. `source_overrides.processing_pdf` indica una copia derivata privata, il suo SHA-256 e il manifest di trasformazione: hash derivato e originale verificati prima dell'acquisizione, provenienza nelle unità. Un collegamento può avere una cartella risolta e verificata; non viene eseguito né dichiarato letto il suo contenuto.

Il rendering conserva schede non valide senza eccezione su localizzatori mancanti e mostra gli errori. La prova privata `verify-reader-recovery-2026-10-09.py` usa una scheda fallita reale, riproduce il vecchio arresto, conserva SHA-256/output e verifica che l'ancora inesistente resti respinta. Per segmenti ASR molto brevi l'evidenza può coincidere con l'intero segmento non vuoto anche sotto15 caratteri; la sottostringa breve di un testo lungo rimane non valida. Sono controlli di provenienza letterale, non di validità dell'interpretazione. La revisione di fonte, figure, notazione e ascolto rimane necessaria.
