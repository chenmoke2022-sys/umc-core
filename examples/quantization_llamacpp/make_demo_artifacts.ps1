Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot/../..
try {
  $art = ".\examples\quantization_llamacpp\artifacts"
  New-Item -ItemType Directory -Force -Path $art | Out-Null

  python .\tools\collect_env.py --out (Join-Path $art "env.json")

  @'
{
  "schema_version": "1.0",
  "data_status": "example",
  "baseline": {
    "name": "llama.cpp quantization workflow (example)",
    "version": "n/a",
    "quant_profile": "GGUF / Q4_K_M (example)",
    "backend": "llama.cpp"
  },
  "device": { "os": "<FILL>", "cpu": "<FILL>", "ram_gb": "<FILL>" },
  "metrics": {
    "load_time_ms_p50": 0,
    "load_time_ms_p95": 0,
    "peak_memory_mb": 0,
    "long_run_minutes": 0,
    "crash_count": 0,
    "throughput_tokens_per_s_p50": 0,
    "throughput_tokens_per_s_p95": 0
  },
  "notes": {
    "scope": "Demo placeholder. Replace with real measurements when available."
  }
}
'@ | Set-Content -Encoding UTF8 (Join-Path $art "results.json")

  @'
# Quantization workflow — 1-page report (example)

## What this proves
- I can define a reproducible measurement methodology for quantized inference artifacts.
- I can produce an auditable evidence pack (env/results/report/manifest) with integrity checks.

## Method
- Backend: llama.cpp (or equivalent)
- Compare multiple GGUF quant profiles (e.g., Q8_0 / Q4_K_M / Q2_K)
- Record: cold start (p50/p95), peak RSS, optional throughput

## Results
- This file is an **example** placeholder. Replace numbers after running `run.ps1`.

## Risks & rollback
- If quality drop exceeds threshold, rollback to higher-bit profile.
- If latency variance is high, re-check batch size, thread affinity, and IO.
'@ | Set-Content -Encoding UTF8 (Join-Path $art "report.md")

  python .\tools\make_manifest.py --dir $art --out (Join-Path $art "manifest.json")
  python .\tools\verify_manifest.py --manifest (Join-Path $art "manifest.json")

  Write-Host "OK: demo artifacts generated at $art"
} finally {
  Pop-Location
}

