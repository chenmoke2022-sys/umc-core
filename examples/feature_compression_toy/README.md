# Feature Compression Toy — reproducible rate/distortion + bandwidth sanity check

本示例用于展示一个**与具体算法无关**、但在研究院里非常常用的能力：把“特征压缩”问题落到**可复现口径**与**可对比指标**上。

- 不依赖任何私有数据/权重
- 不假设你掌握复杂学术细节
- 只输出可审计的证据包（`env/results/report/manifest`）

## What it does

对一组**合成特征向量**做简单的逐通道线性量化（2/4/8 bits），输出：

- 率（rate）：bits per element（bpe）
- 失真（distortion）：MSE（重建误差）
-（可选）传输延迟粗估：在给定带宽下的 payload latency（不含端到端系统复杂性）

## Run (measured)

```powershell
pwsh .\examples\feature_compression_toy\run.ps1
```

输出目录：

- `examples/feature_compression_toy/artifacts/`

## Notes (public boundary)

这是一个 **toy**：它不是自动驾驶特征压缩 SOTA，也不承诺真实业务效果。
它的价值在于：把“评测面”做干净，让任何后续算法都能接入同一套证据输出结构。


