import json
import platform
import sys
import time
from pathlib import Path


def _write_artifacts(artifacts: Path, results: dict, report: str) -> None:
    tools_dir = artifacts.parent.parent.parent / "tools"
    subprocess = __import__("subprocess")
    artifacts.mkdir(parents=True, exist_ok=True)
    subprocess.check_call([sys.executable, str(tools_dir / "collect_env.py"), "--out", str(artifacts / "env.json")])
    (artifacts / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    (artifacts / "report.md").write_text(report, encoding="utf-8")
    subprocess.check_call(
        [
            sys.executable,
            str(tools_dir / "make_manifest.py"),
            "--dir",
            str(artifacts),
            "--out",
            str(artifacts / "manifest.json"),
        ]
    )
    subprocess.check_call([sys.executable, str(tools_dir / "verify_manifest.py"), "--manifest", str(artifacts / "manifest.json")])
    subprocess.check_call([sys.executable, str(tools_dir / "validate_artifacts.py"), "--artifacts", str(artifacts)])


def main() -> int:
    root = Path(__file__).resolve().parent
    artifacts = root / "artifacts"
    templates_dir = root.parent.parent / "templates"

    tmpl = json.loads((templates_dir / "results.json").read_text(encoding="utf-8"))
    tmpl["baseline"]["name"] = "triton_op_microbench"
    tmpl["baseline"]["version"] = "0.1"
    tmpl["baseline"]["quant_profile"] = "n/a"
    tmpl["baseline"]["backend"] = "triton"
    tmpl["device"]["os"] = platform.platform()
    tmpl["device"]["cpu"] = platform.processor() or "unknown"
    tmpl["device"]["ram_gb"] = "unknown"

    bench = {"status": "skipped", "reason": ""}
    report_lines = [
        "# triton_op_microbench — 一页报告",
        "",
        "## 范围",
        "Triton kernel microbench（公开模板）。",
        "",
        "## 结果",
    ]

    # Best-effort: run only if triton + CUDA are available.
    try:
        import torch  # type: ignore
        import triton  # type: ignore
        import triton.language as tl  # type: ignore

        if not torch.cuda.is_available():
            bench["reason"] = "cuda not available"
        else:
            @triton.jit
            def add_kernel(X_ptr, Y_ptr, Z_ptr, n_elements, BLOCK: tl.constexpr):
                pid = tl.program_id(0)
                offs = pid * BLOCK + tl.arange(0, BLOCK)
                mask = offs < n_elements
                x = tl.load(X_ptr + offs, mask=mask, other=0.0)
                y = tl.load(Y_ptr + offs, mask=mask, other=0.0)
                tl.store(Z_ptr + offs, x + y, mask=mask)

            n = 32 * 1024 * 1024
            x = torch.randn((n,), device="cuda", dtype=torch.float16)
            y = torch.randn((n,), device="cuda", dtype=torch.float16)
            z = torch.empty_like(x)

            grid = lambda meta: (triton.cdiv(n, meta["BLOCK"]),)
            # warmup
            add_kernel[grid](x, y, z, n, BLOCK=1024)
            torch.cuda.synchronize()

            iters = 50
            t0 = time.time()
            for _ in range(iters):
                add_kernel[grid](x, y, z, n, BLOCK=1024)
            torch.cuda.synchronize()
            t1 = time.time()

            elapsed_s = (t1 - t0)
            bytes_per_iter = n * 2  # fp16 bytes per element
            traffic = bytes_per_iter * 3  # x read + y read + z write
            gb_s = (traffic * iters) / elapsed_s / (1024**3)

            bench = {
                "status": "measured",
                "n": n,
                "iters": iters,
                "block": 1024,
                "elapsed_ms": elapsed_s * 1000.0,
                "throughput_gb_s": gb_s,
                "torch_version": getattr(torch, "__version__", "unknown"),
                "triton_version": getattr(triton, "__version__", "unknown"),
            }
    except Exception as e:
        bench["reason"] = f"{type(e).__name__}: {e}"

    (root / "bench.json").write_text(json.dumps(bench, indent=2, ensure_ascii=False), encoding="utf-8")

    if bench.get("status") == "measured":
        tmpl["data_status"] = "measured"
        tmpl["metrics"]["load_time_ms_p50"] = float(bench.get("elapsed_ms", 0.0))
        tmpl["metrics"]["load_time_ms_p95"] = float(bench.get("elapsed_ms", 0.0))
        tmpl["metrics"]["peak_memory_mb"] = 0.0
        tmpl["metrics"]["long_run_minutes"] = 0.0
        tmpl["metrics"]["crash_count"] = 0
        tmpl["notes"] = f"triton microbench measured: throughput_gb_s={bench.get('throughput_gb_s')}"
        report_lines += [
            f"- status: measured",
            f"- throughput_gb_s: {bench.get('throughput_gb_s')}",
        ]
    else:
        tmpl["data_status"] = "skipped"
        tmpl["metrics"]["load_time_ms_p50"] = 0.0
        tmpl["metrics"]["load_time_ms_p95"] = 0.0
        tmpl["metrics"]["peak_memory_mb"] = 0.0
        tmpl["metrics"]["long_run_minutes"] = 0.0
        tmpl["metrics"]["crash_count"] = 0
        tmpl["notes"] = f"triton microbench skipped: {bench.get('reason')}"
        report_lines += [
            f"- status: skipped",
            f"- reason: {bench.get('reason')}",
        ]

    report = "\n".join(report_lines) + "\n"
    _write_artifacts(artifacts, tmpl, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


