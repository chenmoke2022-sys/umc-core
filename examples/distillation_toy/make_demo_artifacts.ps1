Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot/../..
try {
  $art = ".\examples\distillation_toy\artifacts"
  New-Item -ItemType Directory -Force -Path $art | Out-Null

  python .\tools\collect_env.py --out (Join-Path $art "env.json")

  @'
{
  "schema_version": "1.0",
  "data_status": "example",
  "baseline": { "name": "toy distillation experiment (example)", "version": "n/a", "quant_profile": "n/a", "backend": "pytorch" },
  "device": { "os": "<FILL>", "cpu": "<FILL>", "ram_gb": "<FILL>" },
  "metrics": {
    "load_time_ms_p50": 0, "load_time_ms_p95": 0, "peak_memory_mb": 0, "long_run_minutes": 0, "crash_count": 0,
    "toy_student_acc_plain": 0.0, "toy_student_acc_distilled": 0.0
  }
}
'@ | Set-Content -Encoding UTF8 (Join-Path $art "results.json")

  @'
# Distillation toy report (example)

This is an example placeholder. Run `pwsh .\examples\distillation_toy\run.ps1` to generate measured results.
'@ | Set-Content -Encoding UTF8 (Join-Path $art "report.md")

  python .\tools\make_manifest.py --dir $art --out (Join-Path $art "manifest.json")
  python .\tools\verify_manifest.py --manifest (Join-Path $art "manifest.json")

  Write-Host "OK: demo artifacts generated at $art"
} finally {
  Pop-Location
}

