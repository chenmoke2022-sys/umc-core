import argparse
import re
from pathlib import Path


DEFAULT_PATTERNS = [
    # Windows absolute paths (most common leakage form)
    r"[A-Za-z]:\\",
]


TEXT_EXTS = {
    ".md",
    ".txt",
    ".py",
    ".ps1",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
}


def main() -> int:
    p = argparse.ArgumentParser(description="Scan public directory for path leaks / sensitive markers.")
    p.add_argument("--root", default=".", help="Root directory to scan")
    p.add_argument("--pattern", action="append", default=[], help="Additional regex pattern (repeatable)")
    args = p.parse_args()

    patterns = list(DEFAULT_PATTERNS) + list(args.pattern or [])
    regexes = [re.compile(p) for p in patterns]

    root = Path(args.root).resolve()
    hits = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_EXTS:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for rx in regexes:
            if rx.search(text):
                hits.append((path, rx.pattern))
                break

    if hits:
        print("Found potential redaction issues:")
        for pth, pat in hits[:200]:
            print(f"- {pth}  (matched: {pat})")
        if len(hits) > 200:
            print(f"... and {len(hits) - 200} more")
        return 2

    print("OK: no redaction markers found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


