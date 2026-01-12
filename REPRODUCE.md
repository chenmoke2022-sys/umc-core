# REPRODUCE — 一键复现与证据工件（纯净版）

> 目标：让任何面试官/同事照抄命令就能得到同口径工件（`env/results/report`），避免口号化。  
> 对外可信来源：只认 `artifacts/` 下的证据工件与完整性校验。

## 0. 运行前检查

- 已安装 Python 3.10+（建议 3.11）
- 已安装 PowerShell 7（命令为 `pwsh`）
- 当前工作目录为**仓库根目录**（包含 `README.md / artifacts/ / tools/`）
- **不要**在本目录放入任何权重文件、私有数据、私有参数表

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

## 5.1 可选：补充 trace.json（仅最小必要信息）

如需记录性能/回滚/错误码的最小追踪信息，可以使用模板：

```powershell
copy .\templates\trace.json .\artifacts\trace.json
python .\tools\make_manifest.py --dir .\artifacts --out .\artifacts\manifest.json
python .\tools\verify_manifest.py --manifest .\artifacts\manifest.json
```

## 6. 一键生成“占位闭环”（先把结构跑通）

```powershell
pwsh .\scripts\make_demo_artifacts.ps1
```



