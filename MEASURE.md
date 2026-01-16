# MEASURE — 基准测量口径说明

本仓库发布的所有 **实测基线 (baseline-measured)** 数据均基于以下固定方法论（详见 `artifacts/results.json`）。

## 1. 测量指标 (Metrics)

*   **冷启动延迟 (Cold Start)**: `load_time_ms_p50` / `load_time_ms_p95`（加载模型并生成首个 token 的耗时）
*   **内存占用 (Memory)**: `peak_memory_mb` (RSS 峰值，反映真实物理内存压力)
*   **稳定性 (Stability)**: `long_run_minutes` (连续运行时间), `crash_count` (崩溃次数)

## 2. 测量方法论 (Methodology)

*   **推理后端**: `llama.cpp` (Windows/CPU)
*   **基线格式**: `GGUF / Q2_K` (已记录在 `artifacts/results.json` 中)
*   **复现原则**: 优先保证**测量方法的一致性**，而非追求不同机器上的数值完全相同。

## 3. 自动化实测脚本 (Windows / CPU)

本仓库提供了一套**不含权重**的自动化脚本，用于在本地复现 GGUF 基线数据：

```powershell
# 1. 下载工具链 (llama.cpp)
pwsh .\scripts\download_llamacpp_windows.ps1

# 2. 下载基线模型 (Qwen GGUF)
pwsh .\scripts\download_hf_gguf.ps1 -RepoId "bartowski/Qwen2.5-0.5B-Instruct-GGUF" -Pattern "Q2_K"

# 3. 运行基准测试 (输出 bench.json 到临时目录)
pwsh .\scripts\bench_llamacpp_cpu.ps1 `
    -LlamaBench "<path-to-llama-bench.exe>" `
    -ModelGguf "<path-to-*.gguf>" `
    -OutJson "$env:TEMP\sw_public_bench.json"

# 4. 回填结果到证据包
pwsh .\scripts\apply_bench_to_results.ps1 -BenchJson "$env:TEMP\sw_public_bench.json"
```

## 4. 如何更新实测结果

当你在新环境或使用新参数重新测量后：

1.  使用相同的方法论运行基准测试。
2.  仅更新 `artifacts/results.json` 中的字段。
3.  重新生成并校验 `artifacts/manifest.json`：

```powershell
python .\tools\make_manifest.py --dir .\artifacts --out .\artifacts\manifest.json
python .\tools\verify_manifest.py --manifest .\artifacts\manifest.json
```

## 5. 范围边界 (Boundary)

*   ❌ **不包含**：模型权重文件、私有数据集。
*   ❌ **不宣称**：模型质量/准确率（Accuracy）指标（除非附带同口径的公开证据）。
