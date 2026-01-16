# UMC Core (Public Evidence Pack Template)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey)]()
[![Status](https://img.shields.io/badge/Status-Public%20Baseline-green)]()

> UMC Core 是一套**公开可复现的工程证据包模板**：用最小的结构与门禁，把一次“模型/推理相关的实验结果”固化成可审计、可回归、可分享的交付物（不含权重/私有数据）。

![Benchmark Card (baseline_measured)](assets/benchmark_card.svg)
> Data source: `artifacts/results.json` (baseline_measured).

---

## 🎯 核心目标 (Mission)

我构建这个项目的初衷，是为了探索端侧模型部署中的**“工程可观测性与复现难题”**：
在资源受限的边缘设备上，如何建立一套标准化的验证方法，让量化模型的性能指标（速度、内存、稳定性）变得**可测量、可复现、可回归**？

UMC Core 提供了一套标准化的**工程证据包 (Evidence Pack)** 骨架，用于把“结果”变成可复现的工件：

*   ✅ **可复现 (Reproducible)**：通过标准化的 `REPRODUCE.md` 流程，致力于让任何人都能在同等环境下跑出一致的指标。
*   ✅ **可审计 (Auditable)**：所有结论绑定 `manifest.json` 完整性校验，提升交付物的透明度与可追溯性。
*   ✅ **生产就绪 (Production-Ready)**：引入回滚策略与长跑稳定性门禁（Stability Gates），探索工业级交付的可靠性。

---

## 📦 包含内容 (What's Inside)

本仓库展示了 **L8 baseline（公开口径）** 的工程化闭环：

| 模块 | 说明 | 关键文件 |
| :--- | :--- | :--- |
| **Evidence** | 核心证据工件（环境/指标/报告/校验） | `artifacts/` |
| **Paper** | 写作草稿（可选，不作为能力门槛） | `paper/PREPRINT_DRAFT.md` |
| **Specs** | 容器与格式规范草案 | `spec/SPEC_UMC_FORMAT.md` |
| **Tools** | 自动化采集与审计脚本 | `tools/` |
| **Policy** | 发布门禁与合规策略（已合并到 README/AUDIT） | `AUDIT.md` |

---

## 🧭 路线图（探索性）

> 目标：把“优化动作”逐步沉淀为可复现、可审计、可回滚的工作流；一切以证据工件与统一口径为准，不做不可验证承诺。

*   **AI 辅助工作流（探索中）**：用 AI 工具加速脚本化与自动化，但对外只呈现可复现工件与门禁结果；不做不可验证承诺。
*   **算子/运行时兼容性（探索中）**：面向端侧/边缘设备的运行时适配与兼容性验证（例如算子对齐、资源预算与回滚策略），以降低落地成本与线上风险。

## 🚀 快速开始

运行以下命令：

```powershell
# 1) 生成演示产物 (Generate demo artifacts)
pwsh .\scripts\make_demo_artifacts.ps1

# 2) 运行审计门禁 (Run audit gate)
pwsh .\scripts\audit_public.ps1
```

输出将写入 `artifacts/` 目录。

## 📤 导出分享包 (可选)

打包一个最小化的证据包（不含权重）：

```powershell
pwsh .\scripts\make_share_bundle.ps1
```

生成的 `share_bundle/` 仅包含 `README/AUDIT/REPRODUCE/SECURITY + artifacts`，不含任何模型权重或私有数据。

---

## ⚖️ 范围与声明 (Scope & Claims)

*   **证据优先 (Evidence-first)**：本仓库的对外主张仅限 `artifacts/` 覆盖到的内容（env/results/report/manifest）。
*   **无前瞻性承诺 (No forward-looking claims)**：不发布不可验证的路线承诺或“隐藏能力”暗示。
*   **风险控制 (Risk control)**：对未知风险采用安全默认配置；需要时以更严格的复现与审计门禁进入已验证档。

---

## 🔮 范围 (Scope)

本仓库只聚焦于一个可复现的工程证据闭环（L8 baseline）与最小门禁工具链；不包含任何模型权重或私有数据。

---

## 🔒 边界声明 (Boundary)

本仓库不接受外部代码贡献。

**不包含**任何模型权重或私有数据集。

---

License: [MIT](LICENSE)
