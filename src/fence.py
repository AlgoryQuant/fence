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


def is_forbidden(path: str, entries: list[str]) -> bool:
    normal = path.replace("\\", "/").lstrip("./")
    for entry in entries:
        rule = entry.replace("\\", "/").strip()
        if not rule:
            continue
        if rule.endswith("/"):
            if normal.startswith(rule):
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a diff against an agent card.")
    parser.add_argument("check_cmd", nargs="?", default="check")
    parser.add_argument("--card", required=True)
    parser.add_argument("--diff", required=True)
    args = parser.parse_args(argv)
    if args.check_cmd != "check":
        print("unknown command", file=sys.stderr)
        return 2
    problem = check(Path(args.card).read_text(encoding="utf-8"), Path(args.diff).read_text(encoding="utf-8"))
    if problem:
        print(problem)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
