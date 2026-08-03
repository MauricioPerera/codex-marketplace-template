#!/usr/bin/env python3
"""Validate the Claude Code + Codex marketplace template layout."""
import json
import re
import sys
from pathlib import Path

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate_plugin_manifests(root, name, plugin, errors):
    claude_path = plugin / ".claude-plugin" / "plugin.json"
    codex_path = plugin / ".codex-plugin" / "plugin.json"
    try:
        claude = load(claude_path)
        codex = load(codex_path)
    except Exception as exc:
        errors.append(f"Invalid plugin manifest: {name}: {exc}")
        return
    for label, manifest in (("Claude", claude), ("Codex", codex)):
        if manifest.get("name") != name:
            errors.append(f"{label} manifest name differs from marketplace entry: {name}")
        if not manifest.get("version") or not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest["version"])):
            errors.append(f"{label} manifest has invalid version: {name}")
        if not manifest.get("description"):
            errors.append(f"{label} manifest is missing description: {name}")
    if claude.get("version") != codex.get("version"):
        errors.append(f"Claude and Codex versions differ: {name}")
    if claude.get("displayName") != codex.get("interface", {}).get("displayName"):
        errors.append(f"Claude and Codex display names differ: {name}")

def main():
    root = Path(__file__).resolve().parents[1]
    files = [root / ".claude-plugin" / "marketplace.json", root / ".agents" / "plugins" / "marketplace.json"]
    errors = []
    manifests = []
    for path in files:
        if not path.exists(): errors.append(f"Missing {path.relative_to(root)}")
        else:
            try: manifests.append(load(path))
            except Exception as exc: errors.append(f"Invalid JSON {path}: {exc}")
    names = []
    categories = []
    for manifest in manifests:
        entries = manifest.get("plugins", [])
        names.append({entry.get("name") for entry in entries})
        categories.append({entry.get("name"): entry.get("category") for entry in entries})
        for entry in entries:
            name = entry.get("name")
            source = entry.get("source")
            relative = source if isinstance(source, str) else (source or {}).get("path")
            plugin = root / relative if relative else root / "missing"
            if not name or not relative or not plugin.is_dir(): errors.append(f"Invalid plugin entry: {entry}")
            elif not (plugin / ".claude-plugin" / "plugin.json").exists(): errors.append(f"Missing Claude manifest: {name}")
            elif not (plugin / ".codex-plugin" / "plugin.json").exists(): errors.append(f"Missing Codex manifest: {name}")
            else:
                validate_plugin_manifests(root, name, plugin, errors)
                if not list((plugin / "skills").glob("*/SKILL.md")): errors.append(f"Missing skill: {name}")
    if len(names) == 2 and names[0] != names[1]: errors.append("Claude and Codex plugin lists differ")
    if len(categories) == 2 and categories[0] != categories[1]: errors.append("Claude and Codex categories differ")
    catalog_path = root / "docs" / "catalog.json"
    if not catalog_path.exists():
        errors.append("Missing docs/catalog.json")
    else:
        try:
            catalog = load(catalog_path)
            catalog_names = {entry.get("name") for entry in catalog.get("plugins", [])}
            if names and catalog_names != names[0]:
                errors.append("docs/catalog.json plugin list differs from marketplace manifests")
            catalog_categories = {entry.get("name"): entry.get("category") for entry in catalog.get("plugins", [])}
            if categories and catalog_categories != categories[0]:
                errors.append("docs/catalog.json categories differ from marketplace manifests")
        except Exception as exc:
            errors.append(f"Invalid JSON docs/catalog.json: {exc}")
    result = {"status": "FAILED" if errors else "PASSED", "errors": errors}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if errors else 0

if __name__ == "__main__": sys.exit(main())
