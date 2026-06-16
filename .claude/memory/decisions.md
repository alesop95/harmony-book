# Registro delle decisioni architetturali

> Convenzione ADR-lite, append-only. Ogni decisione architetturale non ovvia entra come voce
> numerata con data, stato, contesto, decisione, motivazione e conseguenze. Una decisione non si
> cancella e non si riscrive: quando viene superata, si aggiunge una nuova voce che dichiara di
> superare la precedente e ne cita il numero. Le inferenze non confermate si marcano come da
> verificare e si promuovono a decisione solo quando una fonte le conferma.

## ADR-001 — Adozione del sistema di progetto portabile

Data: 2026-06-15
Stato: accettata
Contesto: il progetto necessita di uno stato interamente recuperabile da un clone e di
documentazione che resti allineata al codice senza rilettura integrale a ogni sessione.
Decisione: adottare il sistema descritto in `.claude/PROJECT-SYSTEM.md`, con motore di
riconciliazione ancorato ai commit e doppio livello documentale tracciato/ignorato.
Motivazione: persistenza strutturale su disco indipendente dalla sessione di chat, e controllo
umano sul versionamento.
Conseguenze: ogni passo significativo aggiorna schede, `last-verified-commit`, snapshot e
work-log; commit e push restano manuali.

## ADR-002 — Scelta dello stack rimandata alla sessione ripresa

Data: 2026-06-15
Stato: accettata
Contesto: il progetto è un libro di armonia che deve essere portabile in scrittura sia su Windows 11
sia su Linux, dove il version control funge di fatto da stato di avanzamento del libro. Una ricerca
personale dello stack tecnico esiste già nella cartella ignorata `transform-into-claude-md/`, ma va
letta e discussa con l'utente prima di fissare la tecnologia, e la sessione corrente si chiude per
uno switch di account Claude.
Decisione: completare in questa sessione solo lo scaffold strutturale del sistema di progetto, e
rimandare alla sessione ripresa la lettura di `transform-into-claude-md/`, la decisione condivisa
dello stack (LaTeX e notazione musicale) e il conseguente popolamento delle schede.
Motivazione: non inventare contenuto in fase di init come prescrive `PROJECT-SYSTEM.md`, e non
perdere la discussione sullo stack alla chiusura della sessione per cambio account.
Conseguenze: le schede di `context/` restano col solo frontmatter ancorato a `PENDING-FIRST-COMMIT`;
il pacchetto LaTeX di `.claude/templates/latex/` resta da attivare; la guida operativa della ripresa
vive in `_notes/RESUME-PROMPT.md`.

## ADR-003 — Stack: LaTeX-nativo (LuaLaTeX + memoir + LilyPond via lilypond-book)

Data: 2026-06-15
Stato: accettata
Contesto: serve scrivere un libro di armonia di qualita' editoriale, portabile tra Windows 11 e
Linux, con esempi musicali e diff git puliti (il version control e' lo stato di avanzamento). La
ricerca in `transform-into-claude-md/devBook settings.docx` proponeva uno stack Quarto + Pandoc +
LuaLaTeX + LilyPond + Docker + GitHub Actions multi-formato.
Decisione: adottare un core LaTeX-nativo: engine LuaLaTeX (fissato in `.latexmkrc`), classe `memoir`,
font Libertinus via `fontspec`, `microtype` completo, `babel` italiano, `biblatex`+`biber`,
`imakeidx`, `glossaries`, `cleveref`, `tikz`/`pgfplots`; notazione musicale LilyPond integrata via il
preprocessore `lilypond-book`. Ambiente riproducibile TinyTeX user-local + manifesto
`tex-packages.txt` + `latexmk`, con script `.ps1`/`.sh` e la skill `latex-build`.
Motivazione: massimo controllo tipografico e diff testuali puliti, portabilita' senza Docker,
coerenza con la filosofia del sistema (partire minimale). Quarto/HTML/EPUB/interattivita' e
Docker/CI sono rimandati a Fase 2 e Fase 3, innestabili senza rilavoro perche' le sorgenti
LaTeX+LilyPond si riusano.
Conseguenze: il pacchetto LaTeX del bundle e' stato istanziato e adattato (engine LuaLaTeX, passata
`lilypond-book`, sorgente da `manuscript/` con fallback `sample/`). LilyPond resta un binario esterno
da installare a parte. La scheda `STACK.md` e' popolata.

## ADR-004 — Privacy del contenuto: split tooling pubblico / manoscritto privato

Data: 2026-06-15
Stato: accettata
Contesto: il contenuto del libro non deve mai essere visibile su una repo pubblica, altrimenti se ne
comprometterebbe la vendita; al tempo stesso si vuole che il version control rifletta l'avanzamento.
Decisione: separare nettamente tooling/struttura da contenuto. Il repository pubblico
`alesop95/harmony-book` traccia solo metodo e struttura (`.claude/`, `style/`, `scripts/`, `sample/`,
manifesti, configurazioni); il contenuto vendibile vive in `manuscript/`, ignorata da git. Per ora i
capitoli restano locali e il backup avviene per copia da SSD a SSD portatile, non via remoto git.
`manuscript/` e' un sottoalbero autonomo: in futuro vi si potra' fare `git init` con un remoto
privato (Opzione 2 piena) senza ristrutturare. Forzato LF via `.gitattributes` per coerenza
Windows/Linux.
Motivazione: garantire che la prosa non sia mai pubblica, conservando un version control pubblico
dell'avanzamento di struttura e metodo.
Conseguenze: `.gitignore` esclude `manuscript/` e `build/`; il repository pubblico non compila il
libro reale (compila `sample/`), il libro reale si compila in locale dove `manuscript/` esiste. La
storia git della prosa, finche' resta locale, dipende dal backup SSD dell'utente.

<!-- ADR-005 — <titolo>
Data: <YYYY-MM-DD>
Stato: <proposta / accettata / superata da ADR-NNN>
Contesto: ...
Decisione: ...
Motivazione: ...
Conseguenze: ... -->
