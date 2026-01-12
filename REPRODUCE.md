# REPRODUCE — Reproducible Evidence Pack

Authoritative outputs are the artifacts under `artifacts/` plus the integrity manifest.

## Requirements

- Python 3.10+
- PowerShell 7 (`pwsh`)

## 1. 生成环境工件（env.json）

```powershell
python .\tools\collect_env.py --out .\artifacts\env.json
```

## 2. 准备结果工件（results.json）

将模板复制到 `artifacts/` 后填写：

```powershell
Copy-Item .\templates\results.json .\artifacts\results.json -Force
```

## 3. 准备一页报告（report.md）

```powershell
Copy-Item .\templates\report.md .\artifacts\report.md -Force
```

## 4. 生成完整性清单（manifest.json）

```powershell
python .\tools\make_manifest.py --dir .\artifacts --out .\artifacts\manifest.json
```

## 5. 校验工件是否齐全（门禁）

```powershell
python .\tools\validate_artifacts.py --artifacts .\artifacts
python .\tools\verify_manifest.py --manifest .\artifacts\manifest.json
```

## 6. 测量口径（baseline）

见 `MEASURE.md`（仅说明口径与边界；不附带权重/数据）。

## Optional: trace.json

```powershell
copy .\templates\trace.json .\artifacts\trace.json
python .\tools\make_manifest.py --dir .\artifacts --out .\artifacts\manifest.json
python .\tools\verify_manifest.py --manifest .\artifacts\manifest.json
```

## Demo artifacts

```powershell
pwsh .\scripts\make_demo_artifacts.ps1
```



