# REPRODUCE — 可复现证据包操作指南

> **核心原则**：所有对外结论必须以 `artifacts/` 目录下的工件（Artifacts）与完整性清单（Manifest）为准。

## 环境要求 (Requirements)

- **Python**: 3.10+
- **Shell**: PowerShell 7 (`pwsh`)

---

## 1. 生成环境工件 (env.json)

采集当前运行环境的硬件指纹与软件版本：

```powershell
python .\tools\collect_env.py --out .\artifacts\env.json
```

## 2. 准备结果工件 (results.json)

从模板复制并填写测试结果：

```powershell
Copy-Item .\templates\results.json .\artifacts\results.json -Force
```

## 3. 准备一页报告 (report.md)

复制报告模板（包含摘要、指标表、复现步骤）：

```powershell
Copy-Item .\templates\report.md .\artifacts\report.md -Force
```

## 4. 生成完整性清单 (manifest.json)

计算所有证据文件的 SHA256 哈希值，防止篡改：

```powershell
python .\tools\make_manifest.py --dir .\artifacts --out .\artifacts\manifest.json
```

## 5. 运行校验门禁 (Gate Check)

验证工件是否齐全、格式是否正确、签名是否匹配：

```powershell
# 校验结构
python .\tools\validate_artifacts.py --artifacts .\artifacts

# 校验哈希
python .\tools\verify_manifest.py --manifest .\artifacts\manifest.json
```

---

## 6. 测量基线 (Baseline Measurement)

详细测量口径与边界说明，请见 `MEASURE.md`（本文档仅包含操作步骤，不含权重/数据）。

> **进阶**：如需将 `baseline` 状态从占位符升级为 `baseline_measured`（实测数据），请使用 `MEASURE.md` 中提供的 **Windows/CPU 自动化脚本**。该脚本会将中间产物 `bench.json` 写入 `$env:TEMP`，确保仓库纯净。

---

## 可选操作：生成追踪日志 (Trace)

如果需要附带详细的推理追踪日志：

```powershell
copy .\templates\trace.json .\artifacts\trace.json
python .\tools\make_manifest.py --dir .\artifacts --out .\artifacts\manifest.json
python .\tools\verify_manifest.py --manifest .\artifacts\manifest.json
```

## 一键生成演示产物 (Demo)

快速生成一套完整的演示用证据包（包含所有步骤）：

```powershell
pwsh .\scripts\make_demo_artifacts.ps1
```
