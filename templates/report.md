# 一页报告（模板｜示例结构）

> 说明：这是对外报告的**示例结构**，用于统一口径与审计方式。对外主张必须能在 `artifacts/` 中找到对应证据。

## 结论（示例：必须可复现）

- 结论 1：本次发布包含完整的工程证据闭环（环境指纹、结构化结果、一页报告、完整性清单），可被复核与审计。  
  - 证据位置：`artifacts/env.json`、`artifacts/results.json`、`artifacts/report.md`、`artifacts/manifest.json`
- 结论 2：本项目强调“口径一致”优先于“数值绝对一致”；复核时以相同口径与环境指纹为准。  
  - 证据位置：`artifacts/env.json`（环境）+ `artifacts/results.json`（字段与结果）

## 复现方式

见 `REPRODUCE.md`。

## 环境摘要

见 `artifacts/env.json`。

## 指标摘要

见 `artifacts/results.json`。

## 风险与回滚（示例）

- 风险：不同硬件、后台负载、电源策略会引入波动；复核时请记录环境指纹并保持口径一致。  
- 回滚策略：出现回归时优先回退到上一个已验证稳定档，并重新生成/校验证据工件与完整性清单。


