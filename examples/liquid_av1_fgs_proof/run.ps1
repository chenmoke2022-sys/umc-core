param(
  [Parameter(Mandatory = $true)]
  [string]$InputPath,

  [string]$OutDir = ".\artifacts",

  [int]$Crf = 60,
  [int]$Preset = 8,
  [int]$FgsLevel = 25,
  [int]$FgsDenoise = 1,

  # 0 = full
  [int]$Frames = 0,

  # libvmaf n_subsample (1 = strict/slow)
  [int]$VmafSubsample = 2,

  [ValidateSet("redacted", "raw")]
  [string]$Frame1Mode = "raw",

  [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Python {
  param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
  )
  python @Args
  if ($LASTEXITCODE -ne 0) {
    throw "python failed (exit=$LASTEXITCODE): $($Args -join ' ')"
  }
}

Push-Location $PSScriptRoot
try {
  $art = $OutDir
  New-Item -ItemType Directory -Force -Path $art | Out-Null

  $argsList = @(
    ".\run.py",
    "--input", $InputPath,
    "--out", $art,
    "--crf", $Crf,
    "--preset", $Preset,
    "--fgs-level", $FgsLevel,
    "--fgs-denoise", $FgsDenoise,
    "--n-subsample", $VmafSubsample,
    "--frame1-mode", $Frame1Mode
  )

  if ($Frames -gt 0) { $argsList += @("--frames", $Frames) }
  if ($Force) { $argsList += @("--force") }

  Invoke-Python @argsList

  # Build evidence pack fields required by public audit gate.
  Invoke-Python ..\..\tools\collect_env.py --out (Join-Path $art "env.json")
  Invoke-Python ..\..\tools\make_manifest.py --dir $art --out (Join-Path $art "manifest.json")
  Invoke-Python ..\..\tools\validate_artifacts.py --artifacts $art
  Invoke-Python ..\..\tools\verify_manifest.py --manifest (Join-Path $art "manifest.json")

  Write-Host "OK: measured artifacts generated at $art"
} finally {
  Pop-Location
}

