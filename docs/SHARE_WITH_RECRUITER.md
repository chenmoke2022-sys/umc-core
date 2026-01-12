# 如何把证据包分享给 HR/面试官（不外发权重）

## 目标

让对方看到你“可复现、可审计”的工程交付，而不是听你口头宣称。

## 推荐分享内容（最小集合）

- `README.md`
- `AUDIT.md`
- `REPRODUCE.md`
- `artifacts/`（`env.json`、`results.json`、`report.md`、`manifest.json`）
- `docs/SPEECH_BLACKLIST.md`（口径一致性）

## 一键生成分享包

```powershell
pwsh .\scripts\make_share_bundle.ps1
```

生成后在 `share_bundle/` 目录下。请在发送前再运行一次审计：

```powershell
pwsh .\scripts\audit_public.ps1
```

## 禁止事项

- 不发送任何模型权重、私有数据、内部实现细节
- 不在消息里讨论/暗示公开墙以外的内容


