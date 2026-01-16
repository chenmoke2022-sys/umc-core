# system_perf_microbench — 系统性能微基准（C++/Python，可复现）

本示例提供一个**系统级性能微基准**：用最小的 C++ 程序测量“多线程内存拷贝带宽”，并将结果固化为证据包（Evidence Pack）。

## 1. 目的（为什么这和异构计算相关）

大模型推理的瓶颈经常不是“算子太慢”，而是：

- **内存带宽**（CPU 或 GPU）成为上限
- **线程并行与拓扑**（NUMA/缓存层级）导致扩展性不理想
- **数据移动**（host↔device、layout conversion）占据主要开销

因此，“系统微基准 + 证据包”可用于将讨论锚定到“可测量/可回归”的工程事实。

---

## 2. 运行方式（Windows / PowerShell）

### 2.1 构建与运行（生成 bench.json）

```powershell
pwsh .\run.ps1
```

产物：

- `build/`：C++ 构建产物
- `bench.json`：微基准原始输出
- `artifacts/`：证据包（env/results/report/manifest）

### 2.2 可选参数

```powershell
pwsh .\run.ps1 -Threads 8 -SizeMB 512 -Iters 20
```

---

## 3. 输出说明（Evidence Pack）

输出目录：`examples/system_perf_microbench/artifacts/`

- `env.json`: 运行环境指纹
- `results.json`: 结构化结果（最小 schema），核心细节写在 `notes`
- `report.md`: 一页报告（方法、参数、结论）
- `manifest.json`: SHA256 完整性清单

---

## 4. 边界

- 不包含任何模型权重/私有数据
- 不依赖任何 GPU/厂商 SDK（保持可复现与可分发）


