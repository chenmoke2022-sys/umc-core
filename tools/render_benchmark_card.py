import json
from pathlib import Path


def _fmt_ms(x: float) -> str:
    return f"{x:.0f}ms" if abs(x - round(x)) < 1e-9 else f"{x:.1f}ms"


def render(results_path: Path) -> str:
    d = json.loads(results_path.read_text(encoding="utf-8"))

    b = d["baseline"]
    m = d["metrics"]
    status = d.get("data_status", "unknown")

    title = "UMC L8：端侧推理工程基线（公开可审计）"
    subtitle = f"Baseline (measured): {b['name']} / {b['backend']} / {b['version']}    status: {status}"

    p50 = _fmt_ms(float(m["load_time_ms_p50"]))
    p95 = _fmt_ms(float(m["load_time_ms_p95"]))
    mem = float(m["peak_memory_mb"])
    mins = float(m["long_run_minutes"])
    crash = int(m["crash_count"])

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="430" viewBox="0 0 1200 430">
  <defs>
    <style>
      .bg {{ fill: #0b1220; }}
      .card {{ fill: #121b2f; stroke: #1f2a44; stroke-width: 2; }}
      .title {{ font: 700 40px -apple-system, Segoe UI, Arial, "Microsoft YaHei"; fill: #ffffff; }}
      .sub {{ font: 500 18px -apple-system, Segoe UI, Arial, "Microsoft YaHei"; fill: #b7c3d6; }}
      .h {{ font: 700 22px -apple-system, Segoe UI, Arial, "Microsoft YaHei"; fill: #d7e1f2; }}
      .v {{ font: 800 44px ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; fill: #ffffff; }}
      .note {{ font: 500 16px -apple-system, Segoe UI, Arial, "Microsoft YaHei"; fill: #8fa0bd; }}
    </style>
  </defs>

  <rect class="bg" x="0" y="0" width="1200" height="430" rx="0" />

  <text class="title" x="60" y="78">{title}</text>
  <text class="sub" x="60" y="112">{subtitle}</text>

  <rect class="card" x="60" y="150" width="1080" height="220" rx="18" />

  <text class="h" x="110" y="210">冷启动（Cold Start）p50 / p95</text>
  <text class="v" x="110" y="270">{p50} / {p95}</text>

  <text class="h" x="520" y="210">峰值内存（Peak RSS）</text>
  <text class="v" x="520" y="270">{mem:.0f}MB</text>

  <text class="h" x="860" y="210">稳定性（Stability）</text>
  <text class="v" x="860" y="270">{mins:.0f}min / {crash} crash</text>

  <text class="note" x="60" y="408">Data source: artifacts/results.json (baseline_measured). Only the baseline numbers above are claimed.</text>
</svg>
"""


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    results = root / "artifacts" / "results.json"
    out = root / "assets" / "benchmark_card.svg"
    out.parent.mkdir(parents=True, exist_ok=True)

    svg = render(results)
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


