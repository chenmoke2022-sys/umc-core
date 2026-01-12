# 审计说明（AUDIT）

This document defines what the repository claims, where the evidence lives, and how to verify integrity.

## 1. 对外声明范围（Claims Scope）

This repository is an **Engineering Evidence Pack** for a reproducible L8 baseline.

- **对外可审计的结论**：仅限 `artifacts/` 目录中的证据工件所覆盖的内容（见第 2 节）。
- **不在对外声明范围**：
  - 任何不可验证的能力宣称或路线承诺
  - 任何私有模型权重、私有数据集、内部实现细节
  - 任何不可验证的“无损/几乎无损”质量承诺（除非提供同口径质量证据）

## 2. 证据工件（Evidence Artifacts）

本目录采用“三件套”做证据闭环：

- `artifacts/env.json`：环境指纹（OS/CPU/RAM 等）
- `artifacts/results.json`：结构化结果（机器可读）
- `artifacts/report.md`：一页报告（人类可读）

并提供完整性校验：

- `artifacts/manifest.json`：文件大小 + SHA256 清单

## 3. 完整性校验（Integrity Verification）

校验方式：

```powershell
python .\tools\verify_manifest.py --manifest .\artifacts\manifest.json
```

校验成功应输出 `OK`；否则脚本会返回非 0 退出码。

## 4. 复现口径（Reproduce）

Reproduction instructions are in `REPRODUCE.md`. Results vary by hardware and load; consistency of method matters.

## 5. 脱敏边界（Redaction Boundary）

本目录不包含：

- 模型权重文件
- 私有训练/校准数据
- 内部路径、账号、密钥等敏感信息

If you believe something sensitive is present, stop distribution and report it.


