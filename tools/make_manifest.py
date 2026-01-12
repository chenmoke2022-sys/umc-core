import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(description="Generate manifest.json (size + sha256) for artifacts directory.")
    p.add_argument("--dir", required=True, help="Directory to scan (usually ./artifacts)")
    p.add_argument("--out", required=True, help="Output manifest.json path")
    args = p.parse_args()

    root = Path(args.dir)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    files = []
    for path in sorted(root.glob("*")):
        if not path.is_file():
            continue
        if path.name == out.name:
            continue
        files.append(
            {
                "path": path.name,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )

    data = {"schema_version": "0.1", "files": files}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


