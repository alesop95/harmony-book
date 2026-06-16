#requires -Version 5.1
<#
.SYNOPSIS
  Bootstrap dell'ambiente LaTeX (TinyTeX) per Windows, guidato dal manifesto.
.DESCRIPTION
  Sezione 13 di .claude/PROJECT-SYSTEM.md. Localizza TinyTeX (installazione user-local
  condivisa fra i progetti), e se assente lo installa; poi installa i pacchetti elencati in
  tex-packages.txt con tlmgr, e verifica con una compilazione minima in LuaLaTeX. Segnala se
  LilyPond (binario esterno necessario per gli esempi musicali) non e' sul PATH. Non attiva
  shell interattive: invoca i binari dell'ambiente per percorso, identico in locale e in CI.
.PARAMETER Reinstall
  Rimuove l'installazione TinyTeX esistente e la ricrea da zero.
.PARAMETER TexDir
  Forza la cartella di installazione di TinyTeX (default: $env:APPDATA\TinyTeX).
.PARAMETER SkipPackages
  Salta l'installazione dei pacchetti dal manifesto (solo bootstrap della distribuzione).
.PARAMETER Manifest
  Percorso del manifesto (default: tex-packages.txt nella radice del progetto).
#>
[CmdletBinding()]
param(
    [switch]$Reinstall,
    [string]$TexDir,
    [switch]$SkipPackages,
    [string]$Manifest
)

$ErrorActionPreference = 'Stop'

# --- Percorsi -------------------------------------------------------------------
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
if (-not $Manifest) { $Manifest = Join-Path $ProjectRoot 'tex-packages.txt' }
if (-not $TexDir)   { $TexDir   = Join-Path $env:APPDATA 'TinyTeX' }

function Find-Tlmgr {
    param([string]$Root)
    $cmd = Get-Command tlmgr -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    foreach ($rel in @('bin\windows\tlmgr.bat', 'bin\win32\tlmgr.bat')) {
        $p = Join-Path $Root $rel
        if (Test-Path $p) { return $p }
    }
    return $null
}

# --- Reinstallazione su richiesta ----------------------------------------------
if ($Reinstall -and (Test-Path $TexDir)) {
    Write-Host "[setup-tex] Rimuovo l'installazione esistente: $TexDir"
    Remove-Item -Recurse -Force $TexDir
}

# --- Localizza o installa TinyTeX ----------------------------------------------
$tlmgr = Find-Tlmgr -Root $TexDir
if (-not $tlmgr) {
    Write-Host "[setup-tex] TinyTeX non trovato. Installazione in: $TexDir"
    [Net.ServicePointManager]::SecurityProtocol =
        [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
    if ((Split-Path -Leaf $TexDir) -ne 'TinyTeX') {
        throw "[setup-tex] -TexDir deve terminare con 'TinyTeX' (l'installer crea quella sottocartella). Valore: $TexDir"
    }
    $env:TINYTEX_DIR = Split-Path -Parent $TexDir
    $installer = Join-Path $env:TEMP 'install-tinytex.ps1'
    Invoke-WebRequest -UseBasicParsing 'https://tinytex.yihui.org/install-bin-windows.ps1' -OutFile $installer
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $installer
    $tlmgr = Find-Tlmgr -Root $TexDir
    if (-not $tlmgr) {
        throw "[setup-tex] Installazione di TinyTeX fallita: tlmgr non trovato sotto $TexDir o sul PATH."
    }
}
Write-Host "[setup-tex] tlmgr: $tlmgr"
$TexBin = Split-Path -Parent $tlmgr

# --- Aggiorna tlmgr e installa i pacchetti dal manifesto ------------------------
Write-Host "[setup-tex] Aggiorno tlmgr ..."
& $tlmgr update --self

if (-not $SkipPackages) {
    if (-not (Test-Path $Manifest)) { throw "[setup-tex] Manifesto non trovato: $Manifest" }
    $pkgs = Get-Content $Manifest |
        ForEach-Object { ($_ -replace '#.*$', '').Trim() } |
        Where-Object { $_ }
    if ($pkgs.Count -gt 0) {
        Write-Host "[setup-tex] Installo $($pkgs.Count) pacchetti dal manifesto ..."
        & $tlmgr install @pkgs
    }
}

# --- Verifica con una compilazione minima in LuaLaTeX --------------------------
$lualatex = Join-Path $TexBin 'lualatex.exe'
if (-not (Test-Path $lualatex)) { $lualatex = Join-Path $TexBin 'lualatex' }
Write-Host "[setup-tex] Verifica: compilo un documento di prova con LuaLaTeX ..."
$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("texcheck_" + [System.IO.Path]::GetRandomFileName().Replace('.', ''))
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
$probe = Join-Path $tmp 'probe.tex'
@'
\documentclass{memoir}
\usepackage{fontspec}
\usepackage[italian]{babel}
\usepackage[final,expansion=true,protrusion=true]{microtype}
\usepackage{csquotes}
\begin{document}
Prova di tipografia editoriale: \enquote{armonia} con microtype attivo.
\end{document}
'@ | Set-Content -Encoding utf8 $probe
& $lualatex -interaction=nonstopmode -halt-on-error -output-directory $tmp $probe | Out-Null
$ok = (Test-Path (Join-Path $tmp 'probe.pdf'))
Remove-Item -Recurse -Force $tmp
if (-not $ok) { throw "[setup-tex] Verifica fallita: il documento di prova non ha prodotto un PDF." }
Write-Host "[setup-tex] OK. Ambiente LaTeX (LuaLaTeX) pronto."

# --- Controllo di LilyPond (binario esterno, non parte di TinyTeX) -------------
function Find-LilyBin {
    if ($env:LILYPOND_BIN -and (Test-Path (Join-Path $env:LILYPOND_BIN 'lilypond.exe'))) { return $env:LILYPOND_BIN }
    $cmd = Get-Command lilypond.exe -ErrorAction SilentlyContinue
    if ($cmd) { return (Split-Path -Parent $cmd.Source) }
    foreach ($pf in @($env:ProgramFiles, ${env:ProgramFiles(x86)}, $env:LOCALAPPDATA)) {
        if (-not $pf -or -not (Test-Path $pf)) { continue }
        $dirs = Get-ChildItem -Path $pf -Filter 'lilypond*' -Directory -ErrorAction SilentlyContinue
        foreach ($d in $dirs) {
            $exe = Get-ChildItem -Path $d.FullName -Filter 'lilypond.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($exe) { return (Split-Path -Parent $exe.FullName) }
        }
    }
    return $null
}
$lilyBin = Find-LilyBin
if ($lilyBin -and (Test-Path (Join-Path $lilyBin 'lilypond-book.py') ) ) {
    Write-Host "[setup-tex] LilyPond trovato: $lilyBin (lilypond-book.py invocato via python bundled dallo script di build)."
    if (-not (Get-Command lilypond.exe -ErrorAction SilentlyContinue)) {
        Write-Host "[setup-tex] Nota: non e' sul PATH globale, ma build.ps1 lo rileva sotto Program Files / via LILYPOND_BIN."
    }
} else {
    Write-Warning "[setup-tex] LilyPond NON trovato (PATH, LILYPOND_BIN, Program Files)."
    Write-Host    "[setup-tex] Gli esempi musicali richiedono LilyPond, binario esterno a TinyTeX."
    Write-Host    "[setup-tex] Installalo da https://lilypond.org/download.html; build.ps1 lo cerca poi sotto"
    Write-Host    "[setup-tex] Program Files, oppure imposta `$env:LILYPOND_BIN alla sua cartella bin."
}

Write-Host "[setup-tex] Per compilare il progetto: scripts/build.ps1"
Write-Host "[setup-tex] Nota: aggiungi '$TexBin' al PATH per usare lualatex/latexmk a mano."
