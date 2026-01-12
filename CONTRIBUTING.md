# 贡献指南（Contributing）

我欢迎贡献，但这个仓库的底线很硬：**可审计、可复现、绝对脱敏**。

## 原则（必须遵守）

- 我把对外仓库定位为 **工程证据包**：必须可审计、可复现。
- 请不要添加模型权重、私有数据、私有参数表或任何敏感资产。
- 任何对外结论必须绑定证据工件：`artifacts/env.json`、`artifacts/results.json`、`artifacts/report.md`、`artifacts/manifest.json`。

## 如何贡献

1. Fork 仓库并创建 feature 分支。
2. 尽量提交小而清晰的变更，便于审计。
3. 提交时使用 DCO 签署（commit sign-off），见 `DCO.md`。
4. 本地运行对外审计：

```powershell
pwsh .\scripts\audit_public.ps1
```

5. 提交 PR 时说明：
   - 改了什么
   - 为什么改
   - 如何复现/验证

## 风格

- 我更偏好：小脚本 + 清晰文档。
- 尽量保持依赖最小化。


