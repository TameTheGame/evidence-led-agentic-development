#!/usr/bin/env python3
"""Read-only release metadata checks; never publish or contact GitHub."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VERSION_RE = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)")


def validate(metadata: dict, tag: str | None = None) -> None:
    version = metadata["version"]
    if not VERSION_RE.fullmatch(version):
        raise ValueError("release version must be MAJOR.MINOR without leading zeroes")
    if tag is not None and tag != f"v{version}":
        raise ValueError("release tag must exactly match v + VERSION")
    if metadata["blueprint_version"] != version or metadata["bundle_version"] != version:
        raise ValueError("release, blueprint and bundle versions disagree")
    released = re.search(r"^## (?!Unreleased\b)(\S+) — (\d{4}-\d{2}-\d{2})$", metadata["changelog"], re.MULTILINE)
    if released is None or released.group(1) != version:
        raise ValueError("first dated changelog release must match VERSION")
    if metadata["notes_path"] != f"releases/v{version}.md":
        raise ValueError("release notes path must match VERSION")
    notes = metadata["notes"]
    if not notes.startswith(f"# ELAD v{version} — ") or not notes.strip():
        raise ValueError("release notes must identify the exact version")


def self_test() -> int:
    valid = {
        "version": "0.5", "blueprint_version": "0.5", "bundle_version": "0.5",
        "changelog": "## Unreleased\n\n## 0.5 — 2026-09-05\n",
        "notes_path": "releases/v0.5.md", "notes": "# ELAD v0.5 — Test\n\nSynthetic notes.\n",
    }
    validate(valid)
    validate(valid, "v0.5")
    for value in ("0.5.0", "v0.5", "00.5", "0.05", "0.5-rc1", "0.5\n"):
        candidate = copy.deepcopy(valid)
        candidate["version"] = value
        try:
            validate(candidate)
        except ValueError:
            continue
        raise ValueError(f"invalid version accepted: {value!r}")
    for field, value in (
        ("blueprint_version", "0.4.0"), ("bundle_version", "0.4.0"),
        ("changelog", "## Unreleased\n"),
        ("changelog", "## 0.4.0 — 2026-08-29\n"),
        ("notes_path", "releases/v0.4.0.md"), ("notes", ""),
        ("notes", "# ELAD v0.5.0 — Wrong\n"),
    ):
        candidate = copy.deepcopy(valid)
        candidate[field] = value
        try:
            validate(candidate)
        except ValueError:
            continue
        raise ValueError(f"invalid release metadata accepted: {field}")
    for tag in ("v0.5.0", "v0.6", "0.5"):
        try:
            validate(valid, tag)
        except ValueError:
            continue
        raise ValueError(f"mismatched tag accepted: {tag}")
    return 16


def check_schema_version_patterns() -> int:
    """Exercise actual reference-field patterns, not just the release parser."""
    checked = 0

    def visit(value: object) -> None:
        nonlocal checked
        if isinstance(value, dict):
            properties = value.get("properties", {})
            rule = properties.get("schemaVersion", {}) if isinstance(properties, dict) else {}
            if isinstance(rule, dict) and "pattern" in rule:
                pattern = re.compile(rule["pattern"])
                for candidate, expected in (("0.5", True), ("1.0", True), ("12.34", True),
                                            ("0.5.0", False), ("00.5", False),
                                            ("0.05", False), ("v0.5", False)):
                    if (pattern.fullmatch(candidate) is not None) != expected:
                        raise ValueError(f"schema version-reference pattern rejected/accepted {candidate!r} incorrectly")
                checked += 1
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for path in (ROOT / "spec/schemas").glob("*.schema.json"):
        visit(json.loads(path.read_text(encoding="utf-8")))
    if checked == 0:
        raise ValueError("no version-reference schema patterns were checked")
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", help="exact tag to check before publication")
    args = parser.parse_args()
    try:
        rejected = self_test()
        patterns = check_schema_version_patterns()
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        if not VERSION_RE.fullmatch(version):
            raise ValueError("VERSION must use MAJOR.MINOR before resolving release notes")
        notes_path = f"releases/v{version}.md"
        metadata = {
            "version": version,
            "blueprint_version": json.loads((ROOT / "blueprint.json").read_text(encoding="utf-8"))["version"],
            "bundle_version": json.loads((ROOT / "protocol-bundle.json").read_text(encoding="utf-8"))["version"],
            "changelog": (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"),
            "notes_path": notes_path,
            "notes": (ROOT / notes_path).read_text(encoding="utf-8"),
        }
        validate(metadata, args.tag)
        print(f"PASS — release v{version}: version, changelog, notes and optional tag agree; {rejected} negative checks rejected; {patterns} actual schema patterns checked. Read-only; no publication performed.")
        return 0
    except (ValueError, OSError, KeyError) as exc:
        print(f"FAIL — {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
