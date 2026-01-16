## Distillation (toy) — teacher-student logits distillation

本示例演示蒸馏的基础工程能力：
- teacher / student 架构
- logits distillation（KL + temperature）
- 对比：student 直接训练 vs 蒸馏训练
- 输出：可审计证据包（含精度对比指标）

### 运行（生成真实证据）

```powershell
pwsh .\run.ps1
```

### 快速生成占位证据

```powershell
pwsh .\make_demo_artifacts.ps1
```

