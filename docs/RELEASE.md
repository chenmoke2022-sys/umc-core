# Release（对外发布流程｜一键版）

## 目标

把对外材料发布成“可复现、可审计、口径一致、纯净”的开源仓库或分享包。

## 一键流程（推荐）

1) 生成/更新证据工件（占位或实测）：

```powershell
pwsh .\scripts\make_demo_artifacts.ps1
```

2) 对外发布前审计：

```powershell
pwsh .\scripts\audit_public.ps1
```

3) 生成分享包（给 HR/面试官）：

```powershell
pwsh .\scripts\make_share_bundle.ps1
```

4) 一键打包成 release zip：

```powershell
pwsh .\scripts\release_ready.ps1
```

## 发布前门禁（必须）

见 `docs/RELEASE_CHECKLIST.md`。


