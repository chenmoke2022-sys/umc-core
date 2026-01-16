# VLA Alignment Toy — multimodal alignment proof (offline, reproducible)

本示例用于证明一种“研究验证能力”：

- 不依赖私有数据/权重
- 不需要讲复杂学术细节
- 但可以用 **可复现实验 + 对照** 展示“多模态对齐/CLIP-style”核心形状

输出标准证据包（`env/results/report/manifest`），用于面试时快速说明“我能用 AI 工具把研究流程工程化并跑通”。

## What it does

生成合成的“视觉/文本”成对向量（同一个 latent + 噪声），比较两种投影头：

- Linear projection
- 2-layer MLP projection

使用对比学习（InfoNCE）训练对齐，并报告：

- 训练前/后的 loss
- 简单 retrieval@1（在 batch 内做最近邻检索）

## Run

```powershell
pwsh .\examples\vla_alignment_toy\run.ps1
```

## Boundary

这是 toy 实验：不声称真实 VLA 模型效果，也不声称对自动驾驶/座舱任务的直接收益。
它的价值在于：把“对齐训练 + 对照验证 + 证据包输出”做成可复现闭环。


