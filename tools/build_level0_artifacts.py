#!/usr/bin/env python3
"""Regenerate inert ELAD Level-0 references and the authenticated release bundle.

This script writes only blueprint.json, the synthetic continuation JSON fixture, and
protocol-bundle.json. It never contacts a provider, runs a model, changes authority, or
touches an adopting project.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "continuation-valid"


def canonical(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path.relative_to(ROOT).as_posix()}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def digest_path(path: Path) -> tuple[bytes, str]:
    if path.suffix.lower() == ".json":
        return canonical(read_json(path)), "canonical_json"
    return path.read_bytes(), "raw_bytes"


def update_reference(reference: dict[str, Any]) -> None:
    relative = reference.get("path")
    if not isinstance(relative, str) or "sha256" not in reference:
        return
    target = ROOT / relative
    if not target.is_file():
        raise RuntimeError(f"reference target is missing: {relative}")
    payload, mode = digest_path(target)
    reference["sha256"] = hashlib.sha256(payload).hexdigest().upper()
    if "bytes" in reference:
        reference["bytes"] = len(payload)
    if "digestMode" in reference:
        reference["digestMode"] = mode


def walk_references(value: Any) -> None:
    if isinstance(value, dict):
        update_reference(value)
        for child in value.values():
            walk_references(child)
    elif isinstance(value, list):
        for child in value:
            walk_references(child)


def update_blueprint_registries() -> dict[str, Any]:
    blueprint_path = ROOT / "blueprint.json"
    blueprint = read_json(blueprint_path)
    bindings = blueprint.get("canonicalRegistries")
    if not isinstance(bindings, dict):
        raise RuntimeError("blueprint has no canonical registry bindings")
    for reference in bindings.values():
        if not isinstance(reference, dict):
            raise RuntimeError("blueprint registry reference is not an object")
        update_reference(reference)
    write_json(blueprint_path, blueprint)
    return blueprint


def update_continuation_fixture() -> None:
    order = [
        "authority.json",
        "data-policy.json",
        "evidence-policy.json",
        "intent.json",
        "risk-policy.json",
        "tool-registry.json",
        "evaluator-registry.json",
        "writer-profile.json",
        "project-profile.json",
        "capability-certificate.json",
        "retrieval-manifest.json",
        "packet.json",
        "evidence-manifest.json",
        "receipt.await-human.json",
        "review-bundle.json",
        "external-human-receipt.json",
        "receipt.final.json",
        "anchor.json",
    ]
    actual = {path.name for path in FIXTURE.glob("*.json")}
    if actual != set(order):
        raise RuntimeError(
            "continuation JSON inventory differs from the explicit regeneration order"
        )
    for name in order:
        path = FIXTURE / name
        document = read_json(path)
        walk_references(document)
        write_json(path, document)


def inventory_paths(blueprint: dict[str, Any]) -> list[str]:
    inventory = blueprint.get("artifactInventory")
    if not isinstance(inventory, dict):
        raise RuntimeError("blueprint has no explicit artifact inventory")

    schemas = inventory.get("normativeSchemas")
    registries = inventory.get("normativeRegistries")
    vectors = inventory.get("conformanceVectors")
    drafts = inventory.get("nonNormativeDrafts")
    if not all(isinstance(group, list) for group in (schemas, registries, vectors, drafts)):
        raise RuntimeError("artifact inventory groups must be arrays")

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
    if sorted(schemas) != actual_schemas:
        raise RuntimeError("normative schema inventory is incomplete or extra")
    if sorted(registries) != actual_registries:
        raise RuntimeError("normative registry inventory is incomplete or extra")
    if sorted(vectors) != actual_vectors:
        raise RuntimeError("conformance vector inventory is incomplete or extra")
    for relative in drafts:
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"non-normative draft is missing: {relative}")

    combined = ["blueprint.json", "VERSION", *schemas, *registries, *vectors]
    if len(combined) != len(set(combined)):
        raise RuntimeError("artifact inventory contains duplicates")
    return combined


def build_bundle(blueprint: dict[str, Any]) -> None:
    entries: list[dict[str, Any]] = []
    for relative in inventory_paths(blueprint):
        target = ROOT / relative
        if not target.is_file():
            raise RuntimeError(f"bundle artifact is missing: {relative}")
        payload, mode = digest_path(target)
        artifact_class = (
            "protocol_root"
            if relative == "blueprint.json"
            else "version_marker"
            if relative == "VERSION"
            else "schema"
            if relative.startswith("spec/schemas/")
            else "registry"
            if relative.startswith("spec/registries/")
            else "conformance_oracle"
        )
        entries.append(
            {
                "path": relative,
                "artifactClass": artifact_class,
                "digestMode": mode,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest().upper(),
            }
        )

    bundle = {
        "schemaVersion": "0.5",
        "bundleId": "protocol-bundle:elad_0.5",
        "protocolId": blueprint["protocolId"],
        "version": blueprint["version"],
        "state": "reference_only",
        "framing": "elad-protocol-bundle-v1",
        "entries": entries,
    }
    write_json(ROOT / "protocol-bundle.json", bundle)


def main() -> int:
    blueprint = update_blueprint_registries()
    update_continuation_fixture()
    # The blueprint bytes are stable after registry updates and fixture generation does
    # not feed back into it.
    blueprint = read_json(ROOT / "blueprint.json")
    build_bundle(blueprint)
    print(
        "PASS — regenerated inert Level-0 registry bindings, synthetic continuation "
        "references, and explicit release bundle. No authority granted."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
