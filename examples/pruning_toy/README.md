## Pruning (toy) — magnitude vs random

本示例用一个**可离线运行**的小模型，演示“剪枝/稀疏化”的核心工程能力：
- 幅值剪枝（magnitude pruning）
- 随机剪枝（random pruning）作为硬对照
- 输出：稀疏度、剪枝前后精度对比，以及可审计证据包

### 运行（生成真实证据）

```powershell
pwsh .\run.ps1
```

### 快速生成占位证据（不训练）

```powershell
pwsh .\make_demo_artifacts.ps1
```

