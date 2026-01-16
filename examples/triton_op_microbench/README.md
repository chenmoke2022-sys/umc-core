# triton_op_microbench — Triton 算子 microbench（公开）

本示例用于展示“算子层优化”的公开可交付形态：以 Triton 编写一个最小 kernel，做 microbench，并将结果固化为证据包。

## 范围

- 关注点：kernel 吞吐、launch 开销、数据布局与访存模式
- 交付物：bench.json + artifacts（env/results/report/manifest）
- 边界：不包含权重/私有数据；不绑定任何厂商 NDA 内容

## 运行

```powershell
pwsh .\run.ps1
```

> 若缺少 CUDA/Triton 运行条件，将生成 “skipped” 状态的证据包，不产生性能主张。


