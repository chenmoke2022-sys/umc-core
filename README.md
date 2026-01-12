# UMC Core (Universal Model Container)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey)]()
[![Status](https://img.shields.io/badge/Status-Public%20Baseline-green)]()

> **Universal Model Container (UMC)** is an engineering standard for reproducible, auditable, and rollback-ready edge inference artifacts.

---

## 🎯 核心目标 (Mission)

我构建这个项目的初衷，是为了解决端侧模型部署中的**“最后一公里信任问题”**：
如何证明一个量化后的模型在低资源设备上既快又稳，且不仅是口头承诺？

UMC Core 提供了一套标准化的**工程证据包 (Evidence Pack)** 方案：

*   ✅ **可复现 (Reproducible)**：通过标准化的 `REPRODUCE.md` 流程，任何人都能跑出一致的指标。
*   ✅ **可审计 (Auditable)**：所有结论绑定 `manifest.json` 完整性校验，拒绝“黑箱”。
*   ✅ **生产就绪 (Production-Ready)**：内置回滚策略与长跑稳定性门禁（Stability Gates）。

---

## 📦 包含内容 (What's Inside)

本仓库展示了 **L8 (8-bit)** 基线版本的工程化闭环：

| 模块 | 说明 | 关键文件 |
| :--- | :--- | :--- |
| **Evidence** | 核心证据工件（环境/指标/报告/校验） | `artifacts/` |
| **Specs** | 容器与格式规范草案 | `spec/SPEC_UMC_FORMAT.md` |
| **Tools** | 自动化采集与审计脚本 | `tools/` |
| **Policy** | 发布门禁与合规策略（已合并到 README/AUDIT） | `AUDIT.md` |

---

## 🚀 快速复现 (Quick Start)

你可以通过以下命令，一键生成并校验当前的工程证据包：

```powershell
# 1. 生成环境指纹与示例工件（用于演示与审计口径）
pwsh .\scripts\make_demo_artifacts.ps1

# 2. 运行完整性审计
pwsh .\scripts\audit_public.ps1
```

输出结果将位于 `artifacts/` 目录中，包含一份人类可读的 `report.md`。

## 📤 Export bundle (optional)

To package a minimal evidence bundle, run:

```powershell
pwsh .\scripts\make_share_bundle.ps1
```

The generated `share_bundle/` contains `README/AUDIT/REPRODUCE/SECURITY + artifacts` only (no weights / private data).

---

## ⚖️ Scope & Claims

*   **Evidence-first**：本仓库的对外主张仅限 `artifacts/` 覆盖到的内容（env/results/report/manifest）。
*   **No forward-looking claims**：不发布不可验证的路线承诺或“隐藏能力”暗示。
*   **Risk control**：对未知风险采用安全默认配置；需要时以更严格的复现与审计门禁进入已验证档。

---

## 🔮 Scope

本仓库只聚焦于一个可复现的工程证据闭环（L8 baseline）与最小门禁工具链；不包含任何模型权重或私有数据。

---

## 🔒 使用范围 (Scope)

这是一个用于展示工程交付能力的仓库：聚焦“证据闭环 + 审计门禁 + 回滚策略”。  
为保持材料可控，本仓库默认不接收外部贡献。

> **注意**：本仓库严格脱敏，**请勿提交**任何模型权重、私有数据集或包含敏感路径的文件。

---

License: [MIT](LICENSE)
