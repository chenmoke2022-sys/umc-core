# One-page report (template)

Claims must be backed by files under `artifacts/`.

## Summary

- Evidence: `artifacts/env.json`, `artifacts/results.json`, `artifacts/report.md`, `artifacts/manifest.json`
- Reproduction: `REPRODUCE.md`

## 复现方式

见 `REPRODUCE.md`。

## 环境摘要

见 `artifacts/env.json`。

## 指标摘要

见 `artifacts/results.json`。

## Risk & rollback

- Risk: results vary by hardware, load, and power settings.
- Rollback: revert to the last known-good release and re-generate artifacts + manifest.


