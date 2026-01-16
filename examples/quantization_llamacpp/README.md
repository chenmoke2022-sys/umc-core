## Quantization (llama.cpp) — public workflow

本示例展示“量化与推理测量口径”的工程流程：
- 量化档位选择与对比（Q8/Q4/Q2 等）
- 推理侧指标采集：加载 p50/p95、峰值内存；吞吐为可选指标
- 输出可审计 Evidence Pack：`artifacts/`（env/results/report/manifest）

> 注意：本目录不包含权重。需自行选择公开模型与公开后端；本示例仅提供流程与证据输出结构。

### 1) 快速生成占位证据（不跑模型）

```powershell
pwsh .\make_demo_artifacts.ps1
```

### 2) 跑真实测量：可选项

如本机已安装并可用 `llama.cpp`（或其他推理后端），按 `run.ps1` 的注释填写命令即可：

```powershell
pwsh .\run.ps1
```

