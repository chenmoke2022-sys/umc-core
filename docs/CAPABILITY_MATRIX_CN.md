# UMC Core 能力矩阵（可复现证据导向）

本项目聚焦于**端侧/边缘推理交付的工程验证框架**：用标准化工作流与可复现证据包（Evidence Pack）把“性能与稳定性结论”固化为可审计交付物。

## 设计原则（对外口径）

UMC Core 基于以下原则构建：
1. **证据驱动的质量门禁**：所有技术声明必须有可验证的证据包支持
2. **最小化可复现单元**：通过精简的环境指纹和结构化结果，确保实验的可重复性
3. **完整性保障**：SHA256哈希链确保交付物从评估到部署的完整性和一致性
4. **工程化评估**：把测量口径与复测流程脚本化，减少人为误差

## 技术实现模块

### 量化（Quantization）
- **技术实现**：基于 `llama.cpp` 的 GGUF 路线示例与测量口径（以公开 baseline 为准）
- **工程考量**：量化配置对速度/内存/稳定性的影响与回归门禁（以证据包为准，不做不可验证承诺）
- **性能验证**：复现流程与指标采集见示例与 `MEASURE.md`
- **文档入口**：[量化实现详解](examples/quantization_llamacpp/README.md)
- **证据包位置**：`examples/quantization_llamacpp/artifacts/`（包含环境配置、性能指标、技术报告和完整性校验）

### 剪枝与稀疏化（Pruning & Sparsity）
- **技术实现**：幅值剪枝算法实现，支持结构化与非结构化剪枝的对比实验
- **工程考量**：稀疏度-精度权衡曲线分析，识别对模型性能影响最小的剪枝目标
- **应用场景**：边缘设备内存受限环境下的模型轻量化
- **文档入口**：[剪枝算法实现](examples/pruning_toy/README.md)
- **证据包位置**：`examples/pruning_toy/artifacts/`

### 知识蒸馏（Knowledge Distillation）
- **技术实现**：Teacher-Student架构的logits蒸馏，支持KL散度损失和温度缩放
- **工程考量**：不同蒸馏策略对模型压缩效果的影响分析
- **验证方法**：结构化对照实验设计，确保结果的可比性和可解释性
- **文档入口**：[蒸馏工作流](examples/distillation_toy/README.md)
- **证据包位置**：`examples/distillation_toy/artifacts/`

### 推理性能优化（Inference Performance Engineering）
- **技术实现**：完整的性能剖析-优化-验证工作流：profiling → 代码改动 → 回归测试 → 门禁检查 → 回滚机制
- **工程考量**：性能回归的早期检测和预防，建立性能基准和容差范围
- **工具链**：以可复现实验与日志模板为中心，支持将 Profiling 结论固化为可审计记录（不绑定任何私有工具/私有算法）
- **文档入口**：[推理优化方法论](examples/inference_profiling/README.md)
- **证据包位置**：`examples/inference_profiling/artifacts/`

### 异构计算与系统级性能分析（Heterogeneous Compute & System Performance）
- **能力范围**：围绕“硬件拓扑 → 性能分析 → 瓶颈定位 → 软硬协同优化 → 复测回归”的工程闭环组织材料
- **可交付物**：调优检查清单、场景化瓶颈定位模板、可复现微基准（C++/Python）
- **文档入口**：[异构计算与推理优化实战手册](docs/HETEROGENEOUS_COMPUTE_PLAYBOOK_CN.md)
- **示例入口**：[系统性能微基准（C++/Python）](examples/system_perf_microbench/README.md)
- **框架使能入口**：[vLLM/sglang 新硬件使能与优化交付模板](docs/VLLM_SGLANG_ENABLEMENT_CN.md)
- **算子 microbench**：[Triton 算子 microbench（公开）](examples/triton_op_microbench/README.md)

### 多模态对齐（Multimodal Alignment）
- **技术实现**：基于CLIP架构的视觉-语言对齐框架，实现对比学习和特征空间映射
- **工程考量**：线性投影与MLP投影的消融实验，验证不同对齐策略的有效性
- **验证框架**：结构微调能力的可验证性评估，确保技术方案的可解释性
- **文档入口**：[多模态对齐实现](examples/vla_alignment_toy/README.md)
- **证据包位置**：`examples/vla_alignment_toy/artifacts/`

## 附加技术模块

### 特征压缩评估（Feature Compression）
- **技术实现**：率失真曲线分析和带宽敏感性检查
- **工程价值**：在边缘-云端协同推理场景下的特征传输优化
- **文档入口**：[特征压缩评测](examples/feature_compression_toy/README.md)

### MLOps工程化流水线（MLOps Pipeline）
- **技术实现**：完整的数据质量门禁→模型训练→模型注册→证据包生成DAG
- **工程价值**：标准化模型开发到部署的全流程，确保交付质量
- **文档入口**：[MLOps工作流](examples/mlops_pipeline_toy/README.md)

## 技术验证框架

所有技术实现都基于统一的验证框架：
1. **环境标准化**：`env.json`记录硬件指纹和软件依赖
2. **结果结构化**：`results.json`提供机器可读的性能指标
3. **技术报告**：`report.md`解释技术决策和结果分析
4. **完整性校验**：`manifest.json`通过SHA256确保交付物的完整性

## 工程价值

UMC Core 不仅实现了具体的模型优化技术，更重要的是建立了一套**工程化的验证方法论**：
- **降低技术评估成本**：将复杂的性能评估转化为自动化流水线
- **提高结果可信度**：通过可复现的证据包和完整性校验
- **加速技术迭代**：标准化的评估框架支持快速的技术方案对比
- **促进团队协作**：统一的工程语言和交付标准

通过这一框架，工程师可以专注于技术创新，同时确保技术方案在真实边缘环境中的可行性和可靠性。

