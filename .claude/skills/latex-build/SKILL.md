---
name: latex-build
description: >
  Bootstrap e compilazione dell'ambiente del libro di armonia: TinyTeX user-local (engine
  LuaLaTeX) guidato dal manifesto tex-packages.txt, piu' LilyPond (binario esterno) per gli
  esempi musicali via lilypond-book. Usare per preparare l'ambiente la prima volta o dopo aver
  aggiunto pacchetti al manifesto, e per compilare in modo riproducibile con gli script in
  scripts/. L'output (PDF e ausiliari) finisce in build/, ignorata da git.
disable-model-invocation: true
---

## Premessa

Questa skill non duplica logica: si appoggia ai file versionati del progetto. La fonte di verita'
dell'ambiente TeX e' il manifesto `tex-packages.txt` (sezione 13 di `.claude/PROJECT-SYSTEM.md`); la
distribuzione TeX (TinyTeX) e' esterna al repository, installata user-local e condivisa fra i
progetti, quindi non versionata. L'engine e' LuaLaTeX, fissato in `.latexmkrc`.

La notazione musicale usa LilyPond tramite il preprocessore `lilypond-book`. LilyPond NON e' un
pacchetto TeX: e' un binario esterno a TinyTeX, da installare a parte (da https://lilypond.org o dal
gestore pacchetti del sistema) e da avere sul PATH come `lilypond` e `lilypond-book`. Lo script di
setup lo segnala se manca; lo script di build esegue la passata `lilypond-book` prima di LuaLaTeX
quando il sorgente principale e' un `.lytex`.

Gli script invocano i binari per percorso, senza attivazione interattiva, identici in locale e in CI.
Non eseguono operazioni git: commit e push restano manuali dell'utente.

## Layout sorgenti

Il preambolo condiviso vive in `style/` (tracciato, pubblico). Il contenuto reale del libro vive in
`manuscript/` (ignorato da git, privato, backuppato a parte): `manuscript/main.lytex` include i
capitoli sotto `manuscript/chapters/*.lytex`, gli esempi `manuscript/music/*.ly` e la bibliografia
`manuscript/bib/references.bib`. In `sample/` c'e' un documento minimo tracciato che serve a
verificare l'ambiente senza esporre il contenuto. Lo script di build sceglie automaticamente
`manuscript/main.lytex` se esiste, altrimenti `sample/main.lytex`.

## Procedura

### 1. Preparare l'ambiente dal manifesto

Windows (Windows PowerShell 5.1):

```
powershell -ExecutionPolicy Bypass -File scripts\setup-tex.ps1
```

Unix/macOS:

```
sh scripts/setup-tex.sh
```

Localizza TinyTeX (default `%APPDATA%\TinyTeX` su Windows, `~/.TinyTeX` su Unix); se assente lo
installa; esegue `tlmgr install` dei pacchetti del manifesto; verifica con una compilazione minima
in LuaLaTeX; infine controlla la presenza di LilyPond e avvisa se manca. La prima esecuzione scarica
diversi pacchetti, quindi richiede rete e qualche minuto. Flag: `-Reinstall`/`--reinstall`,
`-TexDir`/`--tex-dir`, `-SkipPackages`/`--skip-packages`.

### 2. Compilare il libro

Windows:

```
powershell -ExecutionPolicy Bypass -File scripts\build.ps1
```

Unix/macOS:

```
sh scripts/build.sh
```

Per un `.lytex` lo script esegue prima `lilypond-book --pdf` (richiede LilyPond) e poi
`latexmk -lualatex`; l'output e' `build/main.pdf`. Flag utili: `-Main`/`--main <file>` per forzare il
sorgente, `-NoLily`/`--no-lily` per saltare gli esempi musicali (compila solo il LaTeX),
`-Clean`/`--clean` per rimuovere gli ausiliari, `-CleanAll`/`--clean-all` per cancellare l'intera
`build/`.

### 3. Aggiungere un pacchetto TeX

Aggiungere il nome `tlmgr` al manifesto `tex-packages.txt` (una voce per riga), poi rieseguire lo
script di setup: installa solo cio' che manca. Il manifesto resta la fonte riproducibile.

## Note di manutenzione

Se la build fallisce per un pacchetto mancante, il messaggio di LuaLaTeX indica il file `.sty`
assente: trovare il pacchetto con `tlmgr search --file <nome>.sty`, aggiungerlo al manifesto e
rilanciare il setup. Non installare pacchetti a mano senza registrarli nel manifesto, altrimenti
l'ambiente non resta riproducibile. Se la build fallisce su `lilypond-book`, verificare che LilyPond
sia installato e sul PATH; in alternativa compilare con `--no-lily` per isolare i problemi di solo
LaTeX.
