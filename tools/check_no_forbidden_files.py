import argparse
from pathlib import Path


FORBIDDEN_SUFFIXES = {
    ".safetensors",
    ".gguf",
    ".bin",
    ".pt",
    ".pth",
    ".onnx",
}


def main() -> int:
    p = argparse.ArgumentParser(description="Scan for forbidden weight/data files in public directory.")
    p.add_argument("--root", default=".", help="Root directory to scan")
    args = p.parse_args()

    root = Path(args.root).resolve()
    bad: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            bad.append(path)

    if bad:
        print("Found forbidden files (do not include these in public package):")
        for f in bad[:100]:
            print(f"- {f}")
        if len(bad) > 100:
            print(f"... and {len(bad) - 100} more")
        return 2

    print("OK: no forbidden weight/data files found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


