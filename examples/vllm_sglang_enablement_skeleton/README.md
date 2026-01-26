# vllm_sglang_enablement_skeleton — 框架使能交付模板（公开）

本示例提供一份“vLLM/sglang 新硬件使能与优化”的**交付模板**：以证据包形式固化硬件拓扑摘要、口径与回归门禁框架。

## 内容

- `run.ps1` / `run.py`：采集硬件拓扑摘要（尽量使用系统自带工具），生成 `artifacts/`
- `artifacts/`：env/results/report/manifest（可审计最小闭环）

## 运行

```powershell
pwsh .\run.ps1
```

## 边界

- 不包含权重/私有数据
- 不绑定任何厂商 NDA 内容
- 不对性能结果做前瞻承诺；对外声明以证据包为准


