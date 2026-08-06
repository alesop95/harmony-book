# tools

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

Rende i diagrammi Mermaid di `.claude/context/diagrams/*.mmd` nei corrispondenti `.svg`, riusando il browser Chromium-based gia installato sul sistema (Edge o Chrome). Non scarica il Chromium di Puppeteer: il download e disattivato e si punta al browser locale, cosi la generazione resta snella e ogni progetto e autonomo.

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
