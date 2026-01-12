# One-page report (baseline_measured)

This repository is an **engineering evidence pack**. Claims are backed by `artifacts/results.json` and reproducible steps in `REPRODUCE.md`.

## Summary

- This public pack currently publishes **baseline-measured** numbers (GGUF / llama.cpp / Q2_K) under a fixed methodology.
- Candidate (UMC L8) numbers are **not** claimed unless measured and recorded under the same methodology.

## Baseline (measured)

- Baseline: **GGUF / llama.cpp / Q2_K**
- Cold start (p50/p95): **567.2ms / 694.8ms**
- Peak RSS: **378.0MB**
- Stability: **30 minutes, crash_count = 0**

## How to reproduce

See `REPRODUCE.md`. Evidence artifacts:

- `artifacts/env.json`
- `artifacts/results.json`
- `artifacts/report.md`
- `artifacts/manifest.json` (integrity)

## Risk & rollback

- Results vary by hardware and system load; the goal is **methodology consistency**, not identical numbers.
- If artifacts are incomplete or audit fails, revert to the previous release/tag and regenerate artifacts + manifest.


