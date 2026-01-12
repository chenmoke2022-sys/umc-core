# Benchmarks（说明）：对标方法与证据口径

> 原则：只对标公开可获得基线；所有结论以证据工件为准（`artifacts/env.json`、`artifacts/results.json`、`artifacts/report.md`）。

## 1. 基线定义（示例）

- 基线名称与版本：`GGUF Q2_K`（以 `artifacts/results.json` 中记录的基线信息为准）
- 量化/档位：以 `results.json` 的字段记录为准（避免口头描述）
- 运行后端：以 `results.json` 的字段记录为准（含版本/commit 时优先记录）

## 2. 测试矩阵（示例）

- 设备：以 `artifacts/env.json` 记录为准（CPU/RAM/OS）
- 模型：以 `artifacts/results.json` 记录为准（名称/格式/参数规模等）
- 场景：cold start / 长对话 / 吞吐压测 / 内存压力（按需要选择并写入 `results.json`）

## 3. 输出工件（对外统一入口）

- `artifacts/env.json`
- `artifacts/results.json`
- `artifacts/report.md`
- `artifacts/manifest.json`（完整性清单）


