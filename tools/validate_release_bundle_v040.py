#!/usr/bin/env python3
"""Validate the exact inert ELAD 0.4 normative protocol bundle."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def deny(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    try:
        bundle = json.loads((ROOT / "protocol-bundle.json").read_text(encoding="utf-8"))
        blueprint = json.loads((ROOT / "blueprint.json").read_text(encoding="utf-8"))
        deny(bundle.get("schemaVersion") == bundle.get("version") == "0.4.0", "bundle version mismatch")
        deny(bundle.get("bundleId") == "protocol-bundle:elad_0.4.0", "bundle identity mismatch")
        deny(bundle.get("protocolId") == blueprint.get("protocolId") == "protocol:elad_0.4.0", "protocol identity mismatch")
        deny(bundle.get("state") == blueprint.get("status") == "reference_only", "bundle or blueprint is not reference-only")
        deny(bundle.get("framing") == "elad-protocol-bundle-v1", "bundle framing mismatch")

        inventory = blueprint.get("artifactInventory")
        deny(isinstance(inventory, dict), "blueprint artifact inventory is missing")
        schemas = inventory.get("normativeSchemas")
        registries = inventory.get("normativeRegistries")
        vectors = inventory.get("conformanceVectors")
        drafts = inventory.get("nonNormativeDrafts")
        deny(
            all(isinstance(group, list) for group in (schemas, registries, vectors, drafts)),
            "artifact inventory groups are not arrays",
        )
        actual_schemas = sorted(
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "spec" / "schemas").glob("*.schema.json")
        )
        actual_registries = sorted(
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "spec" / "registries").glob("*.json")
        )
        actual_vectors = sorted(
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "tests").glob("*vectors.json")
        )
        deny(sorted(schemas) == actual_schemas, "normative schema inventory is incomplete or extra")
        deny(sorted(registries) == actual_registries, "normative registry inventory is incomplete or extra")
        deny(sorted(vectors) == actual_vectors, "conformance-vector inventory is incomplete or extra")
        deny(
            all(isinstance(path, str) and (ROOT / path).is_file() for path in drafts),
            "non-normative draft inventory names a missing artifact",
        )
        expected = ["blueprint.json", "VERSION", *schemas, *registries, *vectors]
        entries = bundle.get("entries")
        deny(isinstance(entries, list), "bundle entries are not an array")
        paths = [entry.get("path") for entry in entries]
        deny(paths == expected, "bundle entry set or order differs from the closed normative inventory")
        deny("protocol-bundle.json" not in paths, "bundle contains a self-entry")
        deny(len(paths) == len(set(paths)), "bundle contains duplicate entries")
        deny(not set(drafts).intersection(paths), "non-normative draft entered the release bundle")

        for entry in entries:
            path = entry["path"]
            target = ROOT / path
            deny(target.is_file(), f"missing bundle artifact: {path}")
            if path == "VERSION":
                expected_class, mode, raw = "version_marker", "raw_bytes", target.read_bytes()
            else:
                raw = canonical(json.loads(target.read_text(encoding="utf-8")))
                mode = "canonical_json"
                expected_class = (
                    "protocol_root" if path == "blueprint.json" else
                    "schema" if path.startswith("spec/schemas/") else
                    "registry" if path.startswith("spec/registries/") else
                    "conformance_oracle"
                )
            deny(entry.get("artifactClass") == expected_class, f"wrong artifact class: {path}")
            deny(entry.get("digestMode") == mode, f"wrong digest mode: {path}")
            deny(entry.get("bytes") == len(raw), f"wrong byte count: {path}")
            deny(entry.get("sha256") == hashlib.sha256(raw).hexdigest().upper(), f"wrong digest: {path}")

        authority = blueprint.get("authority", {})
        deny(blueprint.get("maturity") == {"level": 0, "name": "Blueprint"}, "blueprint is not Level 0")
        deny(authority.get("default") == "deny" and authority.get("operational") is False, "blueprint authority is not deny/non-operational")
        deny(not any(value for key, value in authority.items() if key.startswith("issues")), "blueprint issues authority")
        print(f"PASS — ELAD 0.4 release bundle authenticates {len(entries)} normative artifacts; Level-0 reference only, no self-entry, no authority granted.")
        return 0
    except Exception as exc:
        print(f"FAIL — {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
