param(
    [ValidateSet('prepare','speech','analyze','serve','supervise')]
    [string]$Task = 'prepare',
    [int]$Limit = 0
)
$ErrorActionPreference = 'Stop'
$readingRoot = Split-Path -Parent $PSScriptRoot
$readingState = Join-Path $readingRoot '_notes/10-biblioteca/lettura-locale'
$readingCache = Join-Path $readingRoot '_notes/99-cache/lettura-locale/tmp'
New-Item -ItemType Directory -Force -Path $readingState,$readingCache | Out-Null
if (Test-Path -LiteralPath (Join-Path $readingState 'STOP')) {
    throw 'STOP exists. Remove that project-local marker intentionally before resuming.'
}
$readingPidFile = Join-Path $readingState ($Task + '-process.json')
if (Test-Path -LiteralPath $readingPidFile) {
    $readingPrevious = Get-Content -LiteralPath $readingPidFile -Raw | ConvertFrom-Json
    if (Get-Process -Id $readingPrevious.pid -ErrorAction SilentlyContinue) {
        throw "Task already runs with PID $($readingPrevious.pid)"
    }
}
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:TEMP = $readingCache
$env:TMP = $readingCache
$env:HF_HOME = Join-Path $readingRoot '_notes/99-cache/lettura-locale/huggingface'
$env:HF_HUB_OFFLINE = '1'
$env:TRANSFORMERS_OFFLINE = '1'
$env:LOCAL_READING_STAGE = if ($Task -eq 'speech') { 'speech' } else { 'prepare' }
$readingArgs = @('-B','-u','tools/local-reading.py')
if ($Task -eq 'speech') { $readingArgs += @('prepare','--types','.m4v,.mp4') }
elseif ($Task -eq 'prepare') { $readingArgs += @('prepare','--types','.pdf,.docx,.txt,.mp3,.lnk') }
else { $readingArgs += $Task }
if ($Limit -gt 0) { $readingArgs += @('--limit',"$Limit") }
$readingLogFolder = Join-Path $readingState 'logs'
New-Item -ItemType Directory -Force -Path $readingLogFolder | Out-Null
$readingStamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')
$readingStdout = Join-Path $readingLogFolder ($Task + '-' + $readingStamp + '.stdout.log')
$readingStderr = Join-Path $readingLogFolder ($Task + '-' + $readingStamp + '.stderr.log')
$readingProcess = Start-Process -FilePath (Get-Command python).Source -ArgumentList $readingArgs -WorkingDirectory $readingRoot -WindowStyle Hidden -RedirectStandardOutput $readingStdout -RedirectStandardError $readingStderr -PassThru
@{task=$Task;pid=$readingProcess.Id;started_utc=[DateTime]::UtcNow.ToString('o');arguments=$readingArgs;stdout_log=$readingStdout;stderr_log=$readingStderr} | ConvertTo-Json | Set-Content -LiteralPath $readingPidFile -Encoding UTF8
Write-Output "Started $Task PID $($readingProcess.Id). Logs and checkpoints: $readingState"
