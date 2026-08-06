# Integrazione di contenuto nel libro: fonti, cassaforte, tracciamento, stile

> Regola modulare. Definisce il flusso con cui una fonte, grezza o di ricerca, entra nel manoscritto del libro: dove si annota un'idea al volo, dove si fissa una fonte trovata prima che l'utente la validi, dove si registra ogni aggiunta effettiva, e i vincoli di stile che si applicano a qualunque testo scritto per il libro. Fissata su richiesta esplicita dell'utente il 2026-07-20/21, a partire dal lavoro sul filone modi/tonalità/tritono. Vale per qualunque capitolo o sezione del libro, non solo per quel filone.

## Il flusso a quattro passi

**1. Cattura**, `_notes/fonti-da-processare.md`. Un'idea di fonte che viene in mente durante la scrittura (un PDF, un link, un titolo) si annota lì con una riga, senza fermarsi a formalizzarla. Si processa a lotti, non una alla volta mentre si scrive.

**2. Cassaforte**, `_notes/cassaforte-<filone>.md`, una per filone tematico del libro (per esempio `cassaforte-modi-tritono.md`). È lo staging tra la ricerca grezza e il manoscritto: ogni fonte trovata vi si fissa con citazione esatta, pagina, e perché conta, con uno stato a tre valori (`da validare`, `validata non ancora scritta`, `inserita`). Non si scrive mai nel manoscritto senza prima passare da qui, e non si scrive nel manoscritto senza che l'utente validi sia il contenuto sia la forma esatta del testo proposto.

**3. Tracciamento**, `_notes/tracciamento-fonti-libro.md`. Ogni volta che una voce della cassaforte passa dallo stato "validata" a "inserita", si scrive lì una voce di log con: cosa è entrato, da quale fonte (citekey bibliografico quando applicabile), perché, quale file è stato toccato, e se la fonte grezza originale è stata spostata in archivio o resta al suo posto.

**4. Bibliografia**, `_notes/book-bib-registry.json` + `manuscript/bib/references.bib`, secondo la skill `book-bib-extract`. Ogni fonte citata nel libro, se è un libro o un documento con una vera anagrafica bibliografica, ha una voce nel registro con `bib_status` e una citekey; la cassaforte e il tracciamento riusano quella citekey, non ne creano una parallela.

## Vincoli fermi

Non si cancella mai nulla di quello che l'utente ha già scritto di suo: ogni intervento su un capitolo o un saggio esistente è additivo o di raccordo, mai una sovrascrittura che perde prosa già scritta dall'utente. In caso di dubbio su cosa sia "già scritto dall'utente" rispetto a materiale grezzo ancora da elaborare, si chiede prima di toccare.

Non si cancella mai un file sorgente originale (un PDF scaricato, un `.docx` di appunti grezzi). Si sposta in una sottocartella `_processati/` (o equivalente) solo quando il suo contenuto è stato interamente incorporato nel manoscritto, non parzialmente: fino a quel momento resta al suo posto. Lo spostamento stesso si registra nel tracciamento.

Si traccia sempre anche cosa non si è processato e perché, non solo cosa si è fatto: una fonte letta solo in parte, una sezione volutamente saltata per bassa pertinenza, un file mai apri va dichiarato come tale nella cassaforte, non lasciato in un vuoto silenzioso.

## Stile del testo scritto per il libro

Mai trattini lunghi (—): vale già in generale per la documentazione tecnica secondo `interaction-style.md`, e si applica altrettanto rigidamente alla prosa del libro stesso. Si riformula con la virgola, il punto, o i due punti.

Ogni affermazione armonica dimostrabile va accompagnata, dove ha senso, da un estratto musicale con pentagramma, non solo descritta a parole. Lo strumento è LilyPond, già nello stack del progetto secondo ADR-003 (`.claude/memory/decisions.md`): si genera un file `.ly` minimo mirato alla sola affermazione da dimostrare, si rende in PNG, si ritaglia al solo contenuto (niente intestazioni o tagline di LilyPond), e si inserisce come figura con didascalia. Nei documenti `.docx` ancora pre-manoscritto, la numerazione delle figure aggiunte fuori sequenza si tiene con un suffisso (`Figura 3bis`) invece di rinumerare le figure esistenti; quando il contenuto entra nel manoscritto LaTeX vero, la numerazione delle figure diventa automatica e il problema si estingue da sé. I file `.ly` di lavoro, una volta che il contenuto è nel manoscritto reale, si formalizzano in `manuscript/music/`, non restano solo in una cartella temporanea di sessione.
