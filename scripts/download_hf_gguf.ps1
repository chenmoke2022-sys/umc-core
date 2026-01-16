param(
  [Parameter(Mandatory=$true)][string]$RepoId,
  [string]$Pattern = "Q2_K",
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
  return (Join-Path $base "umc_cache\gguf")
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

Write-Host "== Download GGUF from Hugging Face =="
Write-Host "repo:      $RepoId"
Write-Host "pattern:   $Pattern"
Write-Host "cache_dir: $OutDir"

$api = "https://huggingface.co/api/models/$RepoId"
$model = Invoke-WithRetry -Retries $Retries -DelaySeconds $RetryDelaySeconds -Block {
  Invoke-RestMethod -Uri $api -Headers @{ "User-Agent" = "sw_public" } -TimeoutSec 30
}
if ($null -eq $model.siblings) { throw "No siblings/files found for repo: $RepoId" }

$file = $model.siblings | Where-Object {
  $name = $_.rfilename
  if ($null -eq $name) { return $false }
  $lower = $name.ToString().ToLowerInvariant()
  ($lower.EndsWith(".gguf")) -and ($name.ToString() -like "*$Pattern*")
} | Select-Object -First 1

if ($null -eq $file) {
  $file = $model.siblings | Where-Object {
    $name = $_.rfilename
    if ($null -eq $name) { return $false }
    $name.ToString().ToLowerInvariant().EndsWith(".gguf")
  } | Select-Object -First 1
}
if ($null -eq $file) { throw "No .gguf file found in repo: $RepoId" }

$filename = $file.rfilename
Write-Host "Selected file: $filename"

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }
$outPath = Join-Path $OutDir ($RepoId -replace "[/\\]", "__")
if (-not (Test-Path $outPath)) { New-Item -ItemType Directory -Force -Path $outPath | Out-Null }

$dest = Join-Path $outPath $filename
if ((Test-Path $dest) -and (-not $Force)) {
  Write-Host "Already exists (use -Force to re-download): $dest"
  Write-Host "DONE. GGUF: $dest"
  return
}

$url = "https://huggingface.co/$RepoId/resolve/main/$filename"
Write-Host "Downloading: $url"
Invoke-WithRetry -Retries $Retries -DelaySeconds $RetryDelaySeconds -Block {
  Invoke-WebRequest -Uri $url -OutFile $dest -TimeoutSec 0
}

Write-Host "DONE. GGUF: $dest"


