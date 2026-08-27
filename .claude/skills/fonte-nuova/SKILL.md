---
name: fonte-nuova
description: >
  Porta una fonte nuova dentro il progetto in modo guidato e uniforme: verifica l'anagrafica,
  dichiara il livello di verifica raggiunto, la fissa in cassaforte, la registra in
  book-bib-registry.json, e solo su conferma esplicita scrive la voce in references.bib. Copre
  articoli, capitoli, paper e link, non solo libri. Si invoca ogni volta che una fonte nuova entra
  nel progetto, da ricerca web o da consegna dell'utente. A invocazione manuale.
disable-model-invocation: true
---

## Perché esiste

Il progetto ha già `book-bib-extract`, che pero copre un caso solo: un libro già ingerito da `doc-ingest`, di cui si legge il colophon per ricavarne una voce `@book`. Non copre il caso che ricorre di più nella pratica, cioè una fonte trovata in rete, un articolo di rivista, un capitolo in volume collettivo, un paper dietro paywall, un video o un post.

Quel caso, fatto a mano, e ripetitivo e sempre uguale, e ha un punto in cui si sbaglia facilmente: dire più di quello che si e verificato davvero. Questa skill lo rende una procedura fissa, con il livello di verifica come dato di prima classe invece che come sfumatura nella prosa.

## Il principio che regge tutto: quattro livelli di verifica, mai confusi

Prima di scrivere qualunque cosa, si stabilisce a quale livello si e arrivati. Il livello si scrive nella voce, e determina cosa si può fare con la fonte.

Livello 1, contenuto letto per intero. La fonte e stata aperta e letta integralmente. Si può citare il contenuto, con virgolette e pagina.

Livello 2, contenuto letto in parte. Si e letta la porzione pertinente e si dichiara quale. Si può citare quella porzione, non il resto, e va detto esplicitamente cosa non si e letto.

Livello 3, anagrafica verificata, contenuto non letto. Autore, titolo, sede, anno e pagine vengono dalla pagina dell'editore, dal sito della rivista o dalla bibliografia di una fonte letta direttamente. La voce bibliografica si può scrivere; il contenuto non si può citare.

Livello 4, esistenza segnalata. La fonte e nota solo da una sintesi di ricerca o da una citazione di terzi. Non si scrive nulla nel `.bib`: si registra come candidata.

La regola che ne discende, ed è il motivo per cui la skill esiste: la voce `.bib` asserisce l'anagrafica, non il contenuto. Sono due cose diverse e vanno verificate separatamente.

## Procedura

1. Chiedere all'utente da dove arriva la fonte e a che scopo la vuole, cioè quale affermazione del libro dovrebbe sostenere. Se non sostiene nessuna affermazione precisa, dirlo: e una fonte da inbox, va in `_notes/fonti-da-processare.md` e ci si ferma qui.

2. Provare ad arrivare al testo, in quest'ordine, che è per costo crescente. Il sito dell'editore o della rivista, che spesso ha il PDF libero anche quando l'aggregatore lo blocca; questa e la lezione del 2026-07-31, quando un HTTP 403 su ResearchGate si e rivelato non essere un paywall. Poi i repository ad accesso aperto. Poi la bibliografia di una fonte già letta, che spesso da l'anagrafica esatta anche quando il testo resta irraggiungibile. Non insistere oltre: se e dietro paywall, si scende di livello e lo si dichiara, non si indovina.

3. Se si ottiene un PDF, estrarlo con `pdftotext` invece di rifetcharlo: e deterministico e non costa token. Leggere per fette, mai tutto in una volta se il documento e lungo.

4. Stabilire il livello di verifica secondo lo schema sopra, e dichiararlo.

5. Fissare la fonte in cassaforte, cioè in `_notes/cassaforte-<filone>.md`, con la struttura che il progetto usa già: stato, fonte con anagrafica completa, cosa dice con citazione testuale, perché conta, e quando serve una sezione di cautela su come NON va usata. Se la fonte contraddice o complica qualcosa di già scritto, dirlo qui, non nasconderlo.

6. Registrare in `_notes/book-bib-registry.json`. Chiave `manual-<tipo>-<slug>` per le fonti senza file locale, per esempio `manual-doi-butler-1989` o `manual-url-<slug>`. Campi: `citekey`, `bib_status`, `bib_verified_by` con il livello di verifica in chiaro, `bib_verified_date`, `corpus` (di norma `fonti-esterne`), e in `notes` l'anagrafica per esteso più cosa si e letto e cosa no. Poi rigenerare la tabella con `python tools/render-bib-registry.py`.

7. Proporre la voce `.bib` all'utente e attendere conferma esplicita. Solo dopo la conferma scriverla in `manuscript/bib/references.bib`, impostando `bib_entry_written: true`. Il tipo segue la fonte, non l'abitudine: `@article` per rivista, `@incollection` per capitolo in volume collettivo, `@misc` per web, `@book` per libro. Nel campo `note` va sempre il livello di verifica in maiuscolo, così e visibile a colpo d'occhio rileggendo il file.

8. Prima di scrivere, controllare le collisioni di citekey contro il `.bib` reale e contro il registro. La convenzione e cognome del primo autore più anno, minuscolo e senza accenti, con suffisso `a`, `b`, `c` in caso di collisione.

9. Registrare il passo in `_notes/tracciamento-fonti-libro.md`, dichiarando anche cosa non si e processato e perché.

10. Se il progetto ha la skill `armonia-libro`, aggiornare le parti che dipendono dalla fonte nuova, tipicamente `fatti-verificati.md`, `fonti.md` e `agenda-ricerca.md`, e poi riallineare il manifesto con `python tools/skill-freshness.py .claude/skills/armonia-libro --update`.

## Casi che vanno gestiti in modo particolare

Fonte contestata in letteratura. Se la tesi della fonte ha ricevuto una replica pubblicata, la replica si registra insieme, e nella voce `.bib` di entrambe si scrive che vanno citate insieme. Citare solo il lato che fa comodo e la scorciatoia che questo libro rimprovera ad altri.

Fonte non accademica, cioè forum, video, post. Si cita per quello che è, cioè testimonianza di cosa pensa una comunità o di cosa ha dichiarato una persona, mai come prova di un fatto teorico o storico. Servono metadati verificabili: per YouTube l'endpoint oEmbed da titolo e canale senza costo, e la data di pubblicazione non è esposta e non va inventata; per un thread serve l'URL permanente del commento, non del thread.

Anagrafica incerta. Se anno, editore o pagine divergono fra le fonti, si sceglie il dato dell'editore e si annota la divergenza nella voce. Non si sceglie in silenzio.

Fonte in standby. Se l'utente ha annunciato una fonte ma non l'ha ancora consegnata, si registra la voce con `bib_status: da-verificare` e si lascia un segnaposto esplicito nel testo. Non si scrive contenuto verosimile al suo posto.

## Vincoli

Mai scrivere nel `.bib` reale senza conferma umana esplicita. Mai inventare un campo assente: si omette. Mai promuovere una fonte a `verificata` sulla base di una sintesi di ricerca invece che della lettura. Non toccare il campo `skill_status`, che appartiene a `book-digest`. Non eseguire `git add`, `commit` o `push`.

Idempotenza: rilanciare la skill sulla stessa fonte aggiorna la voce esistente, riconosciuta per citekey o per chiave del registro, e non ne crea una seconda.
