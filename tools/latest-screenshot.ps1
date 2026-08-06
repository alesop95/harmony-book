<#
.SYNOPSIS
Restituisce percorso ed eta dell'immagine piu recente nella cartella di cattura degli screenshot.

.DESCRIPTION
Serve la regola `.claude/rules/manual-screenshots.md`: quando un passo dello sviluppo produce uno
stato che l'agente non puo osservare da se (una interfaccia, una schermata di configurazione, un
errore visibile solo a runtime), l'agente chiede all'utente uno screenshot e poi lo legge dalla
cartella dello strumento di cattura. Questo script individua quale file leggere e, cosa altrettanto
importante, quanti minuti ha: se l'immagine piu recente risale a prima della richiesta, non e quella
giusta e l'agente deve chiedere conferma invece di assumere.

La cartella di default e quella di Screenpresso su Windows 11. Su una macchina dove lo strumento di
cattura salva altrove, il percorso reale si passa con -Folder, non si indovina.

.PARAMETER Folder
Cartella in cui cercare. Default: %USERPROFILE%\Pictures\Screenpresso.

.PARAMETER MaxAgeMinutes
Se maggiore di zero, lo script esce con codice 2 quando l'immagine piu recente e piu vecchia di
questo limite. Utile per non leggere per errore uno screenshot di ieri.

.PARAMETER PathOnly
Emette il solo percorso, senza le righe di contesto, per l'uso dentro un altro comando.

.EXAMPLE
powershell -NoProfile -ExecutionPolicy Bypass -File tools/latest-screenshot.ps1

.EXAMPLE
powershell -NoProfile -ExecutionPolicy Bypass -File tools/latest-screenshot.ps1 -MaxAgeMinutes 10

.EXAMPLE
powershell -NoProfile -ExecutionPolicy Bypass -File tools/latest-screenshot.ps1 -Folder "D:\Catture" -PathOnly
#>
[CmdletBinding()]
param(
    [string] $Folder = (Join-Path $env:USERPROFILE 'Pictures\Screenpresso'),
    [int]    $MaxAgeMinutes = 0,
    [switch] $PathOnly
)

$ErrorActionPreference = 'Stop'
$estensioni = @('.png', '.jpg', '.jpeg', '.gif', '.bmp')

if (-not (Test-Path -LiteralPath $Folder)) {
    Write-Error "Cartella di cattura non trovata: $Folder. Su questa macchina lo strumento di cattura salva altrove: passa il percorso reale con -Folder."
    exit 1
}

$ultimo = Get-ChildItem -LiteralPath $Folder -File |
    Where-Object { $estensioni -contains $_.Extension.ToLower() } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if ($null -eq $ultimo) {
    Write-Error "Nessuna immagine in $Folder."
    exit 1
}

$eta = (Get-Date) - $ultimo.LastWriteTime
$etaTesto = if ($eta.TotalMinutes -lt 1) {
    "{0:N0} secondi" -f $eta.TotalSeconds
} elseif ($eta.TotalHours -lt 1) {
    "{0:N1} minuti" -f $eta.TotalMinutes
} elseif ($eta.TotalDays -lt 1) {
    "{0:N1} ore" -f $eta.TotalHours
} else {
    "{0:N1} giorni" -f $eta.TotalDays
}

if ($PathOnly) {
    Write-Output $ultimo.FullName
} else {
    Write-Output $ultimo.FullName
    Write-Output ("catturato: {0}" -f $ultimo.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))
    Write-Output ("eta:       {0}" -f $etaTesto)
    Write-Output ("peso:      {0:N0} KB" -f ($ultimo.Length / 1KB))
}

if ($MaxAgeMinutes -gt 0 -and $eta.TotalMinutes -gt $MaxAgeMinutes) {
    Write-Warning "L'immagine piu recente ha $etaTesto, oltre il limite di $MaxAgeMinutes minuti: probabilmente non e lo screenshot appena richiesto."
    exit 2
}

exit 0
