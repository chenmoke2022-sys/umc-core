# Liquid AV1 FGS Proof — 极限 CRF + 标准 Film Grain Synthesis 的可复现证据包

本示例把一个“视频压缩配置发现”落到 **公开/可复现/可审计** 的证据包输出上：

- **不包含任何私有视频素材**（输入视频由你自行提供）
- **只依赖 FFmpeg + AV1 编码器 + libvmaf**（你本机已满足）
- 输出统一落到 `artifacts/`：`env/results/report/manifest` + 审计日志（PSNR/SSIM/VMAF）

## 核心要点（公开口径）

- **方法**：`AV1 (CRF very high) + Film Grain Synthesis (FGS)`  
  典型参数：`CRF=60`，`film-grain=25`，`film-grain-denoise=1`
- **解释口径**：FGS 会引入合成纹理/噪声，因此 **PSNR/SSIM 可能下降**，但 **VMAF/主观观感可能上升**。本项目只输出证据，不做不可验证承诺。

## 运行（measured）

> 你需要自备一个视频作为 reference（不要提交到仓库）。

## 素材来源（本示例复现用）

- **下载页**：[Pexels — 4K 视频（ID: 34629124）](https://www.pexels.com/zh-cn/video/4k-34629124/)
- **本地文件大小（该素材）**：`83,746,285 bytes`（≈ `79.86 MiB`）

```powershell
pwsh .\examples\liquid_av1_fgs_proof\run.ps1 -InputPath "E:\your_video.mp4"
```

快速烟雾测试（只跑前 120 帧，节省时间）：

```powershell
pwsh .\examples\liquid_av1_fgs_proof\run.ps1 -InputPath "E:\your_video.mp4" -Frames 120 -Force
```

输出目录：

- `examples/liquid_av1_fgs_proof/artifacts/`
- `examples/liquid_av1_fgs_proof/public_assets/`（可选：用于提交公开图片）

其中包含：

- `base_plain.mp4`：AV1 `CRF`（Plain）
- `base_fgs.mp4`：AV1 `CRF + film-grain`（Native FGS）
- `frame1_compare_raw.png`：**首帧三联图（默认）**（输入/Plain/FGS，原帧清晰）
- `frame1_compare_redacted.png`：**首帧三联图（可选）**（强脱敏：裁剪+像素化）
- `psnr_*.log` / `ssim_*.log` / `vmaf_*.json`
- `env.json` / `results.json` / `report.md` / `manifest.json`

## Public boundary（重要）

- **严禁**把输入视频（或任何受版权保护的样本）放进仓库
- `artifacts/` 属于本地可复现产物，默认应保持为未提交状态（仓库已设置忽略规则）
- 如需公开提交首帧图，请放到 `public_assets/` 并填写 `public_assets/MEDIA_SOURCE.md`

## 压缩倍率（以该 Pexels 素材全长实测为例）

> 口径：以输入文件大小为分母，倍率 = `input_size_bytes / output_size_bytes`。完整可审计数据在 `artifacts/results.json` 与 `artifacts/report.md`。

| 输出 | 参数 | 体积（bytes） | 压缩倍率 |
|---|---|---:|---:|
| Plain | AV1 `CRF=60` | 3,027,971 | 27.66× |
| FGS | AV1 `CRF=60 + film-grain=25 + denoise=1` | 2,895,007 | 28.93× |

## 指标对比（可复现）

> 说明：不同 VMAF 模型/版本会导致绝对值变化；本仓库以 `artifacts/` 中的日志/JSON 为准（默认 `n_subsample=2`）。

- **Plain CRF60（全长实测）**
  - PSNR(mean)：37.56 dB
  - SSIM(mean)：0.9374
  - VMAF(mean)：77.64（`n_subsample=2`）
- **FGS25（全长实测）**
  - PSNR(mean)：36.92 dB
  - SSIM(mean)：0.9225
  - VMAF(mean)：75.02（`n_subsample=2`）

## 论文/笔记中的历史数值（仅作参考）

> 下述数值来自你在文稿中记录的另一组评测结果：  
> - 可能使用了**不同的输入样本**或**不同的 VMAF 模型/版本/参数**  
> - 如果把它写进 README，务必同时保留“可复现”一节，否则会被质疑口径不一致

- **Plain CRF60（历史记录）**
  - PSNR(mean)：37.93 dB
  - SSIM(mean)：0.9455
  - VMAF(mean)：83.85
- **FGS25（历史记录）**
  - PSNR(mean)：37.21 dB
  - SSIM(mean)：0.9311
  - VMAF(mean)：84.43（VMAF 计算使用 `n_subsample=2` 加速；可改为 1 做更严格审计）

## 可选：不生成首帧图

```powershell
pwsh .\examples\liquid_av1_fgs_proof\run.ps1 -InputPath "E:\your_video.mp4" -Frames 120 -Force
# 如不希望生成 frame1_compare_redacted.png，可在 run.py 级别关闭：
python .\examples\liquid_av1_fgs_proof\run.py --input "E:\your_video.mp4" --out ".\examples\liquid_av1_fgs_proof\artifacts" --no-frame1
```

## 可选：生成更清晰的“原帧首帧三联图”（仅本地）

> `raw` 模式会输出清晰原帧，更容易泄露隐私/版权内容；你已确认素材可公开再分发才建议提交。

```powershell
pwsh .\examples\liquid_av1_fgs_proof\run.ps1 -InputPath "E:\your_video.mp4" -Frames 120 -Force -Frame1Mode raw
```

如要提交到 Git（公开）：

```powershell
Copy-Item .\examples\liquid_av1_fgs_proof\artifacts\frame1_compare_raw.png .\examples\liquid_av1_fgs_proof\public_assets\frame1_compare_raw.png -Force
```

