import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path


def _now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main() -> int:
    p = argparse.ArgumentParser(description="Collect minimal environment info for public evidence pack.")
    p.add_argument("--out", required=True, help="Output path for env.json")
    args = p.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "schema_version": "0.1",
        "generated_at_utc": _now_utc(),
        "python": sys.version.split()[0],
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "notes": "仅包含最小必要环境信息；不得包含任何本地路径/用户名/旧项目命名。",
    }

    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


