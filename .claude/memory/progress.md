# Work-log

> Append-only, in ordine cronologico inverso (la voce più recente in alto). Ogni passo
> significativo di codice e ogni intervento manuale rilevante lascia una voce con data, file
> toccati, motivo e commit di riferimento. Qui confluisce anche il log di riconciliazione dei
> documenti `.docx`, con il nome del documento sorgente e l'esito, così la data di allineamento
> sopravvive a un clone.

## 2026-06-16 — Ambiente installato e catena di build verificata

Commit: PENDING-FIRST-COMMIT
File toccati: `tex-packages.txt`, `.latexmkrc`, `scripts/setup-tex.ps1`, `scripts/build.ps1`,
`scripts/build.sh`, `manuscript/main.lytex` (ignorato).
Motivo: reso operativo lo stack di ADR-003. TinyTeX, `lualatex` e `latexmk` erano gia' presenti;
`scripts/setup-tex.ps1` ha installato i pacchetti del manifesto. LilyPond e' stato installato
manualmente dall'utente sotto `C:\Program Files\lilypond-2.26.0-mingw-x86_64\...\bin`; gli script lo
rilevano li' (o via `LILYPOND_BIN`) senza percorsi hardcoded di macchina.
Correzioni emerse dalla verifica, ora parte del progetto:
- Manifesto: `tabularx` -> `tools`, rimosso `graphicx` (coperto da `graphics`), aggiunti `xpatch`
  (dipendenza di memoir) e `makeindex` (binario non incluso nel TinyTeX minimale).
- `build.ps1`: su Windows `lilypond-book` e' un `.py`; invocato esplicitamente col `python.exe`
  incluso in LilyPond, mai via associazione di sistema del `.py` (che su questa macchina puntava a
  un'app Electron). `BIBINPUTS` include anche la cartella sorgente.
- `.latexmkrc`: aggiunto il supporto `glossaries` (cus_dep `makeglossaries`); l'indice via
  `makeindex` e' nativo di latexmk.
Esito verifica (test manuale, vedi `_notes/TEST-CHECKLIST.md`): `scripts/build.ps1 -Main
sample\main.lytex` produce `build/main.pdf` (catena lilypond-book -> LuaLaTeX -> biber -> makeindex,
~40 KB, con esempi musicali); il build di default sullo scheletro `manuscript/` produce un PDF
pulito (~10 KB). Lo scheletro del manoscritto e' stato reso minimo: glossario/indice/bibliografia e
`\include` dei capitoli restano come blocchi commentati da attivare quando esistono voci reali,
perche' attivati a vuoto mandavano latexmk in stallo.

## 2026-06-16 — Decisione dello stack, privacy del contenuto e attivazione del pacchetto LaTeX

Commit: PENDING-FIRST-COMMIT
File toccati: `STACK.md`, `current-work.md`, `roadmap.md`, `decisions.md` (ADR-003, ADR-004),
`.latexmkrc`, `tex-packages.txt`, `scripts/{setup-tex,build}.{ps1,sh}`,
`.claude/skills/latex-build/SKILL.md`, `style/{preamble.tex,harmony-macros.sty}`,
`sample/`, `manuscript/` (ignorata), `README.md`, `.gitattributes`, `.gitignore`.
Motivo: ingestione dell'handoff `transform-into-claude-md/` (sezione 5: estrazione del `.docx` in
`_notes/.tmp-docx-devbook/`, lettura mirata) e decisione condivisa con l'utente. Stack: LaTeX-nativo
LuaLaTeX + memoir + LilyPond via lilypond-book (ADR-003), pacchetto LaTeX del bundle istanziato e
adattato (engine lualatex, passata lilypond-book, sorgente manuscript/ con fallback sample/).
Privacy: split tooling pubblico / `manuscript/` privata ignorata, backup SSD, promovibile a repo
privato (ADR-004). Schede STACK/current-work/roadmap popolate. Ambiente non ancora installato e
catena non ancora compilata (richiede TinyTeX + LilyPond): e' la Definition of Done corrente.
Riconciliazione handoff: documento sorgente `transform-into-claude-md/devBook settings.docx`, esito
= stack fissato (ADR-003/004). Cartella handoff ignorata, non committata.

## 2026-06-15 — Inizializzazione del sistema di progetto

Commit: PENDING-FIRST-COMMIT
File toccati: anatomia di `.claude` (settings.json, memory/, context/, rules/, skills/, templates/),
`CLAUDE.md`, `CLAUDE.local.md`, `.gitignore`, `_notes/`.
Motivo: installazione del sistema portabile di contesto, documentazione e version control descritto
in `.claude/PROJECT-SYSTEM.md`, eseguita in modalità greenfield. Repo git inizializzato su branch
`main` con identità locale `alesop95 <alessio.sopranzi.95@gmail.com>` e remoto
`git@github-personal:alesop95/harmony-book.git` (vedi `.claude/rules/git-identity-and-repo.md`).
Protezione globale `user.useConfigOnly` già attiva sulla macchina, non modificata. Schede di
`context/` create con sola struttura e frontmatter (segnaposto `PENDING-FIRST-COMMIT`), da popolare
nelle sessioni successive senza inventare contenuto.

Decisioni di processo registrate in questa sessione:
- Stack non ancora deciso: la lettura di `transform-into-claude-md/` (handoff ignorato) e la scelta
  dello stack per il libro di armonia sono rimandate alla sessione ripresa, da svolgere insieme
  all'utente. Vedi `_notes/RESUME-PROMPT.md`.
- MCP non configurato: nessun `.mcp.json` né cartella `mcp/`. Resta istanziabile in seguito dal
  template `.claude/templates/mcp.json` rieseguendo il passo MCP della skill `init-project-system`.
- Pacchetto LaTeX non ancora attivato: resta istanziabile da `.claude/templates/latex/` quando lo
  stack lo confermerà.
