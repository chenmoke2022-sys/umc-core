Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot/../..
try {
  $art = ".\examples\pruning_toy\artifacts"
  New-Item -ItemType Directory -Force -Path $art | Out-Null

  python .\tools\collect_env.py --out (Join-Path $art "env.json")

  python .\examples\pruning_toy\run.py --out $art --seed 0 --prune_ratio 0.5

  python .\tools\make_manifest.py --dir $art --out (Join-Path $art "manifest.json")
  python .\tools\verify_manifest.py --manifest (Join-Path $art "manifest.json")

  Write-Host "OK: pruning toy evidence pack ready at $art"
} finally {
  Pop-Location
}

