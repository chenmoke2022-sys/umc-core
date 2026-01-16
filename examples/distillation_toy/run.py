import argparse
import json
import os
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def make_synthetic(n: int = 4096, d: int = 32, seed: int = 0):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(n, d)).astype(np.float32)
    w = rng.normal(size=(d,)).astype(np.float32)
    y = (x @ w + 0.25 * np.sin(x[:, 0]) > 0).astype(np.int64)
    return x, y


class MLP(nn.Module):
    def __init__(self, in_dim: int = 32, hidden: int = 256, out_dim: int = 2):
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


@torch.no_grad()
def accuracy(model: nn.Module, x: torch.Tensor, y: torch.Tensor) -> float:
    pred = model(x).argmax(dim=-1)
    return (pred == y).float().mean().item()


def train_ce(model: nn.Module, x: torch.Tensor, y: torch.Tensor, steps: int, lr: float) -> None:
    model.train()
    opt = optim.AdamW(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    for _ in range(steps):
        opt.zero_grad(set_to_none=True)
        loss = loss_fn(model(x), y)
        loss.backward()
        opt.step()


def distill_logits(
    student: nn.Module,
    teacher: nn.Module,
    x: torch.Tensor,
    y: torch.Tensor,
    steps: int,
    lr: float,
    T: float,
    alpha: float,
) -> None:
    student.train()
    teacher.eval()
    opt = optim.AdamW(student.parameters(), lr=lr)
    ce = nn.CrossEntropyLoss()
    kl = nn.KLDivLoss(reduction="batchmean")

    for _ in range(steps):
        opt.zero_grad(set_to_none=True)
        s_logits = student(x)
        with torch.no_grad():
            t_logits = teacher(x)

        loss_ce = ce(s_logits, y)
        s_logp = nn.functional.log_softmax(s_logits / T, dim=-1)
        t_p = nn.functional.softmax(t_logits / T, dim=-1)
        loss_kd = kl(s_logp, t_p) * (T * T)

        loss = alpha * loss_ce + (1 - alpha) * loss_kd
        loss.backward()
        opt.step()


def write_results(out_dir: Path, acc_plain: float, acc_kd: float) -> None:
    results = {
        "schema_version": "1.0",
        "data_status": "measured",
        "baseline": {
            "name": "toy distillation experiment (logits KD)",
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
            "toy_student_acc_plain": acc_plain,
            "toy_student_acc_distilled": acc_kd,
        },
        "notes": {
            "purpose": "Public skill proof: teacher-student distillation workflow + evidence pack.",
            "caveat": "Toy task for offline reproducibility; not a production LLM benchmark.",
        },
    }
    (out_dir / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")


def write_report(out_dir: Path, acc_plain: float, acc_kd: float, T: float, alpha: float) -> None:
    txt = f"""# Distillation toy report (measured)

## Setup
- Task: synthetic binary classification (offline)
- Teacher: larger MLP
- Student: smaller MLP
- KD: logits distillation (KL + temperature)
- Params: T={T}, alpha={alpha}

## Results
- Student accuracy (plain CE): {acc_plain:.4f}
- Student accuracy (distilled): {acc_kd:.4f}

## Interpretation
- KD should help student approach teacher behavior under limited capacity/budget.

## Engineering mindset
- In real LLM settings, measure both quality and inference cost; keep a rollback path.
"""
    (out_dir / "report.md").write_text(txt, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="artifacts")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--steps_teacher", type=int, default=600)
    ap.add_argument("--steps_student", type=int, default=300)
    ap.add_argument("--T", type=float, default=2.0)
    ap.add_argument("--alpha", type=float, default=0.5)
    args = ap.parse_args()

    set_seed(args.seed)

    x, y = make_synthetic(seed=args.seed)
    x = torch.from_numpy(x)
    y = torch.from_numpy(y)

    teacher = MLP(hidden=512)
    student_plain = MLP(hidden=64)
    student_kd = MLP(hidden=64)

    train_ce(teacher, x, y, steps=args.steps_teacher, lr=1e-3)
    train_ce(student_plain, x, y, steps=args.steps_student, lr=1e-3)
    distill_logits(student_kd, teacher, x, y, steps=args.steps_student, lr=1e-3, T=args.T, alpha=args.alpha)

    acc_plain = accuracy(student_plain, x, y)
    acc_kd = accuracy(student_kd, x, y)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_results(out_dir, acc_plain, acc_kd)
    write_report(out_dir, acc_plain, acc_kd, args.T, args.alpha)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

