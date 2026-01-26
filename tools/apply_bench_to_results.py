import argparse
import json
from pathlib import Path


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Apply a local bench.json (llama.cpp CPU) into artifacts/results.json (public schema)."
    )
    p.add_argument("--bench", required=True, help="Path to bench.json (may contain absolute paths; do NOT commit it).")
    p.add_argument("--results", required=True, help="Path to artifacts/results.json to update.")
    p.add_argument("--notes", default="", help="Optional note suffix appended to results.json notes.")
    args = p.parse_args()

    bench_path = Path(args.bench)
    results_path = Path(args.results)
    if not bench_path.is_file():
        print(f"bench.json not found: {bench_path}")
        return 2
    if not results_path.is_file():
        print(f"results.json not found: {results_path}")
        return 2

    bench = _load_json(bench_path)
    results = _load_json(results_path)

    m = (bench.get("metrics") or {}) if isinstance(bench, dict) else {}
    stability = m.get("stability") or {}

    def _num(v):
        return v if isinstance(v, (int, float)) else None

    load_p50 = _num(m.get("load_time_ms_p50"))
    load_p95 = _num(m.get("load_time_ms_p95"))
    peak_rss = _num(m.get("peak_rss_mb"))
    long_run = _num(stability.get("long_run_minutes"))
    crash = _num(stability.get("crash_count"))

    missing = [k for k, v in {
        "load_time_ms_p50": load_p50,
        "load_time_ms_p95": load_p95,
        "peak_rss_mb": peak_rss,
        "stability.long_run_minutes": long_run,
        "stability.crash_count": crash,
    }.items() if v is None]
    if missing:
        print("bench.json missing required metrics:")
        for k in missing:
            print(f"- {k}")
        return 3

    results.setdefault("metrics", {})
    results["metrics"]["load_time_ms_p50"] = float(load_p50)
    results["metrics"]["load_time_ms_p95"] = float(load_p95)
    results["metrics"]["peak_memory_mb"] = float(peak_rss)
    results["metrics"]["long_run_minutes"] = float(long_run)
    results["metrics"]["crash_count"] = float(crash)
    results["data_status"] = "baseline_measured"

    note = "Baseline measured with llama.cpp-bench-cpu. bench.json contains local absolute paths and is not part of evidence artifacts."
    if args.notes.strip():
        note = note + " " + args.notes.strip()
    results["notes"] = note

    _save_json(results_path, results)
    print(f"OK: updated {results_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


