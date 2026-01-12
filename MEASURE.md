# MEASURE — Baseline Measurement Notes (Public)

This repository publishes **baseline-measured** numbers under a fixed methodology (see `artifacts/results.json`).

## What is measured (public baseline)

- **Cold start**: `load_time_ms_p50/p95`
- **Memory**: `peak_memory_mb` (RSS)
- **Stability**: `long_run_minutes`, `crash_count`

## Methodology (minimal)

- **Backend**: `llama.cpp`
- **Baseline format/profile**: `GGUF / Q2_K` (recorded in `artifacts/results.json`)
- **Reproducibility rule**: prioritize *methodology consistency* over identical numbers across machines.

## How to update results.json (when you re-measure)

- Re-run your benchmark under the same methodology you intend to claim.
- Update `artifacts/results.json` fields only.
- Re-generate and verify `artifacts/manifest.json`:

```powershell
python .\tools\make_manifest.py --dir .\artifacts --out .\artifacts\manifest.json
python .\tools\verify_manifest.py --manifest .\artifacts\manifest.json
```

## Scope boundary

- This repo does **not** include model weights or private datasets.
- Quality / accuracy claims are **out of scope** unless accompanied by equivalent public evidence artifacts.


