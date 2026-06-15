# Work-log

> Append-only, in ordine cronologico inverso (la voce più recente in alto). Ogni passo
> significativo di codice e ogni intervento manuale rilevante lascia una voce con data, file
> toccati, motivo e commit di riferimento. Qui confluisce anche il log di riconciliazione dei
> documenti `.docx`, con il nome del documento sorgente e l'esito, così la data di allineamento
> sopravvive a un clone.

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
