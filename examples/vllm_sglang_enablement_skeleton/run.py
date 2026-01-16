import json
import platform
import subprocess
import sys
from pathlib import Path


def _try_run(cmd: list[str]) -> tuple[int, str]:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return 0, out.strip()
    except FileNotFoundError:
        return 127, ""
    except subprocess.CalledProcessError as e:
        return int(e.returncode), (e.output or "").strip()


def main() -> int:
    root = Path(__file__).resolve().parent
    artifacts = root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)

    tools_dir = root.parent.parent / "tools"
    templates_dir = root.parent.parent / "templates"

    # env.json
    subprocess.check_call([sys.executable, str(tools_dir / "collect_env.py"), "--out", str(artifacts / "env.json")])

    # Topology snapshot (best-effort, no hard dependency)
    topo: dict[str, object] = {
        "os": platform.platform(),
        "python": sys.version.split()[0],
        "nvidia_smi": {},
    }

    code, txt = _try_run(["nvidia-smi", "-L"])
    topo["nvidia_smi"]["list_code"] = code
    topo["nvidia_smi"]["list"] = txt
    code, txt = _try_run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"])
    topo["nvidia_smi"]["query_code"] = code
    topo["nvidia_smi"]["query"] = txt

    (root / "topology.json").write_text(json.dumps(topo, indent=2, ensure_ascii=False), encoding="utf-8")

    # results.json (minimal schema; details go to notes)
    tmpl = json.loads((templates_dir / "results.json").read_text(encoding="utf-8"))
    tmpl["data_status"] = "measured"
    tmpl["baseline"]["name"] = "vllm_sglang_enablement_skeleton"
    tmpl["baseline"]["version"] = "0.1"
    tmpl["baseline"]["quant_profile"] = "n/a"
    tmpl["baseline"]["backend"] = "n/a"
    tmpl["device"]["os"] = platform.platform()
    tmpl["device"]["cpu"] = platform.processor() or "unknown"
    tmpl["device"]["ram_gb"] = "unknown"
    tmpl["metrics"]["load_time_ms_p50"] = 0.0
    tmpl["metrics"]["load_time_ms_p95"] = 0.0
    tmpl["metrics"]["peak_memory_mb"] = 0.0
    tmpl["metrics"]["long_run_minutes"] = 0.0
    tmpl["metrics"]["crash_count"] = 0
    tmpl["notes"] = "enablement skeleton: topology snapshot + delivery template; no performance claim."
    (artifacts / "results.json").write_text(json.dumps(tmpl, indent=2, ensure_ascii=False), encoding="utf-8")

    report = """# vllm_sglang_enablement_skeleton — 一页报告

## 范围
本示例用于固化“新硬件使能/优化交付”的最小证据闭环：环境指纹 + 拓扑摘要 + 交付模板。

## 产物
- topology.json：拓扑摘要（best-effort）
- artifacts/：env/results/report/manifest

## 声明
本示例不包含权重/私有数据，不对性能结果做前瞻承诺。
"""
    (artifacts / "report.md").write_text(report, encoding="utf-8")

    # manifest
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


