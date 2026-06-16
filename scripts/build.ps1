#requires -Version 5.1
<#
.SYNOPSIS
  Compila il libro (LuaLaTeX + LilyPond) in modo riproducibile (Windows).
.DESCRIPTION
  Sezione 13 di .claude/PROJECT-SYSTEM.md. Trova latexmk nell'ambiente TinyTeX user-local e,
  se il sorgente principale e' un .lytex con esempi musicali, esegue prima la passata
  lilypond-book (binario esterno), poi compila con LuaLaTeX (engine fissato in .latexmkrc).
  Output e ausiliari finiscono in build/ (ignorata da git). Invoca i binari per percorso.
.PARAMETER Main
  File principale. Se omesso: manuscript/main.lytex|.tex, poi sample/main.lytex|.tex.
.PARAMETER NoLily
  Salta lilypond-book anche per un .lytex (compila solo il LaTeX, senza rigenerare gli esempi).
.PARAMETER Clean
  Rimuove gli ausiliari della build e termina.
.PARAMETER CleanAll
  Rimuove l'intera cartella build/ (incluso il PDF) e termina.
.PARAMETER TexDir
  Cartella di TinyTeX (default: $env:APPDATA\TinyTeX).
#>
[CmdletBinding()]
param(
    [string]$Main,
    [switch]$NoLily,
    [switch]$Clean,
    [switch]$CleanAll,
    [string]$TexDir
)

$ErrorActionPreference = 'Stop'
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$StyleDir    = Join-Path $ProjectRoot 'style'
$OutDir      = Join-Path $ProjectRoot 'build'
if (-not $TexDir) { $TexDir = Join-Path $env:APPDATA 'TinyTeX' }

function Find-Bin {
    param([string]$Name, [string]$Root)
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    foreach ($rel in @("bin\windows\$Name.exe", "bin\windows\$Name", "bin\win32\$Name.exe", "bin\win32\$Name")) {
        $p = Join-Path $Root $rel
        if (Test-Path $p) { return $p }
    }
    return $null
}

function Find-LilyBin {
    # Cartella bin di LilyPond. Override esplicito, poi PATH, poi ricerca sotto Program Files.
    # Nessun percorso specifico di macchina e' hardcoded: si cerca una qualsiasi 'lilypond*'.
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

function Get-LilyBookCmd {
    # Comando per invocare lilypond-book. Su Windows lilypond-book e' un .py: va eseguito con il
    # python.exe incluso nella bin di LilyPond, MAI affidandosi all'associazione del .py (che sulla
    # macchina puo' puntare ad altro). Quindi si preferisce sempre python.exe + .py; il PATH si usa
    # solo se esiste un vero wrapper eseguibile (.exe/.bat/.cmd).
    param([string]$Bin)
    if ($Bin) {
        $py  = Join-Path $Bin 'lilypond-book.py'
        $exe = Join-Path $Bin 'python.exe'
        if ((Test-Path $py) -and (Test-Path $exe)) { return @($exe, $py) }
    }
    foreach ($w in @('lilypond-book.exe','lilypond-book.bat','lilypond-book.cmd')) {
        $cmd = Get-Command $w -ErrorAction SilentlyContinue
        if ($cmd) { return @($cmd.Source) }
    }
    return $null
}

# --- Pulizia ---
if ($CleanAll) {
    if (Test-Path $OutDir) { Remove-Item -Recurse -Force $OutDir; Write-Host "[build] Rimossa build/." }
    return
}

$latexmk = Find-Bin -Name 'latexmk' -Root $TexDir
if (-not $latexmk) { throw "[build] latexmk non trovato. Esegui prima scripts/setup-tex.ps1." }

# --- Determina il file principale ---
if (-not $Main) {
    foreach ($cand in @('manuscript\main.lytex','manuscript\main.tex','sample\main.lytex','sample\main.tex')) {
        $p = Join-Path $ProjectRoot $cand
        if (Test-Path $p) { $Main = $p; break }
    }
    if (-not $Main) { throw "[build] Nessun main trovato (manuscript/ o sample/). Specifica -Main." }
} elseif (-not [System.IO.Path]::IsPathRooted($Main)) {
    $Main = Join-Path $ProjectRoot $Main
}
if (-not (Test-Path $Main)) { throw "[build] File principale inesistente: $Main" }

$SrcDir   = Split-Path -Parent $Main
$BaseName = [System.IO.Path]::GetFileNameWithoutExtension($Main)
$Ext      = [System.IO.Path]::GetExtension($Main).ToLower()
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

# --- Percorsi di ricerca TeX (preambolo in style/, capitoli/esempi in manuscript/) ---
# Su Windows il separatore di TEXINPUTS e' ';'; '//' = ricerca ricorsiva; ';' finale = default.
$env:TEXINPUTS = "$ProjectRoot;$StyleDir//;$SrcDir//;$OutDir//;"
$env:BIBINPUTS = "$SrcDir;$SrcDir\bib;$ProjectRoot;"

if ($Clean) {
    Push-Location $OutDir
    try { & $latexmk -c "$BaseName.tex" 2>$null } finally { Pop-Location }
    Write-Host "[build] Ausiliari rimossi in build/."
    return
}

# --- Passata LilyPond (solo per .lytex, salvo -NoLily) ---
$texToCompile = $Main
$compileDir   = $SrcDir
if ($Ext -eq '.lytex' -and -not $NoLily) {
    $lilyBin = Find-LilyBin
    if ($lilyBin) { $env:PATH = "$lilyBin;$env:PATH" }   # cosi' lilypond-book trova lilypond.exe
    $lb = Get-LilyBookCmd -Bin $lilyBin
    if (-not $lb) {
        throw "[build] lilypond-book non trovato. Installa LilyPond e mettilo sul PATH, imposta `$env:LILYPOND_BIN alla sua cartella bin, oppure usa -NoLily per saltare gli esempi musicali."
    }
    Write-Host "[build] lilypond-book ($($lb -join ' ')): preprocesso $([System.IO.Path]::GetFileName($Main)) -> build/ ..."
    $prog = $lb[0]
    $pre  = @(); if ($lb.Count -gt 1) { $pre = $lb[1..($lb.Count - 1)] }
    & $prog @pre --pdf --output="$OutDir" --include="$StyleDir" --include="$SrcDir" "$Main"
    if ($LASTEXITCODE -ne 0) { throw "[build] lilypond-book fallito (exit $LASTEXITCODE)." }
    $texToCompile = Join-Path $OutDir "$BaseName.tex"
    $compileDir   = $OutDir
}

# --- Compilazione LuaLaTeX via latexmk ---
Push-Location $compileDir
try {
    Write-Host "[build] Compilo $([System.IO.Path]::GetFileName($texToCompile)) con latexmk (LuaLaTeX) ..."
    if ($compileDir -eq $OutDir) {
        & $latexmk -lualatex (Split-Path -Leaf $texToCompile)
    } else {
        & $latexmk -lualatex -outdir="$OutDir" (Split-Path -Leaf $texToCompile)
    }
    if ($LASTEXITCODE -ne 0) { throw "[build] Compilazione fallita (latexmk exit $LASTEXITCODE)." }
}
finally { Pop-Location }

$pdf = Join-Path $OutDir "$BaseName.pdf"
Write-Host "[build] Fatto: $pdf"
