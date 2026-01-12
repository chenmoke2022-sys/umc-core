# RELEASE_CHECKLIST（P0 门禁｜对外发布前必过）

> 目标：确保对外发布“可复现、可审计、口径一致、无敏感资产”，并保持对外目录纯净。

## 1) 证据闭环（必须）

- [ ] `artifacts/env.json` 已生成（来自 `tools/collect_env.py`）
- [ ] `artifacts/results.json` 已填写（baseline 信息完整、口径清晰）
- [ ] `artifacts/report.md` 已补齐（≥1页，含复现命令、风险与回滚）
- [ ] `artifacts/manifest.json` 已生成（来自 `tools/make_manifest.py`）
- [ ] `tools/validate_artifacts.py` 校验通过
- [ ] `tools/verify_manifest.py` 校验通过

## 2) 口径门禁（必须）

- [ ] 已过 `docs/SPEECH_BLACKLIST.md`
- [ ] 对外仅陈述“公开约束下可验证”的范围；不做未来倍率承诺；不暗示隐藏上限

## 3) 脱敏与隔离（必须）

- [ ] 无权重文件、无私有数据、无私有参数表（可用 `tools/check_no_forbidden_files.py` 扫描）
- [ ] 文档/脚本/示例命令无路径泄露（可用 `tools/scan_redaction.py` 扫描）
- [ ] 如需额外扫描“特征词/敏感线索”，可在本地临时追加扫描规则（不要把特征词硬编码进对外仓；以 `tools/scan_redaction.py --help` 为准）

## 4) 开源合规（建议）

- [ ] `LICENSE/NOTICE` 已补齐（如要发布到公开平台）
- [ ] `SECURITY.md` 联系方式与披露窗口明确


