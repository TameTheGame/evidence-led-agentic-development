#!/usr/bin/env python3
"""Read-only, dependency-free conformance checks for the inert ELAD 0.4.0 slice.

This validator reads only the five new schemas, their five inert templates, and
the external adoption-vector corpus. A PASS proves structural and synthetic
semantic conformance only. It grants no model, routing, mutation, target,
evidence, promotion, publication, or maturity authority.
"""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import math
import re
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any


if sys.version_info < (3, 10):
    print("FAIL — Python 3.10 or newer is required.", file=sys.stderr)
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.4.0"
SCHEMA_TEMPLATE_PAIRS = (
    ("spec/schemas/evaluation-pack.schema.json", "templates/evaluation-pack.template.json"),
    ("spec/schemas/evaluation-result-manifest.schema.json", "templates/evaluation-result-manifest.template.json"),
    ("spec/schemas/resource-envelope.schema.json", "templates/resource-envelope.template.json"),
    ("spec/schemas/adoption-efficacy-plan.schema.json", "templates/adoption-efficacy-plan.template.json"),
    ("spec/schemas/adoption-efficacy-report.schema.json", "templates/adoption-efficacy-report.template.json"),
)
VECTOR_PATH = "tests/adoption-vectors.json"
BUDGET_FIELDS = (
    "contextTokens",
    "outputTokens",
    "retrievals",
    "sequentialToolCalls",
    "totalToolCalls",
    "attempts",
    "spawns",
    "wallSeconds",
    "concurrency",
)
HUMAN_REASON_FIELDS = (
    "intent",
    "subjectiveOrRuntimeException",
    "promotionOrPublication",
    "unresolvedTrust",
    "routineProtocol",
    "otherException",
)
GUARDRAIL_FIELDS = (
    "evaluatorFalseGreens",
    "authorityViolations",
    "scopeViolations",
    "securityOrPrivacyEvents",
)


class ValidationError(RuntimeError):
    pass


class SemanticError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def reject(code: str, message: str) -> None:
    raise SemanticError(code, message)


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _strict_float(text: str) -> float:
    value = float(text)
    require(math.isfinite(value), f"non-finite JSON number: {text}")
    return value


def _strict_constant(text: str) -> None:
    raise ValidationError(f"non-standard JSON constant: {text}")


def load_json(relative_path: str) -> dict[str, Any]:
    data = (ROOT / relative_path).read_bytes()
    require(not data.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM is forbidden: {relative_path}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"JSON is not UTF-8: {relative_path}: {exc}") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_float=_strict_float,
            parse_constant=_strict_constant,
        )
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON: {relative_path}: {exc}") from exc
    require(isinstance(value, dict), f"top-level JSON must be an object: {relative_path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest().upper()


def json_type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
    raise ValidationError(f"validator does not implement JSON Schema type {expected!r}")


def json_equal(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    return left == right


def resolve_local_ref(reference: str, root_schema: dict[str, Any]) -> dict[str, Any]:
    prefix = "#/$defs/"
    require(reference.startswith(prefix), f"only local schema references are permitted: {reference}")
    name = reference[len(prefix) :]
    target = root_schema.get("$defs", {}).get(name)
    require(isinstance(target, dict), f"unresolved local schema reference: {reference}")
    return target


def parse_datetime(value: str, label: str) -> dt.datetime:
    require(isinstance(value, str), f"{label} must be a date-time string")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"invalid date-time at {label}: {value}") from exc
    require(parsed.tzinfo is not None, f"date-time must include an offset at {label}")
    return parsed


def validate_instance(value: Any, schema: dict[str, Any], root_schema: dict[str, Any], path: str = "$") -> None:
    if "$ref" in schema:
        validate_instance(value, resolve_local_ref(schema["$ref"], root_schema), root_schema, path)
        return

    if "const" in schema:
        require(json_equal(value, schema["const"]), f"const mismatch at {path}")
    if "enum" in schema:
        require(any(json_equal(value, item) for item in schema["enum"]), f"enum mismatch at {path}")

    declared_type = schema.get("type")
    if declared_type is not None:
        options = declared_type if isinstance(declared_type, list) else [declared_type]
        require(any(json_type_matches(value, item) for item in options), f"type mismatch at {path}: expected {options}")

    if isinstance(value, dict):
        required = schema.get("required", [])
        require(all(key in value for key in required), f"required property missing at {path}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = set(value) - set(properties)
            require(not extras, f"additional properties at {path}: {sorted(extras)}")
        for key, child in value.items():
            if key in properties:
                validate_instance(child, properties[key], root_schema, f"{path}.{key}")

    if isinstance(value, list):
        if "minItems" in schema:
            require(len(value) >= schema["minItems"], f"too few items at {path}")
        if "maxItems" in schema:
            require(len(value) <= schema["maxItems"], f"too many items at {path}")
        if schema.get("uniqueItems"):
            serialized = [canonical_bytes(item) for item in value]
            require(len(serialized) == len(set(serialized)), f"duplicate array item at {path}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, child in enumerate(value):
                validate_instance(child, item_schema, root_schema, f"{path}[{index}]")

    if isinstance(value, str):
        if "minLength" in schema:
            require(len(value) >= schema["minLength"], f"string too short at {path}")
        if "pattern" in schema:
            require(re.search(schema["pattern"], value) is not None, f"pattern mismatch at {path}: {value!r}")
        if schema.get("format") == "date-time":
            parse_datetime(value, path)

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema:
            require(value >= schema["minimum"], f"value below minimum at {path}")
        if "maximum" in schema:
            require(value <= schema["maximum"], f"value above maximum at {path}")


def validate_closed_schema(schema: dict[str, Any], label: str) -> int:
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", f"wrong JSON Schema dialect: {label}")
    require(schema.get("$id", "").endswith(f":{VERSION}"), f"wrong schema ID/version: {label}")
    require(schema.get("type") == "object", f"schema root is not an object: {label}")
    require(schema.get("additionalProperties") is False, f"schema root is open: {label}")
    require(schema.get("properties", {}).get("schemaVersion", {}).get("const") == VERSION, f"schema version const mismatch: {label}")
    closed_objects = 0

    def walk(node: Any, location: str) -> None:
        nonlocal closed_objects
        if isinstance(node, dict):
            declared = node.get("type")
            object_typed = declared == "object" or (isinstance(declared, list) and "object" in declared)
            if object_typed:
                require(node.get("additionalProperties") is False, f"open object schema at {label}:{location}")
                closed_objects += 1
            for key, child in node.items():
                walk(child, f"{location}/{key}")
        elif isinstance(node, list):
            for index, child in enumerate(node):
                walk(child, f"{location}/{index}")

    walk(schema, "$")
    return closed_objects


def validate_non_authority(value: Any, label: str) -> None:
    require(
        value
        == {
            "grantsAuthority": False,
            "grantsMutation": False,
            "grantsPromotion": False,
            "grantsPublication": False,
        },
        f"{label} is not explicit non-authority",
    )


def validate_inert_template(template: dict[str, Any], template_path: str) -> None:
    require(template.get("schemaVersion") == VERSION, f"template version mismatch: {template_path}")
    require(template.get("state") == "template_inert", f"template is not inert: {template_path}")
    validate_non_authority(template.get("authority"), template_path)
    if template_path.endswith("evaluation-pack.template.json"):
        require(not template["candidateScopes"] and not template["cases"] and not template["thresholdSets"], "evaluation pack template is not deny-all")
        require(template["frozenAt"] is None, "evaluation pack template is already frozen")
    elif template_path.endswith("evaluation-result-manifest.template.json"):
        require(not template["runs"] and not template["scopeResults"], "evaluation result template asserts outcomes")
        require(template["aggregate"]["qualificationState"] == "unrun", "evaluation result template is not unrun")
        require(all(template["aggregate"][key] == 0 for key in template["aggregate"] if key != "qualificationState"), "evaluation result template asserts counts")
        require(template["independentVerification"] is None, "evaluation result template asserts verification")
    elif template_path.endswith("resource-envelope.template.json"):
        require(template["stage"] == "configured" and template["parentEnvelope"] is None, "resource template has live lineage")
        require(template["derivation"] is None and template["observations"] is None, "resource template asserts measurements")
        require(not template["execution"]["local"]["modelArtifacts"], "resource template binds model artifacts")
    elif template_path.endswith("adoption-efficacy-plan.template.json"):
        require(not template["baseline"]["observations"], "efficacy plan template asserts a baseline")
        require(not template["metricDefinitions"] and not template["thresholds"] and not template["hardGuardrails"], "efficacy plan template could advance")
        require(template["frozenAt"] is None and template["approvedByOwner"] is None, "efficacy plan template is activated")
    elif template_path.endswith("adoption-efficacy-report.template.json"):
        require(template["decision"] == "hold", "efficacy report template does not hold")
        require(not template["candidateObservations"] and not template["metricResults"], "efficacy report template asserts results")
        require(template["independentVerification"] is None, "efficacy report template asserts verification")


def make_ref(identifier: str, marker: str) -> dict[str, str]:
    return {
        "id": identifier,
        "path": "reference/README.md",
        "sha256": marker * 64,
        "schemaVersion": VERSION,
    }


def make_subject(harness_name: str) -> dict[str, Any]:
    marker = "A" if harness_name == "worker_a" else "B"
    return {
        "model": {
            "kind": "local_artifacts",
            "id": "model:synthetic_worker",
            "revision": "synthetic-revision",
            "artifacts": [
                {
                    "artifactId": "artifact:synthetic_worker_target",
                    "role": "target",
                    "sourceRepository": "synthetic/model",
                    "sourceRevision": "synthetic-revision",
                    "filename": "synthetic.gguf",
                    "bytes": 1024,
                    "sha256": "C" * 64,
                    "format": "gguf",
                }
            ],
            "cloudDeployment": None,
        },
        "executionLocation": "isolated_local",
        "runtime": make_ref("runtime:synthetic_backend", "D"),
        "harness": make_ref(f"harness:synthetic_{harness_name}", marker),
        "adapter": make_ref(f"adapter:synthetic_{harness_name}", marker),
        "promptTemplate": make_ref(f"template:synthetic_{harness_name}", marker),
        "contextCompiler": make_ref(f"context-compiler:synthetic_{harness_name}", marker),
        "toolSchema": make_ref("schema:synthetic_tools", "E"),
    }


def budget(context: int, calls: int) -> dict[str, int | None]:
    return {
        "contextTokens": context,
        "outputTokens": min(4096, context),
        "retrievals": 2,
        "sequentialToolCalls": calls,
        "totalToolCalls": calls,
        "attempts": 1,
        "spawns": 0,
        "wallSeconds": 300,
        "maxCostUsd": None,
        "concurrency": 1,
    }


def qualification_fixture() -> dict[str, Any]:
    subject = make_subject("worker_a")
    tool_a = {"toolId": "tool:read_slice", "registryEntrySha256": "1" * 64, "effect": "read"}
    tool_b = {"toolId": "tool:inspect_receipt", "registryEntrySha256": "2" * 64, "effect": "read"}
    claim_a = {
        "claimClass": "claim-class:source_grounded",
        "evidenceClass": "deterministic_static",
        "evaluatorId": "evaluator:source_check",
        "evaluatorEntrySha256": "3" * 64,
        "negativeControlId": "case:stale_source",
    }
    claim_b = {
        "claimClass": "claim-class:receipt_consistent",
        "evidenceClass": "deterministic_static",
        "evaluatorId": "evaluator:receipt_check",
        "evaluatorEntrySha256": "4" * 64,
        "negativeControlId": "case:forged_receipt",
    }
    scope_a = {
        "scopeId": "qualification-scope:pi_source",
        "toolBindings": [tool_a],
        "claimBindings": [claim_a],
        "budgetCeiling": budget(16384, 4),
        "outcome": "passed",
    }
    scope_b = {
        "scopeId": "qualification-scope:pi_receipt",
        "toolBindings": [tool_b],
        "claimBindings": [claim_b],
        "budgetCeiling": budget(8192, 2),
        "outcome": "passed",
    }
    result = {
        "state": "sealed",
        "qualificationSubject": subject,
        "qualificationSubjectSha256": canonical_sha256(subject),
        "runs": [
            {"runId": "evaluation-run:pi_source_1", "caseVerdict": "passed"},
            {"runId": "evaluation-run:pi_receipt_1", "caseVerdict": "passed"},
        ],
        "scopeResults": [scope_a, scope_b],
        "aggregate": {
            "qualificationState": "qualified",
            "executedRunCount": 2,
            "passedRunCount": 2,
            "failedRunCount": 0,
            "inconclusiveRunCount": 0,
        },
    }
    request = {
        "qualificationSubject": copy.deepcopy(subject),
        "qualificationSubjectSha256": canonical_sha256(subject),
        "scopeId": scope_a["scopeId"],
        "toolBindings": [copy.deepcopy(tool_a)],
        "claimBindings": [copy.deepcopy(claim_a)],
        "budgets": budget(8192, 2),
    }
    return {"result": result, "request": request}


def validate_qualification(fixture: dict[str, Any]) -> None:
    result = fixture["result"]
    request = fixture["request"]
    aggregate = result["aggregate"]
    if result["state"] != "sealed" or aggregate["qualificationState"] == "unrun":
        reject("QUAL_UNRUN", "qualification result is not a sealed executed result")
    if not result["runs"] and aggregate["executedRunCount"] > 0:
        reject("QUAL_COUNT_ONLY", "asserted qualification counts have no case outcomes")
    counts = {
        "executedRunCount": len(result["runs"]),
        "passedRunCount": sum(run["caseVerdict"] == "passed" for run in result["runs"]),
        "failedRunCount": sum(run["caseVerdict"] == "failed" for run in result["runs"]),
        "inconclusiveRunCount": sum(run["caseVerdict"] == "inconclusive" for run in result["runs"]),
    }
    if any(aggregate[key] != value for key, value in counts.items()):
        reject("QUAL_COUNT_MISMATCH", "qualification aggregates do not match run outcomes")
    if canonical_sha256(result["qualificationSubject"]) != result["qualificationSubjectSha256"]:
        reject("QUAL_SUBJECT_MISMATCH", "result subject digest is invalid")
    if canonical_sha256(request["qualificationSubject"]) != request["qualificationSubjectSha256"]:
        reject("QUAL_SUBJECT_MISMATCH", "request subject digest is invalid")
    if request["qualificationSubjectSha256"] != result["qualificationSubjectSha256"]:
        reject("QUAL_SUBJECT_MISMATCH", "model/runtime/harness/adapter/prompt/context-compiler subject differs")
    scopes = {scope["scopeId"]: scope for scope in result["scopeResults"] if scope["outcome"] == "passed"}
    scope = scopes.get(request["scopeId"])
    if scope is None:
        reject("QUAL_SCOPE_UNKNOWN", "requested qualification scope is not passed")
    all_tools = [item for row in scopes.values() for item in row["toolBindings"]]
    all_claims = [item for row in scopes.values() for item in row["claimBindings"]]
    for item in request["toolBindings"]:
        if item not in scope["toolBindings"]:
            code = "QUAL_SCOPE_UNION" if item in all_tools else "QUAL_SCOPE_UNSUPPORTED"
            reject(code, "requested tool is not in the named scope")
    for item in request["claimBindings"]:
        if item not in scope["claimBindings"]:
            code = "QUAL_SCOPE_UNION" if item in all_claims else "QUAL_SCOPE_UNSUPPORTED"
            reject(code, "requested claim/evaluator/negative-control tuple is not in the named scope")
    for field in BUDGET_FIELDS:
        if request["budgets"][field] > scope["budgetCeiling"][field]:
            reject("QUAL_BUDGET_EXPANSION", f"requested {field} exceeds the named scope")


def mutate_qualification(fixture: dict[str, Any], mutation: str) -> None:
    if mutation == "none":
        return
    if mutation == "union_tool_and_claim_across_scopes":
        fixture["request"]["claimBindings"] = [copy.deepcopy(fixture["result"]["scopeResults"][1]["claimBindings"][0])]
    elif mutation == "substitute_worker_b_subject":
        subject = make_subject("worker_b")
        fixture["request"]["qualificationSubject"] = subject
        fixture["request"]["qualificationSubjectSha256"] = canonical_sha256(subject)
    elif mutation == "mark_unrun":
        fixture["result"]["aggregate"]["qualificationState"] = "unrun"
    elif mutation == "remove_runs_keep_counts":
        fixture["result"]["runs"] = []
    elif mutation == "inflate_passed_count":
        fixture["result"]["aggregate"]["passedRunCount"] += 1
    else:
        raise ValidationError(f"unknown qualification mutation: {mutation}")


def resource_record(identifier: str, stage: str, purpose: str, context: int, calls: int, peak_cap: int, vram_floor: int) -> dict[str, Any]:
    return {
        "envelopeId": identifier,
        "stage": stage,
        "purpose": purpose,
        "lineageId": "resource-lineage:synthetic_local",
        "parentEnvelope": None,
        "qualificationSubjectSha256": "A" * 64,
        "effectiveConfigurationSha256": "B" * 64,
        "limits": {
            "budgets": budget(context, calls),
            "resourceCaps": {"maximumPeakVramBytes": peak_cap},
            "admissionFloors": {"minimumFreeVramBeforeLoadBytes": vram_floor},
        },
        "observations": None,
    }


def resource_fixture() -> dict[str, Any]:
    configured = resource_record("resource-envelope:configured", "configured", "qualification", 32768, 8, 30_000, 20_000)
    measured = resource_record("resource-envelope:measured", "measured_safe", "qualification", 16384, 4, 26_000, 22_000)
    requested = resource_record("resource-envelope:requested", "requested", "task", 8192, 2, 24_000, 22_000)
    observed = resource_record("resource-envelope:observed", "observed", "task", 8192, 2, 24_000, 22_000)
    measured["parentEnvelope"] = {"id": configured["envelopeId"], "sha256": canonical_sha256(configured)}
    requested["parentEnvelope"] = {"id": measured["envelopeId"], "sha256": canonical_sha256(measured)}
    observed["parentEnvelope"] = {"id": requested["envelopeId"], "sha256": canonical_sha256(requested)}
    observed["observations"] = {
        "actualBudgetUse": budget(6000, 2),
        "preflightFreeVramBytes": 25_000,
        "peakVramBytes": 23_000,
    }
    return {row["envelopeId"]: row for row in (configured, measured, requested, observed)}


def rebind_resource_child(records: dict[str, Any], child_id: str, parent_id: str) -> None:
    records[child_id]["parentEnvelope"] = {"id": parent_id, "sha256": canonical_sha256(records[parent_id])}


def mutate_resource(records: dict[str, Any], mutation: str) -> None:
    requested = records["resource-envelope:requested"]
    observed = records["resource-envelope:observed"]
    if mutation == "none":
        return
    if mutation == "break_parent_hash":
        observed["parentEnvelope"]["sha256"] = "0" * 64
    elif mutation == "expand_requested_context":
        requested["limits"]["budgets"]["contextTokens"] = 20000
        rebind_resource_child(records, observed["envelopeId"], requested["envelopeId"])
    elif mutation == "change_subject":
        requested["qualificationSubjectSha256"] = "C" * 64
        rebind_resource_child(records, observed["envelopeId"], requested["envelopeId"])
    elif mutation == "change_effective_config":
        requested["effectiveConfigurationSha256"] = "D" * 64
        rebind_resource_child(records, observed["envelopeId"], requested["envelopeId"])
    elif mutation == "exceed_peak_vram":
        observed["observations"]["peakVramBytes"] = 25000
    elif mutation == "insufficient_preflight_vram":
        observed["observations"]["preflightFreeVramBytes"] = 21000
    else:
        raise ValidationError(f"unknown resource mutation: {mutation}")


def validate_resource(records: dict[str, Any]) -> None:
    order = (
        "resource-envelope:configured",
        "resource-envelope:measured",
        "resource-envelope:requested",
        "resource-envelope:observed",
    )
    allowed_edges = {
        ("configured", "measured_safe"),
        ("configured", "requested"),
        ("measured_safe", "requested"),
        ("requested", "observed"),
    }
    root = records[order[0]]
    for identifier in order[1:]:
        row = records[identifier]
        parent_ref = row["parentEnvelope"]
        parent = records.get(parent_ref["id"])
        if parent is None or parent_ref["sha256"] != canonical_sha256(parent):
            reject("RESOURCE_PARENT_MISMATCH", f"resource parent hash mismatch: {identifier}")
        if (parent["stage"], row["stage"]) not in allowed_edges:
            reject("RESOURCE_STAGE_EDGE", f"illegal resource stage edge: {parent['stage']} -> {row['stage']}")
        if row["lineageId"] != root["lineageId"]:
            reject("RESOURCE_LINEAGE_MISMATCH", "resource lineage ID changed")
        if row["qualificationSubjectSha256"] != root["qualificationSubjectSha256"]:
            reject("RESOURCE_SUBJECT_DRIFT", "qualification subject changed inside resource lineage")
        if row["effectiveConfigurationSha256"] != root["effectiveConfigurationSha256"]:
            reject("RESOURCE_CONFIG_DRIFT", "material backend configuration changed inside resource lineage")
        if row["limits"]["budgets"]["sequentialToolCalls"] > row["limits"]["budgets"]["totalToolCalls"]:
            reject("RESOURCE_BUDGET_EXPANSION", "sequential tool horizon exceeds total horizon")

    configured, measured, requested, observed = (records[item] for item in order)
    for child, parent in ((measured, configured), (requested, measured)):
        for field in BUDGET_FIELDS:
            if child["limits"]["budgets"][field] > parent["limits"]["budgets"][field]:
                reject("RESOURCE_BUDGET_EXPANSION", f"resource budget expanded: {field}")
        if child["limits"]["resourceCaps"]["maximumPeakVramBytes"] > parent["limits"]["resourceCaps"]["maximumPeakVramBytes"]:
            reject("RESOURCE_BUDGET_EXPANSION", "VRAM cap expanded")
    if requested["limits"]["admissionFloors"]["minimumFreeVramBeforeLoadBytes"] < measured["limits"]["admissionFloors"]["minimumFreeVramBeforeLoadBytes"]:
        reject("RESOURCE_BUDGET_EXPANSION", "requested VRAM floor is weaker than measured safe")
    actual = observed["observations"]["actualBudgetUse"]
    for field in BUDGET_FIELDS:
        if actual[field] > requested["limits"]["budgets"][field]:
            reject("RESOURCE_OBSERVED_OVERFLOW", f"observed budget overflow: {field}")
    if observed["observations"]["peakVramBytes"] > requested["limits"]["resourceCaps"]["maximumPeakVramBytes"]:
        reject("RESOURCE_OBSERVED_OVERFLOW", "observed peak VRAM exceeds requested cap")
    if observed["observations"]["preflightFreeVramBytes"] < requested["limits"]["admissionFloors"]["minimumFreeVramBeforeLoadBytes"]:
        reject("RESOURCE_VRAM_FLOOR", "preflight VRAM is below the requested admission floor")


def quality_events() -> dict[str, int]:
    return {
        "evidenceDefects": 0,
        "evaluatorFalseGreens": 0,
        "authorityViolations": 0,
        "scopeViolations": 0,
        "securityOrPrivacyEvents": 0,
        "rollbackEvents": 0,
    }


def human_operations(intent: int, routine: int) -> dict[str, int | None]:
    return {
        "intent": intent,
        "subjectiveOrRuntimeException": 0,
        "promotionOrPublication": 0,
        "unresolvedTrust": 0,
        "routineProtocol": routine,
        "otherException": 0,
    }


def efficacy_observation(identifier: str, *, accepted: bool, intent: int, routine: int, prep: int, retry: int) -> dict[str, Any]:
    return {
        "observationId": identifier,
        "taskStratumId": "code.small",
        "acceptedClosure": accepted,
        "humanOperationsByReason": human_operations(intent, routine),
        "protocolPreparationOperations": prep,
        "retryCount": retry,
        "escalationCount": 0,
        "candidatePromoted": accepted,
        "qualityEvents": quality_events(),
    }


def efficacy_fixture(scenario: str) -> dict[str, Any]:
    baseline_rows = [
        efficacy_observation(f"efficacy-observation:baseline_{index}", accepted=True, intent=1, routine=1, prep=2, retry=1 if index == 1 else 0)
        for index in range(1, 4)
    ]
    candidate_rows = [
        efficacy_observation(f"efficacy-observation:candidate_{index}", accepted=True, intent=1, routine=0, prep=1, retry=0)
        for index in range(1, 4)
    ]
    decision = "advance"
    if scenario == "rollback":
        candidate_rows[0]["qualityEvents"]["evaluatorFalseGreens"] = 1
        decision = "rollback"
    elif scenario == "simplify":
        for row in candidate_rows:
            row["humanOperationsByReason"]["routineProtocol"] = 3
            row["protocolPreparationOperations"] = 4
        decision = "simplify"
    elif scenario == "hold":
        candidate_rows[2]["acceptedClosure"] = False
        candidate_rows[2]["candidatePromoted"] = False
        decision = "hold"
    elif scenario != "advance":
        raise ValidationError(f"unknown efficacy scenario: {scenario}")

    metric_definitions = [
        {"metricId": "metric:accepted_closure_rate", "source": "acceptedClosureRate", "direction": "higher_is_better", "required": True, "humanBurden": False},
        {"metricId": "metric:human_operations", "source": "humanOperationsPerAcceptedClosure", "direction": "lower_is_better", "required": True, "humanBurden": True},
        {"metricId": "metric:routine_protocol", "source": "routineProtocolOperationsPerAcceptedClosure", "direction": "lower_is_better", "required": True, "humanBurden": True},
        {"metricId": "metric:protocol_preparation", "source": "protocolPreparationOperationsPerAcceptedClosure", "direction": "lower_is_better", "required": True, "humanBurden": True},
        {"metricId": "metric:retry_rate", "source": "retryRate", "direction": "lower_is_better", "required": True, "humanBurden": False},
    ]
    thresholds = {
        "metric:accepted_closure_rate": {"kind": "relative", "value": Decimal("0.10"), "minimumImprovement": None},
        "metric:human_operations": {"kind": "relative", "value": Decimal("0.10"), "minimumImprovement": Decimal("0.20")},
        "metric:routine_protocol": {"kind": "absolute", "value": Decimal("0.20"), "minimumImprovement": None},
        "metric:protocol_preparation": {"kind": "relative", "value": Decimal("0.10"), "minimumImprovement": None},
        "metric:retry_rate": {"kind": "absolute", "value": Decimal("0.20"), "minimumImprovement": None},
    }
    return {
        "plan": {
            "state": "frozen",
            "frozenAt": "2026-08-01T12:00:00Z",
            "baseline": {"startAt": "2026-07-01T00:00:00Z", "endAt": "2026-07-31T23:00:00Z", "observations": baseline_rows},
            "candidateWindow": {"earliestStartAt": "2026-08-02T00:00:00Z", "maximumEndAt": "2026-08-31T23:59:59Z", "minimumTasks": 3, "minimumAcceptedClosures": 2, "requiredStrata": ["code.small"]},
            "metricDefinitions": metric_definitions,
            "thresholds": thresholds,
            "hardGuardrails": list(GUARDRAIL_FIELDS),
        },
        "report": {
            "state": "sealed",
            "startedAt": "2026-08-02T12:00:00Z",
            "completedAt": "2026-08-03T12:00:00Z",
            "candidateObservations": candidate_rows,
            "decision": decision,
        },
    }


def mutate_efficacy(fixture: dict[str, Any], mutation: str) -> None:
    if mutation == "none":
        return
    if mutation == "freeze_after_candidate_start":
        fixture["plan"]["frozenAt"] = "2026-08-03T00:00:00Z"
    elif mutation == "remove_candidate_observation":
        fixture["report"]["candidateObservations"].pop()
    elif mutation == "null_human_operations":
        fixture["report"]["candidateObservations"][0]["humanOperationsByReason"]["routineProtocol"] = None
    elif mutation == "claim_advance":
        fixture["report"]["decision"] = "advance"
    else:
        raise ValidationError(f"unknown efficacy mutation: {mutation}")


def decimal_ratio(numerator: int, denominator: int) -> Decimal:
    if denominator == 0:
        reject("EFFICACY_SAMPLE_INCOMPLETE", "accepted-closure denominator is zero")
    return Decimal(numerator) / Decimal(denominator)


def metric_value(source: str, rows: list[dict[str, Any]]) -> Decimal:
    accepted = sum(row["acceptedClosure"] for row in rows)
    if source == "acceptedClosureRate":
        return decimal_ratio(accepted, len(rows))
    if source == "humanOperationsPerAcceptedClosure":
        total = sum(sum(row["humanOperationsByReason"][key] for key in HUMAN_REASON_FIELDS) for row in rows)
        return decimal_ratio(total, accepted)
    if source == "routineProtocolOperationsPerAcceptedClosure":
        return decimal_ratio(sum(row["humanOperationsByReason"]["routineProtocol"] for row in rows), accepted)
    if source == "protocolPreparationOperationsPerAcceptedClosure":
        return decimal_ratio(sum(row["protocolPreparationOperations"] for row in rows), accepted)
    if source == "retryRate":
        return decimal_ratio(sum(row["retryCount"] for row in rows), len(rows))
    raise ValidationError(f"unsupported synthetic efficacy metric source: {source}")


def metric_passes(direction: str, baseline: Decimal, candidate: Decimal, threshold: dict[str, Any]) -> bool:
    margin = threshold["value"]
    if threshold["kind"] == "relative":
        if baseline == 0:
            reject("EFFICACY_THRESHOLD_INVALID", "relative margin cannot use a zero baseline")
        boundary = baseline * (Decimal(1) + margin if direction == "lower_is_better" else Decimal(1) - margin)
    else:
        boundary = baseline + margin if direction == "lower_is_better" else baseline - margin
    return candidate <= boundary if direction == "lower_is_better" else candidate >= boundary


def validate_efficacy(fixture: dict[str, Any]) -> str:
    plan = fixture["plan"]
    report = fixture["report"]
    baseline = plan["baseline"]["observations"]
    candidate = report["candidateObservations"]
    baseline_end = parse_datetime(plan["baseline"]["endAt"], "baseline.endAt")
    frozen_at = parse_datetime(plan["frozenAt"], "plan.frozenAt")
    earliest = parse_datetime(plan["candidateWindow"]["earliestStartAt"], "candidateWindow.earliestStartAt")
    started = parse_datetime(report["startedAt"], "report.startedAt")
    if not (baseline_end <= frozen_at < earliest <= started):
        reject("EFFICACY_BASELINE_POSTHOC", "baseline and thresholds were not frozen before the candidate window")
    if len(candidate) < plan["candidateWindow"]["minimumTasks"]:
        reject("EFFICACY_SAMPLE_INCOMPLETE", "candidate sample is below the frozen minimum")
    accepted = sum(row["acceptedClosure"] for row in candidate)
    if accepted < plan["candidateWindow"]["minimumAcceptedClosures"]:
        reject("EFFICACY_SAMPLE_INCOMPLETE", "accepted closures are below the frozen minimum")
    strata = {row["taskStratumId"] for row in candidate}
    if not set(plan["candidateWindow"]["requiredStrata"]).issubset(strata):
        reject("EFFICACY_SAMPLE_INCOMPLETE", "candidate sample omits a required stratum")
    for row in baseline + candidate:
        human = row.get("humanOperationsByReason")
        if not isinstance(human, dict) or any(human.get(key) is None for key in HUMAN_REASON_FIELDS):
            reject("EFFICACY_HUMAN_BURDEN_MISSING", "human burden is missing and cannot be treated as zero")
        if row.get("protocolPreparationOperations") is None:
            reject("EFFICACY_HUMAN_BURDEN_MISSING", "protocol preparation burden is missing")

    guardrail_failed = any(
        sum(row["qualityEvents"][field] for row in candidate) > 0
        for field in plan["hardGuardrails"]
    )
    human_failure = False
    other_failure = False
    improvement = False
    for definition in plan["metricDefinitions"]:
        baseline_value = metric_value(definition["source"], baseline)
        candidate_value = metric_value(definition["source"], candidate)
        threshold = plan["thresholds"][definition["metricId"]]
        passed = metric_passes(definition["direction"], baseline_value, candidate_value, threshold)
        if definition["required"] and not passed:
            if definition["humanBurden"]:
                human_failure = True
            else:
                other_failure = True
        minimum = threshold["minimumImprovement"]
        if minimum is not None:
            delta = baseline_value - candidate_value if definition["direction"] == "lower_is_better" else candidate_value - baseline_value
            improvement = improvement or delta >= minimum

    if guardrail_failed:
        expected = "rollback"
    elif human_failure:
        expected = "simplify"
    elif other_failure or not improvement:
        expected = "hold"
    else:
        expected = "advance"
    if report["decision"] != expected:
        reject("EFFICACY_DECISION_MISMATCH", f"reported {report['decision']} but recomputed {expected}")
    return expected


def validate_vectors(vectors_document: dict[str, Any]) -> tuple[int, int, dict[str, int]]:
    require(
        set(vectors_document) == {"schemaVersion", "vectorSetId", "state", "authority", "vectors"},
        "adoption vector document has missing or extra fields",
    )
    require(vectors_document["schemaVersion"] == VERSION, "adoption vector version mismatch")
    require(vectors_document["state"] == "template_inert", "adoption vectors are not inert")
    validate_non_authority(vectors_document["authority"], VECTOR_PATH)
    rows = vectors_document["vectors"]
    require(isinstance(rows, list) and rows, "adoption vector corpus is empty")
    required_fields = {"caseId", "category", "scenario", "mutation", "expected", "expectedCode", "expectedDecision"}
    require(all(isinstance(row, dict) and set(row) == required_fields for row in rows), "adoption vector row is incomplete or extra")
    identifiers = [row["caseId"] for row in rows]
    require(len(identifiers) == len(set(identifiers)), "adoption vector IDs are duplicated")

    valid_count = 0
    rejected_count = 0
    category_counts: dict[str, int] = {"qualification": 0, "resource": 0, "efficacy": 0}
    for row in rows:
        category = row["category"]
        require(category in category_counts, f"unknown vector category: {category}")
        category_counts[category] += 1
        observed_code = "OK"
        observed_decision: str | None = None
        try:
            if category == "qualification":
                fixture = qualification_fixture()
                mutate_qualification(fixture, row["mutation"])
                validate_qualification(fixture)
            elif category == "resource":
                fixture = resource_fixture()
                mutate_resource(fixture, row["mutation"])
                validate_resource(fixture)
            else:
                fixture = efficacy_fixture(row["scenario"])
                mutate_efficacy(fixture, row["mutation"])
                observed_decision = validate_efficacy(fixture)
        except SemanticError as exc:
            observed_code = exc.code

        if row["expected"] == "valid":
            require(observed_code == "OK", f"valid vector rejected: {row['caseId']}: {observed_code}")
            require(observed_decision == row["expectedDecision"], f"decision mismatch: {row['caseId']}")
            valid_count += 1
        else:
            require(row["expected"] == "reject", f"invalid expected verdict: {row['caseId']}")
            require(observed_code == row["expectedCode"], f"malicious vector got {observed_code}, expected {row['expectedCode']}: {row['caseId']}")
            rejected_count += 1
    return valid_count, rejected_count, category_counts


def main() -> int:
    try:
        closed_object_count = 0
        for schema_path, template_path in SCHEMA_TEMPLATE_PAIRS:
            schema = load_json(schema_path)
            template = load_json(template_path)
            closed_object_count += validate_closed_schema(schema, schema_path)
            validate_instance(template, schema, schema)
            validate_inert_template(template, template_path)

        valid_count, rejected_count, category_counts = validate_vectors(load_json(VECTOR_PATH))
        total = valid_count + rejected_count
        print(
            "PASS — ELAD 0.4.0 bounded adoption slice: "
            f"5 closed schemas ({closed_object_count} closed object nodes), "
            "5 structurally valid inert templates, "
            f"{total} semantic vectors ({valid_count} valid, {rejected_count} malicious rejected; "
            f"qualification={category_counts['qualification']}, resource={category_counts['resource']}, "
            f"efficacy={category_counts['efficacy']}). No authority granted."
        )
        return 0
    except (OSError, ValidationError) as exc:
        print(f"FAIL — {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
