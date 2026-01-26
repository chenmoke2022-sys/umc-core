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
*   **`liquid_av1_fgs_proof/` (视频压缩证据包)**：以 [Pexels 4K 视频样本](https://www.pexels.com/zh-cn/video/4k-34629124/) 做 AV1 `CRF60` vs `CRF60+FGS25` 对照，输出压缩倍率 + PSNR/SSIM/VMAF，并提供首帧三联图（可选提交到 `public_assets/`）。
*   **`system_perf_microbench/` (系统微基准)**：C++/Python 微基准：多线程内存拷贝带宽测量 → 结果落盘 → 证据包输出，用于支撑“系统级瓶颈定位与调优”能力展示。
*   **`vllm_sglang_enablement_skeleton/` (框架使能模板)**：使能交付模板：拓扑摘要采集 + 证据包结构 + 回归门禁框架（不含权重/私有数据）。
*   **`triton_op_microbench/` (算子 microbench)**：Triton kernel microbench：可选 CUDA 环境下测量带宽/吞吐；缺失条件时输出 skipped 证据包。

### 3. 系统与架构 (Systems & Architecture)
*   **`mlops_pipeline_toy/` (MLOps)**：展示从“数据质量门禁 → 训练 → 模型注册 → 证据打包”的自动化流水线（附 Airflow DAG 模板）。
*   **`vla_alignment_toy/` (多模态对齐)**：实现 CLIP-style 对比学习训练闭环，并通过对照实验（Linear vs MLP）验证结构对齐效果。

---

> 请进入对应子目录阅读 `README.md` 获取详细运行指南。
