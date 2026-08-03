#!/usr/bin/env python3
"""Run the complete validation suite for the marketplace template."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    print("$ python scripts/validate_marketplace.py")
    result = subprocess.run([sys.executable, "scripts/validate_marketplace.py"], cwd=root)
    if result.returncode:
        return result.returncode
    json_files = [root / ".claude-plugin" / "marketplace.json", root / ".agents" / "plugins" / "marketplace.json"]
    json_files.extend(root.glob("plugins/**/plugin.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"Invalid JSON: {path}: {exc}", file=sys.stderr)
            return 1
    print("$ node --check docs/app.js")
    result = subprocess.run(["node", "--check", "docs/app.js"], cwd=root)
    if result.returncode:
        return result.returncode
    print("ALL VALIDATIONS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
