# Certification（认证计划｜最小版本）

说明：本项目中关于“兼容/可用于生产”的任何表述，必须绑定到**可复现的 conformance 结果**，而不是绑定到个人承诺或口头描述。

## 1) 认证对象

我在这个对外仓库里定义的最小“认证对象”是：

- **Evidence Pack 兼容**：能产出并通过校验的 `artifacts/`（env/results/report/manifest）
- **合规门禁**：通过对外审计（无路径泄露、无权重/私有数据）

## 2) 认证方法（机器可验收）

- 运行 Conformance Suite：

```powershell
pwsh .\conformance\run_conformance.ps1
```

## 3) 认证输出（建议随发布一起提供）

- `conformance/conformance_result.json`
- 发布版本号 / tag
- `CHANGELOG.md` 对应条目

## 4) 对外声明模板（推荐）

`本发布通过了 Evidence Pack Conformance（env/results/report/manifest + 合规审计），支持复现与完整性校验；更高档位不做对外承诺。`


