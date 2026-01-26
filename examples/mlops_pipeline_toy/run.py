import argparse
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np


def _save_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _now_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def make_synth_data(n: int, d: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(n, d)).astype(np.float32)
    w = rng.normal(size=(d,)).astype(np.float32)
    logits = x @ w + 0.1 * rng.normal(size=(n,)).astype(np.float32)
    y = (logits > 0).astype(np.int64)
    return x, y


def data_quality_checks(x: np.ndarray, y: np.ndarray) -> dict:
    return {
        "schema_version": "1.0",
        "generated_at_utc": _now_utc(),
        "checks": {
            "row_count": int(x.shape[0]),
            "feature_dim": int(x.shape[1]),
            "nan_ratio": float(np.isnan(x).mean()),
            "label_balance_pos_ratio": float(y.mean()),
        },
        "pass": bool(np.isnan(x).mean() == 0.0 and 0.05 <= y.mean() <= 0.95),
        "notes": "Toy checks: demonstrates data-quality gate shape (not a production policy).",
    }


@dataclass
class TrainOut:
    coef: np.ndarray
    bias: float
    acc: float
    steps: int


def train_logreg(x: np.ndarray, y: np.ndarray, lr: float, steps: int, seed: int) -> TrainOut:
    rng = np.random.default_rng(seed)
    n, d = x.shape
    w = rng.normal(scale=0.01, size=(d,)).astype(np.float32)
    b = 0.0

    def sigmoid(z):
        return 1.0 / (1.0 + np.exp(-z))

    for _ in range(steps):
        z = x @ w + b
        p = sigmoid(z)
        # gradient
        gw = (x.T @ (p - y)) / n
        gb = float(np.mean(p - y))
        w = (w - lr * gw).astype(np.float32)
        b = float(b - lr * gb)

    pred = (sigmoid(x @ w + b) > 0.5).astype(np.int64)
    acc = float((pred == y).mean())
    return TrainOut(coef=w, bias=b, acc=acc, steps=steps)


def write_registry_entry(out_dir: Path, train: TrainOut, seed: int) -> dict:
    # No weights file: store only minimal numeric summary / signature for demo purposes.
    entry = {
        "schema_version": "1.0",
        "generated_at_utc": _now_utc(),
        "model_name": "toy_logreg",
        "version": f"seed-{seed}",
        "artifacts": {
            "format": "json-only",
            "contains_weights": False,
        },
        "signature": {
            "coef_l2": float(np.linalg.norm(train.coef)),
            "bias": float(train.bias),
        },
        "metrics": {
            "train_acc": float(train.acc),
        },
        "notes": "Toy registry entry for demonstrating MLOps-style model registration without shipping weights.",
    }
    _save_json(out_dir / "registry_entry.json", entry)
    return entry


def write_results(out_dir: Path, dq: dict, reg: dict, seed: int, n: int, d: int) -> None:
    results = {
        "schema_version": "1.0",
        "data_status": "measured",
        "baseline": {
            "name": "toy mlops pipeline (data gate -> train -> eval -> registry)",
            "version": "1.0",
            "quant_profile": "n/a",
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
            "toy_rows": float(n),
            "toy_dim": float(d),
            "toy_data_gate_pass": float(1.0 if dq.get("pass") else 0.0),
            "toy_train_acc": float(reg["metrics"]["train_acc"]),
            "toy_coef_l2": float(reg["signature"]["coef_l2"]),
        },
        "notes": "Toy-only: demonstrates CI/CD style gates + auditable artifacts for ML pipelines, without any private data or weights.",
    }
    _save_json(out_dir / "results.json", results)


def write_report(out_dir: Path, dq: dict, reg: dict) -> None:
    txt = f"""# MLOps pipeline toy report (measured)

## What this proves
- The pipeline is **scriptable**, **reproducible**, and outputs auditable artifacts.
- A simple **data quality gate** exists before training.
- A minimal **registry entry** is produced without shipping any weights.

## Data gate
- pass: {dq.get('pass')}
- row_count: {dq['checks']['row_count']}
- nan_ratio: {dq['checks']['nan_ratio']:.6f}
- label_balance_pos_ratio: {dq['checks']['label_balance_pos_ratio']:.3f}

## Train/eval
- train_acc: {reg['metrics']['train_acc']:.4f}
- signature.coef_l2: {reg['signature']['coef_l2']:.4f}

## Boundary
This is a toy pipeline for demonstrating engineering workflow. It does not claim production model quality.
"""
    (out_dir / "report.md").write_text(txt, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="artifacts", help="output artifacts dir")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n", type=int, default=4096)
    ap.add_argument("--d", type=int, default=64)
    ap.add_argument("--lr", type=float, default=0.2)
    ap.add_argument("--steps", type=int, default=200)
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    x, y = make_synth_data(n=args.n, d=args.d, seed=args.seed)
    dq = data_quality_checks(x, y)
    _save_json(out_dir / "data_quality.json", dq)

    train = train_logreg(x, y, lr=args.lr, steps=args.steps, seed=args.seed)
    train_summary = {
        "schema_version": "1.0",
        "generated_at_utc": _now_utc(),
        "algo": "logreg_gd",
        "steps": int(train.steps),
        "lr": float(args.lr),
        "train_acc": float(train.acc),
    }
    _save_json(out_dir / "train_summary.json", train_summary)

    reg = write_registry_entry(out_dir, train=train, seed=args.seed)
    write_results(out_dir, dq=dq, reg=reg, seed=args.seed, n=args.n, d=args.d)
    write_report(out_dir, dq=dq, reg=reg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


