Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot/../..
try {
  $art = ".\examples\inference_profiling\artifacts"
  New-Item -ItemType Directory -Force -Path $art | Out-Null

  python .\tools\collect_env.py --out (Join-Path $art "env.json")

  @'
{
  "schema_version": "1.0",
  "data_status": "example",
  "baseline": { "name": "inference profiling template (example)", "version": "n/a", "quant_profile": "n/a", "backend": "n/a" },
  "device": { "os": "<FILL>", "cpu": "<FILL>", "ram_gb": "<FILL>" },
  "metrics": { "load_time_ms_p50": 0, "load_time_ms_p95": 0, "peak_memory_mb": 0, "long_run_minutes": 0, "crash_count": 0 },
  "notes": { "scope": "Template only. Replace with real profiling + measurement results." }
}
'@ | Set-Content -Encoding UTF8 (Join-Path $art "results.json")

  @'
# Inference profiling report (example)

This is a template evidence pack for recording profiling and optimization work.

Recommended workflow:
- Baseline measurement → profile hotspots → one change at a time → re-measure → gate & rollback.
'@ | Set-Content -Encoding UTF8 (Join-Path $art "report.md")

  python .\tools\make_manifest.py --dir $art --out (Join-Path $art "manifest.json")
  python .\tools\verify_manifest.py --manifest (Join-Path $art "manifest.json")

  Write-Host "OK: demo artifacts generated at $art"
} finally {
  Pop-Location
}

