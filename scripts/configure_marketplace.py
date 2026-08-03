#!/usr/bin/env python3
"""Replace the template placeholders with the owner's marketplace identity."""

from __future__ import annotations

import argparse
from pathlib import Path


TEXT_EXTENSIONS = {".json", ".html", ".js", ".md", ".txt", ".xml", ".yml", ".yaml"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--github-user", required=True, help="GitHub username or organization")
    parser.add_argument("--repository", required=True, help="Repository name")
    parser.add_argument("--marketplace-name", required=True, help="Machine-readable marketplace name")
    parser.add_argument("--display-name", required=True, help="Human-readable marketplace owner/name")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dry-run", action="store_true", help="List files without changing them")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    replacements = {
        "YOUR_GITHUB_USER": args.github_user,
        "YOUR_REPOSITORY": args.repository,
        "YOUR_MARKETPLACE_NAME": args.marketplace_name,
        "YOUR_DISPLAY_NAME": args.display_name,
    }
    changed: list[Path] = []
    for path in args.root.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        original = path.read_text(encoding="utf-8")
        updated = original
        for source, target in replacements.items():
            updated = updated.replace(source, target)
        if updated != original:
            changed.append(path)
            if not args.dry_run:
                path.write_text(updated, encoding="utf-8", newline="")
    action = "Would update" if args.dry_run else "Updated"
    print(f"{action} {len(changed)} files.")
    for path in changed:
        print(f"- {path.relative_to(args.root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
