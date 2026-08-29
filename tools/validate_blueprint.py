#!/usr/bin/env python3
"""Dependency-free Level 0 conformance checks.

The validator reads only this blueprint repository. A PASS means that the inert
reference contracts, examples, and malicious controls agree. It grants no model,
repository, target, evidence, promotion, publication, or runtime authority.
"""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import itertools
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Iterable


if sys.version_info < (3, 10):
    print("FAIL — Python 3.10 or newer is required.", file=sys.stderr)
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
SHA256_RE = re.compile(r"^[A-F0-9]{64}$")
WRITER_RE = re.compile(r"^writer:[a-z0-9][a-z0-9._-]*$")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
PATH_PATTERN_SOURCE = "spec/schemas/task-packet.schema.json"
FIXTURE_ROOT = "tests/fixtures/continuation-valid"
TRUSTED_CONTINUATION_ANCHOR_SHA256 = "1C59765D0C93ABDED658FA7EA33C8074C9715B3658BD6A77405066AB42D1FC57"
_PATH_RE: re.Pattern[str] | None = None


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _strict_float(text: str) -> float:
    value = float(text)
    require(math.isfinite(value), f"non-finite JSON number: {text}")
    return value


def _strict_constant(text: str) -> None:
    fail(f"non-standard JSON constant: {text}")


def strict_json_load_bytes(data: bytes, label: str, *, require_object: bool = True) -> Any:
    require(not data.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM is forbidden: {label}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"JSON is not UTF-8 in {label}: {exc}")
    try:
        document = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_float=_strict_float,
            parse_constant=_strict_constant,
        )
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {label}: {exc}")
    if require_object:
        require(isinstance(document, dict), f"top-level JSON must be an object: {label}")
    return document


def load_json(relative_path: str) -> dict[str, Any]:
    path = ROOT / relative_path
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        fail(f"missing JSON file: {relative_path}")
    document = strict_json_load_bytes(data, relative_path)
    require(isinstance(document, dict), f"top-level JSON must be an object: {relative_path}")
    return document


def canonical_json_bytes(document: Any) -> bytes:
    return (
        json.dumps(
            document,
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def canonical_sha256(document: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(document)).hexdigest().upper()


def repository_path_regex() -> re.Pattern[str]:
    global _PATH_RE
    if _PATH_RE is None:
        schema = load_json(PATH_PATTERN_SOURCE)
        pattern = schema["$defs"]["repositoryPath"]["pattern"]
        _PATH_RE = re.compile(pattern)
    return _PATH_RE


def is_portable_repository_path(value: str) -> bool:
    return isinstance(value, str) and repository_path_regex().fullmatch(value) is not None


def validate_path_set(values: Iterable[str], label: str) -> None:
    paths = list(values)
    require(all(is_portable_repository_path(path) for path in paths), f"{label} contains a non-portable path")
    require(len(paths) == len(set(paths)), f"{label} contains an exact duplicate path")
    folded = [path.casefold() for path in paths]
    require(len(folded) == len(set(folded)), f"{label} contains a case-fold-colliding path")


def iter_repository_paths(value: Any, key: str | None = None) -> Iterable[str]:
    scalar_path_keys = {"path"}
    array_path_keys = {
        "allowedRoots",
        "allowedExisting",
        "allowedNew",
        "prohibited",
        "changedPaths",
    }
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            if child_key in scalar_path_keys and isinstance(child_value, str):
                yield child_value
            elif child_key in array_path_keys and isinstance(child_value, list):
                yield from (entry for entry in child_value if isinstance(entry, str))
            yield from iter_repository_paths(child_value, child_key)
    elif isinstance(value, list):
        for child in value:
            yield from iter_repository_paths(child, key)


def validate_reference(reference: Any, label: str) -> dict[str, Any]:
    require(isinstance(reference, dict), f"{label} is not an immutable reference object")
    require(
        set(reference) == {"id", "path", "sha256", "schemaVersion"},
        f"{label} immutable-reference fields are incomplete or extra",
    )
    require(isinstance(reference["id"], str) and ":" in reference["id"], f"{label} has an invalid ID")
    require(is_portable_repository_path(reference["path"]), f"{label} has a non-portable path")
    require(SHA256_RE.fullmatch(reference["sha256"]) is not None, f"{label} has an invalid SHA-256")
    require(re.fullmatch(r"^[0-9]+\.[0-9]+\.[0-9]+$", reference["schemaVersion"]) is not None, f"{label} has an invalid schema version")
    return reference


def require_same_reference(left: Any, right: Any, label: str) -> None:
    validate_reference(left, f"{label} left")
    validate_reference(right, f"{label} right")
    require(left == right, f"immutable reference mismatch: {label}")


def require_reference_id(reference: Any, expected_id: Any, label: str) -> None:
    checked = validate_reference(reference, label)
    require(checked["id"] == expected_id, f"{label} ID does not resolve exactly")


def validate_outer_reference(reference: dict[str, Any], document: dict[str, Any], id_field: str, label: str) -> None:
    checked = validate_reference(reference, label)
    require(checked["id"] == document.get(id_field), f"{label} outer-envelope ID mismatch")
    require(checked["schemaVersion"] == document.get("schemaVersion"), f"{label} outer-envelope schema-version mismatch")
    require(checked["sha256"] == canonical_sha256(document), f"{label} outer-envelope digest mismatch")


def resolve_outer_reference(reference: Any, id_field: str, label: str) -> dict[str, Any]:
    checked = validate_reference(reference, label)
    document = load_json(checked["path"])
    validate_outer_reference(checked, document, id_field, label)
    return document


def load_canonical_registries(blueprint: dict[str, Any]) -> dict[str, dict[str, Any]]:
    expected = {
        "roles": ("registryId", "vocabulary:elad_roles_0.3.0"),
        "evidenceClasses": ("registryId", "vocabulary:elad_evidence_classes_0.3.0"),
        "terminalStatuses": ("registryId", "vocabulary:elad_terminal_statuses_0.3.0"),
        "failureClasses": ("registryId", "vocabulary:elad_failure_classes_0.3.0"),
        "maturityCeilings": ("registryId", "vocabulary:elad_maturity_ceilings_0.3.0"),
        "subjectSelectors": ("registryId", "vocabulary:elad_subject_selectors_0.3.0"),
        "taskRigorProfiles": ("registryId", "vocabulary:elad_task_rigor_profiles_0.3.0"),
    }
    bindings = blueprint.get("canonicalRegistries")
    require(isinstance(bindings, dict) and set(bindings) == set(expected), "blueprint canonical-registry bindings are incomplete or extra")
    registries: dict[str, dict[str, Any]] = {}
    for name, (id_field, expected_id) in expected.items():
        document = resolve_outer_reference(bindings[name], id_field, f"canonical registry {name}")
        require(document.get(id_field) == expected_id, f"unexpected canonical registry identity: {name}")
        require(document.get("schemaVersion") == blueprint.get("schemaVersion"), f"canonical registry version mismatch: {name}")
        require(document.get("status") == "reference_only", f"canonical registry is not reference-only: {name}")
        registries[name] = document

    roles = registries["roles"].get("roles", [])
    role_ids = [row.get("id") for row in roles]
    require(len(role_ids) == len(set(role_ids)) and all(isinstance(item, str) for item in role_ids), "canonical role IDs are missing or duplicated")
    for row in roles:
        require(
            set(row) == {"id", "mayMutateCandidate", "mayMutateTarget", "mayPromote", "purpose"},
            f"canonical role row is incomplete or extra: {row.get('id')}",
        )
        require(
            all(isinstance(row.get(field), bool) for field in ("mayMutateCandidate", "mayMutateTarget", "mayPromote")),
            f"canonical role permissions are not Boolean: {row.get('id')}",
        )

    for name, field in (
        ("evidenceClasses", "evidenceClasses"),
        ("terminalStatuses", "terminalStatuses"),
        ("failureClasses", "failureClasses"),
    ):
        values = registries[name].get(field, [])
        require(values and len(values) == len(set(values)) and all(isinstance(item, str) for item in values), f"canonical vocabulary is empty or duplicated: {name}")

    expected_terminals = {"COMPLETE", "NEED_CONTEXT", "EVIDENCE_FAILED", "OUT_OF_SCOPE", "ESCALATE"}
    require(set(registries["terminalStatuses"]["terminalStatuses"]) == expected_terminals, "terminal registry does not define the closed lifecycle domain")
    return registries


def canonical_vocabulary_sets(registries: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    return {
        "roles": {row["id"] for row in registries["roles"]["roles"]},
        "evidenceClasses": set(registries["evidenceClasses"]["evidenceClasses"]),
        "terminalStatuses": set(registries["terminalStatuses"]["terminalStatuses"]),
        "failureClasses": set(registries["failureClasses"]["failureClasses"]),
    }


def validate_canonical_vocabulary_usage(
    documents: Iterable[dict[str, Any]],
    registries: dict[str, dict[str, Any]],
) -> None:
    vocab = canonical_vocabulary_sets(registries)

    def walk(value: Any, key: str | None = None, location: str = "$") -> None:
        if key == "roleId" and isinstance(value, str):
            require(value in vocab["roles"], f"non-canonical role at {location}: {value}")
        elif key == "roles" and isinstance(value, list) and all(isinstance(item, str) for item in value):
            require(set(value).issubset(vocab["roles"]), f"non-canonical role in {location}")
        elif key == "evidenceClass" and isinstance(value, str):
            require(value in vocab["evidenceClasses"], f"non-canonical evidence class at {location}: {value}")
        elif key == "evidenceClasses" and isinstance(value, list) and all(isinstance(item, str) for item in value):
            require(set(value).issubset(vocab["evidenceClasses"]), f"non-canonical evidence class in {location}")
        elif key == "terminalStatus" and isinstance(value, str):
            require(value in vocab["terminalStatuses"], f"non-canonical terminal status at {location}: {value}")
        elif key == "stopStates" and isinstance(value, list) and all(isinstance(item, str) for item in value):
            require(set(value).issubset(vocab["terminalStatuses"] - {"COMPLETE"}), f"non-canonical stop state in {location}")
        elif key == "failureClass" and isinstance(value, str):
            require(value in vocab["failureClasses"], f"non-canonical failure class at {location}: {value}")

        if isinstance(value, dict):
            for child_key, child_value in value.items():
                walk(child_value, child_key, f"{location}.{child_key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, key, f"{location}[{index}]")

    for index, document in enumerate(documents):
        walk(document, location=f"document[{index}]")


def role_permissions(registries: dict[str, dict[str, Any]], role_id: str) -> dict[str, Any]:
    rows = [row for row in registries["roles"]["roles"] if row.get("id") == role_id]
    require(len(rows) == 1, f"role does not resolve in canonical registry: {role_id}")
    return rows[0]


def validate_default_deny(blueprint: dict[str, Any], authority: dict[str, Any]) -> None:
    require(blueprint.get("status") == "reference_only", "blueprint status is not reference_only")
    require(blueprint.get("maturity") == {"level": 0, "name": "Blueprint"}, "blueprint maturity is not Level 0")
    blueprint_authority = blueprint.get("authority", {})
    require(blueprint_authority.get("default") == "deny", "blueprint default is not deny")
    for field in (
        "operational",
        "issuesMutationAuthority",
        "issuesEvidenceAuthority",
        "issuesPromotionAuthority",
        "issuesPublicationAuthority",
    ):
        require(blueprint_authority.get(field) is False, f"blueprint authority field {field} is not false")

    require(authority.get("state") in {"template_inert", "held"}, "authority is not inert or held")
    require(authority.get("maturityLevel") == 0, "authority maturity is not zero")
    authorizations = authority.get("authorizations", {})
    required = {"candidateMutation", "targetMutation", "evidenceAcceptance", "promotion", "publication"}
    require(set(authorizations) == required, "authority authorization fields are incomplete or extra")
    require(not any(authorizations.values()), "authority enables an authorization")


def validate_profile_templates(
    project: dict[str, Any],
    writer: dict[str, Any],
    certificate: dict[str, Any],
    risk_policy: dict[str, Any],
    data_policy: dict[str, Any],
    evidence_policy: dict[str, Any],
    tool_registry: dict[str, Any],
    evaluator_registry: dict[str, Any],
    retrieval_manifest: dict[str, Any],
    evidence_manifest: dict[str, Any],
    packet: dict[str, Any],
    receipt: dict[str, Any],
    human_receipt: dict[str, Any],
) -> None:
    require(project.get("state") == "template_inert", "project profile is not template_inert")
    require(all(item.get("state") == "placeholder" for item in project.get("targetOperations", [])), "project template has a live target operation")

    writer_id = writer.get("profileId")
    require(isinstance(writer_id, str) and WRITER_RE.fullmatch(writer_id) is not None, "writer template ID is not canonical")
    require(writer.get("state") == "unqualified", "writer template is not unqualified")
    require(writer.get("mutationCeiling") == "read_only", "writer template exceeds read-only")
    require(writer.get("executionLocation") in {"cloud", "local", "isolated_local"}, "writer template has no explicit execution location")

    require(certificate.get("state") == "unqualified", "certificate template is not unqualified")
    require_reference_id(certificate.get("writerProfile"), writer_id, "certificate writer profile")
    eligibility = certificate.get("eligibility", {})
    for field in ("roles", "taskFamilies", "riskClasses", "dataClasses", "artifactLanes", "effectClasses", "evidenceClasses"):
        require(eligibility.get(field) == [], f"unqualified certificate has eligibility: {field}")
    require(eligibility.get("mutationCeiling") == "read_only", "certificate template exceeds read-only")
    require(certificate.get("issuedAt") is None and certificate.get("expiresAt") is None, "unqualified certificate has live dates")

    require(risk_policy.get("state") == "template_inert", "risk policy is not template_inert")
    require(data_policy.get("state") == "template_inert", "data policy is not template_inert")
    require(evidence_policy.get("state") == "template_inert", "evidence policy is not template_inert")
    for rule in evidence_policy.get("rules", []):
        require(rule.get("machineDelegation") is False, "evidence policy delegates a claim")
        require(rule.get("eligibleWriterProfiles") == [], "inert evidence policy lists eligible writers")

    require(tool_registry.get("state") == "template_inert", "tool registry is not template_inert")
    require(all(item.get("state") == "placeholder" for item in tool_registry.get("tools", [])), "tool registry contains a live tool")
    require(evaluator_registry.get("state") == "template_inert", "evaluator registry is not template_inert")
    require(all(item.get("state") == "placeholder" for item in evaluator_registry.get("evaluators", [])), "evaluator registry contains a live evaluator")
    require(retrieval_manifest.get("state") == "template_inert", "retrieval manifest is not template_inert")
    require(evidence_manifest.get("state") == "template_inert", "evidence manifest is not template_inert")
    require(evidence_manifest.get("outerEnvelopeRequired") is True, "evidence manifest does not require an outer envelope")
    require(packet.get("state") == "template_inert", "task packet is not template_inert")
    require(receipt.get("terminalStatus") == "OUT_OF_SCOPE", "template receipt does not refuse execution")
    require(receipt.get("finalizationState") == "not_started", "template receipt claims progress")

    require(human_receipt.get("state") == "template_inert", "human receipt template appears recorded")
    require(human_receipt.get("recordedAt") is None, "human receipt template has a recorded time")


def validate_gate_set(gates: dict[str, Any], require_inert: bool = True) -> None:
    gate_items = gates.get("gates")
    require(isinstance(gate_items, list), "gate set does not contain a gate list")
    ids = [item.get("gateId") for item in gate_items]
    require(all(isinstance(gate_id, str) for gate_id in ids), "gate ID is missing")
    require(len(ids) == len(set(ids)), "duplicate gate ID")
    known = set(ids)
    owner = gates.get("ownerRepositoryId")
    graph: dict[str, list[str]] = {}
    for item in gate_items:
        gate_id = item["gateId"]
        require(item.get("ownerRepositoryId") == owner, f"gate owner mismatch: {gate_id}")
        prerequisites = item.get("prerequisites", [])
        require(all(prerequisite in known for prerequisite in prerequisites), f"unknown gate prerequisite: {gate_id}")
        require(gate_id not in prerequisites, f"gate directly depends on itself: {gate_id}")
        graph[gate_id] = prerequisites

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(gate_id: str) -> None:
        if gate_id in visiting:
            fail(f"gate cycle detected at {gate_id}")
        if gate_id in visited:
            return
        visiting.add(gate_id)
        for prerequisite in graph[gate_id]:
            visit(prerequisite)
        visiting.remove(gate_id)
        visited.add(gate_id)

    for gate_id in graph:
        visit(gate_id)

    if require_inert:
        require(gates.get("planningSummaryOnly") is True, "gate template is not planning-only")
        require(gates.get("canonicalForExecution") is False, "gate template claims execution authority")
        require(gates.get("transitionCardsImplemented") is False, "gate template claims implemented transitions")
        require(all(item.get("state") == "unrun" for item in gate_items), "gate template contains a run gate")


def validate_manifest_entries(
    entries: Any,
    label: str,
    *,
    path_key: str = "path",
    id_key: str | None = None,
) -> None:
    require(isinstance(entries, list), f"{label} entries are not an array")
    paths = [entry.get(path_key) for entry in entries]
    require(all(isinstance(path, str) for path in paths), f"{label} entry path is missing")
    validate_path_set(paths, f"{label} paths")
    if id_key is not None:
        ids = [entry.get(id_key) for entry in entries]
        require(all(isinstance(item_id, str) for item_id in ids), f"{label} entry ID is missing")
        require(len(ids) == len(set(ids)), f"{label} contains a duplicate entry ID")


def validate_packet_paths(packet: dict[str, Any]) -> None:
    path_contract = packet.get("paths", {})
    allowed_existing = path_contract.get("allowedExisting", [])
    allowed_new = path_contract.get("allowedNew", [])
    prohibited = path_contract.get("prohibited", [])
    validate_path_set(allowed_existing, "packet allowed-existing paths")
    validate_path_set(allowed_new, "packet allowed-new paths")
    validate_path_set(prohibited, "packet prohibited paths")
    allowed_folded = {path.casefold() for path in allowed_existing + allowed_new}
    prohibited_folded = {path.casefold() for path in prohibited}
    require(not (allowed_folded & prohibited_folded), "packet both allows and prohibits the same path")


def validate_budget_invariants(budgets: dict[str, Any], label: str, *, usage: bool = False) -> None:
    sequential = budgets.get("sequentialToolCalls")
    total = budgets.get("totalToolCalls")
    if usage:
        if sequential is not None and total is not None:
            require(sequential <= total, f"{label} sequential tool calls exceed total tool calls")
    else:
        require(isinstance(sequential, int) and isinstance(total, int), f"{label} tool-call budgets are not integers")
        require(sequential <= total, f"{label} sequential tool-call budget exceeds total tool-call budget")


def validate_budget_ceiling(upper: dict[str, Any], lower: dict[str, Any], label: str) -> None:
    validate_budget_invariants(upper, f"{label} upper")
    validate_budget_invariants(lower, f"{label} lower")
    for field in (
        "contextTokens",
        "outputTokens",
        "retrievals",
        "sequentialToolCalls",
        "totalToolCalls",
        "attempts",
        "spawns",
        "wallSeconds",
    ):
        require(lower.get(field) <= upper.get(field), f"{label} lower budget exceeds upper budget: {field}")

    upper_cost = upper.get("maxCostUsd")
    lower_cost = lower.get("maxCostUsd")
    if upper_cost is None:
        require(lower_cost is None, f"{label} invents a numeric cost ceiling beneath an explicitly unmetered ceiling")
    else:
        require(lower_cost is not None and lower_cost <= upper_cost, f"{label} lower cost budget exceeds or drops the upper cost budget")
    require(
        lower.get("resourceEnvelope") == upper.get("resourceEnvelope"),
        f"{label} resource envelope changed",
    )


def validate_receipt_usage(packet_budgets: dict[str, Any], metrics: dict[str, Any], *, sealed: bool) -> None:
    validate_budget_invariants(packet_budgets, "packet")
    validate_budget_invariants(metrics, "receipt metrics", usage=True)
    for field in (
        "contextTokens",
        "outputTokens",
        "retrievals",
        "sequentialToolCalls",
        "totalToolCalls",
        "attempts",
        "spawns",
        "wallSeconds",
    ):
        usage = metrics.get(field)
        if sealed:
            require(usage is not None, f"sealed receipt omits measured usage: {field}")
        if usage is not None:
            require(usage <= packet_budgets.get(field), f"receipt usage exceeds packet budget: {field}")

    packet_cost = packet_budgets.get("maxCostUsd")
    receipt_cost = metrics.get("costUsd")
    if packet_cost is None:
        require(receipt_cost is None, "receipt asserts cost beneath an explicitly unmetered packet cost ceiling")
    elif sealed:
        require(receipt_cost is not None and receipt_cost <= packet_cost, "sealed receipt cost is absent or over budget")
    elif receipt_cost is not None:
        require(receipt_cost <= packet_cost, "receipt cost exceeds packet budget")
    require(metrics.get("resourceEnvelope") == packet_budgets.get("resourceEnvelope"), "receipt resource envelope differs from packet")


def validate_intent_packet(intent: dict[str, Any], packet: dict[str, Any]) -> None:
    require_reference_id(packet.get("intent"), intent.get("intentId"), "packet intent")
    require(intent.get("riskClass") == packet.get("riskClass"), "intent/packet risk class mismatch")
    require(intent.get("dataClass") == packet.get("dataClass"), "intent/packet data class mismatch")
    require(intent.get("stopStates") == packet.get("stopStates"), "intent/packet stop states differ")

    intent_claims = intent.get("claims", [])
    packet_claims = packet.get("claims", [])
    intent_ids = [claim.get("claimId") for claim in intent_claims]
    packet_ids = [claim.get("claimId") for claim in packet_claims]
    require(len(intent_ids) == len(set(intent_ids)), "intent contains duplicate claims")
    require(len(packet_ids) == len(set(packet_ids)), "packet contains duplicate claims")
    require(intent_ids == packet_ids, "intent/packet claim ordering or identity changed")
    identity_fields = ("claimId", "claimClass", "description", "acceptanceOwner", "evidenceClass", "subject")
    for intent_claim, packet_claim in zip(intent_claims, packet_claims):
        for field in identity_fields:
            require(
                intent_claim.get(field) == packet_claim.get(field),
                f"intent/packet claim field changed: {intent_claim.get('claimId')}:{field}",
            )
        subject = packet_claim.get("subject", {})
        repository = packet.get("repository", {})
        require(subject.get("repositoryId") == repository.get("repositoryId"), f"claim subject repository differs from packet: {packet_claim.get('claimId')}")
        require(subject.get("baseHead") == repository.get("baseHead"), f"claim subject base differs from packet: {packet_claim.get('claimId')}")
        require(subject.get("id") == repository.get("candidateId"), f"claim subject candidate differs from packet: {packet_claim.get('claimId')}")

    intent_budgets = intent.get("budgets", {})
    packet_budgets = packet.get("budgets", {})
    mappings = {
        "attempts": "attempts",
        "toolCalls": "totalToolCalls",
        "retrievals": "retrievals",
        "spawns": "spawns",
    }
    for intent_field, packet_field in mappings.items():
        require(
            packet_budgets.get(packet_field) <= intent_budgets.get(intent_field),
            f"packet exceeds intent budget: {intent_field}",
        )
    validate_budget_invariants(packet_budgets, "packet")


def resolve_claim_subject(selector: dict[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    require(selector.get("selector") == "receipt_candidate", f"unsupported claim subject selector: {selector.get('selector')}")
    candidate = receipt.get("candidate", {})
    require(selector.get("kind") == "candidate", "receipt_candidate selector is not a candidate")
    resolved = {
        "kind": selector.get("kind"),
        "repositoryId": selector.get("repositoryId"),
        "id": candidate.get("candidateId"),
        "baseHead": candidate.get("baseHead"),
        "sha256": candidate.get("candidateSha256"),
    }
    require(selector.get("id") == resolved["id"], "claim subject candidate ID does not resolve")
    require(selector.get("baseHead") == resolved["baseHead"], "claim subject base does not resolve")
    if selector.get("sha256") is not None:
        require(selector.get("sha256") == resolved["sha256"], "claim subject digest does not resolve")
    return resolved


def validate_retrieval_manifest(manifest: dict[str, Any], packet: dict[str, Any]) -> None:
    require_reference_id(packet.get("retrievalManifest"), manifest.get("manifestId"), "packet retrieval manifest")
    require_same_reference(manifest.get("protocolBundle"), packet.get("protocolBundle"), "retrieval protocol")
    subject = manifest.get("subject", {})
    repository = packet.get("repository", {})
    require(subject.get("repositoryId") == repository.get("repositoryId"), "retrieval repository mismatch")
    require(subject.get("baseRef") == repository.get("baseRef"), "retrieval base ref mismatch")
    require(subject.get("baseHead") == repository.get("baseHead"), "retrieval base head mismatch")
    require_same_reference(subject.get("projectProfile"), packet.get("projectProfile"), "retrieval project profile")
    require_same_reference(subject.get("authority"), packet.get("authority"), "retrieval authority")
    require(manifest.get("framing") == "elad-canonical-json-outer-sha256-v1", "retrieval framing mismatch")
    entries = manifest.get("entries", [])
    validate_manifest_entries(entries, "retrieval manifest")
    require(all(entry.get("repositoryId") == subject.get("repositoryId") for entry in entries), "retrieval entry repository mismatch")


def validate_evidence_manifest(
    manifest: dict[str, Any],
    packet: dict[str, Any],
    receipt: dict[str, Any],
) -> None:
    require_reference_id(receipt.get("evidenceManifest"), manifest.get("manifestId"), "receipt evidence manifest")
    require_same_reference(manifest.get("protocolBundle"), packet.get("protocolBundle"), "evidence protocol")
    require(manifest.get("framing") == "elad-canonical-json-outer-sha256-v1", "evidence framing mismatch")
    require(manifest.get("outerEnvelopeRequired") is True, "evidence manifest does not require outer-envelope hashing")
    subject = manifest.get("subject", {})
    candidate = receipt.get("candidate", {})
    require(subject.get("kind") == "candidate", "receipt evidence subject is not a candidate")
    require(subject.get("id") == candidate.get("candidateId"), "evidence candidate ID mismatch")
    require(subject.get("sha256") == candidate.get("candidateSha256"), "evidence candidate digest mismatch")
    require(subject.get("baseHead") == candidate.get("baseHead"), "evidence candidate base mismatch")

    entries = manifest.get("entries", [])
    validate_manifest_entries(entries, "evidence manifest", id_key="evidenceId")
    packet_by_id = {claim.get("claimId"): claim for claim in packet.get("claims", [])}
    receipt_by_id = {claim.get("claimId"): claim for claim in receipt.get("claims", [])}
    for entry in entries:
        claim_ids = entry.get("claimIds", [])
        require(set(claim_ids).issubset(packet_by_id), f"evidence maps to an unknown claim: {entry.get('evidenceId')}")
        for claim_id in claim_ids:
            require(entry.get("evidenceClass") == packet_by_id[claim_id].get("evidenceClass"), f"evidence class relabels claim: {claim_id}")
            require(entry.get("resolvedSubject") == receipt_by_id[claim_id].get("resolvedSubject"), f"evidence subject relabels claim: {claim_id}")


def lifecycle_admitted_by_rules(values: tuple[Any, ...]) -> bool:
    """Derive lifecycle admission without consulting the external allowed-row table."""
    require(len(values) == 7, "lifecycle rules received a tuple with the wrong arity")
    (
        finalization_ceiling,
        terminal_status,
        finalization_state,
        candidate_state,
        claim_aggregate,
        manifest_state,
        next_action,
    ) = values

    if manifest_state != "sealed":
        return False

    if finalization_state == "not_started" and candidate_state == "unchanged":
        return (
            (terminal_status == "NEED_CONTEXT" and claim_aggregate == "N" and next_action == "supply_context")
            or (terminal_status == "OUT_OF_SCOPE" and claim_aggregate == "N" and next_action == "owner_decision")
            or (terminal_status == "ESCALATE" and claim_aggregate in {"N", "I"} and next_action == "owner_decision")
            or (terminal_status == "EVIDENCE_FAILED" and claim_aggregate == "XF" and next_action == "fix_causal_layer")
            or (terminal_status == "EVIDENCE_FAILED" and claim_aggregate == "XH" and next_action == "owner_decision")
        )

    if (
        finalization_state == "candidate_checkpoint"
        and candidate_state == "checkpointed"
        and finalization_ceiling in {"candidate_checkpoint", "finalized_on_candidate"}
    ):
        return (
            (terminal_status == "COMPLETE" and claim_aggregate == "U" and next_action == "independent_verification")
            or (terminal_status == "EVIDENCE_FAILED" and claim_aggregate == "XF" and next_action == "fix_causal_layer")
            or (terminal_status == "EVIDENCE_FAILED" and claim_aggregate == "XH" and next_action == "owner_decision")
            or (terminal_status == "ESCALATE" and claim_aggregate == "I" and next_action == "owner_decision")
        )

    expected_candidate_state = "unchanged" if finalization_ceiling == "read_only" else "checkpointed"
    if finalization_state == "technical_evidence_green" and candidate_state == expected_candidate_state:
        return terminal_status == "COMPLETE" and claim_aggregate == "P" and next_action == "none"

    if finalization_state == "await_external_human_receipt" and candidate_state == expected_candidate_state:
        return terminal_status == "COMPLETE" and claim_aggregate == "M" and next_action == "external_human_review"

    return (
        finalization_ceiling == "finalized_on_candidate"
        and terminal_status == "COMPLETE"
        and finalization_state == "finalized_on_candidate"
        and candidate_state == "finalized"
        and claim_aggregate == "P"
        and next_action == "prepare_promotion"
    )


def load_lifecycle_oracle() -> dict[str, Any]:
    oracle = load_json("tests/receipt-lifecycle-vectors.json")
    dimensions = oracle.get("dimensions", [])
    domains = oracle.get("domains", {})
    require(
        dimensions == [
            "finalizationCeiling",
            "terminalStatus",
            "finalizationState",
            "candidateState",
            "claimAggregate",
            "manifestState",
            "nextAction",
        ],
        "lifecycle oracle dimensions changed",
    )
    require(set(domains) == set(dimensions), "lifecycle oracle domains are incomplete or extra")
    total = math.prod(len(domains[name]) for name in dimensions)
    require(total == oracle.get("crossProduct", {}).get("totalCombinations") == 44100, "lifecycle oracle cross-product count is not 44,100")
    allowed_rows = oracle.get("allowedRows", [])
    require(len(allowed_rows) == oracle.get("crossProduct", {}).get("allowedCombinations") == 33, "lifecycle oracle must contain exactly 33 allowed rows")
    row_ids = [row.get("id") for row in allowed_rows]
    require(len(row_ids) == len(set(row_ids)), "lifecycle oracle contains duplicate row IDs")
    allowed: set[tuple[Any, ...]] = set()
    for row in allowed_rows:
        require(set(row) == {"id", *dimensions}, f"lifecycle row is incomplete or extra: {row.get('id')}")
        values = tuple(row[name] for name in dimensions)
        require(all(row[name] in domains[name] for name in dimensions), f"lifecycle row uses a value outside its domain: {row.get('id')}")
        allowed.add(values)
    require(len(allowed) == 33, "lifecycle oracle contains duplicate admitted tuples")

    admitted = 0
    for values in itertools.product(*(domains[name] for name in dimensions)):
        table_admits = values in allowed
        rules_admit = lifecycle_admitted_by_rules(values)
        require(
            rules_admit is table_admits,
            f"lifecycle rules disagree with the external oracle: {values}; rules={rules_admit}, oracle={table_admits}",
        )
        if rules_admit:
            admitted += 1
    require(admitted == 33, "independent lifecycle rules did not admit exactly 33 of 44,100 combinations")
    oracle["_allowedTuples"] = allowed
    return oracle


def derive_claim_aggregate(receipt: dict[str, Any]) -> str:
    claims = receipt.get("claims", [])
    machine_results = [claim.get("result") for claim in claims if claim.get("acceptanceOwner") == "machine"]
    human_results = [claim.get("result") for claim in claims if claim.get("acceptanceOwner") == "external_human"]
    require(not ("failed" in machine_results and "failed" in human_results), "receipt has simultaneous machine and human failure without a unique aggregate")
    if "failed" in machine_results:
        return "XF"
    if "failed" in human_results:
        return "XH"
    if "inconclusive" in machine_results or "inconclusive" in human_results:
        return "I"
    if all(result == "not_evaluated" for result in machine_results + human_results):
        return "N"
    if any(result == "not_evaluated" for result in machine_results):
        return "U"
    if any(result == "not_evaluated" for result in human_results):
        return "M"
    require(all(result == "passed" for result in machine_results + human_results), "receipt claims do not map to a lifecycle aggregate")
    return "P"


def validate_receipt_lifecycle(
    packet: dict[str, Any],
    receipt: dict[str, Any],
    evidence_manifest: dict[str, Any],
    oracle: dict[str, Any],
) -> None:
    if receipt.get("recordState") == "template_inert":
        return
    require(receipt.get("recordState") == "sealed", "non-template receipt is not sealed")
    values = (
        packet.get("finalizationCeiling"),
        receipt.get("terminalStatus"),
        receipt.get("finalizationState"),
        receipt.get("candidate", {}).get("state"),
        derive_claim_aggregate(receipt),
        evidence_manifest.get("state"),
        receipt.get("requestedNextAction"),
    )
    require(values in oracle["_allowedTuples"], f"worker receipt lifecycle tuple is not admitted: {values}")


def validate_lifecycle_semantic_vectors(oracle: dict[str, Any]) -> tuple[int, int, int]:
    vectors = load_json("tests/lifecycle-semantic-vectors.json")
    require(
        set(vectors) == {"schemaVersion", "vectorSetId", "description", "claimAggregateVectors", "lifecycleVectors"},
        "lifecycle semantic-vector file is incomplete or extra",
    )
    require(vectors.get("schemaVersion") == "0.3.0", "lifecycle semantic vectors use the wrong schema version")
    require(vectors.get("vectorSetId") == "elad-lifecycle-semantics-v1", "unknown lifecycle semantic-vector set")

    claim_vectors = vectors.get("claimAggregateVectors")
    require(isinstance(claim_vectors, list) and len(claim_vectors) == 12, "claim-aggregate vector set must contain exactly 12 cases")
    claim_ids = [vector.get("id") for vector in claim_vectors]
    require(all(isinstance(vector_id, str) and vector_id for vector_id in claim_ids), "claim-aggregate vector ID is missing")
    require(len(claim_ids) == len(set(claim_ids)), "duplicate claim-aggregate vector ID")

    aggregate_domain = set(oracle.get("domains", {}).get("claimAggregate", []))
    observed_aggregates: set[str] = set()
    rejection_count = 0
    for vector in claim_vectors:
        require(set(vector) == {"id", "claims", "expected"}, f"claim-aggregate vector is incomplete or extra: {vector.get('id')}")
        claims = vector.get("claims")
        require(isinstance(claims, list) and claims, f"claim-aggregate vector has no claims: {vector.get('id')}")
        for claim in claims:
            require(isinstance(claim, dict) and set(claim) == {"acceptanceOwner", "result"}, f"claim-aggregate vector has an invalid claim: {vector.get('id')}")
            require(claim.get("acceptanceOwner") in {"machine", "external_human"}, f"claim-aggregate vector has an invalid owner: {vector.get('id')}")
            require(claim.get("result") in {"passed", "failed", "inconclusive", "not_evaluated"}, f"claim-aggregate vector has an invalid result: {vector.get('id')}")

        expected = vector.get("expected")
        require(isinstance(expected, dict) and expected.get("outcome") in {"aggregate", "reject"}, f"claim-aggregate vector has an invalid expected outcome: {vector.get('id')}")
        if expected.get("outcome") == "aggregate":
            require(set(expected) == {"outcome", "aggregate"}, f"claim-aggregate vector expectation is incomplete or extra: {vector.get('id')}")
            require(expected.get("aggregate") in aggregate_domain, f"claim-aggregate vector expects an unknown aggregate: {vector.get('id')}")
        else:
            require(set(expected) == {"outcome"}, f"rejected claim-aggregate vector expectation is incomplete or extra: {vector.get('id')}")

        try:
            actual = derive_claim_aggregate({"claims": claims})
            rejected = False
        except ValidationError:
            actual = None
            rejected = True

        if expected.get("outcome") == "reject":
            require(rejected, f"claim-aggregate vector was not rejected: {vector.get('id')}")
            rejection_count += 1
        else:
            require(not rejected and actual == expected.get("aggregate"), f"claim-aggregate vector mismatch: {vector.get('id')}")
            observed_aggregates.add(actual)

    require(observed_aggregates == aggregate_domain, "claim-aggregate vectors do not cover every aggregate")
    require(rejection_count == 1, "claim-aggregate vectors must contain exactly one ambiguity rejection")

    lifecycle_vectors = vectors.get("lifecycleVectors")
    require(isinstance(lifecycle_vectors, list), "lifecycle-vector set is not an array")
    lifecycle_ids = [vector.get("id") for vector in lifecycle_vectors]
    require(all(isinstance(vector_id, str) and vector_id for vector_id in lifecycle_ids), "lifecycle vector ID is missing")
    require(len(lifecycle_ids) == len(set(lifecycle_ids)), "duplicate lifecycle vector ID")

    dimensions = oracle.get("dimensions", [])
    domains = oracle.get("domains", {})
    allowed = oracle.get("_allowedTuples", set())
    by_id = {vector["id"]: vector for vector in lifecycle_vectors}
    shape_count = 0
    mutation_count = 0
    mutation_fields: set[str] = set()
    seen_lifecycle_tuples: set[tuple[Any, ...]] = set()
    observed_shapes: set[tuple[Any, ...]] = set()
    for vector in lifecycle_vectors:
        kind = vector.get("kind")
        expected_keys = {"id", "kind", "admitted", "tuple"}
        if kind == "single_field_mutation":
            expected_keys |= {"baseVectorId", "mutatedField"}
        require(set(vector) == expected_keys, f"lifecycle vector is incomplete or extra: {vector.get('id')}")
        require(kind in {"shape", "single_field_mutation"}, f"lifecycle vector has an unknown kind: {vector.get('id')}")
        require(isinstance(vector.get("admitted"), bool), f"lifecycle vector has no Boolean verdict: {vector.get('id')}")
        tuple_object = vector.get("tuple")
        require(isinstance(tuple_object, dict) and set(tuple_object) == set(dimensions), f"lifecycle vector tuple fields changed: {vector.get('id')}")
        require(all(tuple_object[name] in domains[name] for name in dimensions), f"lifecycle vector uses a value outside its domain: {vector.get('id')}")
        values = tuple(tuple_object[name] for name in dimensions)
        require(values not in seen_lifecycle_tuples, f"duplicate lifecycle semantic tuple: {vector.get('id')}")
        seen_lifecycle_tuples.add(values)
        require(lifecycle_admitted_by_rules(values) is vector["admitted"], f"lifecycle rules disagree with semantic vector: {vector.get('id')}")
        require((values in allowed) is vector["admitted"], f"external lifecycle table disagrees with semantic vector: {vector.get('id')}")

        if kind == "shape":
            require(vector["admitted"] is True, f"lifecycle shape is not an admitted example: {vector.get('id')}")
            observed_shapes.add(tuple(tuple_object[name] for name in dimensions if name != "finalizationCeiling"))
            shape_count += 1
            continue

        require(vector["admitted"] is False, f"single-field mutation is not a denied example: {vector.get('id')}")
        base = by_id.get(vector.get("baseVectorId"))
        require(base is not None and base.get("kind") == "shape" and base.get("admitted") is True, f"lifecycle mutation has no admitted shape base: {vector.get('id')}")
        mutated_field = vector.get("mutatedField")
        require(mutated_field in dimensions, f"lifecycle mutation names an unknown field: {vector.get('id')}")
        differences = [name for name in dimensions if tuple_object[name] != base["tuple"][name]]
        require(differences == [mutated_field], f"lifecycle mutation does not change exactly its named field: {vector.get('id')}")
        mutation_fields.add(mutated_field)
        mutation_count += 1

    require(shape_count == 15, "lifecycle semantic vectors must contain exactly 15 representative admitted shapes")
    require(mutation_count == 12, "lifecycle semantic vectors must contain exactly 12 single-field denials")
    require(mutation_fields == set(dimensions), "lifecycle mutation vectors do not cover every tuple dimension")
    expected_shapes = {
        tuple(row[name] for name in dimensions if name != "finalizationCeiling")
        for row in oracle.get("allowedRows", [])
    }
    require(observed_shapes == expected_shapes, "lifecycle semantic vectors do not cover every admitted shape")

    post_checkpoint_context = by_id.get("deny-need-context-after-checkpoint")
    require(
        post_checkpoint_context is not None
        and post_checkpoint_context.get("admitted") is False
        and post_checkpoint_context.get("tuple", {}).get("terminalStatus") == "NEED_CONTEXT"
        and post_checkpoint_context.get("tuple", {}).get("candidateState") == "checkpointed",
        "unproven post-checkpoint NEED_CONTEXT state is not preserved as denied",
    )
    return len(claim_vectors), shape_count, mutation_count


def reconcile_packet_receipt(
    packet: dict[str, Any],
    receipt: dict[str, Any],
    evidence_manifest: dict[str, Any],
    *,
    intent: dict[str, Any] | None = None,
    authority: dict[str, Any] | None = None,
    human_receipts: dict[str, dict[str, Any]] | None = None,
    lifecycle_oracle: dict[str, Any] | None = None,
    authenticate_packet_reference: bool = False,
) -> None:
    packet_reference = receipt.get("packet")
    require_reference_id(packet_reference, packet.get("packetId"), "receipt packet")
    if authenticate_packet_reference:
        validate_outer_reference(packet_reference, packet, "packetId", "receipt packet")
    if intent is not None:
        validate_intent_packet(intent, packet)

    bindings = receipt.get("bindings", {})
    binding_pairs = (
        ("protocolBundle", packet.get("protocolBundle")),
        ("intent", packet.get("intent")),
        ("projectProfile", packet.get("projectProfile")),
        ("authority", packet.get("authority")),
        ("riskPolicy", packet.get("policyBindings", {}).get("risk")),
        ("dataPolicy", packet.get("policyBindings", {}).get("data")),
        ("evidencePolicy", packet.get("policyBindings", {}).get("evidence")),
        ("toolRegistry", packet.get("toolRegistry")),
        ("evaluatorRegistry", packet.get("evaluatorRegistry")),
    )
    for receipt_name, packet_reference_value in binding_pairs:
        require_same_reference(bindings.get(receipt_name), packet_reference_value, f"packet/receipt binding {receipt_name}")

    for field in ("riskClass", "dataClass", "taskFamily", "artifactLane", "requestedEffects"):
        require(receipt.get(field) == packet.get(field), f"packet/receipt mismatch: {field}")

    require_same_reference(receipt.get("writer", {}).get("profile"), packet.get("writer", {}).get("profile"), "packet/receipt writer profile")
    require_same_reference(receipt.get("writer", {}).get("certificate"), packet.get("writer", {}).get("certificate"), "packet/receipt certificate")

    packet_repository = packet.get("repository", {})
    receipt_candidate = receipt.get("candidate", {})
    require(receipt_candidate.get("candidateId") == packet_repository.get("candidateId"), "candidate ID mismatch")
    require(receipt_candidate.get("baseHead") == packet_repository.get("baseHead"), "candidate base mismatch")

    packet_claims = packet.get("claims", [])
    receipt_claims = receipt.get("claims", [])
    packet_ids = [item.get("claimId") for item in packet_claims]
    receipt_ids = [item.get("claimId") for item in receipt_claims]
    require(all(count == 1 for count in Counter(packet_ids).values()), "duplicate packet claim")
    require(all(count == 1 for count in Counter(receipt_ids).values()), "duplicate receipt claim")
    require(set(packet_ids) == set(receipt_ids) and len(packet_ids) == len(receipt_ids), "packet/receipt claims do not reconcile exactly")

    packet_by_id = {item["claimId"]: item for item in packet_claims}
    evidence_entries = evidence_manifest.get("entries", [])
    evidence_by_id = {item["evidenceId"]: item for item in evidence_entries}
    open_human = receipt.get("openHumanClaims", [])
    require(len(open_human) == len(set(open_human)), "duplicate open human claim")

    expected_open_human: list[str] = []
    for result in receipt_claims:
        claim_id = result["claimId"]
        packet_claim = packet_by_id[claim_id]
        owner = packet_claim.get("acceptanceOwner")
        require(result.get("acceptanceOwner") == owner, f"claim owner changed: {claim_id}")
        require(result.get("claimClass") == packet_claim.get("claimClass"), f"claim class changed: {claim_id}")
        require(result.get("evidenceClass") == packet_claim.get("evidenceClass"), f"claim evidence class changed: {claim_id}")
        require(result.get("resolvedSubject") == resolve_claim_subject(packet_claim.get("subject", {}), receipt), f"claim subject did not resolve exactly: {claim_id}")
        refs = result.get("evidenceRefs", [])
        require(len(refs) == len(set(refs)), f"duplicate evidence reference: {claim_id}")
        require(all(ref in evidence_by_id for ref in refs), f"claim references unknown evidence: {claim_id}")
        for evidence_id in refs:
            require(claim_id in evidence_by_id[evidence_id].get("claimIds", []), f"evidence is not bound to its referencing claim: {claim_id}")

        external_receipt = result.get("externalHumanReceipt")
        if owner == "machine":
            require(external_receipt is None, f"machine claim carries a human receipt: {claim_id}")
            if result.get("result") == "not_evaluated":
                require(refs == [], f"unevaluated machine claim asserts evidence: {claim_id}")
            else:
                require(len(refs) > 0, f"evaluated machine claim lacks evidence: {claim_id}")
        elif external_receipt is None:
            expected_open_human.append(claim_id)
            require(result.get("result") == "not_evaluated", f"open human claim asserts a result: {claim_id}")
            require(refs == [], f"open human claim asserts machine evidence: {claim_id}")
        else:
            validate_reference(external_receipt, f"external human receipt for {claim_id}")
            require(result.get("result") in {"passed", "failed", "inconclusive"}, f"closed human claim has no result: {claim_id}")
            require(human_receipts is not None and external_receipt.get("id") in human_receipts, f"external human receipt payload is unavailable: {claim_id}")
            human_document = human_receipts[external_receipt["id"]]
            validate_outer_reference(external_receipt, human_document, "receiptId", f"external human receipt for {claim_id}")
            require(human_document.get("claimId") == claim_id, f"human receipt closes the wrong claim: {claim_id}")
            require(human_document.get("claimClass") == packet_claim.get("claimClass"), f"human receipt relabels claim class: {claim_id}")
            require(human_document.get("evidenceClass") == packet_claim.get("evidenceClass"), f"human receipt relabels evidence class: {claim_id}")
            require(human_document.get("candidate", {}).get("candidateId") == receipt_candidate.get("candidateId"), f"human receipt candidate ID mismatch: {claim_id}")
            require(human_document.get("candidate", {}).get("candidateSha256") == receipt_candidate.get("candidateSha256"), f"human receipt candidate digest mismatch: {claim_id}")
            require(human_document.get("resolvedSubject") == result.get("resolvedSubject"), f"human receipt subject mismatch: {claim_id}")
            expected_result = {"accepted": "passed", "rejected": "failed", "inconclusive": "inconclusive"}[human_document.get("decision")]
            require(result.get("result") == expected_result, f"human receipt decision/result mismatch: {claim_id}")

    require(set(open_human) == set(expected_open_human), "open human claim list does not match claim results")
    finalization = receipt.get("finalizationState")
    if finalization in {"technical_evidence_green", "await_external_human_receipt", "finalized_on_candidate"}:
        require(authority is not None and authority.get("authorizations", {}).get("evidenceAcceptance") is True, "green or accepted closure lacks evidence-acceptance authority")

    validate_packet_paths(packet)
    changed_paths = receipt.get("changedPaths", [])
    validate_path_set(changed_paths, "receipt changed paths")
    allowed_paths = set(packet.get("paths", {}).get("allowedExisting", [])) | set(packet.get("paths", {}).get("allowedNew", []))
    require(set(changed_paths).issubset(allowed_paths), "receipt contains an unauthorized changed path")
    validate_receipt_usage(packet.get("budgets", {}), receipt.get("metrics", {}), sealed=receipt.get("recordState") == "sealed")
    validate_evidence_manifest(evidence_manifest, packet, receipt)
    if lifecycle_oracle is not None:
        validate_receipt_lifecycle(packet, receipt, evidence_manifest, lifecycle_oracle)


def validate_writer_chain(
    writer: dict[str, Any],
    certificate: dict[str, Any],
    packet: dict[str, Any],
    receipt: dict[str, Any],
) -> None:
    canonical = writer.get("profileId")
    require(isinstance(canonical, str) and WRITER_RE.fullmatch(canonical) is not None, "writer profile ID is invalid")
    require_reference_id(certificate.get("writerProfile"), canonical, "certificate writer")
    require_same_reference(certificate.get("writerProfile"), packet.get("writer", {}).get("profile"), "certificate/packet writer")
    require_same_reference(certificate.get("writerProfile"), receipt.get("writer", {}).get("profile"), "certificate/receipt writer")
    require_reference_id(packet.get("writer", {}).get("certificate"), certificate.get("certificateId"), "packet certificate")
    require_same_reference(packet.get("writer", {}).get("certificate"), receipt.get("writer", {}).get("certificate"), "packet/receipt certificate")


def validate_packet_bindings(
    project: dict[str, Any],
    writer: dict[str, Any],
    certificate: dict[str, Any],
    authority: dict[str, Any],
    risk_policy: dict[str, Any],
    data_policy: dict[str, Any],
    evidence_policy: dict[str, Any],
    tool_registry: dict[str, Any],
    evaluator_registry: dict[str, Any],
    retrieval_manifest: dict[str, Any],
    packet: dict[str, Any],
) -> None:
    repository_id = project.get("repositoryId")
    require(packet.get("repository", {}).get("repositoryId") == repository_id, "packet repository does not match project profile")
    require(authority.get("ownerRepositoryId") == repository_id, "authority owner repository does not match project")
    require(evidence_policy.get("ownerRepositoryId") == repository_id, "evidence-policy owner repository does not match project")
    require(tool_registry.get("ownerRepositoryId") == repository_id, "tool-registry owner repository does not match project")
    require(evaluator_registry.get("ownerRepositoryId") == repository_id, "evaluator-registry owner repository does not match project")
    require_reference_id(packet.get("projectProfile"), project.get("profileId"), "packet project profile")
    require_reference_id(packet.get("authority"), authority.get("authorityId"), "packet authority")
    require_reference_id(packet.get("policyBindings", {}).get("risk"), risk_policy.get("policyId"), "packet risk policy")
    require_reference_id(packet.get("policyBindings", {}).get("data"), data_policy.get("policyId"), "packet data policy")
    require_reference_id(packet.get("policyBindings", {}).get("evidence"), evidence_policy.get("policyId"), "packet evidence policy")
    require_reference_id(packet.get("toolRegistry"), tool_registry.get("registryId"), "packet tool registry")
    require_reference_id(packet.get("evaluatorRegistry"), evaluator_registry.get("registryId"), "packet evaluator registry")

    require_same_reference(project.get("protocolBundle"), packet.get("protocolBundle"), "project/packet protocol")
    require_same_reference(writer.get("identityBindings", {}).get("protocolBundle"), packet.get("protocolBundle"), "writer/packet protocol")
    require_same_reference(certificate.get("protocolBundle"), packet.get("protocolBundle"), "certificate/packet protocol")
    require_same_reference(project.get("authority"), packet.get("authority"), "project/packet authority")
    require_same_reference(project.get("policyBindings", {}).get("risk"), packet.get("policyBindings", {}).get("risk"), "project/packet risk policy")
    require_same_reference(project.get("policyBindings", {}).get("data"), packet.get("policyBindings", {}).get("data"), "project/packet data policy")
    require_same_reference(project.get("policyBindings", {}).get("evidence"), packet.get("policyBindings", {}).get("evidence"), "project/packet evidence policy")
    require_same_reference(project.get("policyBindings", {}).get("toolRegistry"), packet.get("toolRegistry"), "project/packet tool registry")
    require_same_reference(project.get("policyBindings", {}).get("evaluatorRegistry"), packet.get("evaluatorRegistry"), "project/packet evaluator registry")
    require_same_reference(certificate.get("toolRegistry"), packet.get("toolRegistry"), "certificate/packet tool registry")
    require_same_reference(certificate.get("evaluatorRegistry"), packet.get("evaluatorRegistry"), "certificate/packet evaluator registry")
    require_same_reference(tool_registry.get("protocolBundle"), packet.get("protocolBundle"), "tool-registry/packet protocol")
    require_same_reference(evaluator_registry.get("protocolBundle"), packet.get("protocolBundle"), "evaluator-registry/packet protocol")
    require_same_reference(certificate.get("writerProfile"), packet.get("writer", {}).get("profile"), "certificate/packet writer profile")
    require_reference_id(certificate.get("writerProfile"), writer.get("profileId"), "certificate writer profile")
    require_reference_id(packet.get("writer", {}).get("certificate"), certificate.get("certificateId"), "packet certificate")
    validate_retrieval_manifest(retrieval_manifest, packet)


def validate_budget_subset(packet_budgets: dict[str, Any], measured: dict[str, Any]) -> None:
    validate_budget_ceiling(measured, packet_budgets, "certificate/packet")


def path_is_within_roots(path: str, roots: list[str]) -> bool:
    folded = path.casefold()
    return any(folded == root.casefold() or folded.startswith(root.casefold() + "/") for root in roots)


def validate_operational_admission(
    project: dict[str, Any],
    writer: dict[str, Any],
    certificate: dict[str, Any],
    authority: dict[str, Any],
    risk_policy: dict[str, Any],
    data_policy: dict[str, Any],
    evidence_policy: dict[str, Any],
    tool_registry: dict[str, Any],
    evaluator_registry: dict[str, Any],
    retrieval_manifest: dict[str, Any],
    packet: dict[str, Any],
    *,
    intent: dict[str, Any] | None = None,
    registries: dict[str, dict[str, Any]] | None = None,
    expected_repository_id: str | None = None,
) -> None:
    if intent is None:
        intent_path = validate_reference(packet.get("intent"), "packet intent")["path"]
        intent = load_json(intent_path)
    repository_registries = load_canonical_registries(load_json("blueprint.json"))
    if registries is not None:
        require(registries == repository_registries, "caller substituted a coordinated non-canonical vocabulary bundle")
    registries = repository_registries
    validate_packet_bindings(
        project,
        writer,
        certificate,
        authority,
        risk_policy,
        data_policy,
        evidence_policy,
        tool_registry,
        evaluator_registry,
        retrieval_manifest,
        packet,
    )
    validate_intent_packet(intent, packet)
    validate_packet_paths(packet)
    if expected_repository_id is not None:
        require(project.get("repositoryId") == expected_repository_id, "coordinated repository substitution escaped the trusted repository identity")

    require(project.get("state") == "active", "project profile is not active")
    require(authority.get("state") == "active", "authority is not active")
    require(authority.get("maturityLevel", 0) > 0, "authority has no activated maturity level")
    require(writer.get("state") in {"qualified", "candidate_only"}, "writer is not qualified for operational admission")
    require(certificate.get("state") in {"qualified", "candidate_only"}, "certificate is not qualified")
    require(packet.get("state") == "admitted", "packet is not admitted")
    require(risk_policy.get("state") == "active", "risk policy is not active")
    require(data_policy.get("state") == "active", "data policy is not active")
    require(evidence_policy.get("state") == "active", "evidence policy is not active")
    require(tool_registry.get("state") == "active", "tool registry is not active")
    require(evaluator_registry.get("state") == "active", "evaluator registry is not active")
    require(retrieval_manifest.get("state") == "frozen", "retrieval manifest is not frozen")

    model_subject = writer.get("modelSubject", {})
    require(
        model_subject.get("id") not in {None, "", "model:replace_with_exact_subject"}
        and model_subject.get("revision") not in {None, "", "unqualified-template", "no-qualification-run"},
        "writer model subject is not exact",
    )
    if writer.get("executionLocation") in {"local", "isolated_local"}:
        require(
            isinstance(model_subject.get("artifactSha256"), str)
            and SHA256_RE.fullmatch(model_subject["artifactSha256"]) is not None,
            "local writer model bytes are not hash-bound",
        )

    evaluation_pack = certificate.get("evaluationPack", {})
    for field in ("positiveCases", "negativeCases", "holdoutCases", "coldRuns"):
        require(evaluation_pack.get(field, 0) > 0, f"qualified certificate has no measured evaluation coverage: {field}")
    try:
        issued_at = dt.datetime.fromisoformat(certificate["issuedAt"].replace("Z", "+00:00"))
        expires_at = dt.datetime.fromisoformat(certificate["expiresAt"].replace("Z", "+00:00"))
    except (AttributeError, KeyError, ValueError):
        fail("qualified certificate has invalid issuance or expiry")
    now = dt.datetime.now(dt.timezone.utc)
    require(issued_at <= now < expires_at, "qualified certificate is not currently valid")

    eligibility = certificate.get("eligibility", {})
    role_id = packet.get("writer", {}).get("roleId")
    permissions = role_permissions(registries, role_id)
    require(role_id in writer.get("roles", []), "packet role is absent from writer profile")
    require(role_id in eligibility.get("roles", []), "packet role is outside certificate eligibility")
    require(packet.get("taskFamily") in eligibility.get("taskFamilies", []), "packet task family is outside certificate eligibility")
    require(packet.get("riskClass") in eligibility.get("riskClasses", []), "packet risk class is outside certificate eligibility")
    require(packet.get("dataClass") in eligibility.get("dataClasses", []), "packet data class is outside certificate eligibility")
    require(packet.get("artifactLane") in project.get("artifactLanes", []), "packet artifact lane is outside project profile")
    require(packet.get("artifactLane") in eligibility.get("artifactLanes", []), "packet artifact lane is outside certificate eligibility")
    require(set(packet.get("requestedEffects", [])).issubset(set(eligibility.get("effectClasses", []))), "packet effect is outside certificate eligibility")
    machine_evidence_classes = {
        claim.get("evidenceClass")
        for claim in packet.get("claims", [])
        if claim.get("acceptanceOwner") == "machine"
    }
    require(machine_evidence_classes.issubset(set(eligibility.get("evidenceClasses", []))), "machine claim evidence class is outside certificate eligibility")
    vocabulary = canonical_vocabulary_sets(registries)
    require(set(writer.get("roles", [])).issubset(vocabulary["roles"]), "writer profile invents a role")
    require(set(eligibility.get("roles", [])).issubset(vocabulary["roles"]), "certificate invents a role")
    require(set(eligibility.get("evidenceClasses", [])).issubset(vocabulary["evidenceClasses"]), "certificate invents an evidence class")
    require(all(claim.get("evidenceClass") in vocabulary["evidenceClasses"] for claim in packet.get("claims", [])), "packet invents an evidence class")
    requested_effects = set(packet.get("requestedEffects", []))
    if "candidate_write" in requested_effects:
        require(permissions.get("mayMutateCandidate") is True, "canonical role may not mutate a candidate")
    if requested_effects & {"target_native_write", "runtime_process", "data_write"}:
        require(permissions.get("mayMutateTarget") is True, "canonical role may not mutate a target")

    allowed_by_ceiling = {
        "read_only": {"read"},
        "candidate_only": {"read", "candidate_write"},
        "target_operation": {"read", "candidate_write", "target_native_write", "runtime_process", "data_write"},
    }
    require(set(packet.get("requestedEffects", [])).issubset(allowed_by_ceiling.get(eligibility.get("mutationCeiling"), set())), "packet exceeds certificate mutation ceiling")
    require(set(packet.get("requestedEffects", [])).issubset(allowed_by_ceiling.get(writer.get("mutationCeiling"), set())), "packet exceeds writer mutation ceiling")
    validate_budget_ceiling(writer.get("configuredBudgets", {}), certificate.get("measuredSafeBudgets", {}), "writer/certificate")
    validate_budget_subset(packet.get("budgets", {}), certificate.get("measuredSafeBudgets", {}))

    risk_rows = [row for row in risk_policy.get("classes", []) if row.get("riskClass") == packet.get("riskClass")]
    require(len(risk_rows) == 1, "packet risk class does not resolve uniquely")
    require(set(packet.get("requestedEffects", [])).issubset(set(risk_rows[0].get("allowedEffects", []))), "packet effect is disallowed by risk policy")
    require(risk_rows[0].get("requiresHumanDecision") is False, "risk policy requires an unrecorded human decision")

    data_rows = [row for row in data_policy.get("classes", []) if row.get("dataClass") == packet.get("dataClass")]
    require(len(data_rows) == 1, "packet data class does not resolve uniquely")
    require(writer.get("executionLocation") in data_rows[0].get("allowedExecutionLocations", []), "writer execution location is disallowed by data policy")

    allowed_roots = project.get("allowedRoots", [])
    validate_path_set(allowed_roots, "project allowed roots")
    scoped_paths = packet.get("paths", {}).get("allowedExisting", []) + packet.get("paths", {}).get("allowedNew", [])
    require(all(path_is_within_roots(path, allowed_roots) for path in scoped_paths), "packet path is outside project roots")

    active_operation_effects = {
        effect
        for operation in project.get("targetOperations", [])
        if operation.get("state") == "active"
        for effect in operation.get("effects", [])
    }
    require(set(packet.get("requestedEffects", [])).issubset(active_operation_effects), "packet requests an inactive project operation")

    authorizations = authority.get("authorizations", {})
    requested = set(packet.get("requestedEffects", []))
    if "candidate_write" in requested:
        require(authorizations.get("candidateMutation") is True, "candidate mutation is not authorized")
    if requested & {"target_native_write", "runtime_process", "data_write"}:
        require(authorizations.get("targetMutation") is True, "target mutation is not authorized")
    if any(claim.get("acceptanceOwner") == "machine" for claim in packet.get("claims", [])):
        require(authorizations.get("evidenceAcceptance") is True, "machine operational admission lacks evidence-acceptance authority")

    tool_entries = tool_registry.get("tools", [])
    require(len([entry.get("toolId") for entry in tool_entries]) == len(set(entry.get("toolId") for entry in tool_entries)), "tool registry has duplicate IDs")
    tools_by_id = {entry["toolId"]: entry for entry in tool_entries}
    for requested_tool in packet.get("tools", []):
        tool_id = requested_tool.get("toolId")
        require(tool_id in tools_by_id, f"packet tool is absent from the bound registry: {tool_id}")
        registry_tool = tools_by_id[tool_id]
        require(registry_tool.get("state") == "active", f"packet tool is inactive: {tool_id}")
        require(requested_tool.get("registryEntrySha256") == registry_tool.get("entrySha256"), f"packet tool entry digest mismatch: {tool_id}")
        require(requested_tool.get("effect") == registry_tool.get("effect"), f"packet tool effect mismatch: {tool_id}")
        require(requested_tool.get("effect") in requested, f"packet tool effect was not requested: {tool_id}")

    evaluator_entries = evaluator_registry.get("evaluators", [])
    require(len([entry.get("evaluatorId") for entry in evaluator_entries]) == len(set(entry.get("evaluatorId") for entry in evaluator_entries)), "evaluator registry has duplicate IDs")
    evaluators_by_id = {entry["evaluatorId"]: entry for entry in evaluator_entries}
    evidence_rules = evidence_policy.get("rules", [])
    for claim in packet.get("claims", []):
        evaluator_id = claim.get("evaluatorId")
        require(evaluator_id in evaluators_by_id, f"claim evaluator is absent from the bound registry: {evaluator_id}")
        evaluator = evaluators_by_id[evaluator_id]
        require(evaluator.get("state") == "calibrated", f"claim evaluator is not calibrated: {evaluator_id}")
        require(packet.get("taskFamily") in evaluator.get("taskFamilies", []), f"evaluator is not eligible for task family: {evaluator_id}")
        require(claim.get("evidenceClass") in evaluator.get("evidenceClasses", []), f"evaluator is not eligible for evidence class: {evaluator_id}")
        require(claim.get("negativeControlId") in evaluator.get("negativeControlIds", []), f"claim negative control is not registered: {evaluator_id}")

        matching_rules = [
            rule
            for rule in evidence_rules
            if rule.get("claimClass") == claim.get("claimClass")
            and rule.get("evidenceClass") == claim.get("evidenceClass")
            and rule.get("acceptanceOwner") == claim.get("acceptanceOwner")
            and rule.get("evaluatorId") == evaluator_id
        ]
        require(len(matching_rules) == 1, f"claim evidence rule does not resolve uniquely: {claim.get('claimId')}")
        rule = matching_rules[0]
        if claim.get("acceptanceOwner") == "machine":
            require(rule.get("machineDelegation") is True, f"machine claim is not delegated: {claim.get('claimId')}")
            require(writer.get("profileId") in rule.get("eligibleWriterProfiles", []), f"writer is ineligible for machine claim: {claim.get('claimId')}")


def validate_manifest_bytes(manifest: dict[str, Any], files: dict[str, bytes], label: str) -> None:
    entries = manifest.get("entries", [])
    validate_manifest_entries(entries, label, id_key="evidenceId" if entries and "evidenceId" in entries[0] else None)
    expected_paths = {entry["path"] for entry in entries}
    require(set(files) == expected_paths, f"{label} file set is missing or extra")
    for entry in entries:
        payload = files[entry["path"]]
        require(len(payload) == entry.get("bytes"), f"{label} byte count mismatch: {entry['path']}")
        require(hashlib.sha256(payload).hexdigest().upper() == entry.get("sha256"), f"{label} payload digest mismatch: {entry['path']}")


def validate_fresh_context_continuation(
    packet: dict[str, Any],
    receipt: dict[str, Any],
    retrieval_manifest: dict[str, Any],
    evidence_manifest: dict[str, Any],
) -> None:
    validate_retrieval_manifest(retrieval_manifest, packet)
    reconcile_packet_receipt(packet, receipt, evidence_manifest)


def validate_manifest_disk_bytes(manifest: dict[str, Any], label: str) -> set[str]:
    entries = manifest.get("entries", [])
    validate_manifest_entries(
        entries,
        label,
        id_key="evidenceId" if entries and "evidenceId" in entries[0] else ("artifactId" if entries and "artifactId" in entries[0] else None),
    )
    paths: set[str] = set()
    for entry in entries:
        relative = entry["path"]
        require(relative not in paths, f"{label} contains a duplicate raw payload path")
        paths.add(relative)
        path = (ROOT / relative).resolve()
        try:
            path.relative_to(ROOT)
        except ValueError:
            fail(f"{label} raw payload escapes the repository: {relative}")
        require(path.is_file(), f"{label} raw payload is missing: {relative}")
        payload = path.read_bytes()
        require(len(payload) == entry.get("bytes"), f"{label} raw byte count mismatch: {relative}")
        require(hashlib.sha256(payload).hexdigest().upper() == entry.get("sha256"), f"{label} raw digest mismatch: {relative}")
    return paths


def validate_exact_payload_git_attributes(raw_paths: set[str]) -> None:
    """Require raw-byte fixture payloads to survive Git checkout unchanged."""

    attribute_lines = [
        line.strip()
        for line in (ROOT / ".gitattributes").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    expected_tail = [f"{path} -text" for path in sorted(raw_paths)]
    require(
        attribute_lines[-len(expected_tail) :] == expected_tail,
        "exact-byte continuation payloads are not the final explicit -text Git attributes",
    )


def _fixture_path(name: str) -> str:
    return f"{FIXTURE_ROOT}/{name}"


def resolve_fixture_reference(
    reference: Any,
    expected_path: str,
    id_field: str,
    label: str,
) -> dict[str, Any]:
    checked = validate_reference(reference, label)
    require(checked["path"] == expected_path, f"{label} points to a phantom or substituted artifact")
    document = load_json(expected_path)
    validate_outer_reference(checked, document, id_field, label)
    return document


def receipt_candidate_for_review(receipt: dict[str, Any]) -> dict[str, Any]:
    candidate = receipt.get("candidate", {})
    return {
        "candidateState": candidate.get("state"),
        "candidateId": candidate.get("candidateId"),
        "candidateSha256": candidate.get("candidateSha256"),
        "baseHead": candidate.get("baseHead"),
        "head": candidate.get("head"),
    }


def validate_review_and_human_receipt(
    review: dict[str, Any],
    human: dict[str, Any],
    packet: dict[str, Any],
    receipt: dict[str, Any],
    evidence_manifest: dict[str, Any],
    evidence_policy: dict[str, Any],
) -> set[str]:
    require(review.get("state") == "sealed", "continuation review bundle is not sealed")
    require(human.get("state") == "recorded", "continuation human receipt is not recorded")
    require(human.get("recordedAt") is not None, "recorded human receipt has no timestamp")
    require_same_reference(review.get("protocolBundle"), packet.get("protocolBundle"), "review/packet protocol")
    validate_outer_reference(review.get("packet"), packet, "packetId", "review packet")
    validate_outer_reference(review.get("evidenceManifest"), evidence_manifest, "manifestId", "review evidence manifest")
    require(review.get("candidate") == receipt_candidate_for_review(receipt), "review candidate differs from final receipt")
    require_same_reference(human.get("protocolBundle"), packet.get("protocolBundle"), "human/packet protocol")
    validate_outer_reference(human.get("packet"), packet, "packetId", "human receipt packet")
    validate_outer_reference(human.get("reviewBundle"), review, "bundleId", "human receipt review bundle")
    require(human.get("candidate") == receipt_candidate_for_review(receipt), "human receipt candidate differs from final receipt")

    packet_claims = {claim["claimId"]: claim for claim in packet.get("claims", [])}
    claim_id = human.get("claimId")
    require(claim_id in packet_claims, "human receipt closes an unknown claim")
    claim = packet_claims[claim_id]
    require(claim.get("acceptanceOwner") == "external_human", "human receipt closes a machine claim")
    require(human.get("claimClass") == claim.get("claimClass"), "human receipt changes claim class")
    require(human.get("evidenceClass") == claim.get("evidenceClass"), "human receipt changes evidence class")
    expected_subject = resolve_claim_subject(claim.get("subject", {}), receipt)
    require(human.get("resolvedSubject") == expected_subject, "human receipt changes claim subject")
    require(review.get("resolvedSubject") == expected_subject, "review bundle changes claim subject")
    require(claim_id in review.get("claimIds", []), "review bundle does not cover the human claim")

    rules = [
        rule
        for rule in evidence_policy.get("rules", [])
        if rule.get("claimClass") == claim.get("claimClass")
        and rule.get("evidenceClass") == claim.get("evidenceClass")
        and rule.get("acceptanceOwner") == "external_human"
        and rule.get("evaluatorId") == human.get("reviewer", {}).get("evaluatorId")
    ]
    require(len(rules) == 1, "human receipt does not resolve to one evidence-policy rule")
    require(human.get("reviewer", {}).get("reviewerId") in rules[0].get("eligibleReviewerIds", []), "human reviewer is not eligible")
    require(rules[0].get("machineDelegation") is False, "external human policy delegates acceptance to a machine")

    evidence_ids = {entry.get("evidenceId") for entry in evidence_manifest.get("entries", [])}
    for entry in review.get("entries", []):
        require(set(entry.get("evidenceIds", [])).issubset(evidence_ids), f"review entry references phantom evidence: {entry.get('artifactId')}")
    return validate_manifest_disk_bytes(review, "continuation review bundle")


def validate_exact_byte_continuation(
    blueprint: dict[str, Any],
    registries: dict[str, dict[str, Any]],
    lifecycle_oracle: dict[str, Any],
) -> tuple[int, int]:
    require(
        TRUSTED_CONTINUATION_ANCHOR_SHA256 != "REPLACE_AFTER_FIXTURE_SEAL",
        "continuation fixture exists but its trusted anchor digest has not been sealed into the validator",
    )
    anchor = load_json(_fixture_path("anchor.json"))
    require(canonical_sha256(anchor) == TRUSTED_CONTINUATION_ANCHOR_SHA256, "trusted continuation anchor digest mismatch")
    require(anchor.get("state") == "trusted", "continuation anchor is not trusted")

    final_receipt = resolve_fixture_reference(
        anchor.get("receipt"),
        _fixture_path("receipt.final.json"),
        "receiptId",
        "anchor final receipt",
    )
    await_receipt = resolve_fixture_reference(
        final_receipt.get("supersedes"),
        _fixture_path("receipt.await-human.json"),
        "receiptId",
        "final receipt supersession",
    )
    require(final_receipt.get("receiptId") != await_receipt.get("receiptId"), "receipt supersession is self-referential")

    packet = resolve_fixture_reference(
        final_receipt.get("packet"),
        _fixture_path("packet.json"),
        "packetId",
        "final receipt packet",
    )
    validate_outer_reference(await_receipt.get("packet"), packet, "packetId", "await-human receipt packet")

    expected_bindings = {
        "intent": ("intent.json", "intentId"),
        "projectProfile": ("project-profile.json", "profileId"),
        "authority": ("authority.json", "authorityId"),
        "riskPolicy": ("risk-policy.json", "policyId"),
        "dataPolicy": ("data-policy.json", "policyId"),
        "evidencePolicy": ("evidence-policy.json", "policyId"),
        "toolRegistry": ("tool-registry.json", "registryId"),
        "evaluatorRegistry": ("evaluator-registry.json", "registryId"),
    }
    documents: dict[str, dict[str, Any]] = {}
    for binding_name, (filename, id_field) in expected_bindings.items():
        final_reference = final_receipt.get("bindings", {}).get(binding_name)
        require_same_reference(await_receipt.get("bindings", {}).get(binding_name), final_reference, f"receipt binding continuity {binding_name}")
        documents[binding_name] = resolve_fixture_reference(
            final_reference,
            _fixture_path(filename),
            id_field,
            f"continuation binding {binding_name}",
        )

    protocol_reference = final_receipt.get("bindings", {}).get("protocolBundle")
    require_same_reference(await_receipt.get("bindings", {}).get("protocolBundle"), protocol_reference, "receipt binding continuity protocol")
    validate_outer_reference(protocol_reference, blueprint, "protocolId", "continuation protocol bundle")
    require(protocol_reference.get("path") == "blueprint.json", "continuation protocol points outside the trusted blueprint")

    writer = resolve_fixture_reference(
        final_receipt.get("writer", {}).get("profile"),
        _fixture_path("writer-profile.json"),
        "profileId",
        "continuation writer profile",
    )
    certificate = resolve_fixture_reference(
        final_receipt.get("writer", {}).get("certificate"),
        _fixture_path("capability-certificate.json"),
        "certificateId",
        "continuation capability certificate",
    )
    require_same_reference(await_receipt.get("writer", {}).get("profile"), final_receipt.get("writer", {}).get("profile"), "receipt writer continuity")
    require_same_reference(await_receipt.get("writer", {}).get("certificate"), final_receipt.get("writer", {}).get("certificate"), "receipt certificate continuity")

    retrieval = resolve_fixture_reference(
        packet.get("retrievalManifest"),
        _fixture_path("retrieval-manifest.json"),
        "manifestId",
        "continuation retrieval manifest",
    )
    evidence_manifest = resolve_fixture_reference(
        final_receipt.get("evidenceManifest"),
        _fixture_path("evidence-manifest.json"),
        "manifestId",
        "continuation evidence manifest",
    )
    require_same_reference(await_receipt.get("evidenceManifest"), final_receipt.get("evidenceManifest"), "receipt evidence-manifest continuity")

    human_references = [
        result.get("externalHumanReceipt")
        for result in final_receipt.get("claims", [])
        if result.get("externalHumanReceipt") is not None
    ]
    require(len(human_references) == 1, "final continuation receipt must contain exactly one external human receipt")
    human = resolve_fixture_reference(
        human_references[0],
        _fixture_path("external-human-receipt.json"),
        "receiptId",
        "continuation external human receipt",
    )
    review = resolve_fixture_reference(
        human.get("reviewBundle"),
        _fixture_path("review-bundle.json"),
        "bundleId",
        "continuation review bundle",
    )

    intent = documents["intent"]
    project = documents["projectProfile"]
    authority = documents["authority"]
    evidence_policy = documents["evidencePolicy"]
    require(anchor.get("ownerRepositoryId") == project.get("repositoryId"), "anchor owner repository differs from project")
    validate_packet_bindings(
        project,
        writer,
        certificate,
        authority,
        documents["riskPolicy"],
        documents["dataPolicy"],
        evidence_policy,
        documents["toolRegistry"],
        documents["evaluatorRegistry"],
        retrieval,
        packet,
    )
    validate_intent_packet(intent, packet)
    validate_operational_admission(
        project,
        writer,
        certificate,
        authority,
        documents["riskPolicy"],
        documents["dataPolicy"],
        evidence_policy,
        documents["toolRegistry"],
        documents["evaluatorRegistry"],
        retrieval,
        packet,
        intent=intent,
        registries=registries,
        expected_repository_id=anchor.get("ownerRepositoryId"),
    )

    human_documents = {human["receiptId"]: human}
    reconcile_packet_receipt(
        packet,
        await_receipt,
        evidence_manifest,
        intent=intent,
        authority=authority,
        human_receipts={},
        lifecycle_oracle=lifecycle_oracle,
        authenticate_packet_reference=True,
    )
    reconcile_packet_receipt(
        packet,
        final_receipt,
        evidence_manifest,
        intent=intent,
        authority=authority,
        human_receipts=human_documents,
        lifecycle_oracle=lifecycle_oracle,
        authenticate_packet_reference=True,
    )

    raw_paths = set()
    raw_paths |= validate_manifest_disk_bytes(retrieval, "continuation retrieval manifest")
    raw_paths |= validate_manifest_disk_bytes(evidence_manifest, "continuation evidence manifest")
    raw_paths |= validate_review_and_human_receipt(
        review,
        human,
        packet,
        final_receipt,
        evidence_manifest,
        evidence_policy,
    )
    fixture_directory = ROOT / FIXTURE_ROOT
    actual_raw = {
        path.relative_to(ROOT).as_posix()
        for path in fixture_directory.rglob("*")
        if path.is_file() and path.suffix.lower() != ".json" and path.name != "README.md"
    }
    require(raw_paths == actual_raw, "continuation fixture has missing, extra, or unmanifested raw payloads")
    validate_exact_payload_git_attributes(raw_paths)
    return len(raw_paths), 2


def validate_all_json() -> tuple[list[Path], list[dict[str, Any]]]:
    paths = sorted(path for path in ROOT.rglob("*.json") if ".git" not in path.parts)
    documents: list[dict[str, Any]] = []
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        document = strict_json_load_bytes(path.read_bytes(), relative)
        require(isinstance(document, dict), f"top-level JSON must be an object: {relative}")
        documents.append(document)
    return paths, documents


def validate_schemas(paths: Iterable[Path]) -> int:
    schemas = [path for path in paths if path.parent.name == "schemas"]
    for path in schemas:
        relative = path.relative_to(ROOT).as_posix()
        document = strict_json_load_bytes(path.read_bytes(), relative)
        require(document.get("$schema") == "https://json-schema.org/draft/2020-12/schema", f"wrong schema draft: {relative}")
        require(isinstance(document.get("$id"), str) and document["$id"].startswith("urn:elad:schema:"), f"missing ELAD schema ID: {relative}")
        require(document.get("type") == "object", f"schema top level is not object: {relative}")
        require(document.get("additionalProperties") is False, f"schema does not fail closed on extra top-level properties: {relative}")
        require(isinstance(document.get("required"), list) and document["required"], f"schema lacks required properties: {relative}")
    return len(schemas)


def validate_schema_instance(instance: Any, schema: dict[str, Any], root_schema: dict[str, Any], location: str = "$") -> None:
    """Validate the dependency-free JSON-Schema subset used by Level 0."""

    reference = schema.get("$ref")
    if reference is not None:
        prefix = "#/$defs/"
        require(isinstance(reference, str) and reference.startswith(prefix), f"unsupported schema reference at {location}: {reference!r}")
        definition_name = reference[len(prefix):]
        definitions = root_schema.get("$defs", {})
        require(definition_name in definitions, f"missing schema definition at {location}: {definition_name}")
        validate_schema_instance(instance, definitions[definition_name], root_schema, location)
        return

    if "const" in schema:
        require(instance == schema["const"], f"schema const mismatch at {location}")
    if "enum" in schema:
        require(instance in schema["enum"], f"schema enum mismatch at {location}: {instance!r}")

    declared_type = schema.get("type")
    if declared_type is not None:
        expected_types = declared_type if isinstance(declared_type, list) else [declared_type]

        def matches_type(type_name: str) -> bool:
            if type_name == "null":
                return instance is None
            if type_name == "object":
                return isinstance(instance, dict)
            if type_name == "array":
                return isinstance(instance, list)
            if type_name == "string":
                return isinstance(instance, str)
            if type_name == "boolean":
                return isinstance(instance, bool)
            if type_name == "integer":
                return isinstance(instance, int) and not isinstance(instance, bool)
            if type_name == "number":
                return isinstance(instance, (int, float)) and not isinstance(instance, bool)
            fail(f"unsupported schema type at {location}: {type_name}")
            return False

        require(any(matches_type(type_name) for type_name in expected_types), f"schema type mismatch at {location}: expected {expected_types}, got {type(instance).__name__}")

    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        for property_name in schema.get("required", []):
            require(property_name in instance, f"missing required property at {location}.{property_name}")
        if schema.get("additionalProperties") is False:
            extras = set(instance) - set(properties)
            require(not extras, f"unexpected properties at {location}: {sorted(extras)}")
        for property_name, property_value in instance.items():
            if property_name in properties:
                validate_schema_instance(property_value, properties[property_name], root_schema, f"{location}.{property_name}")

    if isinstance(instance, list):
        if "minItems" in schema:
            require(len(instance) >= schema["minItems"], f"array shorter than minItems at {location}")
        if "maxItems" in schema:
            require(len(instance) <= schema["maxItems"], f"array longer than maxItems at {location}")
        if schema.get("uniqueItems") is True:
            serialized = [json.dumps(item, allow_nan=False, sort_keys=True, separators=(",", ":")) for item in instance]
            require(len(serialized) == len(set(serialized)), f"duplicate array item at {location}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                validate_schema_instance(item, item_schema, root_schema, f"{location}[{index}]")

    if isinstance(instance, str):
        if "minLength" in schema:
            require(len(instance) >= schema["minLength"], f"string shorter than minLength at {location}")
        if "pattern" in schema:
            require(re.search(schema["pattern"], instance) is not None, f"string pattern mismatch at {location}: {instance!r}")
        if schema.get("format") == "date-time":
            try:
                dt.datetime.fromisoformat(instance.replace("Z", "+00:00"))
            except ValueError:
                fail(f"invalid date-time at {location}: {instance!r}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema:
            require(instance >= schema["minimum"], f"number below minimum at {location}")
        if "maximum" in schema:
            require(instance <= schema["maximum"], f"number above maximum at {location}")


def validate_schema_instances() -> int:
    template_pairs = [
        ("templates/active-authority.template.json", "active-authority.schema.json"),
        ("templates/adoption-efficacy-plan.template.json", "adoption-efficacy-plan.schema.json"),
        ("templates/adoption-efficacy-report.template.json", "adoption-efficacy-report.schema.json"),
        ("templates/capability-certificate.template.json", "capability-certificate.schema.json"),
        ("templates/context-delivery.template.json", "context-delivery.schema.json"),
        ("templates/continuation-anchor.template.json", "continuation-anchor.schema.json"),
        ("templates/core.lock.template.json", "core-lock.schema.json"),
        ("templates/data-policy.template.json", "data-policy.schema.json"),
        ("templates/evaluation-pack.template.json", "evaluation-pack.schema.json"),
        ("templates/evaluation-result-manifest.template.json", "evaluation-result-manifest.schema.json"),
        ("templates/evaluator-registry.template.json", "evaluator-registry.schema.json"),
        ("templates/evidence-manifest.template.json", "evidence-manifest.schema.json"),
        ("templates/evidence-policy.template.json", "evidence-policy.schema.json"),
        ("templates/external-human-receipt.template.json", "external-human-receipt.schema.json"),
        ("templates/failure-record.template.json", "failure-record.schema.json"),
        ("templates/gate-set.template.json", "gate-set.schema.json"),
        ("templates/intent-brief.template.json", "intent-brief.schema.json"),
        ("templates/project-profile.template.json", "project-profile.schema.json"),
        ("templates/protocol-bundle.template.json", "protocol-bundle.schema.json"),
        ("templates/resource-envelope.template.json", "resource-envelope.schema.json"),
        ("templates/retrieval-manifest.template.json", "retrieval-manifest.schema.json"),
        ("templates/review-bundle.template.json", "review-bundle.schema.json"),
        ("templates/risk-policy.template.json", "risk-policy.schema.json"),
        ("templates/task-packet.template.json", "task-packet.schema.json"),
        ("templates/task-rigor-decision.template.json", "task-rigor-decision.schema.json"),
        ("templates/tool-registry.template.json", "tool-registry.schema.json"),
        ("templates/typed-reference.template.json", "typed-reference.schema.json"),
        ("templates/worker-receipt.template.json", "worker-receipt.schema.json"),
        ("templates/writer-profile.template.json", "writer-profile.schema.json"),
    ]
    require(len(template_pairs) == 29, "every normative 0.3.0 schema must have one template pair")
    require(
        {schema_name for _, schema_name in template_pairs}
        == {path.name for path in (ROOT / "spec" / "schemas").glob("*.schema.json")},
        "template/schema coverage is not exactly one-to-one",
    )

    example_pairs = [
        ("examples/two-repository-product/app.active-authority.json", "active-authority.schema.json"),
        ("examples/two-repository-product/world.active-authority.json", "active-authority.schema.json"),
        ("examples/two-repository-product/world-content.profile.json", "project-profile.schema.json"),
        ("examples/two-repository-product/simulation-app.profile.json", "project-profile.schema.json"),
        ("examples/two-repository-product/risk-policy.json", "risk-policy.schema.json"),
        ("examples/two-repository-product/data-policy.json", "data-policy.schema.json"),
        ("examples/two-repository-product/world.evidence-policy.json", "evidence-policy.schema.json"),
        ("examples/two-repository-product/app.evidence-policy.json", "evidence-policy.schema.json"),
        ("examples/two-repository-product/world.tool-registry.json", "tool-registry.schema.json"),
        ("examples/two-repository-product/world.evaluator-registry.json", "evaluator-registry.schema.json"),
        ("examples/two-repository-product/app.tool-registry.json", "tool-registry.schema.json"),
        ("examples/two-repository-product/app.evaluator-registry.json", "evaluator-registry.schema.json"),
        ("examples/two-repository-product/application-review.intent.json", "intent-brief.schema.json"),
        ("examples/two-repository-product/application-review.retrieval-manifest.json", "retrieval-manifest.schema.json"),
        ("examples/two-repository-product/application-review.evidence-manifest.json", "evidence-manifest.schema.json"),
        ("examples/two-repository-product/application-review.writer-profile.json", "writer-profile.schema.json"),
        ("examples/two-repository-product/application-review.capability-certificate.json", "capability-certificate.schema.json"),
        ("examples/two-repository-product/application-review.packet.json", "task-packet.schema.json"),
        ("examples/two-repository-product/application-review.receipt.json", "worker-receipt.schema.json"),
    ]

    fixture_pairs = [
        (f"{FIXTURE_ROOT}/anchor.json", "continuation-anchor.schema.json"),
        (f"{FIXTURE_ROOT}/intent.json", "intent-brief.schema.json"),
        (f"{FIXTURE_ROOT}/project-profile.json", "project-profile.schema.json"),
        (f"{FIXTURE_ROOT}/authority.json", "active-authority.schema.json"),
        (f"{FIXTURE_ROOT}/risk-policy.json", "risk-policy.schema.json"),
        (f"{FIXTURE_ROOT}/data-policy.json", "data-policy.schema.json"),
        (f"{FIXTURE_ROOT}/evidence-policy.json", "evidence-policy.schema.json"),
        (f"{FIXTURE_ROOT}/tool-registry.json", "tool-registry.schema.json"),
        (f"{FIXTURE_ROOT}/evaluator-registry.json", "evaluator-registry.schema.json"),
        (f"{FIXTURE_ROOT}/writer-profile.json", "writer-profile.schema.json"),
        (f"{FIXTURE_ROOT}/capability-certificate.json", "capability-certificate.schema.json"),
        (f"{FIXTURE_ROOT}/retrieval-manifest.json", "retrieval-manifest.schema.json"),
        (f"{FIXTURE_ROOT}/packet.json", "task-packet.schema.json"),
        (f"{FIXTURE_ROOT}/evidence-manifest.json", "evidence-manifest.schema.json"),
        (f"{FIXTURE_ROOT}/review-bundle.json", "review-bundle.schema.json"),
        (f"{FIXTURE_ROOT}/external-human-receipt.json", "external-human-receipt.schema.json"),
        (f"{FIXTURE_ROOT}/receipt.await-human.json", "worker-receipt.schema.json"),
        (f"{FIXTURE_ROOT}/receipt.final.json", "worker-receipt.schema.json"),
    ]
    pairs = template_pairs + example_pairs + fixture_pairs
    for instance_path, schema_name in pairs:
        instance = load_json(instance_path)
        schema = load_json(f"spec/schemas/{schema_name}")
        validate_schema_instance(instance, schema, schema)
    return len(pairs)


def validate_path_contract() -> tuple[int, int]:
    schemas_with_paths: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    patterns: set[str] = set()
    for path in sorted((ROOT / "spec" / "schemas").glob("*.json")):
        relative = path.relative_to(ROOT).as_posix()
        schema = strict_json_load_bytes(path.read_bytes(), relative)
        definition = schema.get("$defs", {}).get("repositoryPath")
        if definition is not None:
            schemas_with_paths.append((path.name, schema, definition))
            patterns.add(definition.get("pattern"))
    require(len(patterns) == 1, "repository-path schemas do not share one normative grammar")
    require(next(iter(patterns)) == repository_path_regex().pattern, "semantic path grammar differs from schema grammar")

    corpus = load_json("tests/path-vectors.json")
    require(corpus.get("grammarId") == "elad-repository-path-v1", "unknown path-vector grammar")
    vector_ids = [item.get("id") for item in corpus.get("vectors", [])]
    require(len(vector_ids) == len(set(vector_ids)), "duplicate scalar path-vector ID")
    for vector in corpus.get("vectors", []):
        value = vector.get("value")
        expected = vector.get("valid")
        semantic = is_portable_repository_path(value)
        require(semantic is expected, f"semantic path-vector mismatch: {vector.get('id')}")
        for schema_name, root_schema, path_schema in schemas_with_paths:
            try:
                validate_schema_instance(value, path_schema, root_schema)
                schema_result = True
            except ValidationError:
                schema_result = False
            require(schema_result is expected, f"schema path-vector mismatch: {schema_name}:{vector.get('id')}")

    set_ids = [item.get("id") for item in corpus.get("setVectors", [])]
    require(len(set_ids) == len(set(set_ids)), "duplicate set path-vector ID")
    for vector in corpus.get("setVectors", []):
        try:
            validate_path_set(vector.get("values", []), f"path-vector {vector.get('id')}")
            set_result = True
        except ValidationError:
            set_result = False
        require(set_result is vector.get("validTogether"), f"set path-vector mismatch: {vector.get('id')}")
    return len(schemas_with_paths), len(vector_ids) + len(set_ids)


def validate_paths(documents: Iterable[dict[str, Any]]) -> int:
    paths = list(iter_repository_paths(list(documents)))
    for path in paths:
        require(is_portable_repository_path(path), f"non-portable repository path: {path!r}")
    return len(paths)


def validate_markdown_links() -> int:
    count = 0
    for markdown in sorted(ROOT.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (markdown.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(f"Markdown link escapes repository: {markdown.relative_to(ROOT).as_posix()} -> {target}")
            require(resolved.exists(), f"broken Markdown link: {markdown.relative_to(ROOT).as_posix()} -> {target}")
            count += 1
    return count


def validate_text_hygiene() -> int:
    text_extensions = {".md", ".json", ".py", ".ps1", ".txt", ".yml", ".yaml"}
    explicit_names = {"LICENSE", "VERSION"}
    count = 0
    for path in sorted(item for item in ROOT.rglob("*") if item.is_file() and ".git" not in item.parts):
        if path.suffix.lower() not in text_extensions and path.name not in explicit_names:
            continue
        data = path.read_bytes()
        relative = path.relative_to(ROOT).as_posix()
        require(not data.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM is forbidden: {relative}")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            fail(f"file is not UTF-8: {relative}: {exc}")
        require("\x00" not in text, f"NUL byte in text file: {relative}")
        require(text.endswith(("\n", "\r\n")), f"text file lacks final newline: {relative}")
        for line_number, line in enumerate(text.splitlines(), start=1):
            require(line == line.rstrip(" \t"), f"trailing whitespace: {relative}:{line_number}")
        count += 1
    return count


def validate_proportional_review_policy() -> int:
    required_fragments = {
        "docs/ADAPTIVE_RIGOR.md": (
            "expected lifecycle cost is lower than the expected cost of recurrence",
            "least expensive durable mechanism that prevents the validated failure",
            "passing an assurance system's own tests proves internal consistency",
            "assurance depth and verification frequency are selected separately from task rigor",
            "quick: at most one critic pass plus decisive checks",
            "standard: at most one complete review/correction cycle",
            "high assurance: at most two complete review/correction cycles",
            "renaming, recreating, or reframing a candidate does not reset it",
            "unresolved high-consequence uncertainty together with new objective evidence",
            "fresh explicit owner authorization",
            "stop with `blocked`, `revise`, or a narrower claim",
            "invalidates only the claims and evidence it can causally affect",
            "causal footprint cannot be bounded",
            "alters architecture, authority, evidence meaning",
            "git commit and blob identity together with clean/dirty state",
            "when git cannot supply the needed identity",
            "prefer eligible local verification",
        ),
        "templates/WORKFLOW.template.md": (
            "assurance depth and verification frequency from uncertainty",
            "quick: at most one critic pass plus decisive checks",
            "standard: at most one complete review/correction cycle",
            "high assurance: at most two complete cycles",
            "candidate recreation, renaming, or reframing does not reset it",
            "revalidate only the claims and evidence a change can causally affect",
            "extra cycle requires unresolved high-consequence uncertainty plus new objective evidence",
            "never lower the acceptance threshold",
            "git commit/blob identity and clean/dirty state",
            "prefer eligible local verification",
        ),
    }
    checked = 0
    for relative, fragments in required_fragments.items():
        normalized = " ".join((ROOT / relative).read_text(encoding="utf-8").casefold().split())
        for fragment in fragments:
            require(fragment in normalized, f"proportional review policy is incomplete: {relative}: {fragment}")
            checked += 1

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    require(
        "docs/ADAPTIVE_RIGOR.md#proportional-assurance-budgets-and-causal-revalidation" in agents,
        "AGENTS.md does not reference the canonical proportional assurance policy",
    )
    return checked + 1


def validate_no_generated_cache() -> None:
    generated = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and (path.suffix == ".pyc" or "__pycache__" in path.parts)
    ]
    require(not generated, f"generated Python cache must not be retained: {generated}")


def expect_failure(label: str, operation: Callable[[], None]) -> None:
    try:
        operation()
    except ValidationError:
        return
    fail(f"malicious negative unexpectedly passed: {label}")


def build_operational_fixture(
    project: dict[str, Any],
    writer: dict[str, Any],
    certificate: dict[str, Any],
    authority: dict[str, Any],
    risk_policy: dict[str, Any],
    data_policy: dict[str, Any],
    evidence_policy: dict[str, Any],
    tool_registry: dict[str, Any],
    evaluator_registry: dict[str, Any],
    retrieval_manifest: dict[str, Any],
    packet: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    fixture = {
        "project": copy.deepcopy(project),
        "writer": copy.deepcopy(writer),
        "certificate": copy.deepcopy(certificate),
        "authority": copy.deepcopy(authority),
        "risk": copy.deepcopy(risk_policy),
        "data": copy.deepcopy(data_policy),
        "evidence": copy.deepcopy(evidence_policy),
        "tools": copy.deepcopy(tool_registry),
        "evaluators": copy.deepcopy(evaluator_registry),
        "retrieval": copy.deepcopy(retrieval_manifest),
        "packet": copy.deepcopy(packet),
    }
    fixture["project"]["state"] = "active"
    for operation in fixture["project"]["targetOperations"]:
        operation["state"] = "active"
    fixture["writer"]["state"] = "qualified"
    fixture["writer"]["modelSubject"] = {
        "id": "model:synthetic_exact_local",
        "revision": "revision:synthetic_1",
        "artifactSha256": "1212121212121212121212121212121212121212121212121212121212121212",
        "artifactSha256NullReason": None,
    }
    fixture["certificate"]["state"] = "qualified"
    fixture["certificate"]["evaluationPack"]["positiveCases"] = 4
    fixture["certificate"]["evaluationPack"]["negativeCases"] = 4
    fixture["certificate"]["evaluationPack"]["holdoutCases"] = 1
    fixture["certificate"]["evaluationPack"]["coldRuns"] = 2
    fixture["certificate"]["eligibility"] = {
        "roles": ["role:candidate_worker"],
        "taskFamilies": ["read_only_contract_review"],
        "riskClasses": ["low"],
        "dataClasses": ["internal"],
        "artifactLanes": ["ordinary_source"],
        "effectClasses": ["read"],
        "evidenceClasses": ["deterministic", "external_human"],
        "mutationCeiling": "read_only",
    }
    fixture["certificate"]["measuredSafeBudgets"] = copy.deepcopy(fixture["packet"]["budgets"])
    fixture["certificate"]["issuedAt"] = "2026-01-01T00:00:00Z"
    fixture["certificate"]["expiresAt"] = "2099-01-01T00:00:00Z"
    fixture["authority"]["state"] = "active"
    fixture["authority"]["maturityLevel"] = 1
    fixture["authority"]["authorizations"]["evidenceAcceptance"] = True
    fixture["risk"]["state"] = "active"
    fixture["data"]["state"] = "active"
    fixture["evidence"]["state"] = "active"
    for row in fixture["risk"]["classes"]:
        if row["riskClass"] == "low":
            row["allowedEffects"] = ["read"]
            row["requiresHumanDecision"] = False
    for rule in fixture["evidence"]["rules"]:
        if rule["evidenceClass"] == "deterministic":
            rule["acceptanceOwner"] = "machine"
            rule["machineDelegation"] = True
            rule["eligibleWriterProfiles"] = [fixture["writer"]["profileId"]]
    fixture["tools"]["state"] = "active"
    for tool in fixture["tools"]["tools"]:
        tool["state"] = "active"
    fixture["evaluators"]["state"] = "active"
    for evaluator in fixture["evaluators"]["evaluators"]:
        evaluator["state"] = "calibrated"
    fixture["retrieval"]["state"] = "frozen"
    fixture["packet"]["state"] = "admitted"
    return fixture


def run_negative_controls(
    blueprint: dict[str, Any],
    authority: dict[str, Any],
    project: dict[str, Any],
    writer: dict[str, Any],
    certificate: dict[str, Any],
    risk_policy: dict[str, Any],
    data_policy: dict[str, Any],
    evidence_policy: dict[str, Any],
    tool_registry: dict[str, Any],
    evaluator_registry: dict[str, Any],
    retrieval_manifest: dict[str, Any],
    evidence_manifest: dict[str, Any],
    packet: dict[str, Any],
    receipt: dict[str, Any],
    gates: dict[str, Any],
    lifecycle_oracle: dict[str, Any],
) -> int:
    controls: list[tuple[str, Callable[[], None]]] = []

    mismatched_receipt = copy.deepcopy(receipt)
    mismatched_receipt["writer"]["profile"]["id"] = "writer:invented_profile"
    controls.append(("writer mismatch", lambda: validate_writer_chain(writer, certificate, packet, mismatched_receipt)))

    stale_reference_receipt = copy.deepcopy(receipt)
    stale_reference_receipt["bindings"]["projectProfile"]["sha256"] = "AB" * 32
    controls.append(("stale immutable reference hash", lambda: reconcile_packet_receipt(packet, stale_reference_receipt, evidence_manifest)))

    duplicate_claim_receipt = copy.deepcopy(receipt)
    duplicate_claim_receipt["claims"].append(copy.deepcopy(duplicate_claim_receipt["claims"][0]))
    controls.append(("duplicate receipt claim", lambda: reconcile_packet_receipt(packet, duplicate_claim_receipt, evidence_manifest)))

    extra_claim_receipt = copy.deepcopy(receipt)
    extra_claim_receipt["claims"].append({
        "claimId": "claim:invented_extra",
        "acceptanceOwner": "machine",
        "result": "not_evaluated",
        "evidenceRefs": [],
        "externalHumanReceipt": None,
    })
    controls.append(("extra receipt claim", lambda: reconcile_packet_receipt(packet, extra_claim_receipt, evidence_manifest)))

    forged_human_receipt = copy.deepcopy(receipt)
    for result in forged_human_receipt["claims"]:
        if result["acceptanceOwner"] == "external_human":
            result["result"] = "passed"
    forged_human_receipt["openHumanClaims"] = []
    forged_human_receipt["finalizationState"] = "finalized_on_candidate"
    controls.append(("forged human closure", lambda: reconcile_packet_receipt(packet, forged_human_receipt, evidence_manifest)))

    unauthorized_change_receipt = copy.deepcopy(receipt)
    unauthorized_change_receipt["changedPaths"] = ["src/unauthorized.py"]
    controls.append(("unauthorized changed path", lambda: reconcile_packet_receipt(packet, unauthorized_change_receipt, evidence_manifest)))

    unknown_evidence_receipt = copy.deepcopy(receipt)
    unknown_evidence_receipt["claims"][0]["result"] = "passed"
    unknown_evidence_receipt["claims"][0]["evidenceRefs"] = ["evidence:invented"]
    controls.append(("evidence absent from manifest", lambda: reconcile_packet_receipt(packet, unknown_evidence_receipt, evidence_manifest)))

    stale_retrieval = copy.deepcopy(retrieval_manifest)
    stale_retrieval["subject"]["baseHead"] = "b" * 40
    controls.append(("stale retrieval subject", lambda: validate_retrieval_manifest(stale_retrieval, packet)))

    duplicate_retrieval = copy.deepcopy(retrieval_manifest)
    duplicate_retrieval["entries"].append(copy.deepcopy(duplicate_retrieval["entries"][0]))
    controls.append(("duplicate retrieval path", lambda: validate_retrieval_manifest(duplicate_retrieval, packet)))

    casefold_retrieval = copy.deepcopy(retrieval_manifest)
    colliding = copy.deepcopy(casefold_retrieval["entries"][0])
    colliding["path"] = colliding["path"].upper()
    casefold_retrieval["entries"].append(colliding)
    controls.append(("case-fold retrieval collision", lambda: validate_retrieval_manifest(casefold_retrieval, packet)))

    cyclic_gates = copy.deepcopy(gates)
    cyclic_gates["gates"][0]["prerequisites"] = [cyclic_gates["gates"][1]["gateId"]]
    controls.append(("gate cycle", lambda: validate_gate_set(cyclic_gates)))

    active_default_authority = copy.deepcopy(authority)
    active_default_authority["state"] = "active"
    active_default_authority["authorizations"]["candidateMutation"] = True
    controls.append(("accidental authority activation", lambda: validate_default_deny(blueprint, active_default_authority)))

    missing_policy_packet = copy.deepcopy(packet)
    del missing_policy_packet["policyBindings"]["risk"]
    packet_schema = load_json("spec/schemas/task-packet.schema.json")
    controls.append(("missing risk policy", lambda: validate_schema_instance(missing_policy_packet, packet_schema, packet_schema)))

    operational = build_operational_fixture(
        project,
        writer,
        certificate,
        authority,
        risk_policy,
        data_policy,
        evidence_policy,
        tool_registry,
        evaluator_registry,
        retrieval_manifest,
        packet,
    )

    expected_repository_id = operational["project"]["repositoryId"]

    def admit(
        candidate: dict[str, dict[str, Any]],
        *,
        intent_override: dict[str, Any] | None = None,
        registry_override: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        validate_operational_admission(
            candidate["project"],
            candidate["writer"],
            candidate["certificate"],
            candidate["authority"],
            candidate["risk"],
            candidate["data"],
            candidate["evidence"],
            candidate["tools"],
            candidate["evaluators"],
            candidate["retrieval"],
            candidate["packet"],
            intent=intent_override,
            registries=registry_override,
            expected_repository_id=expected_repository_id,
        )

    admit(operational)

    for label, mutate in (
        ("unqualified role", lambda value: value["packet"]["writer"].update({"roleId": "role:invented"})),
        ("unqualified task family", lambda value: value["packet"].update({"taskFamily": "invented_task"})),
        ("unqualified risk class", lambda value: value["packet"].update({"riskClass": "normal"})),
        ("unqualified data class", lambda value: value["packet"].update({"dataClass": "restricted"})),
        ("unqualified artifact lane", lambda value: value["packet"].update({"artifactLane": "runtime"})),
        ("unqualified effect", lambda value: value["packet"].update({"requestedEffects": ["candidate_write"]})),
        ("unqualified evidence class", lambda value: value["packet"]["claims"][0].update({"evidenceClass": "invented_evidence"})),
        ("packet exceeds measured budget", lambda value: value["packet"]["budgets"].update({"sequentialToolCalls": 999})),
        ("packet outside project roots", lambda value: value["packet"]["paths"].update({"allowedExisting": ["outside/file.md"]})),
        ("unqualified certificate", lambda value: value["certificate"].update({"state": "unqualified"})),
    ):
        candidate = copy.deepcopy(operational)
        mutate(candidate)
        controls.append((label, lambda value=candidate: admit(value)))

    missing_tool = copy.deepcopy(operational)
    missing_tool["packet"]["tools"][0]["toolId"] = "tool:invented"
    controls.append(("tool absent from hash-bound registry", lambda: admit(missing_tool)))

    stale_tool = copy.deepcopy(operational)
    stale_tool["packet"]["tools"][0]["registryEntrySha256"] = "CD" * 32
    controls.append(("tool registry-entry digest mismatch", lambda: admit(stale_tool)))

    inactive_evaluator = copy.deepcopy(operational)
    inactive_evaluator["evaluators"]["evaluators"][0]["state"] = "expired"
    controls.append(("expired evaluator", lambda: admit(inactive_evaluator)))

    missing_evaluator = copy.deepcopy(operational)
    missing_evaluator["packet"]["claims"][0]["evaluatorId"] = "evaluator:invented"
    controls.append(("evaluator absent from hash-bound registry", lambda: admit(missing_evaluator)))

    authority_escape = copy.deepcopy(operational)
    authority_escape["packet"]["requestedEffects"] = ["candidate_write"]
    authority_escape["packet"]["tools"][0]["effect"] = "candidate_write"
    authority_escape["tools"]["tools"][0]["effect"] = "candidate_write"
    authority_escape["certificate"]["eligibility"]["effectClasses"] = ["candidate_write"]
    authority_escape["certificate"]["eligibility"]["mutationCeiling"] = "candidate_only"
    authority_escape["writer"]["mutationCeiling"] = "candidate_only"
    authority_escape["risk"]["classes"][0]["allowedEffects"] = ["candidate_write"]
    authority_escape["project"]["targetOperations"][0]["effects"] = ["candidate_write"]
    controls.append(("packet exceeds repository authority", lambda: admit(authority_escape)))

    payloads = {
        "evidence/one.json": b'{"ok":true}\n',
        "evidence/two.txt": b"verified\n",
    }
    byte_manifest = {
        "entries": [
            {
                "evidenceId": f"evidence:byte_{index}",
                "path": path,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest().upper(),
            }
            for index, (path, payload) in enumerate(payloads.items(), start=1)
        ]
    }
    validate_manifest_bytes(byte_manifest, payloads, "byte fixture")

    missing_payload = dict(payloads)
    del missing_payload["evidence/two.txt"]
    controls.append(("manifest missing file", lambda: validate_manifest_bytes(byte_manifest, missing_payload, "byte fixture")))

    extra_payload = dict(payloads)
    extra_payload["evidence/extra.txt"] = b"extra\n"
    controls.append(("manifest extra file", lambda: validate_manifest_bytes(byte_manifest, extra_payload, "byte fixture")))

    altered_payload = dict(payloads)
    altered_payload["evidence/one.json"] = b'{"ok":false}\n'
    controls.append(("manifest altered bytes", lambda: validate_manifest_bytes(byte_manifest, altered_payload, "byte fixture")))

    outer_document = {
        "schemaVersion": "0.3.0",
        "manifestId": "evidence-manifest:outer_test",
        "entries": [],
    }
    outer_reference = {
        "id": "evidence-manifest:outer_test",
        "path": "evidence/outer-test.json",
        "sha256": canonical_sha256(outer_document),
        "schemaVersion": "0.3.0",
    }
    validate_outer_reference(outer_reference, outer_document, "manifestId", "outer-envelope fixture")
    bad_outer = copy.deepcopy(outer_reference)
    bad_outer["sha256"] = "EF" * 32
    controls.append(("outer-envelope manifest digest mismatch", lambda: validate_outer_reference(bad_outer, outer_document, "manifestId", "outer-envelope fixture")))

    controls.extend(
        [
            ("strict JSON duplicate key", lambda: strict_json_load_bytes(b'{"x":1,"x":2}\n', "duplicate-key control")),
            ("strict JSON NaN", lambda: strict_json_load_bytes(b'{"x":NaN}\n', "NaN control")),
            ("strict JSON infinite exponent", lambda: strict_json_load_bytes(b'{"x":1e9999}\n', "infinite-number control")),
            ("strict JSON UTF-8 BOM", lambda: strict_json_load_bytes(b'\xef\xbb\xbf{"x":1}\n', "BOM control")),
        ]
    )

    intent_template = load_json("templates/intent-brief.template.json")

    changed_description = copy.deepcopy(packet)
    changed_description["claims"][0]["description"] = "Coordinated wording substitution."
    controls.append(("intent claim description substitution", lambda value=changed_description: validate_intent_packet(intent_template, value)))

    changed_owner = copy.deepcopy(packet)
    changed_owner["claims"][0]["acceptanceOwner"] = "external_human"
    controls.append(("intent claim owner substitution", lambda value=changed_owner: validate_intent_packet(intent_template, value)))

    changed_selector = copy.deepcopy(packet)
    changed_selector["claims"][0]["subject"]["selector"] = "invented_selector"
    controls.append(("intent claim selector substitution", lambda value=changed_selector: validate_intent_packet(intent_template, value)))

    changed_claim_class = copy.deepcopy(operational)
    changed_claim_class["packet"]["claims"][0]["claimClass"] = "claim-class:invented_but_well_formed"
    changed_claim_class_intent = copy.deepcopy(intent_template)
    changed_claim_class_intent["claims"][0]["claimClass"] = "claim-class:invented_but_well_formed"
    controls.append(
        (
            "evidence-policy claim-class mismatch",
            lambda value=changed_claim_class, intent_value=changed_claim_class_intent: admit(value, intent_override=intent_value),
        )
    )

    no_evidence_acceptance = copy.deepcopy(operational)
    no_evidence_acceptance["authority"]["authorizations"]["evidenceAcceptance"] = False
    controls.append(("machine admission without evidence acceptance", lambda value=no_evidence_acceptance: admit(value)))

    role_permission_escape = copy.deepcopy(operational)
    role_permission_escape["packet"]["requestedEffects"] = ["candidate_write"]
    role_permission_escape["packet"]["writer"]["roleId"] = "role:orchestrator"
    role_permission_escape["packet"]["tools"][0]["effect"] = "candidate_write"
    role_permission_escape["tools"]["tools"][0]["effect"] = "candidate_write"
    role_permission_escape["writer"]["roles"] = ["role:orchestrator"]
    role_permission_escape["writer"]["mutationCeiling"] = "candidate_only"
    role_permission_escape["certificate"]["eligibility"]["roles"] = ["role:orchestrator"]
    role_permission_escape["certificate"]["eligibility"]["effectClasses"] = ["candidate_write"]
    role_permission_escape["certificate"]["eligibility"]["mutationCeiling"] = "candidate_only"
    role_permission_escape["authority"]["authorizations"]["candidateMutation"] = True
    role_permission_escape["risk"]["classes"][0]["allowedEffects"] = ["candidate_write"]
    role_permission_escape["project"]["targetOperations"][0]["effects"] = ["candidate_write"]
    controls.append(("canonical role permission escape", lambda value=role_permission_escape: admit(value)))

    coordinated_repository = copy.deepcopy(operational)
    coordinated_intent = copy.deepcopy(intent_template)
    substituted_repository_id = "repo:coordinated_substitution"
    coordinated_repository["project"]["repositoryId"] = substituted_repository_id
    coordinated_repository["authority"]["ownerRepositoryId"] = substituted_repository_id
    coordinated_repository["evidence"]["ownerRepositoryId"] = substituted_repository_id
    coordinated_repository["tools"]["ownerRepositoryId"] = substituted_repository_id
    coordinated_repository["evaluators"]["ownerRepositoryId"] = substituted_repository_id
    coordinated_repository["packet"]["repository"]["repositoryId"] = substituted_repository_id
    coordinated_repository["retrieval"]["subject"]["repositoryId"] = substituted_repository_id
    for entry in coordinated_repository["retrieval"]["entries"]:
        entry["repositoryId"] = substituted_repository_id
    for claim in coordinated_repository["packet"]["claims"]:
        claim["subject"]["repositoryId"] = substituted_repository_id
    for claim in coordinated_intent["claims"]:
        claim["subject"]["repositoryId"] = substituted_repository_id
    controls.append(
        (
            "coordinated cross-repository substitution",
            lambda value=coordinated_repository, intent_value=coordinated_intent: admit(value, intent_override=intent_value),
        )
    )

    coordinated_vocab = copy.deepcopy(operational)
    coordinated_vocab["packet"]["writer"]["roleId"] = "role:coordinated_invention"
    coordinated_vocab["writer"]["roles"] = ["role:coordinated_invention"]
    coordinated_vocab["certificate"]["eligibility"]["roles"] = ["role:coordinated_invention"]
    invented_registries = copy.deepcopy(load_canonical_registries(blueprint))
    invented_registries["roles"]["roles"].append(
        {
            "id": "role:coordinated_invention",
            "mayMutateCandidate": False,
            "mayMutateTarget": False,
            "mayPromote": False,
            "purpose": "Malicious coordinated vocabulary substitution.",
        }
    )
    controls.append(
        (
            "coordinated canonical-vocabulary substitution",
            lambda value=coordinated_vocab, vocab=invented_registries: admit(value, registry_override=vocab),
        )
    )

    invented_failure = {"failureClass": "invented_failure_class"}
    controls.append(
        (
            "invented failure taxonomy",
            lambda value=invented_failure: validate_canonical_vocabulary_usage([value], load_canonical_registries(blueprint)),
        )
    )

    writer_under_certificate = copy.deepcopy(operational)
    writer_under_certificate["writer"]["configuredBudgets"]["contextTokens"] = 1
    controls.append(("writer budget below certificate", lambda value=writer_under_certificate: admit(value)))

    certificate_under_packet = copy.deepcopy(operational)
    certificate_under_packet["certificate"]["measuredSafeBudgets"]["outputTokens"] = 1
    controls.append(("certificate budget below packet", lambda value=certificate_under_packet: admit(value)))

    sequential_over_total = copy.deepcopy(operational)
    sequential_over_total["packet"]["budgets"]["sequentialToolCalls"] = sequential_over_total["packet"]["budgets"]["totalToolCalls"] + 1
    controls.append(("sequential tool-call budget over total", lambda value=sequential_over_total: admit(value)))

    invented_numeric_cost = copy.deepcopy(operational)
    invented_numeric_cost["packet"]["budgets"]["maxCostUsd"] = 1.0
    controls.append(("numeric cost beneath null cost ceiling", lambda value=invented_numeric_cost: admit(value)))

    changed_resource_envelope = copy.deepcopy(operational)
    changed_resource_envelope["packet"]["budgets"]["resourceEnvelope"] = "resource-envelope:invented"
    controls.append(("packet resource-envelope substitution", lambda value=changed_resource_envelope: admit(value)))

    intent_budget_escape = copy.deepcopy(packet)
    intent_budget_escape["budgets"]["totalToolCalls"] = intent_template["budgets"]["toolCalls"] + 1
    intent_budget_escape["budgets"]["sequentialToolCalls"] = intent_budget_escape["budgets"]["totalToolCalls"]
    controls.append(("packet exceeds intent budget", lambda value=intent_budget_escape: validate_intent_packet(intent_template, value)))

    fixture_packet = load_json(_fixture_path("packet.json"))
    fixture_intent = load_json(_fixture_path("intent.json"))
    fixture_authority = load_json(_fixture_path("authority.json"))
    fixture_evidence = load_json(_fixture_path("evidence-manifest.json"))
    fixture_final = load_json(_fixture_path("receipt.final.json"))
    fixture_human = load_json(_fixture_path("external-human-receipt.json"))
    fixture_review = load_json(_fixture_path("review-bundle.json"))
    fixture_policy = load_json(_fixture_path("evidence-policy.json"))
    fixture_humans = {fixture_human["receiptId"]: fixture_human}

    bad_lifecycle_action = copy.deepcopy(fixture_final)
    bad_lifecycle_action["requestedNextAction"] = "owner_decision"
    controls.append(
        (
            "unlisted receipt lifecycle tuple",
            lambda value=bad_lifecycle_action: validate_receipt_lifecycle(fixture_packet, value, fixture_evidence, lifecycle_oracle),
        )
    )

    unsealed_lifecycle_manifest = copy.deepcopy(fixture_evidence)
    unsealed_lifecycle_manifest["state"] = "draft"
    controls.append(
        (
            "lifecycle closure with unsealed manifest",
            lambda manifest=unsealed_lifecycle_manifest: validate_receipt_lifecycle(fixture_packet, fixture_final, manifest, lifecycle_oracle),
        )
    )

    receipt_over_budget = copy.deepcopy(fixture_final)
    receipt_over_budget["metrics"]["totalToolCalls"] = fixture_packet["budgets"]["totalToolCalls"] + 1
    receipt_over_budget["metrics"]["sequentialToolCalls"] = receipt_over_budget["metrics"]["totalToolCalls"]
    controls.append(("receipt usage over packet budget", lambda value=receipt_over_budget: validate_receipt_usage(fixture_packet["budgets"], value["metrics"], sealed=True)))

    receipt_resource_substitution = copy.deepcopy(fixture_final)
    receipt_resource_substitution["metrics"]["resourceEnvelope"] = "resource-envelope:invented"
    controls.append(("receipt resource-envelope substitution", lambda value=receipt_resource_substitution: validate_receipt_usage(fixture_packet["budgets"], value["metrics"], sealed=True)))

    receipt_claim_relabel = copy.deepcopy(fixture_final)
    receipt_claim_relabel["claims"][0]["claimClass"] = "claim-class:coordinated_relabel"
    controls.append(
        (
            "receipt claim-class relabel",
            lambda value=receipt_claim_relabel: reconcile_packet_receipt(
                fixture_packet,
                value,
                fixture_evidence,
                intent=fixture_intent,
                authority=fixture_authority,
                human_receipts=fixture_humans,
                lifecycle_oracle=lifecycle_oracle,
                authenticate_packet_reference=True,
            ),
        )
    )

    receipt_subject_relabel = copy.deepcopy(fixture_final)
    receipt_subject_relabel["claims"][0]["resolvedSubject"]["sha256"] = "AB" * 32
    controls.append(
        (
            "receipt resolved-subject relabel",
            lambda value=receipt_subject_relabel: reconcile_packet_receipt(
                fixture_packet,
                value,
                fixture_evidence,
                intent=fixture_intent,
                authority=fixture_authority,
                human_receipts=fixture_humans,
                lifecycle_oracle=lifecycle_oracle,
                authenticate_packet_reference=True,
            ),
        )
    )

    evidence_class_relabel = copy.deepcopy(fixture_evidence)
    evidence_class_relabel["entries"][0]["evidenceClass"] = "external_human"
    controls.append(("evidence-manifest claim-class relabel", lambda value=evidence_class_relabel: validate_evidence_manifest(value, fixture_packet, fixture_final)))

    no_green_authority = copy.deepcopy(fixture_authority)
    no_green_authority["authorizations"]["evidenceAcceptance"] = False
    controls.append(
        (
            "green closure without evidence acceptance",
            lambda value=no_green_authority: reconcile_packet_receipt(
                fixture_packet,
                fixture_final,
                fixture_evidence,
                intent=fixture_intent,
                authority=value,
                human_receipts=fixture_humans,
                lifecycle_oracle=lifecycle_oracle,
                authenticate_packet_reference=True,
            ),
        )
    )

    ineligible_human = copy.deepcopy(fixture_human)
    ineligible_human["reviewer"]["reviewerId"] = "human:invented_reviewer"
    controls.append(
        (
            "ineligible external human reviewer",
            lambda value=ineligible_human: validate_review_and_human_receipt(
                fixture_review,
                value,
                fixture_packet,
                fixture_final,
                fixture_evidence,
                fixture_policy,
            ),
        )
    )

    phantom_review_evidence = copy.deepcopy(fixture_review)
    phantom_review_evidence["entries"][0]["evidenceIds"] = ["evidence:phantom"]
    controls.append(
        (
            "review bundle phantom evidence",
            lambda value=phantom_review_evidence: validate_review_and_human_receipt(
                value,
                fixture_human,
                fixture_packet,
                fixture_final,
                fixture_evidence,
                fixture_policy,
            ),
        )
    )

    wrong_review_payload = copy.deepcopy(fixture_review)
    wrong_review_payload["entries"][0]["sha256"] = "CD" * 32
    controls.append(("review bundle wrong raw payload digest", lambda value=wrong_review_payload: validate_manifest_disk_bytes(value, "review payload control")))

    phantom_packet_reference = copy.deepcopy(fixture_final["packet"])
    phantom_packet_reference["path"] = _fixture_path("phantom-packet.json")
    controls.append(
        (
            "phantom outer-reference artifact",
            lambda value=phantom_packet_reference: resolve_fixture_reference(value, _fixture_path("packet.json"), "packetId", "phantom packet control"),
        )
    )

    stale_supersession = copy.deepcopy(fixture_final["supersedes"])
    stale_supersession["sha256"] = "EF" * 32
    fixture_await = load_json(_fixture_path("receipt.await-human.json"))
    controls.append(("stale receipt supersession", lambda value=stale_supersession: validate_outer_reference(value, fixture_await, "receiptId", "supersession control")))

    for label, operation in controls:
        expect_failure(label, operation)
    return len(controls)


def main() -> int:
    validate_no_generated_cache()
    json_paths, json_documents = validate_all_json()
    schema_count = validate_schemas(json_paths)
    instance_count = validate_schema_instances()
    path_schema_count, path_vector_count = validate_path_contract()
    path_count = validate_paths(json_documents)
    link_count = validate_markdown_links()
    text_count = validate_text_hygiene()
    proportional_policy_count = validate_proportional_review_policy()

    blueprint = load_json("blueprint.json")
    registries = load_canonical_registries(blueprint)
    lifecycle_oracle = load_lifecycle_oracle()
    claim_aggregate_vector_count, lifecycle_shape_count, lifecycle_mutation_count = validate_lifecycle_semantic_vectors(lifecycle_oracle)
    authority = load_json("templates/active-authority.template.json")
    project = load_json("templates/project-profile.template.json")
    writer = load_json("templates/writer-profile.template.json")
    certificate = load_json("templates/capability-certificate.template.json")
    risk_policy = load_json("templates/risk-policy.template.json")
    data_policy = load_json("templates/data-policy.template.json")
    evidence_policy = load_json("templates/evidence-policy.template.json")
    tool_registry = load_json("templates/tool-registry.template.json")
    evaluator_registry = load_json("templates/evaluator-registry.template.json")
    retrieval_manifest = load_json("templates/retrieval-manifest.template.json")
    evidence_manifest = load_json("templates/evidence-manifest.template.json")
    packet = load_json("templates/task-packet.template.json")
    receipt = load_json("templates/worker-receipt.template.json")
    human_receipt = load_json("templates/external-human-receipt.template.json")
    gates = load_json("templates/gate-set.template.json")
    intent = load_json("templates/intent-brief.template.json")
    failure_template = load_json("templates/failure-record.template.json")

    require((ROOT / "VERSION").read_text(encoding="utf-8").strip() == blueprint.get("version"), "VERSION and blueprint.json disagree")
    validate_default_deny(blueprint, authority)
    validate_profile_templates(
        project,
        writer,
        certificate,
        risk_policy,
        data_policy,
        evidence_policy,
        tool_registry,
        evaluator_registry,
        retrieval_manifest,
        evidence_manifest,
        packet,
        receipt,
        human_receipt,
    )
    validate_gate_set(gates)
    require(failure_template.get("failureClass") in canonical_vocabulary_sets(registries)["failureClasses"], "failure template does not use the canonical failure taxonomy")
    validate_packet_bindings(
        project,
        writer,
        certificate,
        authority,
        risk_policy,
        data_policy,
        evidence_policy,
        tool_registry,
        evaluator_registry,
        retrieval_manifest,
        packet,
    )
    validate_intent_packet(intent, packet)
    validate_writer_chain(writer, certificate, packet, receipt)
    reconcile_packet_receipt(packet, receipt, evidence_manifest, intent=intent)

    example_authority = load_json("examples/two-repository-product/app.active-authority.json")
    example_project = load_json("examples/two-repository-product/simulation-app.profile.json")
    example_writer = load_json("examples/two-repository-product/application-review.writer-profile.json")
    example_certificate = load_json("examples/two-repository-product/application-review.capability-certificate.json")
    example_risk = load_json("examples/two-repository-product/risk-policy.json")
    example_data = load_json("examples/two-repository-product/data-policy.json")
    example_evidence_policy = load_json("examples/two-repository-product/app.evidence-policy.json")
    example_tools = load_json("examples/two-repository-product/app.tool-registry.json")
    example_evaluators = load_json("examples/two-repository-product/app.evaluator-registry.json")
    example_packet = load_json("examples/two-repository-product/application-review.packet.json")
    example_receipt = load_json("examples/two-repository-product/application-review.receipt.json")
    example_retrieval = load_json("examples/two-repository-product/application-review.retrieval-manifest.json")
    example_evidence = load_json("examples/two-repository-product/application-review.evidence-manifest.json")
    example_intent = load_json("examples/two-repository-product/application-review.intent.json")
    validate_default_deny(blueprint, example_authority)
    validate_packet_bindings(
        example_project,
        example_writer,
        example_certificate,
        example_authority,
        example_risk,
        example_data,
        example_evidence_policy,
        example_tools,
        example_evaluators,
        example_retrieval,
        example_packet,
    )
    validate_intent_packet(example_intent, example_packet)
    validate_writer_chain(example_writer, example_certificate, example_packet, example_receipt)
    reconcile_packet_receipt(example_packet, example_receipt, example_evidence, intent=example_intent)

    validate_canonical_vocabulary_usage(json_documents, registries)
    raw_fixture_count, continuation_receipt_count = validate_exact_byte_continuation(
        blueprint,
        registries,
        lifecycle_oracle,
    )

    negative_count = run_negative_controls(
        blueprint,
        authority,
        project,
        writer,
        certificate,
        risk_policy,
        data_policy,
        evidence_policy,
        tool_registry,
        evaluator_registry,
        retrieval_manifest,
        evidence_manifest,
        packet,
        receipt,
        gates,
        lifecycle_oracle,
    )

    print(
        "PASS — Evidence-Led Agentic Development Level 0 has coherent inert structural chains, "
        "one modeled synthetic admission, and one exact-byte continuation fixture; it remains default-deny and non-operational. "
        f"Validated {len(json_paths)} JSON files, {schema_count} schemas, {instance_count} schema instances, "
        f"{path_schema_count} path-bearing schemas against {path_vector_count} canonical vectors, "
        f"{path_count} repository paths, {link_count} relative Markdown links, {text_count} text files, "
        f"{proportional_policy_count} proportional review policy bindings, "
        f"all 44,100 receipt lifecycle tuples with exactly 33 independently rule-derived admissions, "
        f"{claim_aggregate_vector_count} claim-aggregate vectors, {lifecycle_shape_count} admitted lifecycle shapes, "
        f"{lifecycle_mutation_count} single-field lifecycle denials, {continuation_receipt_count} anchored receipt states, "
        f"{raw_fixture_count} exact raw payloads, and {negative_count} malicious controls. No authority granted."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(f"FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1)
