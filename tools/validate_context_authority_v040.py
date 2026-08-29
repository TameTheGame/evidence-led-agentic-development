#!/usr/bin/env python3
"""Standalone protocol-0.3 context and authority conformance checks.

This dependency-free validator exercises only the bounded files introduced by the
0.4.0 context/authority/core-lock correction.  It uses an in-memory synthetic fixture;
a PASS grants no authority over a real repository, model, harness, target, reviewer,
promotion, or publication surface.
"""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SHA256_RE = re.compile(r"^[A-F0-9]{64}$")
ZERO_SHA256 = "0" * 64
ZERO_COMMIT = "0" * 40


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_load_bytes(data: bytes, label: str) -> Any:
    require(not data.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM is forbidden: {label}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"invalid UTF-8 in {label}: {exc}") from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=strict_pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(ValidationError(f"non-standard JSON constant in {label}: {value}")),
        )
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {label}: {exc}") from exc


def load_json(relative_path: str) -> dict[str, Any]:
    document = strict_load_bytes((ROOT / relative_path).read_bytes(), relative_path)
    require(isinstance(document, dict), f"top-level JSON is not an object: {relative_path}")
    return document


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def canonical_sha256(value: Any) -> str:
    return sha256(canonical_json_bytes(value))


def parse_datetime(value: Any, label: str) -> None:
    require(isinstance(value, str), f"{label} is not a date-time string")
    try:
        dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"{label} is not a valid date-time") from exc


def schema_types(value: Any, declared: str | list[str]) -> bool:
    names = [declared] if isinstance(declared, str) else declared
    mapping = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool) and math.isfinite(item),
        "boolean": lambda item: isinstance(item, bool),
        "null": lambda item: item is None,
    }
    return any(mapping[name](value) for name in names)


def validate_schema_instance(value: Any, schema: dict[str, Any], root: dict[str, Any], location: str = "$") -> None:
    if "$ref" in schema:
        reference = schema["$ref"]
        require(reference.startswith("#/$defs/"), f"unsupported schema reference at {location}: {reference}")
        definition = reference.split("/", 2)[2]
        validate_schema_instance(value, root["$defs"][definition], root, location)
        return
    if "const" in schema:
        require(value == schema["const"], f"const mismatch at {location}")
    if "enum" in schema:
        require(value in schema["enum"], f"enum mismatch at {location}")
    if "type" in schema:
        require(schema_types(value, schema["type"]), f"type mismatch at {location}")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            require(key in value, f"missing required property at {location}.{key}")
        if schema.get("additionalProperties") is False:
            require(not (set(value) - set(properties)), f"extra properties at {location}")
        for key, child in value.items():
            if key in properties:
                validate_schema_instance(child, properties[key], root, f"{location}.{key}")
    if isinstance(value, list):
        if "minItems" in schema:
            require(len(value) >= schema["minItems"], f"array below minItems at {location}")
        if schema.get("uniqueItems"):
            normalized = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in value]
            require(len(normalized) == len(set(normalized)), f"duplicate array item at {location}")
        if isinstance(schema.get("items"), dict):
            for index, child in enumerate(value):
                validate_schema_instance(child, schema["items"], root, f"{location}[{index}]")
    if isinstance(value, str):
        if "minLength" in schema:
            require(len(value) >= schema["minLength"], f"string below minLength at {location}")
        if "pattern" in schema:
            require(re.search(schema["pattern"], value) is not None, f"pattern mismatch at {location}")
        if schema.get("format") == "date-time":
            parse_datetime(value, location)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema:
            require(value >= schema["minimum"], f"number below minimum at {location}")
        if "maximum" in schema:
            require(value <= schema["maximum"], f"number above maximum at {location}")


def validate_templates() -> int:
    pairs = [
        ("templates/protocol-bundle.template.json", "spec/schemas/protocol-bundle.schema.json"),
        ("templates/core.lock.template.json", "spec/schemas/core-lock.schema.json"),
        ("templates/context-delivery.template.json", "spec/schemas/context-delivery.schema.json"),
    ]
    for template_path, schema_path in pairs:
        schema = load_json(schema_path)
        template = load_json(template_path)
        validate_schema_instance(template, schema, schema)
        require(template.get("state") == "template_inert", f"template is not inert: {template_path}")
    core = load_json("templates/core.lock.template.json")
    require(core["targetCompatibility"] == "not_evaluated", "core-lock template claims compatibility")
    require(core["approvedBy"] is None and core["approvedAt"] is None, "core-lock template claims approval")
    context = load_json("templates/context-delivery.template.json")
    require(context["segments"] == [] and context["createdAt"] is None, "context template claims delivery")
    bundle = load_json("templates/protocol-bundle.template.json")
    require(bundle["entries"] == [], "protocol-bundle template claims a sealed entry set")
    return len(pairs)


def validate_maturity_registry(vectors: dict[str, Any]) -> dict[int, dict[str, Any]]:
    registry = load_json("spec/registries/maturity-ceilings.json")
    require(registry.get("schemaVersion") == "0.4.0", "maturity registry version mismatch")
    require(registry.get("status") == "reference_only", "maturity registry is not reference-only")
    rows = registry.get("levels", [])
    require([row.get("level") for row in rows] == list(range(7)), "maturity registry must contain ordered levels 0-6")
    expected = vectors.get("expectedMaturityLevels", [])
    require(len(expected) == 7, "maturity vector oracle must contain seven rows")
    for actual, oracle in zip(rows, expected):
        for key in ("level", "allowedEffects", "allowedFinalizationCeilings", "maxTrueAuthorizations"):
            require(actual.get(key) == oracle.get(key), f"maturity registry/oracle mismatch: level {oracle.get('level')}:{key}")
        require("promotion" not in actual["maxTrueAuthorizations"], "promotion is not an implemented 0.3 surface")
        require("publication" not in actual["maxTrueAuthorizations"], "publication is not an implemented 0.3 surface")
    return {row["level"]: row for row in rows}


def validate_maturity_case(case: dict[str, Any], matrix: dict[int, dict[str, Any]]) -> None:
    level = case.get("level")
    require(level in matrix and level > 0, "authority maturity is not operational")
    row = matrix[level]
    require(set(case.get("effects", [])).issubset(row["allowedEffects"]), "effect exceeds maturity")
    require(case.get("finalizationCeiling") in row["allowedFinalizationCeilings"], "finalization exceeds maturity")
    require(set(case.get("trueAuthorizations", [])).issubset(row["maxTrueAuthorizations"]), "authorization exceeds maturity")


def immutable_reference(identifier: str, path: str, document: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": identifier,
        "path": path,
        "sha256": canonical_sha256(document),
        "schemaVersion": "0.4.0",
    }


def raw_descriptor(path: str, data: bytes) -> dict[str, Any]:
    return {"path": path, "bytes": len(data), "sha256": sha256(data)}


def validate_raw_descriptor(descriptor: dict[str, Any], artifacts: dict[str, bytes], label: str) -> bytes:
    path = descriptor.get("path")
    require(path in artifacts, f"{label} artifact is missing: {path}")
    data = artifacts[path]
    require(descriptor.get("bytes") == len(data), f"{label} byte count mismatch: {path}")
    require(descriptor.get("sha256") == sha256(data), f"{label} digest mismatch: {path}")
    return data


def protocol_entry(path: str, artifact_class: str, digest_mode: str, data: bytes) -> dict[str, Any]:
    digest_bytes = data
    if digest_mode == "canonical_json":
        digest_bytes = canonical_json_bytes(strict_load_bytes(data, path))
    return {
        "path": path,
        "artifactClass": artifact_class,
        "digestMode": digest_mode,
        "bytes": len(digest_bytes),
        "sha256": sha256(digest_bytes),
    }


def validate_protocol_bundle(bundle: dict[str, Any], files: dict[str, bytes], expected_paths: set[str]) -> None:
    require(bundle.get("schemaVersion") == bundle.get("version") == "0.4.0", "protocol bundle version mismatch")
    require(bundle.get("bundleId") == "protocol-bundle:elad_0.4.0", "protocol bundle ID mismatch")
    require(bundle.get("protocolId") == "protocol:elad_0.4.0", "protocol ID mismatch")
    require(bundle.get("framing") == "elad-protocol-bundle-v1", "protocol bundle framing mismatch")
    require(bundle.get("state") in {"reference_only", "released"}, "protocol bundle is not sealed for inspection")
    entries = bundle.get("entries", [])
    paths = [entry.get("path") for entry in entries]
    require(len(paths) == len(set(paths)), "protocol bundle contains duplicate paths")
    require(len([path.casefold() for path in paths]) == len(set(path.casefold() for path in paths)), "protocol bundle paths collide by case")
    require("protocol-bundle.json" not in paths, "protocol bundle contains itself")
    require(set(paths) == expected_paths == set(files), "protocol bundle entry set is missing or extra")
    for entry in entries:
        path = entry["path"]
        data = files[path]
        mode = entry.get("digestMode")
        if mode == "canonical_json":
            digest_bytes = canonical_json_bytes(strict_load_bytes(data, path))
            require(path.endswith(".json"), f"canonical JSON mode used for a non-JSON artifact: {path}")
        else:
            require(mode == "raw_bytes", f"unknown protocol digest mode: {path}")
            digest_bytes = data
        require(entry.get("bytes") == len(digest_bytes), f"protocol entry byte mismatch: {path}")
        require(entry.get("sha256") == sha256(digest_bytes), f"protocol entry digest mismatch: {path}")


def validate_reference(reference: dict[str, Any], identifier: str, path: str, document: dict[str, Any], label: str) -> None:
    require(reference.get("id") == identifier, f"{label} ID mismatch")
    require(reference.get("path") == path, f"{label} path mismatch")
    require(reference.get("schemaVersion") == "0.4.0", f"{label} schema version mismatch")
    require(reference.get("sha256") == canonical_sha256(document), f"{label} digest mismatch")


def validate_core_lock(
    core: dict[str, Any],
    bundle: dict[str, Any],
    repository_id: str,
    owner_id: str,
) -> None:
    require(core.get("state") == "approved", "core lock is not approved")
    require(core.get("ownerRepositoryId") == repository_id, "core lock owner repository mismatch")
    blueprint = core.get("blueprint", {})
    require(blueprint.get("name") == "Evidence-Led Agentic Development", "core lock blueprint name mismatch")
    require(blueprint.get("version") == bundle.get("version") == "0.4.0", "core lock blueprint version mismatch")
    require(blueprint.get("protocolId") == bundle.get("protocolId"), "core lock protocol mismatch")
    require(blueprint.get("distributionIdentity") not in {None, "", "replace-with-approved-private-or-public-source"}, "core lock distribution identity is a placeholder")
    require(blueprint.get("sourceCommit") != ZERO_COMMIT, "approved core lock contains a placeholder commit")
    require(blueprint.get("distributionSha256") != ZERO_SHA256, "approved core lock contains a placeholder distribution digest")
    require(core.get("targetCompatibility") == "compatible", "core lock target compatibility is not accepted")
    require(core.get("approvedBy") == owner_id, "core lock approver differs from repository owner")
    parse_datetime(core.get("approvedAt"), "core lock approvedAt")
    validate_reference(
        core.get("protocolBundle", {}),
        bundle["bundleId"],
        "automation/protocol/protocol-bundle.json",
        bundle,
        "core lock protocol bundle",
    )


def validate_selector(selector: dict[str, Any], repository: dict[str, Any]) -> None:
    require(set(selector) == {"kind", "selector", "repositoryId", "id", "baseHead", "sha256"}, "selector fields are incomplete or extra")
    require(selector.get("kind") == "candidate", "unsupported pre-run subject kind")
    require(selector.get("selector") == "receipt_candidate", "unsupported pre-run selector")
    require(selector.get("repositoryId") == repository.get("repositoryId"), "selector repository mismatch")
    require(selector.get("id") == repository.get("candidateId"), "selector candidate mismatch")
    require(selector.get("baseHead") == repository.get("baseHead"), "selector base mismatch")
    require(selector.get("sha256") is None, "receipt_candidate pre-run SHA must be null")


def validate_intent_contract(
    project: dict[str, Any],
    authority: dict[str, Any],
    intent: dict[str, Any],
    packet: dict[str, Any],
    receipt: dict[str, Any],
) -> None:
    require(intent.get("state") == "accepted", "intent is not accepted")
    acceptance = intent.get("acceptance", {})
    require(acceptance.get("acceptedBy") == authority.get("owner"), "intent acceptor differs from authority owner")
    parse_datetime(acceptance.get("acceptedAt"), "intent acceptedAt")
    for field in ("humanOnlyDecisions", "maximumUsefulExperiment", "fallbackPlan", "contextDeltaPolicy"):
        require(packet.get(field) == intent.get(field), f"intent/packet field changed: {field}")
        require(receipt.get(field) == packet.get(field), f"packet/receipt field changed: {field}")

    policy_rows = project.get("humanOnlyDecisions", [])
    policy_classes = [row.get("decisionClass") for row in policy_rows]
    require(len(policy_classes) == len(set(policy_classes)), "project decision classes are duplicated")
    policy_by_class = {row["decisionClass"]: row for row in policy_rows}
    decisions = intent.get("humanOnlyDecisions", [])
    decision_ids = [row.get("decisionId") for row in decisions]
    require(len(decision_ids) == len(set(decision_ids)), "human decision IDs are duplicated")
    for decision in decisions:
        decision_class = decision.get("decisionClass")
        require(decision_class in policy_by_class, "human decision class is not owner-declared")
        resolution = decision.get("resolution", {})
        require(resolution.get("state") == "recorded", "human decision is unresolved")
        require(resolution.get("executionDisposition") in {"permit", "not_applicable"}, "human decision does not permit execution")
        require(resolution.get("resolvedBy") in policy_by_class[decision_class].get("eligibleOwnerIds", []), "human decision owner is ineligible")
        parse_datetime(resolution.get("resolvedAt"), f"human decision {decision.get('decisionId')} resolvedAt")

    repository = packet.get("repository", {})
    claims = packet.get("claims", [])
    require(claims and len([claim.get("claimId") for claim in claims]) == len(set(claim.get("claimId") for claim in claims)), "packet claims are empty or duplicated")
    for claim in claims:
        validate_selector(claim.get("subject", {}), repository)

    budgets = packet.get("budgets", {})
    require(budgets.get("contextTokens", 0) + budgets.get("outputTokens", 0) <= budgets.get("contextWindowTokens", 0), "packet context plus output exceeds the window")
    experiment = intent.get("maximumUsefulExperiment", {})
    claim_ids = {claim["claimId"] for claim in claims}
    experiment_claims = experiment.get("claimIds", [])
    require(experiment_claims and len(experiment_claims) == len(set(experiment_claims)), "experiment claim set is empty or duplicated")
    require(set(experiment_claims).issubset(claim_ids), "experiment references an unknown claim")
    require(0 < experiment.get("attemptCeiling", 0) <= intent.get("budgets", {}).get("attempts", 0), "experiment exceeds intent attempt budget")
    require(experiment.get("attemptCeiling") <= budgets.get("attempts", 0), "experiment exceeds packet attempt budget")
    require(experiment.get("stopWhen") in {"first_discriminating_result", "all_listed_claims_resolved"}, "unknown experiment stop condition")

    stop_states = intent.get("stopStates", [])
    fallback = intent.get("fallbackPlan", [])
    triggers = [row.get("triggerState") for row in fallback]
    require(len(triggers) == len(set(triggers)), "fallback triggers are duplicated")
    require(set(triggers) == set(stop_states), "fallback plan does not cover every stop state exactly")
    require(all(row.get("requiresFreshPacket") is True for row in fallback), "fallback can execute without a fresh packet")

    delta = intent.get("contextDeltaPolicy", {})
    require(delta.get("maxRequests") in {0, 1}, "context delta permits more than one request")
    if delta.get("maxRequests") == 0:
        require(delta.get("maxEntries") == delta.get("maxAdditionalBytes") == delta.get("maxAdditionalTokens") == 0, "disabled delta has a nonzero budget")
        require(delta.get("allowedPaths") == [], "disabled delta has allowed paths")
    else:
        require(delta.get("maxEntries", 0) > 0, "enabled delta has no entry budget")
        require(delta.get("allowedPaths"), "enabled delta has no exact path allowlist")


def materialize_utf8_lf_lines(data: bytes, start: int, end: int) -> bytes:
    require(not data.startswith(b"\xef\xbb\xbf"), "slice source contains a BOM")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError("slice source is not UTF-8") from exc
    require(1 <= start <= end, "slice line range is invalid")
    lines = data.splitlines(keepends=True)
    if data and not lines:
        lines = [data]
    require(end <= len(lines), "slice line range exceeds source")
    return b"".join(lines[start - 1 : end])


def validate_retrieval(retrieval: dict[str, Any], artifacts: dict[str, bytes]) -> dict[str, dict[str, Any]]:
    require(retrieval.get("state") == "frozen", "retrieval manifest is not frozen")
    require(retrieval.get("deltaOrdinal") in {0, 1}, "retrieval delta ordinal exceeds protocol ceiling")
    entries = retrieval.get("entries", [])
    ids = [entry.get("entryId") for entry in entries]
    require(ids and len(ids) == len(set(ids)), "retrieval entries are empty or duplicated")
    by_id: dict[str, dict[str, Any]] = {}
    for entry in entries:
        require(entry.get("workerAccess") == "prebundled", "0.3 admitted retrieval is not prebundled")
        source = entry.get("source", {})
        delivery = entry.get("delivery", {})
        source_data = validate_raw_descriptor(source, artifacts, "retrieval source")
        delivery_data = validate_raw_descriptor(delivery, artifacts, "retrieval delivery")
        mode = delivery.get("mode")
        if mode == "whole_file":
            require(delivery.get("selector") is None, "whole-file delivery has a slice selector")
            require(delivery_data == source_data, "whole-file delivery differs from its source")
        elif mode == "materialized_utf8_lf_lines_v1":
            selector = delivery.get("selector", {})
            expected = materialize_utf8_lf_lines(source_data, selector.get("startLine", 0), selector.get("endLine", 0))
            require(delivery_data == expected, "materialized slice differs from the selected source lines")
        else:
            raise ValidationError("unsupported retrieval delivery mode")
        by_id[entry["entryId"]] = entry
    return by_id


def compile_context(segments: list[dict[str, Any]], artifacts: dict[str, bytes]) -> bytes:
    compiled_segments: list[dict[str, Any]] = []
    for segment in segments:
        delivered = validate_raw_descriptor(segment.get("delivered", {}), artifacts, "context segment")
        try:
            content = delivered.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValidationError("model-visible segment is not UTF-8") from exc
        require(not delivered.startswith(b"\xef\xbb\xbf"), "model-visible segment contains a BOM")
        compiled_segments.append(
            {
                "ordinal": segment.get("ordinal"),
                "segmentId": segment.get("segmentId"),
                "channel": segment.get("channel"),
                "content": content,
            }
        )
    return canonical_json_bytes({"format": "elad-model-visible-context-v1", "segments": compiled_segments})


def validate_context_delivery(
    context: dict[str, Any],
    packet: dict[str, Any],
    retrieval: dict[str, Any],
    bundle: dict[str, Any],
    receipt: dict[str, Any],
    artifacts: dict[str, bytes],
) -> None:
    require(context.get("state") == "sealed", "context delivery is not sealed")
    validate_reference(context.get("protocolBundle", {}), bundle["bundleId"], "automation/protocol/protocol-bundle.json", bundle, "context protocol")
    validate_reference(context.get("packet", {}), packet["packetId"], "automation/packets/review.json", packet, "context packet")
    validate_reference(context.get("retrievalManifest", {}), retrieval["manifestId"], "automation/retrieval/review.json", retrieval, "context retrieval")
    retrieval_by_id = validate_retrieval(retrieval, artifacts)
    segments = context.get("segments", [])
    require([segment.get("ordinal") for segment in segments] == list(range(len(segments))), "context ordinals are not contiguous and ordered")
    segment_ids = [segment.get("segmentId") for segment in segments]
    require(len(segment_ids) == len(set(segment_ids)), "context segment IDs are duplicated")
    expected_origins = {"prompt-template:synthetic", packet["packetId"], "tool-schema:synthetic", *retrieval_by_id}
    actual_origins = {segment.get("origin", {}).get("id") for segment in segments}
    require(actual_origins == expected_origins and len(segments) == len(expected_origins), "context omits or invents a model-visible segment")
    for segment in segments:
        origin = segment.get("origin", {})
        origin_data = validate_raw_descriptor(origin, artifacts, "context origin")
        delivered_data = validate_raw_descriptor(segment.get("delivered", {}), artifacts, "context delivered")
        require(delivered_data == origin_data, "context delivery changes origin bytes")
        if origin.get("kind") == "retrieval_entry":
            require(origin.get("id") in retrieval_by_id, "context references an unknown retrieval entry")
            expected_delivery = retrieval_by_id[origin["id"]]["delivery"]
            require(segment.get("delivered") == {key: expected_delivery[key] for key in ("path", "bytes", "sha256")}, "context retrieval segment differs from its delivery manifest")
        else:
            require(origin.get("kind") == "contract_artifact", "context origin kind is unsupported")
    expected_compiled = compile_context(segments, artifacts)
    actual_compiled = validate_raw_descriptor(context.get("compiledArtifact", {}), artifacts, "compiled context")
    require(actual_compiled == expected_compiled, "compiled context differs from ordered segment bytes")
    accounting = context.get("accounting", {})
    require(accounting.get("methodId") == "context-accounting:synthetic_byte_count_v1", "context accounting method is not qualified by this synthetic fixture")
    require(accounting.get("counterToolId") == "tool:synthetic_byte_counter", "context counter tool mismatch")
    require(accounting.get("counterRegistryEntrySha256") == "A" * 64, "context counter registry digest mismatch")
    require(accounting.get("inputTokens") == len(expected_compiled), "context input accounting differs from the synthetic counter")
    budgets = packet.get("budgets", {})
    require(accounting.get("inputTokens") <= budgets.get("contextTokens", 0), "compiled context exceeds packet input budget")
    require(accounting.get("outputReserveTokens") == budgets.get("outputTokens"), "context output reserve differs from packet")
    require(accounting.get("requiredContextTokens") == accounting.get("inputTokens") + accounting.get("outputReserveTokens"), "required context accounting is not additive")
    require(accounting.get("requiredContextTokens") <= budgets.get("contextWindowTokens", 0), "compiled input plus output reserve exceeds the context window")
    validate_reference(receipt.get("contextDelivery", {}), context["bundleId"], "automation/context/review.json", context, "receipt context delivery")


def validate_delta_and_fallback(intent: dict[str, Any], packet: dict[str, Any], receipt: dict[str, Any]) -> None:
    terminal = receipt.get("terminalStatus")
    request = receipt.get("contextDeltaRequest")
    disposition = receipt.get("fallbackDisposition")
    fallback_by_state = {row["triggerState"]: row for row in packet.get("fallbackPlan", [])}
    if terminal == "COMPLETE":
        require(request is None, "COMPLETE receipt contains a context request")
        require(disposition is None, "COMPLETE receipt contains a fallback disposition")
        require(receipt.get("requestedNextAction") == "none", "COMPLETE receipt requests more work")
        return
    require(terminal in fallback_by_state, "terminal state has no fallback")
    fallback = fallback_by_state[terminal]
    expected = {
        "fallbackId": fallback["fallbackId"],
        "triggerState": terminal,
        "requestedNextAction": fallback["requestedNextAction"],
    }
    require(disposition == expected, "receipt fallback disposition differs from the packet")
    require(receipt.get("requestedNextAction") == fallback["requestedNextAction"], "receipt next action differs from fallback")
    if terminal != "NEED_CONTEXT":
        require(request is None, "non-NEED_CONTEXT receipt contains a context request")
        return
    require(request is not None, "NEED_CONTEXT receipt omits its structured delta request")
    policy = intent.get("contextDeltaPolicy", {})
    require(policy.get("maxRequests") == 1, "context delta is not enabled")
    require(request.get("ordinal") == 1, "context request is not the one permitted delta")
    entries = request.get("entries", [])
    require(0 < len(entries) <= policy.get("maxEntries", 0), "context request entry count exceeds policy")
    paths = [entry.get("path") for entry in entries]
    require(len(paths) == len(set(path.casefold() for path in paths)), "context request paths collide or duplicate")
    require(set(paths).issubset(set(policy.get("allowedPaths", []))), "context request path is outside the exact allowlist")
    require(all(entry.get("repositoryId") == packet.get("repository", {}).get("repositoryId") for entry in entries), "context request repository mismatch")
    byte_sum = sum(entry.get("maxBytes", 0) for entry in entries)
    token_sum = sum(entry.get("maxTokens", 0) for entry in entries)
    require(request.get("totalMaxBytes") == byte_sum <= policy.get("maxAdditionalBytes", 0), "context request exceeds byte policy")
    require(request.get("totalMaxTokens") == token_sum <= policy.get("maxAdditionalTokens", 0), "context request exceeds token policy")
    require(all(entry.get("deliveryMode") in {"whole_file", "materialized_utf8_lf_lines_v1"} for entry in entries), "context request has an unsupported delivery mode")


def build_fixture() -> dict[str, Any]:
    protocol_files = {
        "blueprint.json": canonical_json_bytes({"schemaVersion": "0.4.0", "protocolId": "protocol:elad_0.4.0"}),
        "VERSION": b"0.4.0\n",
        "spec/schemas/synthetic.schema.json": canonical_json_bytes({"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"}),
        "spec/registries/synthetic.json": canonical_json_bytes({"schemaVersion": "0.4.0", "values": ["synthetic"]}),
        "tests/synthetic-oracle.json": canonical_json_bytes({"schemaVersion": "0.4.0", "expected": "deny_by_default"}),
    }
    bundle = {
        "schemaVersion": "0.4.0",
        "bundleId": "protocol-bundle:elad_0.4.0",
        "protocolId": "protocol:elad_0.4.0",
        "version": "0.4.0",
        "state": "reference_only",
        "framing": "elad-protocol-bundle-v1",
        "entries": [
            protocol_entry("blueprint.json", "protocol_root", "canonical_json", protocol_files["blueprint.json"]),
            protocol_entry("VERSION", "version_marker", "raw_bytes", protocol_files["VERSION"]),
            protocol_entry("spec/schemas/synthetic.schema.json", "schema", "canonical_json", protocol_files["spec/schemas/synthetic.schema.json"]),
            protocol_entry("spec/registries/synthetic.json", "registry", "canonical_json", protocol_files["spec/registries/synthetic.json"]),
            protocol_entry("tests/synthetic-oracle.json", "conformance_oracle", "canonical_json", protocol_files["tests/synthetic-oracle.json"]),
        ],
    }
    owner = "human:synthetic_owner"
    repository_id = "repo:synthetic_context_fixture"
    core = {
        "schemaVersion": "0.4.0",
        "lockId": "core-lock:synthetic_context_fixture",
        "state": "approved",
        "ownerRepositoryId": repository_id,
        "blueprint": {
            "name": "Evidence-Led Agentic Development",
            "version": "0.4.0",
            "protocolId": "protocol:elad_0.4.0",
            "distributionIdentity": "synthetic:inline_protocol_distribution",
            "sourceCommit": "e" * 40,
            "distributionSha256": "9" * 64,
        },
        "protocolBundle": immutable_reference(bundle["bundleId"], "automation/protocol/protocol-bundle.json", bundle),
        "targetCompatibility": "compatible",
        "approvedBy": owner,
        "approvedAt": "2026-08-22T20:00:00Z",
        "supersedes": None,
    }
    authority = {
        "state": "active",
        "owner": owner,
        "ownerRepositoryId": repository_id,
        "maturityLevel": 1,
        "authorizations": {
            "candidateMutation": False,
            "targetMutation": False,
            "machineEvidenceAcceptance": True,
            "promotion": False,
            "publication": False,
        },
    }
    project = {
        "repositoryId": repository_id,
        "humanOnlyDecisions": [
            {
                "decisionClass": "human-decision-class:execution_boundary",
                "description": "Owner retains the execution-boundary choice.",
                "eligibleOwnerIds": [owner],
            }
        ],
    }
    selector = {
        "kind": "candidate",
        "selector": "receipt_candidate",
        "repositoryId": repository_id,
        "id": "candidate:synthetic_context_fixture",
        "baseHead": "f" * 40,
        "sha256": None,
    }
    decisions = [
        {
            "decisionId": "human-decision:synthetic_read_only_boundary",
            "decisionClass": "human-decision-class:execution_boundary",
            "question": "May the synthetic read-only fixture run?",
            "resolution": {
                "state": "recorded",
                "executionDisposition": "permit",
                "selectedValue": "read_only",
                "rationale": "Synthetic conformance only.",
                "resolvedBy": owner,
                "resolvedAt": "2026-08-22T20:01:00Z",
            },
        }
    ]
    experiment = {
        "experimentId": "experiment:synthetic_context_fixture",
        "description": "One bounded read-only run discriminates the exact identity claim.",
        "claimIds": ["claim:synthetic_context_identity"],
        "attemptCeiling": 1,
        "stopWhen": "all_listed_claims_resolved",
    }
    fallback = [
        {"fallbackId": "fallback:need_context", "triggerState": "NEED_CONTEXT", "requestedNextAction": "supply_context", "ownerRoleId": "role:orchestrator", "description": "Return one bounded delta request.", "requiresFreshPacket": True},
        {"fallbackId": "fallback:evidence_failed", "triggerState": "EVIDENCE_FAILED", "requestedNextAction": "fix_causal_layer", "ownerRoleId": "role:orchestrator", "description": "Correct the first causal layer in a fresh packet.", "requiresFreshPacket": True},
        {"fallbackId": "fallback:out_of_scope", "triggerState": "OUT_OF_SCOPE", "requestedNextAction": "owner_decision", "ownerRoleId": "role:product_authority", "description": "Return scope to the owner.", "requiresFreshPacket": True},
        {"fallbackId": "fallback:escalate", "triggerState": "ESCALATE", "requestedNextAction": "owner_decision", "ownerRoleId": "role:product_authority", "description": "Return the exact unresolved decision.", "requiresFreshPacket": True},
    ]
    delta_policy = {
        "maxRequests": 1,
        "maxEntries": 1,
        "maxAdditionalBytes": 1024,
        "maxAdditionalTokens": 512,
        "allowedPaths": ["docs/optional-context.md"],
    }
    intent_budgets = {"attempts": 1, "toolCalls": 2, "retrievals": 1, "spawns": 0}
    intent = {
        "intentId": "intent:synthetic_context_fixture",
        "state": "accepted",
        "acceptance": {"acceptedBy": owner, "acceptedAt": "2026-08-22T20:02:00Z"},
        "claims": [{"claimId": "claim:synthetic_context_identity", "subject": copy.deepcopy(selector)}],
        "humanOnlyDecisions": copy.deepcopy(decisions),
        "maximumUsefulExperiment": copy.deepcopy(experiment),
        "fallbackPlan": copy.deepcopy(fallback),
        "contextDeltaPolicy": copy.deepcopy(delta_policy),
        "budgets": intent_budgets,
        "stopStates": ["NEED_CONTEXT", "EVIDENCE_FAILED", "OUT_OF_SCOPE", "ESCALATE"],
    }
    packet = {
        "packetId": "packet:synthetic_context_fixture",
        "protocolBundle": immutable_reference(bundle["bundleId"], "automation/protocol/protocol-bundle.json", bundle),
        "coreLock": immutable_reference(core["lockId"], "automation/core.lock.json", core),
        "repository": {
            "repositoryId": repository_id,
            "baseHead": "f" * 40,
            "candidateId": "candidate:synthetic_context_fixture",
        },
        "requestedEffects": ["read"],
        "finalizationCeiling": "read_only",
        "claims": [{"claimId": "claim:synthetic_context_identity", "subject": copy.deepcopy(selector)}],
        "humanOnlyDecisions": copy.deepcopy(decisions),
        "maximumUsefulExperiment": copy.deepcopy(experiment),
        "fallbackPlan": copy.deepcopy(fallback),
        "contextDeltaPolicy": copy.deepcopy(delta_policy),
        "budgets": {
            "contextTokens": 8192,
            "outputTokens": 512,
            "contextWindowTokens": 10000,
            "attempts": 1,
        },
    }
    artifacts: dict[str, bytes] = {
        "docs/source.md": b"bounded source\n",
        "automation/context/source.md": b"bounded source\n",
        "docs/notes.md": b"zero\none\r\ntwo\nthree",
        "automation/context/notes-lines-2-3.md": b"one\r\ntwo\n",
        "automation/prompts/worker.md": b"Review exactly the supplied contract.\n",
        "automation/tools/worker-schema.json": b'{"tools":[]}\n',
    }
    retrieval = {
        "manifestId": "retrieval-manifest:synthetic_context_fixture",
        "state": "frozen",
        "deltaOrdinal": 0,
        "supersedes": None,
        "entries": [
            {
                "entryId": "context-entry:whole_source",
                "role": "frozen_review_subject",
                "freshness": "current_at_base",
                "workerAccess": "prebundled",
                "source": {"repositoryId": repository_id, **raw_descriptor("docs/source.md", artifacts["docs/source.md"])},
                "delivery": {"mode": "whole_file", **raw_descriptor("automation/context/source.md", artifacts["automation/context/source.md"]), "selector": None},
            },
            {
                "entryId": "context-entry:sliced_notes",
                "role": "bounded_supporting_context",
                "freshness": "current_at_base",
                "workerAccess": "prebundled",
                "source": {"repositoryId": repository_id, **raw_descriptor("docs/notes.md", artifacts["docs/notes.md"])},
                "delivery": {
                    "mode": "materialized_utf8_lf_lines_v1",
                    **raw_descriptor("automation/context/notes-lines-2-3.md", artifacts["automation/context/notes-lines-2-3.md"]),
                    "selector": {"startLine": 2, "endLine": 3},
                },
            },
        ],
    }
    artifacts["automation/packets/review.json"] = canonical_json_bytes(packet)
    contract_origins = [
        ("context-segment:prompt", "system", "prompt-template:synthetic", "automation/prompts/worker.md"),
        ("context-segment:packet", "user", packet["packetId"], "automation/packets/review.json"),
        ("context-segment:tools", "tool_schema", "tool-schema:synthetic", "automation/tools/worker-schema.json"),
    ]
    segments: list[dict[str, Any]] = []
    for segment_id, channel, origin_id, path in contract_origins:
        descriptor = raw_descriptor(path, artifacts[path])
        segments.append(
            {
                "ordinal": len(segments),
                "segmentId": segment_id,
                "channel": channel,
                "origin": {"kind": "contract_artifact", "id": origin_id, **descriptor},
                "delivered": copy.deepcopy(descriptor),
            }
        )
    for entry in retrieval["entries"]:
        descriptor = {key: entry["delivery"][key] for key in ("path", "bytes", "sha256")}
        segments.append(
            {
                "ordinal": len(segments),
                "segmentId": f"context-segment:{entry['entryId'].split(':', 1)[1]}",
                "channel": "retrieval",
                "origin": {"kind": "retrieval_entry", "id": entry["entryId"], **descriptor},
                "delivered": copy.deepcopy(descriptor),
            }
        )
    compiled = compile_context(segments, artifacts)
    artifacts["automation/context/model-visible-context.json"] = compiled
    context = {
        "schemaVersion": "0.4.0",
        "bundleId": "context-delivery:synthetic_context_fixture",
        "state": "sealed",
        "protocolBundle": immutable_reference(bundle["bundleId"], "automation/protocol/protocol-bundle.json", bundle),
        "packet": immutable_reference(packet["packetId"], "automation/packets/review.json", packet),
        "retrievalManifest": immutable_reference(retrieval["manifestId"], "automation/retrieval/review.json", retrieval),
        "framing": "elad-model-visible-context-v1",
        "segments": segments,
        "compiledArtifact": raw_descriptor("automation/context/model-visible-context.json", compiled),
        "accounting": {
            "methodId": "context-accounting:synthetic_byte_count_v1",
            "counterToolId": "tool:synthetic_byte_counter",
            "counterRegistryEntrySha256": "A" * 64,
            "inputTokens": len(compiled),
            "outputReserveTokens": packet["budgets"]["outputTokens"],
            "requiredContextTokens": len(compiled) + packet["budgets"]["outputTokens"],
        },
        "createdAt": "2026-08-22T20:03:00Z",
        "supersedes": None,
    }
    receipt = {
        "terminalStatus": "COMPLETE",
        "requestedNextAction": "none",
        "humanOnlyDecisions": copy.deepcopy(decisions),
        "maximumUsefulExperiment": copy.deepcopy(experiment),
        "fallbackPlan": copy.deepcopy(fallback),
        "contextDeltaPolicy": copy.deepcopy(delta_policy),
        "contextDeltaRequest": None,
        "fallbackDisposition": None,
        "coreLock": immutable_reference(core["lockId"], "automation/core.lock.json", core),
        "contextDelivery": immutable_reference(context["bundleId"], "automation/context/review.json", context),
    }
    return {
        "protocolFiles": protocol_files,
        "bundle": bundle,
        "core": core,
        "authority": authority,
        "project": project,
        "intent": intent,
        "packet": packet,
        "retrieval": retrieval,
        "context": context,
        "receipt": receipt,
        "artifacts": artifacts,
    }


def make_valid_need_context(fixture: dict[str, Any]) -> None:
    receipt = fixture["receipt"]
    receipt["terminalStatus"] = "NEED_CONTEXT"
    receipt["requestedNextAction"] = "supply_context"
    receipt["fallbackDisposition"] = {
        "fallbackId": "fallback:need_context",
        "triggerState": "NEED_CONTEXT",
        "requestedNextAction": "supply_context",
    }
    receipt["contextDeltaRequest"] = {
        "requestId": "context-request:synthetic_optional_context",
        "ordinal": 1,
        "reasonClass": "missing_required_source",
        "entries": [
            {
                "repositoryId": fixture["packet"]["repository"]["repositoryId"],
                "path": "docs/optional-context.md",
                "deliveryMode": "whole_file",
                "selector": None,
                "purpose": "Resolve the one explicitly anticipated ambiguity.",
                "maxBytes": 512,
                "maxTokens": 256,
            }
        ],
        "totalMaxBytes": 512,
        "totalMaxTokens": 256,
    }


def apply_mutation(fixture: dict[str, Any], mutation: str) -> None:
    if mutation == "none":
        return
    if mutation == "valid_need_context":
        make_valid_need_context(fixture)
    elif mutation == "draft_intent":
        fixture["intent"]["state"] = "draft"
    elif mutation == "wrong_acceptor":
        fixture["intent"]["acceptance"]["acceptedBy"] = "human:neighbor"
    elif mutation == "open_decision":
        for document in (fixture["intent"], fixture["packet"], fixture["receipt"]):
            document["humanOnlyDecisions"][0]["resolution"]["state"] = "open"
    elif mutation == "denied_decision":
        for document in (fixture["intent"], fixture["packet"], fixture["receipt"]):
            document["humanOnlyDecisions"][0]["resolution"]["executionDisposition"] = "deny"
    elif mutation == "invented_decision_class":
        for document in (fixture["intent"], fixture["packet"], fixture["receipt"]):
            document["humanOnlyDecisions"][0]["decisionClass"] = "human-decision-class:invented"
    elif mutation == "ineligible_decision_owner":
        for document in (fixture["intent"], fixture["packet"], fixture["receipt"]):
            document["humanOnlyDecisions"][0]["resolution"]["resolvedBy"] = "human:neighbor"
    elif mutation == "packet_decision_changed":
        fixture["packet"]["humanOnlyDecisions"][0]["resolution"]["selectedValue"] = "target_write"
    elif mutation == "receipt_decision_changed":
        fixture["receipt"]["humanOnlyDecisions"][0]["resolution"]["rationale"] = "Worker-authored substitution."
    elif mutation in {"invented_selector", "invented_kind", "nonnull_selector_sha"}:
        for document in (fixture["intent"], fixture["packet"]):
            selector = document["claims"][0]["subject"]
            if mutation == "invented_selector":
                selector["selector"] = "invented_selector"
            elif mutation == "invented_kind":
                selector["kind"] = "artifact"
            else:
                selector["sha256"] = "B" * 64
    elif mutation == "source_changed":
        fixture["artifacts"]["docs/source.md"] = b"substituted source\n"
    elif mutation == "whole_delivery_changed":
        fixture["artifacts"]["automation/context/source.md"] = b"substituted delivery\n"
    elif mutation == "slice_wrong":
        fixture["artifacts"]["automation/context/notes-lines-2-3.md"] = b"one\r\nthree"
    elif mutation == "missing_segment":
        fixture["context"]["segments"].pop()
    elif mutation == "reordered_segments":
        fixture["context"]["segments"].reverse()
        for index, segment in enumerate(fixture["context"]["segments"]):
            segment["ordinal"] = index
    elif mutation == "compiled_changed":
        fixture["artifacts"]["automation/context/model-visible-context.json"] += b" "
    elif mutation == "input_tokens_changed":
        fixture["context"]["accounting"]["inputTokens"] += 1
    elif mutation == "context_over_input":
        fixture["packet"]["budgets"]["contextTokens"] = 1
    elif mutation == "context_over_window":
        fixture["packet"]["budgets"]["contextWindowTokens"] = fixture["context"]["accounting"]["requiredContextTokens"] - 1
    elif mutation == "bundle_wrong_packet":
        fixture["context"]["packet"]["id"] = "packet:neighbor"
    elif mutation == "receipt_wrong_context":
        fixture["receipt"]["contextDelivery"]["sha256"] = "C" * 64
    elif mutation == "missing_delta":
        make_valid_need_context(fixture)
        fixture["receipt"]["contextDeltaRequest"] = None
    elif mutation == "delta_on_complete":
        make_valid_need_context(fixture)
        fixture["receipt"]["terminalStatus"] = "COMPLETE"
        fixture["receipt"]["requestedNextAction"] = "none"
        fixture["receipt"]["fallbackDisposition"] = None
    elif mutation in {"delta_path_outside", "delta_over_bytes", "delta_ordinal_two"}:
        make_valid_need_context(fixture)
        request = fixture["receipt"]["contextDeltaRequest"]
        if mutation == "delta_path_outside":
            request["entries"][0]["path"] = "secrets/private.txt"
        elif mutation == "delta_over_bytes":
            request["entries"][0]["maxBytes"] = 2048
            request["totalMaxBytes"] = 2048
        else:
            request["ordinal"] = 2
    elif mutation == "experiment_unknown_claim":
        for document in (fixture["intent"], fixture["packet"], fixture["receipt"]):
            document["maximumUsefulExperiment"]["claimIds"] = ["claim:invented"]
    elif mutation == "experiment_over_attempts":
        for document in (fixture["intent"], fixture["packet"], fixture["receipt"]):
            document["maximumUsefulExperiment"]["attemptCeiling"] = 2
    elif mutation == "missing_fallback":
        for document in (fixture["intent"], fixture["packet"], fixture["receipt"]):
            document["fallbackPlan"] = document["fallbackPlan"][:-1]
    elif mutation == "fallback_changed":
        make_valid_need_context(fixture)
        fixture["receipt"]["fallbackDisposition"]["requestedNextAction"] = "owner_decision"
    elif mutation == "complete_fallback_nonnull":
        fixture["receipt"]["fallbackDisposition"] = {
            "fallbackId": "fallback:need_context",
            "triggerState": "NEED_CONTEXT",
            "requestedNextAction": "supply_context",
        }
    elif mutation == "stopped_fallback_null":
        make_valid_need_context(fixture)
        fixture["receipt"]["fallbackDisposition"] = None
    elif mutation == "stale_core_lock_hash":
        fixture["core"]["protocolBundle"]["sha256"] = "D" * 64
    elif mutation == "cross_repo_lock":
        fixture["core"]["ownerRepositoryId"] = "repo:neighbor"
        reference = immutable_reference(fixture["core"]["lockId"], "automation/core.lock.json", fixture["core"])
        fixture["packet"]["coreLock"] = copy.deepcopy(reference)
        fixture["receipt"]["coreLock"] = copy.deepcopy(reference)
    elif mutation == "approved_placeholder":
        fixture["core"]["blueprint"]["sourceCommit"] = ZERO_COMMIT
    elif mutation == "bundle_self_entry":
        fixture["bundle"]["entries"].append({"path": "protocol-bundle.json", "artifactClass": "protocol_root", "digestMode": "raw_bytes", "bytes": 0, "sha256": sha256(b"")})
        fixture["protocolFiles"]["protocol-bundle.json"] = b""
    elif mutation == "bundle_missing_entry":
        removed = fixture["bundle"]["entries"].pop()
        del fixture["protocolFiles"][removed["path"]]
    elif mutation == "bundle_extra_entry":
        data = b"extra\n"
        fixture["protocolFiles"]["EXTRA"] = data
        fixture["bundle"]["entries"].append(protocol_entry("EXTRA", "version_marker", "raw_bytes", data))
    elif mutation == "bundle_digest_mode_confusion":
        for entry in fixture["bundle"]["entries"]:
            if entry["path"] == "VERSION":
                entry["digestMode"] = "canonical_json"
                break
    elif mutation == "protocol_ref_blueprint":
        fixture["core"]["protocolBundle"]["id"] = "protocol:elad_0.4.0"
        fixture["core"]["protocolBundle"]["path"] = "blueprint.json"
    else:
        raise ValidationError(f"unknown semantic mutation: {mutation}")


def validate_fixture(fixture: dict[str, Any], matrix: dict[int, dict[str, Any]]) -> None:
    expected_protocol_paths = {
        "blueprint.json",
        "VERSION",
        "spec/schemas/synthetic.schema.json",
        "spec/registries/synthetic.json",
        "tests/synthetic-oracle.json",
    }
    validate_protocol_bundle(fixture["bundle"], fixture["protocolFiles"], expected_protocol_paths)
    repository_id = fixture["project"]["repositoryId"]
    owner = fixture["authority"]["owner"]
    validate_core_lock(fixture["core"], fixture["bundle"], repository_id, owner)
    validate_reference(fixture["packet"]["protocolBundle"], fixture["bundle"]["bundleId"], "automation/protocol/protocol-bundle.json", fixture["bundle"], "packet protocol bundle")
    validate_reference(fixture["packet"]["coreLock"], fixture["core"]["lockId"], "automation/core.lock.json", fixture["core"], "packet core lock")
    validate_reference(fixture["receipt"]["coreLock"], fixture["core"]["lockId"], "automation/core.lock.json", fixture["core"], "receipt core lock")
    authority = fixture["authority"]
    true_authorizations = [name for name, value in authority["authorizations"].items() if value]
    validate_maturity_case(
        {
            "level": authority["maturityLevel"],
            "effects": fixture["packet"]["requestedEffects"],
            "finalizationCeiling": fixture["packet"]["finalizationCeiling"],
            "trueAuthorizations": true_authorizations,
        },
        matrix,
    )
    validate_intent_contract(fixture["project"], authority, fixture["intent"], fixture["packet"], fixture["receipt"])
    validate_context_delivery(fixture["context"], fixture["packet"], fixture["retrieval"], fixture["bundle"], fixture["receipt"], fixture["artifacts"])
    validate_delta_and_fallback(fixture["intent"], fixture["packet"], fixture["receipt"])


def main() -> int:
    require(sys.version_info >= (3, 10), "Python 3.10 or newer is required")
    template_count = validate_templates()
    vectors = load_json("tests/context-authority-vectors.json")
    require(vectors.get("schemaVersion") == "0.4.0", "vector version mismatch")
    matrix = validate_maturity_registry(vectors)

    maturity_count = 0
    for case in vectors.get("maturityCases", []):
        passed = True
        try:
            validate_maturity_case(case, matrix)
        except ValidationError:
            passed = False
        require(passed is case.get("valid"), f"maturity vector verdict mismatch: {case.get('id')}")
        maturity_count += 1

    semantic_count = 0
    for case in vectors.get("semanticCases", []):
        fixture = build_fixture()
        apply_mutation(fixture, case.get("mutation"))
        passed = True
        try:
            validate_fixture(fixture, matrix)
        except ValidationError:
            passed = False
        require(passed is case.get("valid"), f"semantic vector verdict mismatch: {case.get('id')}")
        semantic_count += 1

    print(
        "PASS — protocol 0.4 context/authority slice: "
        f"templates={template_count}, maturity_vectors={maturity_count}, "
        f"semantic_vectors={semantic_count}, total_vectors={maturity_count + semantic_count}."
    )
    print("NOTE — synthetic Level-0 conformance only; no real operational authority was created or tested.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, KeyError, TypeError, ValidationError) as exc:
        print(f"FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1)
