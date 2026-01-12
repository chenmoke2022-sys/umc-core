# One-page report

All claims must be backed by `artifacts/results.json` and reproducible steps in `REPRODUCE.md`.

## Summary

- Cold start（p50/p95）已记录在 `metrics.load_time_ms_p50/p95`
- 峰值内存与长跑稳定性已记录在 `metrics.peak_memory_mb` 与 `metrics.crash_count`

## 复现方式

见 `REPRODUCE.md`。

## 环境摘要

见 `artifacts/env.json`。

## 指标摘要

见 `artifacts/results.json`。

## Risk & rollback

- Risk: results vary by hardware and system load.
- Rollback: revert to the previous release/tag if artifacts are incomplete or audit fails.


