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

<!-- ADR-003 — <titolo>
Data: <YYYY-MM-DD>
Stato: <proposta / accettata / superata da ADR-NNN>
Contesto: ...
Decisione: ...
Motivazione: ...
Conseguenze: ... -->
