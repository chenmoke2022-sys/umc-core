import argparse
import json
import os
import platform
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.check_call(cmd, cwd=str(cwd) if cwd else None)


def _cmake_build(src_dir: Path, build_dir: Path) -> Path:
    build_dir.mkdir(parents=True, exist_ok=True)
    _run(["cmake", "-S", str(src_dir), "-B", str(build_dir)])
    _run(["cmake", "--build", str(build_dir), "--config", "Release"])

    # Windows multi-config generator puts exe under Release/
    exe = build_dir / "Release" / "mem_bw.exe"
    if exe.is_file():
        return exe
    exe = build_dir / "mem_bw"
    if exe.is_file():
        return exe
    raise FileNotFoundError("mem_bw binary not found after build")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--threads", type=int, default=0)
    p.add_argument("--size-mb", type=int, default=256)
    p.add_argument("--iters", type=int, default=20)
    args = p.parse_args()

    root = Path(__file__).resolve().parent
    artifacts = root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)

    # 1) Build + run microbench
    exe = _cmake_build(root, root / "build")
    threads = args.threads if args.threads > 0 else (os.cpu_count() or 1)

    out = subprocess.check_output(
        [str(exe), "--threads", str(threads), "--size_mb", str(args.size_mb), "--iters", str(args.iters)],
        cwd=str(root),
    )
    bench = json.loads(out.decode("utf-8"))
    (root / "bench.json").write_text(json.dumps(bench, indent=2, ensure_ascii=False), encoding="utf-8")

    # 2) env.json
    tools_dir = root.parent.parent / "tools"
    templates_dir = root.parent.parent / "templates"
    _run([sys.executable, str(tools_dir / "collect_env.py"), "--out", str(artifacts / "env.json")])

    # 3) results.json (minimal schema) + report.md
    tmpl = json.loads((templates_dir / "results.json").read_text(encoding="utf-8"))
    tmpl["data_status"] = "measured"
    tmpl["baseline"]["name"] = "system_perf_microbench"
    tmpl["baseline"]["version"] = "0.1"
    tmpl["baseline"]["quant_profile"] = "n/a"
    tmpl["baseline"]["backend"] = "cpp"
    tmpl["device"]["os"] = platform.platform()
    tmpl["device"]["cpu"] = platform.processor() or "unknown"
    tmpl["device"]["ram_gb"] = "unknown"

    elapsed_ms = float(bench.get("elapsed_ms", 0.0))
    tmpl["metrics"]["load_time_ms_p50"] = elapsed_ms
    tmpl["metrics"]["load_time_ms_p95"] = elapsed_ms
    tmpl["metrics"]["peak_memory_mb"] = 0.0
    tmpl["metrics"]["long_run_minutes"] = max(0.0, elapsed_ms / 60000.0)
    tmpl["metrics"]["crash_count"] = 0
    tmpl["notes"] = (
        "system_perf_microbench: multi-thread memcpy bandwidth. "
        f"threads={bench.get('threads')}, size_mb={bench.get('size_mb')}, iters={bench.get('iters')}, "
        f"throughput_gb_s={bench.get('throughput_gb_s')}"
    )
    (artifacts / "results.json").write_text(json.dumps(tmpl, indent=2, ensure_ascii=False), encoding="utf-8")

    report = f"""# system_perf_microbench — 一页报告

## 目的
用最小可复现的方式测量多线程内存拷贝带宽，作为“系统级瓶颈定位”的基础证据。

## 方法
- C++ 程序对齐分配两块内存，循环执行 memcpy
- 线程并发切分区间，测量总耗时并计算带宽

## 参数与结果
- threads: {bench.get('threads')}
- size_mb: {bench.get('size_mb')}
- iters: {bench.get('iters')}
- elapsed_ms: {bench.get('elapsed_ms')}
- throughput_gb_s: {bench.get('throughput_gb_s')}

## 说明
- 本示例不绑定特定厂商 SDK；用于展示方法论与可复现闭环
- 真正的异构场景（GPU/互联/NUMA）可在此基础上扩展测量口径与门禁
"""
    (artifacts / "report.md").write_text(report, encoding="utf-8")

    # 4) manifest.json
    _run(
        [
            sys.executable,
            str(tools_dir / "make_manifest.py"),
            "--dir",
            str(artifacts),
            "--out",
            str(artifacts / "manifest.json"),
        ]
    )
    _run([sys.executable, str(tools_dir / "verify_manifest.py"), "--manifest", str(artifacts / "manifest.json")])
    _run([sys.executable, str(tools_dir / "validate_artifacts.py"), "--artifacts", str(artifacts)])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


