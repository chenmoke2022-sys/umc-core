# MEASURE_GUIDE（CPU 基线实测｜模板）

> 目标：在公开可获得基线（例如 GGUF + llama.cpp）上，按一致口径产出 `artifacts/` 证据工件。  
> 注意：本指南不下载权重、不内置任何私有资源；你需要自行准备公开可获得的模型文件与工具。

## 1) 你需要准备什么

- `llama-bench`（来自 `llama.cpp` 构建产物）
- 一个公开可获得的 GGUF 模型文件（你自行下载并存放在本机任意位置）

## 2) 运行一次基线测试（示例命令）

> 下面命令仅示意参数风格；请以你手里的 `llama-bench --help` 为准。

```powershell
# 示例：把输出写成 json（如果你的 llama-bench 支持）
& "<PATH_TO_LLAMA_BENCH_EXE>" `
  -m "<PATH_TO_MODEL_GGUF>" `
  --threads 8 `
  --n-predict 128 `
  --json > .\artifacts\bench_raw.json
```

如果你的版本不支持 `--json`，你也可以把 stdout 保存下来并手工抽取关键字段，写入 `artifacts/results.json`。

## 3) 把结果写入 results.json（口径门禁）

- baseline.name/version/backend/quant_profile 必填
- metrics：加载（p50/p95）、吞吐（p50/p95）、峰值内存、长跑分钟、crash 数

填写完成后，运行：

```powershell
python .\tools\make_manifest.py --dir .\artifacts --out .\artifacts\manifest.json
python .\tools\validate_artifacts.py --artifacts .\artifacts
python .\tools\verify_manifest.py --manifest .\artifacts\manifest.json
```

## 4) 写一页 report.md（给面试官看的）

- 只写 1 页：结论、关键指标表、复现命令、风险与回滚
- 禁止出现：隐藏上限、未来倍率承诺、锁死/惩罚第三方等表述（见 `docs/SPEECH_BLACKLIST.md`）


