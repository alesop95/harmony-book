# tools

## Elaborazione locale del corpus privato

`python -B tools/local-reading.py prepare` prepara unità con pagine/paragrafi/minuti e un indice SQLite FTS5; riusa estrazioni, completa OCR e trascrive media con strumenti già presenti. `analyze` usa un modello locale via API Ollama, porzioni senza tagli, output strutturati ed evidenze controllate nella specifica unità. `report` aggiorna copertura e lacune, `search --query '<testo>'` interroga l'indice, `retry` rimette in coda schede fallite conservando gli output. Le schede restano non revisionate: non aggiornano L1/L2, bibliografia o manoscritto.

`tools/start-local-reading.ps1 -Task <prepare|speech|serve|analyze|supervise>` avvia processi nascosti indipendenti, con log e checkpoint dentro il progetto. `serve` usa `tools/isolated-ollama-host.py` in memoria tramite SSH: Landlock nega scritture sull'host e permette temporanei in RAM eliminati alla chiusura del canale; i modelli preesistenti rimangono in sola lettura. `supervise` prosegue dopo un pilota con evidenze ancorate e chiude il servizio dedicato alla fine o all'errore. Configurazione e valori di macchina sono in `_notes/00-regia/lettura-locale/config.json`; istruzioni e limiti nella guida privata `_notes/00-regia/LETTURA-LOCALE.md`. Nessun modello o dipendenza viene scaricato automaticamente. `STOP` interrompe il lotto, `SERVER-STOP` chiude il servizio remoto; verificare marcatori e PID prima di riprendere.

## Fonti Reddit tramite il pacchetto community-sources

Il lettore è già in `.claude/templates/community-sources/tools/fetch-reddit.py`; per un post usare `python tools/fetch-community.py post <URL-o-ID>`. La copia di archivio e lo stato della corsa sono privati sotto `_notes/20-ricerca/acquisizioni-community/`. Caricare `fonti-non-recuperabili` al primo rifiuto: un 403 diretto non descrive l’accessibilità dell’archivio. `riprendi` estende una corsa esistente con tetti dichiarati. Il lettore acquisisce materiale; la lettura e l’unità citabile si registrano separatamente nel ledger e nel registro bibliografico.

`python tools/source-library.py audit` censisce il registro, la bibliografia reale e il ledger privato delle letture senza annullare le attestazioni precedenti. `python tools/source-library.py extract` estrae una volta il testo nativo dei PDF disponibili, con hash e mappa per pagina; `--limit N` limita le nuove estrazioni, `--retry-errors` riprova file invariati che avevano fallito. Le copie acquisite possono essere collegate in `local_copy_path` nel ledger privato. Una soglia di testo segnala pagine da aprire come immagini o OCR, senza attribuire un livello di lettura. File e risultati rimangono in `_notes/10-biblioteca/` e nella cache privata; nessun originale esterno viene modificato.

`python tools/sync-book-bib.py --proposals <file.bib>` prepara il confronto con le voci reali. `--apply`, solo se gli aggiornamenti bibliografici sono autorizzati nella sessione, importa le voci assenti con anagrafica verificata nel registro, conserva le voci esistenti, salva un backup privato e riconcilia i flag del JSON. Ogni importazione conserva anche un rapporto datato in `_notes/10-biblioteca/importazioni/`, oltre al puntatore all'ultimo giro. Una chiave condivisa da più record richiede riconciliazione prima dell'importazione. Questo strumento non aggiorna automaticamente campi di voci già presenti e non dichiara contenuto letto.

`python tools/fetch-source-files.py --url <url> --out <file>` acquisisce un documento accessibile e scrive accanto al file URL, data, MIME e SHA-256. La destinazione deve essere dentro `_notes/`: il controllo del percorso risolto impedisce di scrivere fonti e provenienza nel livello pubblico. Rifiuta una risposta non PDF se la destinazione ha estensione `.pdf` e conserva file e manifest già esistenti. Non supera controlli di accesso; non verifica anagrafica o lettura.

`python tools/check-book.py` esegue il controllo preliminare in sola lettura del manoscritto privato; `python tools/check-book.py --main sample/main.lytex` usa il campione pubblico. Segnala inclusioni e bibliografie mancanti, citekey duplicate o irrisolte e capitoli `.lytex` presenti ma non inclusi nel main. Il controllo non sostituisce compilazione e lettura del PDF.

`python tools/audit-local-sources.py --root "J:\MAIN\MUSIC\THEORY and INSTRUMENTS" --snapshot _notes/catalogo-locale-AAAA-MM-GG.json` fotografa in un file privato i percorsi PDF, EPUB e DOCX di un corpus locale e li confronta con i percorsi già presenti nel registro bibliografico. Una scansione successiva con `--previous <fotografia-precedente>` distingue nuovi arrivi e cambiamenti di dimensione o data dai file che semplicemente non hanno ancora una voce. Il confronto per percorso non sostituisce una verifica per contenuto o anagrafica.

La descrizione di tutti gli strumenti di questa cartella, con il ruolo architetturale di ciascuno, sta nella sezione "Gli strumenti sotto `tools/`" di `.claude/context/STACK.md`, che è la scheda che li copre. Qui restano le note d'uso dei due che hanno prerequisiti o parametri non ovvi.

## latest-screenshot.ps1

Restituisce percorso, data di cattura, età e peso dell'immagine più recente nella cartella dello strumento di cattura, per la regola `.claude/rules/manual-screenshots.md`. L'età serve a non leggere per errore uno screenshot vecchio: se la più recente risale a prima della richiesta, si chiede conferma invece di assumere.

Uso:

```
powershell -NoProfile -ExecutionPolicy Bypass -File tools/latest-screenshot.ps1
```

La cartella di default è quella di Screenpresso su Windows 11, cioè `%USERPROFILE%\Pictures\Screenpresso`. Su una macchina che salva altrove il percorso reale si passa con `-Folder`, non si indovina. Con `-MaxAgeMinutes N` lo script esce con codice 2 se l'immagine è più vecchia del limite, così un agente distingue lo screenshot appena richiesto da uno rimasto in cartella. Con `-PathOnly` emette il solo percorso, per l'uso dentro un altro comando.

Su Linux non esiste Screenpresso: vale la stessa logica con lo strumento di cattura locale, per esempio Flameshot o Spectacle, passando la sua cartella di salvataggio a `-Folder`.

## render-diagrams.mjs

Rende i diagrammi Mermaid di `.claude/context/diagrams/*.mmd` nei corrispondenti `.svg`, riusando il browser Chromium-based già installato sul sistema (Edge o Chrome). Non scarica il Chromium di Puppeteer: il download e disattivato e si punta al browser locale, così la generazione resta snella e ogni progetto e autonomo.

Uso:

```
node tools/render-diagrams.mjs
```

Per rendere una cartella diversa:

```
node tools/render-diagrams.mjs <cartella>
```

Prerequisiti: Node e un browser Edge o Chrome. Alla prima esecuzione `npx` scarica i soli script di mermaid-cli, mai un browser. Se l'autorilevamento del browser fallisce, forzalo con la variabile d'ambiente `PUPPETEER_EXECUTABLE_PATH` puntata all'eseguibile di Edge o Chrome.

I `.svg` prodotti sono versionati accanto ai `.mmd` sorgente, secondo l'anatomia canonica del sistema di progetto.

## Censimento completo e destinazioni dopo il riordino

`audit-local-sources.py --all-files` estende il censimento oltre PDF/EPUB/DOCX; l’uso senza il flag mantiene il perimetro precedente. `audit-reading-corpus.py --root <cartella> --name <nome>` censisce tutti i file in sola lettura, conserva hash, corrispondenze bibliografiche e metadati tecnici, estrae i DOCX in porzioni private e misura i media con ffprobe. Richiede Python e PyMuPDF per i PDF non già censiti; ffprobe è facoltativo, e se manca lo segnala. Non assegna livelli di lettura.

`source-library.py` usa `_notes/10-biblioteca/` e `_notes/99-cache/doc-ingest/source-library/`. Il registro centrale conserva il percorso `_notes/book-bib-registry.json`; `sync-book-bib.py` conserva i propri report nella biblioteca riorganizzata. `fetch-community.py` delega al lettore vendorizzato, mantenendolo intatto, e indirizza le nuove acquisizioni verso `_notes/20-ricerca/acquisizioni-community/`. `post` e `riprendi` mantengono i comandi del template; l’help e la destinazione sono verificati senza acquisizione di nuovi contenuti in questo giro.

Le procedure private attuali sono in `_notes/80-strumenti/`; gli script di lavorazioni precedenti sono archiviati e non vanno rieseguiti come aggiornamenti correnti. La procedura di snapshot esclude l’intera cache e i propri ZIP. La migrazione conserva hash, percorsi precedenti e copie delle note anteriori al riallineamento dei link; le validazioni distinguono file autoriali immutati da documentazione operativa aggiornata.


## Lettore: recuperi e corpora aggiuntivi, 2026-10-09

Configurazione privata `additional_corpora` per accodare inventari con lo stesso schema; gli hash mantengono le identità. `source_overrides.processing_pdf` indica una copia derivata privata, il suo SHA-256 e il manifest di trasformazione: hash derivato e originale verificati prima dell'acquisizione, provenienza nelle unità. Un collegamento può avere una cartella risolta e verificata; non viene eseguito né dichiarato letto il suo contenuto.

Il rendering conserva schede non valide senza eccezione su localizzatori mancanti e mostra gli errori. La prova privata `verify-reader-recovery-2026-10-09.py` usa una scheda fallita reale, riproduce il vecchio arresto, conserva SHA-256/output e verifica che l'ancora inesistente resti respinta. Per segmenti ASR molto brevi l'evidenza può coincidere con l'intero segmento non vuoto anche sotto15 caratteri; la sottostringa breve di un testo lungo rimane non valida. Sono controlli di provenienza letterale, non di validità dell'interpretazione. La revisione di fonte, figure, notazione e ascolto rimane necessaria.
