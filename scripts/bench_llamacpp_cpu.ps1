param(
  [Parameter(Mandatory=$true)][string]$LlamaBench,
  [Parameter(Mandatory=$true)][string]$ModelGguf,
  [string]$OutJson,
  [int]$Runs = 5,
  [int]$PromptTokens = 8,
  [int]$GenTokens = 1,
  [int]$LongRunMinutes = 30,
  [string]$ProgressLog = ".\\_logs\\bench_progress.log"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-DefaultBenchOut {
  $t = $env:TEMP
  if ([string]::IsNullOrWhiteSpace($t)) { $t = $HOME }
  return (Join-Path $t "sw_public_bench.json")
}
if ([string]::IsNullOrWhiteSpace($OutJson)) { $OutJson = Get-DefaultBenchOut }

function Get-Ms {
  param([datetime]$Start, [datetime]$End)
  return [math]::Round(($End - $Start).TotalMilliseconds, 1)
}

if (-not (Test-Path $LlamaBench)) { throw "llama-bench not found: $LlamaBench" }
if (-not (Test-Path $ModelGguf)) { throw "GGUF model not found: $ModelGguf" }

$progressDir = Split-Path -Parent $ProgressLog
if ($progressDir -and (-not (Test-Path $progressDir))) { New-Item -ItemType Directory -Force -Path $progressDir | Out-Null }
Add-Content -Path $ProgressLog -Encoding UTF8 -Value ("[{0}] START runs={1} long_run_minutes={2}" -f (Get-Date).ToString("s"), $Runs, $LongRunMinutes)

Write-Host "== bench llama.cpp (CPU) =="
Write-Host "llama-bench: $LlamaBench"
Write-Host "model:      $ModelGguf"
Write-Host "out_json:   $OutJson"
Write-Host "NOTE: out_json contains local absolute paths; do NOT place it under the repo or commit it."

$times = New-Object System.Collections.Generic.List[double]
$peakRss = New-Object System.Collections.Generic.List[double]
$crashCount = 0

for ($i=1; $i -le $Runs; $i++) {
  $tmpOut = [System.IO.Path]::GetTempFileName()
  $tmpErr = [System.IO.Path]::GetTempFileName()
  $start = Get-Date
  $p = Start-Process -FilePath $LlamaBench -ArgumentList @(
    "-m", $ModelGguf,
    "-o", "json",
    "-r", "1",
    "-p", "$PromptTokens",
    "-n", "$GenTokens",
    "--no-warmup"
  ) -NoNewWindow -PassThru -RedirectStandardOutput $tmpOut -RedirectStandardError $tmpErr

  $maxWs = 0
  while (-not $p.HasExited) {
    try {
      $gp = Get-Process -Id $p.Id -ErrorAction Stop
      if ($gp.WorkingSet64 -gt $maxWs) { $maxWs = $gp.WorkingSet64 }
    } catch { }
    Start-Sleep -Milliseconds 50
  }
  $p.Refresh()
  $end = Get-Date

  $ms = Get-Ms $start $end
  $times.Add($ms) | Out-Null

  $rss = $null
  try {
    $peak = [math]::Max([double]$maxWs, [double]$p.PeakWorkingSet64)
    if ($peak -gt 0) { $rss = [math]::Round(($peak / 1MB), 1) }
  } catch { }
  if ($null -ne $rss) { $peakRss.Add([double]$rss) | Out-Null }

  if ($p.ExitCode -ne 0) { $crashCount++ }
  Write-Host ("run#{0}: {1}ms exit={2} peak_rss_mb={3}" -f $i, $ms, $p.ExitCode, $rss)
  Add-Content -Path $ProgressLog -Encoding UTF8 -Value ("[{0}] short_run {1}/{2} ms={3} exit={4} peak_rss_mb={5}" -f (Get-Date).ToString("s"), $i, $Runs, $ms, $p.ExitCode, $rss)

  Remove-Item -Force $tmpOut -ErrorAction SilentlyContinue
  Remove-Item -Force $tmpErr -ErrorAction SilentlyContinue
}

function Percentile {
  param([double[]]$arr, [double]$p)
  if ($arr.Length -eq 0) { return $null }
  $sorted = $arr | Sort-Object
  $idx = [math]::Ceiling(($p/100.0)*$sorted.Length) - 1
  if ($idx -lt 0) { $idx = 0 }
  if ($idx -ge $sorted.Length) { $idx = $sorted.Length - 1 }
  return [math]::Round($sorted[$idx], 1)
}

$timesArr = $times.ToArray()
$rssArr = $peakRss.ToArray()

$loadP50 = Percentile $timesArr 50
$loadP95 = Percentile $timesArr 95
$peakRssMb = if ($rssArr.Length -gt 0) { [math]::Round(($rssArr | Measure-Object -Maximum).Maximum, 1) } else { $null }

# Long-run stability: repeat short runs until time budget
$deadline = (Get-Date).AddMinutes($LongRunMinutes)
$longRuns = 0
$longCrashes = 0
$lastBeat = Get-Date
while ((Get-Date) -lt $deadline) {
  $tmpOut2 = [System.IO.Path]::GetTempFileName()
  $tmpErr2 = [System.IO.Path]::GetTempFileName()
  $p2 = Start-Process -FilePath $LlamaBench -ArgumentList @(
    "-m", $ModelGguf,
    "-o", "json",
    "-r", "1",
    "-p", "1",
    "-n", "1",
    "--no-warmup"
  ) -NoNewWindow -PassThru -Wait -RedirectStandardOutput $tmpOut2 -RedirectStandardError $tmpErr2
  $longRuns++
  if ($p2.ExitCode -ne 0) { $longCrashes++ }
  Remove-Item -Force $tmpOut2 -ErrorAction SilentlyContinue
  Remove-Item -Force $tmpErr2 -ErrorAction SilentlyContinue

  $now = Get-Date
  if (($now - $lastBeat).TotalSeconds -ge 60) {
    $elapsedMin = [math]::Floor((($now) - ($deadline.AddMinutes(-$LongRunMinutes))).TotalMinutes)
    Add-Content -Path $ProgressLog -Encoding UTF8 -Value ("[{0}] heartbeat elapsed_min={1} long_runs={2} crash_count={3}" -f $now.ToString("s"), $elapsedMin, $longRuns, $longCrashes)
    $lastBeat = $now
  }
}

$out = @{
  schema_version = "1.0"
  method = "llama.cpp-bench-cpu"
  runs = $Runs
  prompt_tokens = $PromptTokens
  gen_tokens = $GenTokens
  metrics = @{
    load_time_ms_p50 = $loadP50
    load_time_ms_p95 = $loadP95
    peak_rss_mb = $peakRssMb
    stability = @{
      long_run_minutes = $LongRunMinutes
      crash_count = $longCrashes
      notes = "CPU loop of llama-bench invocations; crash_count counts non-zero exit codes"
    }
  }
  inputs = @{
    llama_bench = $LlamaBench
    model_gguf = $ModelGguf
  }
}

$outDir = Split-Path -Parent $OutJson
if ($outDir -and (-not (Test-Path $outDir))) { New-Item -ItemType Directory -Force -Path $outDir | Out-Null }
$out | ConvertTo-Json -Depth 20 | Set-Content -Path $OutJson -Encoding UTF8
Write-Host "Wrote bench json: $OutJson"
Add-Content -Path $ProgressLog -Encoding UTF8 -Value ("[{0}] END wrote={1}" -f (Get-Date).ToString("s"), $OutJson)


