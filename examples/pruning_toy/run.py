import argparse
import json
import math
import os
import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


@dataclass
class Metrics:
    acc_before: float
    acc_after_mag: float
    acc_after_rand: float
    sparsity: float


class TinyMLP(nn.Module):
    def __init__(self, in_dim: int = 32, hidden: int = 128, out_dim: int = 2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, out_dim),
        )

    def forward(self, x):
        return self.net(x)


def make_synthetic(n: int = 4096, d: int = 32, seed: int = 0):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(n, d)).astype(np.float32)
    w = rng.normal(size=(d,)).astype(np.float32)
    y = (x @ w + 0.25 * np.sin(x[:, 0]) > 0).astype(np.int64)
    return x, y


@torch.no_grad()
def accuracy(model: nn.Module, x: torch.Tensor, y: torch.Tensor) -> float:
    logits = model(x)
    pred = logits.argmax(dim=-1)
    return (pred == y).float().mean().item()


def _all_linear_weights(model: nn.Module):
    for m in model.modules():
        if isinstance(m, nn.Linear):
            yield m.weight


@torch.no_grad()
def apply_magnitude_pruning(model: nn.Module, prune_ratio: float) -> float:
    weights = [w.view(-1).abs().cpu() for w in _all_linear_weights(model)]
    all_abs = torch.cat(weights)
    k = int(math.floor(prune_ratio * all_abs.numel()))
    if k <= 0:
        return 0.0
    thr = torch.kthvalue(all_abs, k).values.item()

    total = 0
    zeros = 0
    for w in _all_linear_weights(model):
        mask = w.abs() <= thr
        w[mask] = 0.0
        total += w.numel()
        zeros += int(mask.sum().item())
    return zeros / float(total)


@torch.no_grad()
def apply_random_pruning(model: nn.Module, prune_ratio: float, seed: int) -> float:
    g = torch.Generator(device="cpu")
    g.manual_seed(seed)

    total = 0
    zeros = 0
    for w in _all_linear_weights(model):
        mask = torch.rand(w.shape, generator=g) < prune_ratio
        w[mask] = 0.0
        total += w.numel()
        zeros += int(mask.sum().item())
    return zeros / float(total)


def train(model: nn.Module, x: torch.Tensor, y: torch.Tensor, steps: int = 400, lr: float = 1e-3) -> None:
    model.train()
    opt = optim.AdamW(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    for _ in range(steps):
        opt.zero_grad(set_to_none=True)
        logits = model(x)
        loss = loss_fn(logits, y)
        loss.backward()
        opt.step()


def write_results(out_dir: Path, m: Metrics) -> None:
    results = {
        "schema_version": "1.0",
        "data_status": "measured",
        "baseline": {
            "name": "toy pruning experiment (magnitude vs random)",
            "version": "1.0",
            "quant_profile": "n/a",
            "backend": "pytorch",
        },
        "device": {"os": os.name, "cpu": "unknown", "ram_gb": "unknown"},
        "metrics": {
            "load_time_ms_p50": 0,
            "load_time_ms_p95": 0,
            "peak_memory_mb": 0,
            "long_run_minutes": 0,
            "crash_count": 0,
            "toy_acc_before": m.acc_before,
            "toy_acc_after_magnitude": m.acc_after_mag,
            "toy_acc_after_random": m.acc_after_rand,
            "toy_sparsity": m.sparsity,
        },
        "notes": {
            "purpose": "Public skill proof: pruning methodology + control experiment + auditable artifacts.",
            "caveat": "Toy task for offline reproducibility; not a production LLM benchmark.",
        },
    }
    (out_dir / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")


def write_report(out_dir: Path, m: Metrics, prune_ratio: float) -> None:
    txt = f"""# Pruning toy report (measured)

## Setup
- Task: synthetic binary classification (offline)
- Model: TinyMLP
- Prune ratio target: {prune_ratio:.2f}

## Results
- Accuracy (before): {m.acc_before:.4f}
- Accuracy (after magnitude pruning): {m.acc_after_mag:.4f}
- Accuracy (after random pruning): {m.acc_after_rand:.4f}
- Achieved sparsity: {m.sparsity:.3f}

## Interpretation
- Magnitude pruning should degrade accuracy less than random pruning at the same prune ratio.
- If this invariant fails, it indicates an implementation bug or unstable training.

## Safety / rollback mindset
- Production sparsity only makes sense when backend kernels/hardware can exploit it.
- If latency does not improve or quality drops, rollback to dense weights or higher-precision alternatives.
"""
    (out_dir / "report.md").write_text(txt, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="artifacts", help="output artifacts dir")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--prune_ratio", type=float, default=0.5)
    args = ap.parse_args()

    set_seed(args.seed)

    x, y = make_synthetic(seed=args.seed)
    x = torch.from_numpy(x)
    y = torch.from_numpy(y)

    model_base = TinyMLP()
    train(model_base, x, y)
    acc0 = accuracy(model_base, x, y)

    model_mag = TinyMLP()
    model_mag.load_state_dict(model_base.state_dict())
    spars_mag = apply_magnitude_pruning(model_mag, args.prune_ratio)
    acc_mag = accuracy(model_mag, x, y)

    model_rnd = TinyMLP()
    model_rnd.load_state_dict(model_base.state_dict())
    apply_random_pruning(model_rnd, args.prune_ratio, seed=args.seed + 1337)
    acc_rnd = accuracy(model_rnd, x, y)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    m = Metrics(acc_before=acc0, acc_after_mag=acc_mag, acc_after_rand=acc_rnd, sparsity=float(spars_mag))
    write_results(out_dir, m)
    write_report(out_dir, m, args.prune_ratio)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

