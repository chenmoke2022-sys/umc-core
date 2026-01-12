# 发布分支与对外发布策略（制度化门禁）

说明：公开仓库建议仅从“发布分支”推送；发布分支应避免引入敏感历史与大体积二进制资产，保证公开材料可审计、可复现、可维护。

## 1) 发布分支（Release Branch）

建议实践（任选一种）：

- **方案 A（推荐）**：`main` 作为发布分支
  - 只允许合并通过 `docs/RELEASE_CHECKLIST.md` 的内容
  - 禁止提交权重/私有数据/大二进制

- **方案 B**：`release` 作为发布分支
  - 日常开发在 `dev`，对外只从 `release` 打 tag

## 2) 发布前门禁（必须）

- **命令门禁**：
  - `pwsh .\\scripts\\audit_public.ps1`
  - `pwsh .\\scripts\\release_ready.ps1`
- **文案门禁**：
  - `docs/SPEECH_BLACKLIST.md`
  - `docs/RELEASE_CHECKLIST.md`

## 3) 绝对禁止

- 提交任何权重文件（`.gguf/.safetensors/.bin/.pt/.onnx` 等）
- 提交任何可关联内部体系的命名/路径/注释
- 引入“锁死/惩罚第三方/不可破解”等叙事


