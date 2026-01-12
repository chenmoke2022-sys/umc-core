import argparse
import json
from pathlib import Path


REQUIRED_FILES = ["env.json", "results.json", "report.md", "manifest.json"]


def _die(msg: str, code: int) -> int:
    print(msg)
    return code


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _require(obj: dict, key: str, typ) -> None:
    if key not in obj:
        raise KeyError(key)
    if not isinstance(obj[key], typ):
        if isinstance(typ, tuple):
            expected = " | ".join(t.__name__ for t in typ)
        else:
            expected = typ.__name__
        raise TypeError(f"{key} expected {expected}, got {type(obj[key]).__name__}")


def _validate_env(env: dict) -> None:
    _require(env, "schema_version", str)
    _require(env, "generated_at_utc", str)
    _require(env, "python", str)
    _require(env, "platform", dict)

    plat = env["platform"]
    for k in ["system", "release", "version", "machine", "processor"]:
        _require(plat, k, str)


def _validate_results(results: dict) -> None:
    _require(results, "schema_version", str)
    _require(results, "data_status", str)

    _require(results, "baseline", dict)
    b = results["baseline"]
    for k in ["name", "version", "quant_profile", "backend"]:
        _require(b, k, str)

    _require(results, "device", dict)
    d = results["device"]
    for k in ["os", "cpu", "ram_gb"]:
        _require(d, k, str)

    _require(results, "metrics", dict)
    m = results["metrics"]
    for k in ["load_time_ms_p50", "load_time_ms_p95", "peak_memory_mb", "long_run_minutes"]:
        _require(m, k, (int, float))
    _require(m, "crash_count", (int, float))

    # Optional metrics (if present, must be numeric)
    for k in ["throughput_tokens_per_s_p50", "throughput_tokens_per_s_p95"]:
        if k in m and not isinstance(m[k], (int, float)):
            raise TypeError(f"{k} expected number, got {type(m[k]).__name__}")


def _validate_manifest(manifest: dict) -> None:
    _require(manifest, "schema_version", str)
    _require(manifest, "files", list)
    for it in manifest["files"]:
        if not isinstance(it, dict):
            raise TypeError("files[] item must be object")
        for k in ["path", "sha256"]:
            _require(it, k, str)
        _require(it, "size_bytes", (int, float))


def main() -> int:
    p = argparse.ArgumentParser(description="Validate required evidence artifacts exist and have basic shape.")
    p.add_argument("--artifacts", required=True, help="Artifacts directory (contains env/results/report/manifest).")
    args = p.parse_args()

    root = Path(args.artifacts)
    missing = [name for name in REQUIRED_FILES if not (root / name).is_file()]
    if missing:
        print("Missing required artifacts:")
        for name in missing:
            print(f"- {root / name}")
        return 2

    # JSON parse + structural validation
    try:
        env = _load_json(root / "env.json")
        results = _load_json(root / "results.json")
        manifest = _load_json(root / "manifest.json")
    except Exception as e:
        return _die(f"Invalid JSON: {e}", 3)

    try:
        _validate_env(env)
        _validate_results(results)
        _validate_manifest(manifest)
    except Exception as e:
        return _die(f"Schema check failed: {e}", 4)

    report = (root / "report.md").read_text(encoding="utf-8")
    if len(report.strip()) < 20:
        print("report.md looks too short; please write at least a 1-page summary.")
        return 5

    print("OK: artifacts are present and minimally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


