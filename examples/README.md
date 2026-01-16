# Examples — 能力证明示例（公开/可复现）

本目录包含一系列**微型工程示例 (Toy Examples)**，用于证明我在模型压缩、推理优化与 MLOps 领域的工程落地能力。

**核心原则**：
*   ✅ **零权重/零私有数据**：完全基于公开/合成数据，合规安全。
*   ✅ **可复现 (Reproducible)**：提供一键运行脚本。
*   ✅ **可审计 (Auditable)**：统一输出 `env/results/report/manifest` 标准证据包。

## 示例列表

### 1. 模型压缩与推理 (Model Compression)
*   **`quantization_llamacpp/` (量化)**：展示基于 llama.cpp 的量化工作流与推理侧指标采集（GGUF 路线）。
*   **`pruning_toy/` (剪枝)**：幅值剪枝 vs 随机剪枝的对照实验，验证稀疏化对精度的影响（离线运行）。
*   **`distillation_toy/` (蒸馏)**：Teacher-Student Logits 蒸馏实验，展示知识蒸馏的基本工程闭环（离线运行）。

### 2. 性能工程与基准 (Performance Engineering)
*   **`inference_profiling/` (性能分析)**：演示“Profiling → 优化改动 → 复测 → 回归门禁”的标准优化工作流模板。
*   **`feature_compression_toy/` (特征压缩)**：定义 Rate/Distortion 评测口径，并进行带宽约束下的健全性检查（Sanity Check）。

### 3. 系统与架构 (Systems & Architecture)
*   **`mlops_pipeline_toy/` (MLOps)**：展示从“数据质量门禁 → 训练 → 模型注册 → 证据打包”的自动化流水线（附 Airflow DAG 模板）。
*   **`vla_alignment_toy/` (多模态对齐)**：实现 CLIP-style 对比学习训练闭环，并通过对照实验（Linear vs MLP）验证结构对齐效果。

---

> 请进入对应子目录阅读 `README.md` 获取详细运行指南。
