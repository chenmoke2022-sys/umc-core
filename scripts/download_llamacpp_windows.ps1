param(
  [string]$OutDir,
  [switch]$Force,
  [int]$Retries = 5,
  [int]$RetryDelaySeconds = 2
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-DefaultCacheDir {
  $base = $env:LOCALAPPDATA
  if ([string]::IsNullOrWhiteSpace($base)) { $base = $HOME }
  return (Join-Path $base "umc_cache\llama.cpp")
}

if ([string]::IsNullOrWhiteSpace($OutDir)) { $OutDir = Get-DefaultCacheDir }

function Invoke-WithRetry {
  param(
    [scriptblock]$Block,
    [int]$Retries = 5,
    [int]$DelaySeconds = 2
  )
  for ($i = 1; $i -le $Retries; $i++) {
    try {
      return & $Block
    } catch {
      if ($i -eq $Retries) { throw }
      Write-Host "WARN: attempt $i failed: $($_.Exception.Message)"
      Start-Sleep -Seconds ($DelaySeconds * $i)
    }
  }
}

Write-Host "== Download llama.cpp (Windows) =="
Write-Host "cache_dir: $OutDir"

$api = "https://api.github.com/repos/ggerganov/llama.cpp/releases/latest"
$release = Invoke-WithRetry -Retries $Retries -DelaySeconds $RetryDelaySeconds -Block {
  Invoke-RestMethod -Uri $api -Headers @{ "User-Agent" = "sw_public" } -TimeoutSec 30
}
if ($null -eq $release.assets) { throw "No assets found in latest release response." }

# Pick a Windows x64 zip (prefer CPU)
$asset = $release.assets | Where-Object {
  $n = $_.name
  if ($null -eq $n) { return $false }
  $s = $n.ToString().ToLowerInvariant()
  ($s.EndsWith(".zip")) -and ($s.Contains("win")) -and ($s.Contains("x64")) -and ($s.Contains("cpu"))
} | Select-Object -First 1

if ($null -eq $asset) {
  $asset = $release.assets | Where-Object {
    $n = $_.name
    if ($null -eq $n) { return $false }
    $s = $n.ToString().ToLowerInvariant()
    ($s.EndsWith(".zip")) -and ($s.Contains("win")) -and ($s.Contains("x64"))
  } | Select-Object -First 1
}
if ($null -eq $asset) { throw "Could not find a Windows zip asset in llama.cpp latest release." }

Write-Host "Selected asset: $($asset.name)"

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }

$zipPath = Join-Path $OutDir $asset.name
if ((Test-Path $zipPath) -and (-not $Force)) {
  Write-Host "Zip already exists (use -Force to re-download): $zipPath"
} else {
  Write-Host "Downloading to: $zipPath"
  Invoke-WithRetry -Retries $Retries -DelaySeconds $RetryDelaySeconds -Block {
    Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $zipPath -TimeoutSec 0
  }
}

Write-Host "Extracting..."
$extractDir = Join-Path $OutDir ("release-" + ($release.tag_name -replace "[^a-zA-Z0-9._-]", "_"))
if ((Test-Path $extractDir) -and $Force) { Remove-Item -Recurse -Force $extractDir }
if (-not (Test-Path $extractDir)) { New-Item -ItemType Directory -Force -Path $extractDir | Out-Null }

Expand-Archive -Path $zipPath -DestinationPath $extractDir -Force

$bench = Get-ChildItem -Path $extractDir -Recurse -Filter "llama-bench.exe" | Select-Object -First 1
$cli = Get-ChildItem -Path $extractDir -Recurse -Filter "llama-cli.exe" | Select-Object -First 1

if ($null -ne $bench) { Write-Host "llama-bench.exe: $($bench.FullName)" }
if ($null -ne $cli) { Write-Host "llama-cli.exe:   $($cli.FullName)" }

if ($null -eq $bench) {
  throw "Downloaded llama.cpp release did not contain llama-bench.exe. Please pick a different asset or provide a custom build."
}

Write-Host "DONE."


