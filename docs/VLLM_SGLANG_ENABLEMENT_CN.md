# vLLM / sglang 新硬件使能与优化：交付模板（公开版）

> **定位**：给出“新硬件使能 + 推理性能优化”的可交付物结构与验证口径。  
> **边界**：不包含厂商 NDA 内容；不包含权重/私有数据；不做不可验证的性能承诺。对外声明以证据包为准。

---

## 1. 交付物（Deliverables）

一份可验收的“框架使能/优化交付”建议包含：

- **Enablement Checklist**：编译链/依赖、后端选择、算子路径、回退策略、已知限制。
- **Profiling 证据**：端到端 trace、热点分解、瓶颈定位结论与反证实验记录。
- **Regression Gate**：同口径基线、容差阈值、回归触发条件、回滚条件。
- **场景化配置**：不同业务场景（吞吐/时延/显存/稳定性/成本）的参数方案与边界说明。

---

## 2. 使能检查清单（Enablement Checklist）

### 2.1 硬件与拓扑

- GPU 型号/显存容量/驱动版本、互联拓扑（PCIe/NVLink）、多卡跨 NUMA 情况
- CPU sockets/NUMA nodes、内存容量与带宽特征
- 网络与存储（若涉及分布式/远程加载）

### 2.2 软件栈与编译链

- CUDA/ROCm/OneAPI 等运行时版本与兼容矩阵（以公开文档为准）
- 编译器与编译选项，关键依赖版本锁定
- 框架后端与 kernel 路径（CUDA kernel / Triton / CUTLASS / FlashAttention 等）

### 2.3 回退与降级策略

- 算子回退（fast path → fallback path）的触发条件
- OOM 与长跑稳定性策略（batch/seq 降级、KV cache 策略调整）
- 观测点与告警（显存曲线、tail latency、崩溃/异常率）

---

## 3. 性能分析与优化主题（工程视角）

### 3.1 KV Cache（显存/带宽）

- 关注：decode 阶段显存占用与显存带宽
- 口径：不同 batch/seq 下的显存曲线、tokens/s、OOM 边界、tail latency
- 交付：可复测脚本 + 证据包 + 回归门禁

### 3.2 并行化（TP/EP/PP）

- 关注：通信占比、负载不均、拓扑不匹配导致的 scaling 受限
- 口径：单卡 vs 多卡 scaling、通信占比、尾延迟与失败率
- 交付：拓扑摘要 + 并行策略说明 + 回归门禁

### 3.3 投机采样（Speculative Decoding）

- 关注：accept rate、吞吐提升与尾延迟边界
- 口径：同口径对比（开启/关闭），记录场景约束与失败模式

### 3.4 算子优化（Triton / CUTLASS）

- 关注：热点 kernel、融合与内存访问模式
- 口径：microbench → 集成验证 → 回归门禁
- 说明：公开仓库中可用“可选 CUDA 的 microbench”呈现路径与证据结构；不绑定任何私有实现。

---

## 4. 模型侧提示（Qwen / DeepSeek）

在公开边界下，可展示的内容建议限定为：

- **计算特性画像**：prefill/decode 开销占比、KV cache 压力、长上下文场景的资源边界
- **参数策略**：batch/seq、并行切分、缓存策略对吞吐/显存/稳定性的影响与口径

避免对模型质量（准确率/对齐）做无证据主张；如需主张，需提供同口径公开评测证据。

---

## 5. 仓库内的对应入口

- `examples/vllm_sglang_enablement_skeleton/`：使能交付模板（证据包结构 + 拓扑摘要采集）
- `examples/triton_op_microbench/`：Triton microbench（可选 CUDA），用于算子层证据与回归口径示例


