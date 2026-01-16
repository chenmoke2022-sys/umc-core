# MLOps Pipeline Toy — evidence-first CI/CD mindset (offline, no cloud required)

本示例用于证明一种“与业务无关、但对生产系统很关键”的能力：把一次 ML 流程（数据检查 → 训练 → 评估 → 产物登记）变成**可复现、可审计**的交付物。

- 不依赖 AWS / Airflow（可选提供 DAG 模板）
- 不包含任何模型权重文件（仅输出结构化 JSON 产物）
- 输出标准证据包：`env/results/report/manifest`

## Run

```powershell
pwsh .\examples\mlops_pipeline_toy\run.ps1
```

Outputs:

- `examples/mlops_pipeline_toy/artifacts/`

## What you get

- `data_quality.json`：数据质量检查结果（toy）
- `train_summary.json`：训练过程摘要（toy）
- `registry_entry.json`：模型注册条目（toy，不含权重）
- `results.json`：结构化指标与口径
- `report.md`：一页报告（面试官友好）


