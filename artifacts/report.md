# 一页报告（Example）

> 这是一份示例报告，用于展示“证据包应该长什么样”。实际对外结论以 `artifacts/results.json` 与复现流程为准。

## 结论（示例）

- Cold start（p50/p95）已记录在 `metrics.load_time_ms_p50/p95`
- 峰值内存与长跑稳定性已记录在 `metrics.peak_memory_mb` 与 `metrics.crash_count`

## 复现方式

见 `REPRODUCE.md`。

## 环境摘要

见 `artifacts/env.json`。

## 指标摘要

见 `artifacts/results.json`。

## 风险与回滚

- 风险：不同硬件/系统负载会导致数值波动；请优先保证“口径一致”
- 回滚策略：如证据不全或审计失败，撤回发布并回退到上一版本 tag


