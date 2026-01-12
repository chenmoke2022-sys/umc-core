import argparse
import json
from pathlib import Path


REQUIRED_FILES = ["env.json", "results.json", "report.md", "manifest.json"]


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

    # Basic JSON parse checks
    for name in ["env.json", "results.json", "manifest.json"]:
        path = root / name
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Invalid JSON: {path} ({e})")
            return 3

    report = (root / "report.md").read_text(encoding="utf-8")
    if len(report.strip()) < 20:
        print("report.md looks too short; please write at least a 1-page summary.")
        return 4

    print("OK: artifacts are present and minimally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


