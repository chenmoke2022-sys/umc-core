param(
  [Parameter(Mandatory=$true)][string]$BenchJson,
  [string]$ArtifactsDir = ".\\artifacts"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot/..
try {
  if (-not (Test-Path $BenchJson)) { throw "bench.json not found: $BenchJson" }
  if (-not (Test-Path $ArtifactsDir)) { throw "artifacts dir not found: $ArtifactsDir" }

  $results = Join-Path $ArtifactsDir "results.json"
  if (-not (Test-Path $results)) { throw "results.json not found: $results" }

  Write-Host "[1/4] apply bench -> artifacts/results.json"
  python .\tools\apply_bench_to_results.py --bench $BenchJson --results $results

  Write-Host "[2/4] re-generate manifest.json"
  python .\tools\make_manifest.py --dir $ArtifactsDir --out (Join-Path $ArtifactsDir "manifest.json")

  Write-Host "[3/4] validate + verify"
  python .\tools\validate_artifacts.py --artifacts $ArtifactsDir
  python .\tools\verify_manifest.py --manifest (Join-Path $ArtifactsDir "manifest.json")

  Write-Host "[4/4] run public audit gate"
  pwsh .\scripts\audit_public.ps1

  Write-Host "OK: bench applied and artifacts updated"
} finally {
  Pop-Location
}


