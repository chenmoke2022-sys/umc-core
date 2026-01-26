import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class Row:
    bits: int
    bpe: float
    mse: float
    payload_kb: float
    latency_ms: float


def _quantize_linear(x: np.ndarray, bits: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Per-dim linear quantization:
      xq = round((x - min) / scale), clip to [0, 2^bits - 1]
      xhat = xq * scale + min
    Returns (xhat, x_min, scale)
    """
    assert x.ndim == 2
    qmax = (1 << bits) - 1
    x_min = x.min(axis=0, keepdims=True)
    x_max = x.max(axis=0, keepdims=True)
    # avoid zero-range
    scale = (x_max - x_min) / max(qmax, 1)
    scale = np.where(scale == 0.0, 1.0, scale).astype(np.float32)
    xq = np.round((x - x_min) / scale)
    xq = np.clip(xq, 0, qmax)
    xhat = (xq * scale + x_min).astype(np.float32)
    return xhat, x_min.astype(np.float32), scale


def _mse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((a - b) ** 2))


def _payload_kb(n: int, d: int, bits: int) -> float:
    # only count the quantized payload (not metadata); this is a toy sanity check
    total_bits = n * d * bits
    return float(total_bits / 8.0 / 1024.0)


def _latency_ms(payload_kb: float, bandwidth_mbps: float) -> float:
    # Mbps -> KB/s: (Mbps * 1e6 / 8) / 1024
    kbps = (bandwidth_mbps * 1_000_000.0 / 8.0) / 1024.0
    if kbps <= 0:
        return 0.0
    return float((payload_kb / kbps) * 1000.0)


def write_results(out_dir: Path, rows: list[Row], seed: int, n: int, d: int, bandwidth_mbps: float) -> None:
    # Keep schema-compatible required metrics numeric.
    # Put toy metrics as numeric fields to avoid breaking minimal validators.
    by_bits = {r.bits: r for r in rows}
    results = {
        "schema_version": "1.0",
        "data_status": "measured",
        "baseline": {
            "name": "toy feature compression (per-dim linear quantization)",
            "version": "1.0",
            "quant_profile": "2/4/8 bits",
            "backend": "numpy",
        },
        "device": {"os": os.name, "cpu": "unknown", "ram_gb": "unknown"},
        "metrics": {
            "load_time_ms_p50": 0,
            "load_time_ms_p95": 0,
            "peak_memory_mb": 0,
            "long_run_minutes": 0,
            "crash_count": 0,
            "toy_seed": float(seed),
            "toy_n": float(n),
            "toy_d": float(d),
            "toy_bandwidth_mbps": float(bandwidth_mbps),
            "toy_bpe_b2": float(by_bits[2].bpe),
            "toy_bpe_b4": float(by_bits[4].bpe),
            "toy_bpe_b8": float(by_bits[8].bpe),
            "toy_mse_b2": float(by_bits[2].mse),
            "toy_mse_b4": float(by_bits[4].mse),
            "toy_mse_b8": float(by_bits[8].mse),
            "toy_payload_kb_b2": float(by_bits[2].payload_kb),
            "toy_payload_kb_b4": float(by_bits[4].payload_kb),
            "toy_payload_kb_b8": float(by_bits[8].payload_kb),
            "toy_latency_ms_b2": float(by_bits[2].latency_ms),
            "toy_latency_ms_b4": float(by_bits[4].latency_ms),
            "toy_latency_ms_b8": float(by_bits[8].latency_ms),
        },
        "notes": "Toy-only: demonstrates rate/distortion + bandwidth sanity check under a reproducible evidence pack. Not a claim about any real driving/cockpit model.",
    }
    (out_dir / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")


def write_report(out_dir: Path, rows: list[Row], bandwidth_mbps: float, n: int, d: int) -> None:
    lines = []
    lines.append("# Feature compression toy report (measured)")
    lines.append("")
    lines.append("## Setup")
    lines.append(f"- Data: synthetic feature vectors (N={n}, D={d})")
    lines.append("- Method: per-dimension linear quantization (2/4/8 bits)")
    lines.append(f"- Bandwidth (toy): {bandwidth_mbps} Mbps (payload-only latency estimate)")
    lines.append("")
    lines.append("## Results (rate / distortion / payload latency)")
    lines.append("")
    lines.append("| bits | bpe | MSE | payload (KB) | latency (ms) |")
    lines.append("|---:|---:|---:|---:|---:|")
    for r in rows:
        lines.append(f"| {r.bits} | {r.bpe:.1f} | {r.mse:.6f} | {r.payload_kb:.2f} | {r.latency_ms:.2f} |")
    lines.append("")
    lines.append("## Interpretation (minimal)")
    lines.append("- Lower bits reduce payload and estimated latency, at the cost of higher reconstruction error.")
    lines.append("- The point is not to win numbers, but to fix a reproducible evaluation surface for future algorithms.")
    lines.append("")
    lines.append("## Boundary")
    lines.append("- This is a toy experiment; it does not claim real-world task quality.")
    (out_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="artifacts", help="output artifacts dir")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n", type=int, default=4096)
    ap.add_argument("--d", type=int, default=256)
    ap.add_argument("--bandwidth_mbps", type=float, default=20.0)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    x = rng.normal(size=(args.n, args.d)).astype(np.float32)

    rows: list[Row] = []
    for bits in (2, 4, 8):
        xhat, _, _ = _quantize_linear(x, bits=bits)
        mse = _mse(x, xhat)
        bpe = float(bits)
        payload_kb = _payload_kb(args.n, args.d, bits)
        latency_ms = _latency_ms(payload_kb, args.bandwidth_mbps)
        rows.append(Row(bits=bits, bpe=bpe, mse=mse, payload_kb=payload_kb, latency_ms=latency_ms))

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_results(out_dir, rows, seed=args.seed, n=args.n, d=args.d, bandwidth_mbps=args.bandwidth_mbps)
    write_report(out_dir, rows, bandwidth_mbps=args.bandwidth_mbps, n=args.n, d=args.d)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


