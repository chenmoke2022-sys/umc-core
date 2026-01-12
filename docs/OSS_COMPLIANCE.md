# OSS Compliance（开源合规｜最小落地）

说明：本项目的开源合规关注点包括：SBOM、许可证清单、NOTICE、供应链风险与安全响应流程。

## 1) 许可证与 NOTICE

- `LICENSE`：本仓库使用 MIT License
- `NOTICE`：第三方声明（如未来引入 vendored 代码或依赖，需要更新）

## 2) SBOM（建议作为必须项）

我把这个对外仓库保持为“最小依赖”的证据包：仅包含少量脚本与文档，不打包第三方二进制，也不 vendoring 第三方源码。  
如未来引入依赖（Python/Node/二进制工具），请生成并提交 SBOM（任选其一）：

- SPDX
- CycloneDX

建议输出路径（择一）：
- `sbom/sbom.spdx.json`
- `sbom/sbom.cdx.json`

## 3) 安全响应（必须）

见 `SECURITY.md`（漏洞报告渠道、披露窗口）。


