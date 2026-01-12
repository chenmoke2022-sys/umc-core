# UMC 格式规范（v0.1｜对外草案）

> 范围：我只对外讨论公开墙内（L8 基线及其证据闭环），更高档位不在本规范范围。

## 1. 设计目标

我把 UMC 定位为**工程证据包**的载体：重点是可审计、可复现、可回滚，而不是追求不可验证的“奇迹叙事”。

## 2. 包结构（最小）

A valid UMC package consists of the following artifacts (virtual or physical):

```text
/
├── artifacts/
│   ├── env.json        # Hardware & Runtime Fingerprint
│   ├── results.json    # Key Performance Metrics (p50/p95)
│   ├── report.md       # One-page Summary
│   └── manifest.json   # Integrity Checksum (SHA256)
```

## 3. 字段定义（最小）

### 3.1 `results.json`

| Field | Type | Description |
| :--- | :--- | :--- |
| `schema_version` | string | Version of this schema (e.g. "0.1"). |
| `baseline.name` | string | The public baseline used for comparison (e.g. "GGUF"). |
| `metrics.load_time_ms_p50` | float | Median cold start time in milliseconds. |
| `metrics.peak_memory_mb` | float | Peak RSS usage during inference. |

### 3.2 `manifest.json`

| Field | Type | Description |
| :--- | :--- | :--- |
| `files` | array | List of file objects. |
| `files[].path` | string | Relative path to the file. |
| `files[].sha256` | string | SHA-256 hash of the file content. |

## 4. 版本策略（最小）

- **Major（0.x -> 1.x）**：`manifest.json` 结构发生不兼容变化。
- **Minor（0.1 -> 0.2）**：`results.json` 增加可选字段（保持向后兼容）。
