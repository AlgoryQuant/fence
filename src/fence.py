"""Check a diff against the 'May not write' line of an agent card."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def forbidden_entries(card_text: str) -> list[str]:
    for line in card_text.splitlines():
        if line.lower().startswith("may not write:"):
            rest = line.split(":", 1)[1]
            return [part.strip().strip("`") for part in rest.split(",") if part.strip()]
    return []


def changed_files(diff_text: str) -> list[str]:
    files: list[str] = []
    seen: set[str] = set()
    for line in diff_text.splitlines():
        path = ""
        if line.startswith("diff --git "):
            bits = line.split()
            if bits and bits[-1].startswith("b/"):
                path = bits[-1][2:]
        if path and path != "/dev/null" and path not in seen:
            seen.add(path)
            files.append(path)
    return files


def normalize(path: str) -> str:
    """Collapse '.' and '..' so a write cannot hide behind a prefix."""
    raw = path.replace("\\", "/").strip()
    while raw.startswith("./"):
        raw = raw[2:]
    if raw.startswith("/") or (len(raw) >= 2 and raw[1] == ":"):
        return raw
    parts: list[str] = []
    for part in raw.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts and parts[-1] != "..":
                parts.pop()
            else:
                parts.append("..")
        else:
            parts.append(part)
    return "/".join(parts)


def is_forbidden(path: str, entries: list[str]) -> bool:
    normal = normalize(path)
    if not normal or normal.startswith("..") or normal.startswith("/") or (len(normal) >= 2 and normal[1] == ":"):
        return True
    for entry in entries:
        rule = normalize(entry.replace("\\", "/").strip())
        if not rule:
            continue
        if entry.replace("\\", "/").strip().endswith("/"):
            if normal == rule or normal.startswith(rule + "/"):
                return True
        elif normal == rule:
            return True
    return False


def check(card_text: str, diff_text: str) -> str | None:
    """Return the first problem, or None when the diff stays inside the card."""
    entries = forbidden_entries(card_text)
    if not entries:
        return "card has no May not write line"
    files = changed_files(diff_text)
    if not files:
        return "diff has no files"
    for path in files:
        if is_forbidden(path, entries):
            return path
    return None


# The denominator. Expected None means the diff is accepted.
CASES: tuple[tuple[str, str | None], ...] = (
    ("samples/ok.diff", None),
    ("samples/bad.diff", "README.md"),
    ("samples/cards.diff", "cards/implement.md"),
    ("samples/escape.diff", "src/../README.md"),
    ("samples/outside.diff", "../secrets.env"),
    ("samples/empty.diff", "diff has no files"),
)


def report(root: Path) -> tuple[int, list[str]]:
    """Run every locked case. Return (count, mismatch lines)."""
    card = (root / "cards" / "implement.md").read_text(encoding="utf-8")
    mismatches: list[str] = []
    for name, expected in CASES:
        got = check(card, (root / name).read_text(encoding="utf-8"))
        if got != expected:
            mismatches.append(f"{name}: expected {expected!r}, got {got!r}")
    return len(CASES), mismatches


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a diff against an agent card.")
    parser.add_argument("command", nargs="?", default="check")
    parser.add_argument("--card")
    parser.add_argument("--diff")
    args = parser.parse_args(argv)
    if args.command == "report":
        count, mismatches = report(Path(__file__).resolve().parents[1])
        print(f"cases {count}")
        print(f"passed {count - len(mismatches)}")
        print(f"failed {len(mismatches)}")
        for line in mismatches:
            print(line)
        return 1 if mismatches else 0
    if args.command != "check":
        print("unknown command", file=sys.stderr)
        return 2
    if not args.card or not args.diff:
        print("check needs --card and --diff", file=sys.stderr)
        return 2
    problem = check(Path(args.card).read_text(encoding="utf-8"), Path(args.diff).read_text(encoding="utf-8"))
    if problem:
        print(problem)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
