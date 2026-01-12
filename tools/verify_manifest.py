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
    p = argparse.ArgumentParser(description="Verify manifest.json (size + sha256).")
    p.add_argument("--manifest", required=True, help="Path to artifacts/manifest.json")
    args = p.parse_args()

    manifest_path = Path(args.manifest)
    root = manifest_path.parent
    m = json.loads(manifest_path.read_text(encoding="utf-8"))

    bad = 0
    for item in m.get("files", []):
        rel = item.get("path")
        expected_size = item.get("size_bytes")
        expected_sha = item.get("sha256")
        if not rel:
            bad += 1
            continue
        path = root / rel
        if not path.is_file():
            print(f"Missing: {path}")
            bad += 1
            continue
        size = path.stat().st_size
        sha = sha256_file(path)
        if expected_size is not None and size != expected_size:
            print(f"Size mismatch: {rel} expected={expected_size} actual={size}")
            bad += 1
        if expected_sha and sha.lower() != str(expected_sha).lower():
            print(f"SHA256 mismatch: {rel}")
            bad += 1

    if bad:
        print(f"FAILED: {bad} problem(s) found")
        return 2
    print("OK: manifest verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


