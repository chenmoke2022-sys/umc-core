## Inference Profiling — public checklist & template

本示例不绑定任何私有优化算法，而是提供一套业界常用的 **profiling → 变更 → 复测 → 回归门禁** 模板。

### 1) 生成占位证据包（模板）

```powershell
pwsh .\make_demo_artifacts.ps1
```

### 2) 记录一次真实优化（你填）

复制 `TEMPLATE_OPT_LOG.md`，记录一次优化：
- profile 发现什么瓶颈
- 做了什么改动（配置/线程/批处理/缓存/算子融合等）
- 复测结果与回归门禁、回滚方案

