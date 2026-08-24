#!/usr/bin/env python3
"""Dependency-free checks for the ELAD 0.3 adaptive-rigor core.

This validator is read-only. A rigor decision selects evidence posture only; it never
grants mutation, evidence-acceptance, promotion, publication, or target authority.
"""

from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "spec" / "registries" / "task-rigor-profiles.json"
SCHEMA_PATH = ROOT / "spec" / "schemas" / "task-rigor-decision.schema.json"
TEMPLATE_PATH = ROOT / "templates" / "task-rigor-decision.template.json"
VECTORS_PATH = ROOT / "tests" / "task-rigor-vectors.json"
DOC_PATH = ROOT / "docs" / "ADAPTIVE_RIGOR.md"
LIGHT_TEMPLATE_PATH = ROOT / "templates" / "LIGHT_TASK.template.md"

VERSION = "0.3.0"
REGISTRY_ID = "vocabulary:elad_task_rigor_profiles_0.3.0"
REGISTRY_REPO_PATH = "spec/registries/task-rigor-profiles.json"
PROFILES = ["light", "bounded", "evaluated", "assured"]
RANK = {name: index for index, name in enumerate(PROFILES)}

DIMENSION_KEYS = {
    "uncertainty",
    "complexity",
    "reversibility",
    "consequence",
    "delegationDistance",
}
CLAIM_DOMAINS = {
    "static_deterministic",
    "semantic_or_stochastic",
    "runtime_or_operational",
}
TASK_EFFECTS = {
    "read_only",
    "reversible_artifact_change",
    "stateful_reversible_change",
    "irreversible_or_durable_external_effect",
}
EVALUATOR_CLASSES = {"exact_deterministic", "fallible"}
EVALUATOR_MATURITIES = {"not_applicable", "proven", "partial", "unproven", "none"}
CLAIM_KEYS = {"claimDomain", "evaluatorClass", "evaluatorMaturity"}
APPLICABILITY_KEYS = {"claims", "taskEffect"}
DECISION_KEYS = {
    "schemaVersion",
    "decisionId",
    "state",
    "authorityEffect",
    "registry",
    "loop",
    "dimensions",
    "evidenceApplicability",
    "recommendedMinimumProfile",
    "selectedProfile",
    "higherRigorReason",
    "evidenceStrategy",
    "evidencePlan",
    "escalationTriggers",
    "simplificationTriggers",
    "scaffolding",
    "rationale",
}
ITERATION_KEYS = {
    "iterationId",
    "tryingToEstablish",
    "materialUncertainty",
    "cheapestReliableEvidence",
    "evidenceSource",
    "observedResult",
    "nextChange",
    "completionBasis",
}
EVIDENCE_KEYS = {
    "evidenceKind",
    "sourceId",
    "expectedResult",
    "detectsFailure",
    "independence",
}
SCAFFOLD_KEYS = {
    "reuseExisting",
    "createOnceOrPeriodic",
    "recurForThisTask",
    "proportionalityRationale",
}


class ValidationFailure(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


def require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise ValidationFailure(code, message)


def load_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationFailure("E-JSON", f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc
    require(isinstance(value, dict), "E-JSON", f"{path.relative_to(ROOT)} is not an object")
    return value


def canonical_sha256(value: dict[str, Any]) -> str:
    payload = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def exact_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    require(isinstance(value, dict), "E-SCHEMA", f"{label} is not an object")
    require(set(value) == keys, "E-SCHEMA", f"{label} fields are incomplete or extra")
    return value


def validate_registry(registry: dict[str, Any]) -> None:
    top_keys = {
        "schemaVersion",
        "registryId",
        "status",
        "authorityEffect",
        "description",
        "profileOrder",
        "selectionDimensions",
        "compoundEscalations",
        "evidenceKindOrder",
        "evidenceModules",
        "profiles",
        "escalationTriggers",
        "simplificationTriggers",
    }
    exact_object(registry, top_keys, "task-rigor registry")
    require(registry["schemaVersion"] == VERSION, "E-REGISTRY", "registry version changed")
    require(registry["registryId"] == REGISTRY_ID, "E-REGISTRY", "registry identity changed")
    require(registry["status"] == "reference_only", "E-REGISTRY", "registry is not reference-only")
    require(registry["authorityEffect"] == "none", "E-AUTHORITY", "registry claims authority")
    require(nonempty(registry["description"]), "E-REGISTRY", "registry description is empty")
    require(registry["profileOrder"] == PROFILES, "E-REGISTRY", "profile order changed")

    expected_domains = {
        "uncertainty": {"low", "moderate", "high"},
        "complexity": {"low", "moderate", "high"},
        "reversibility": {"easy", "managed", "difficult", "irreversible"},
        "consequence": {"low", "moderate", "high", "critical"},
        "delegationDistance": {
            "same_episode",
            "supervised_worker",
            "bounded_handoff",
            "autonomous_cross_context",
            "external_target",
        },
    }
    dimensions = exact_object(registry["selectionDimensions"], DIMENSION_KEYS, "selection dimensions")
    for name, expected in expected_domains.items():
        mapping = dimensions[name]
        require(isinstance(mapping, dict) and set(mapping) == expected, "E-REGISTRY", f"dimension domain changed: {name}")
        require(all(floor in RANK for floor in mapping.values()), "E-REGISTRY", f"unknown profile floor: {name}")

    evidence_order = registry["evidenceKindOrder"]
    require(isinstance(evidence_order, list) and evidence_order, "E-REGISTRY", "evidence kinds are empty")
    require(len(evidence_order) == len(set(evidence_order)), "E-REGISTRY", "evidence kinds are duplicated")

    rows = registry["profiles"]
    require(isinstance(rows, list) and len(rows) == 4, "E-REGISTRY", "registry does not define four profiles")
    profile_keys = {
        "profileId",
        "name",
        "rank",
        "purpose",
        "baseEvidenceKinds",
        "requiresIndependentVerification",
        "requiresMachineReadableDecision",
    }
    for rank, row in enumerate(rows):
        exact_object(row, profile_keys, f"profile row {rank}")
        name = PROFILES[rank]
        require(row["name"] == name and row["profileId"] == f"rigor:{name}", "E-REGISTRY", f"profile identity mismatch: {name}")
        require(row["rank"] == rank, "E-REGISTRY", f"profile rank mismatch: {name}")
        require(nonempty(row["purpose"]), "E-REGISTRY", f"profile purpose is empty: {name}")
        base = row["baseEvidenceKinds"]
        require(isinstance(base, list) and base, "E-REGISTRY", f"profile base evidence is empty: {name}")
        require(len(base) == len(set(base)), "E-REGISTRY", f"profile base evidence is duplicated: {name}")
        require(set(base).issubset(evidence_order), "E-REGISTRY", f"profile has unknown base evidence: {name}")
        require(isinstance(row["requiresIndependentVerification"], bool), "E-REGISTRY", f"independence flag is invalid: {name}")
        require(isinstance(row["requiresMachineReadableDecision"], bool), "E-REGISTRY", f"machine-readable flag is invalid: {name}")
    require(rows[0]["requiresMachineReadableDecision"] is False, "E-REGISTRY", "light profile incorrectly mandates JSON")
    require(rows[3]["requiresIndependentVerification"] is True, "E-REGISTRY", "assured profile lacks independent verification")
    require(all("runtime_or_trace" not in row["baseEvidenceKinds"] for row in rows), "E-REGISTRY", "runtime evidence is hard-coded into a profile base")
    require(all("rollback_proof" not in row["baseEvidenceKinds"] for row in rows), "E-REGISTRY", "rollback evidence is hard-coded into a profile base")
    require(all("evaluator_check" not in row["baseEvidenceKinds"] for row in rows), "E-REGISTRY", "evaluator evidence is hard-coded into a profile base")

    modules = exact_object(registry["evidenceModules"], {"claimDomains", "taskEffects", "evaluatorMaturity"}, "evidence modules")
    claim_modules = exact_object(modules["claimDomains"], CLAIM_DOMAINS, "claim-domain modules")
    effect_modules = exact_object(modules["taskEffects"], TASK_EFFECTS, "task-effect modules")
    evaluator_modules = exact_object(modules["evaluatorMaturity"], EVALUATOR_MATURITIES, "evaluator-maturity modules")
    for label, mapping in (("claim domain", claim_modules), ("task effect", effect_modules)):
        for name, module in mapping.items():
            exact_object(module, {"description", "minimumProfile", "requiredEvidenceKinds"}, f"{label} module {name}")
            require(nonempty(module["description"]), "E-REGISTRY", f"{label} description is empty: {name}")
            require(module["minimumProfile"] in RANK, "E-REGISTRY", f"{label} module has unknown profile floor: {name}")
            evidence = module["requiredEvidenceKinds"]
            require(isinstance(evidence, list) and len(evidence) == len(set(evidence)), "E-REGISTRY", f"{label} module evidence is invalid: {name}")
            require(set(evidence).issubset(evidence_order), "E-REGISTRY", f"{label} module has unknown evidence: {name}")
    for name, module in evaluator_modules.items():
        exact_object(module, {"minimumProfile", "requiredEvidenceKinds"}, f"evaluator-maturity module {name}")
        require(module["minimumProfile"] in RANK, "E-REGISTRY", f"evaluator module has unknown profile floor: {name}")
        evidence = module["requiredEvidenceKinds"]
        require(isinstance(evidence, list) and len(evidence) == len(set(evidence)), "E-REGISTRY", f"evaluator module evidence is invalid: {name}")
        require(set(evidence).issubset(evidence_order), "E-REGISTRY", f"evaluator module has unknown evidence: {name}")

    rules = registry["compoundEscalations"]
    require(isinstance(rules, list) and rules, "E-REGISTRY", "compound escalation rules are empty")
    rule_ids: list[str] = []
    for rule in rules:
        exact_object(rule, {"ruleId", "all", "minimumProfile"}, "compound escalation rule")
        require(nonempty(rule["ruleId"]), "E-REGISTRY", "compound rule ID is empty")
        rule_ids.append(rule["ruleId"])
        predicates = rule["all"]
        require(isinstance(predicates, dict) and predicates and set(predicates).issubset(DIMENSION_KEYS), "E-REGISTRY", "compound predicates are invalid")
        for dimension, values in predicates.items():
            require(isinstance(values, list) and values, "E-REGISTRY", "compound predicate is empty")
            require(set(values).issubset(dimensions[dimension]), "E-REGISTRY", "compound predicate uses unknown value")
        require(rule["minimumProfile"] in RANK, "E-REGISTRY", "compound rule has unknown profile")
    require(len(rule_ids) == len(set(rule_ids)), "E-REGISTRY", "compound rule IDs are duplicated")

    for field in ("escalationTriggers", "simplificationTriggers"):
        values = registry[field]
        require(isinstance(values, list) and values, "E-REGISTRY", f"{field} is empty")
        require(len(values) == len(set(values)), "E-REGISTRY", f"{field} has duplicates")


def validate_schema_contract(schema: dict[str, Any], registry: dict[str, Any]) -> None:
    require(schema.get("$id") == "urn:elad:schema:task-rigor-decision:0.3.0", "E-SCHEMA-CONTRACT", "schema ID changed")
    require(schema.get("type") == "object" and schema.get("additionalProperties") is False, "E-SCHEMA-CONTRACT", "schema root is not closed")
    require(set(schema.get("required", [])) == DECISION_KEYS, "E-SCHEMA-CONTRACT", "schema required fields changed")
    properties = schema.get("properties", {})
    require(set(properties) == DECISION_KEYS, "E-SCHEMA-CONTRACT", "schema properties changed")
    require(properties["authorityEffect"].get("const") == "none", "E-AUTHORITY", "schema permits authority effects")

    defs = schema.get("$defs", {})
    require(defs.get("profileName", {}).get("enum") == PROFILES, "E-SCHEMA-CONTRACT", "schema profile domain differs")
    schema_dimensions = properties["dimensions"]["properties"]
    require(set(schema_dimensions) == DIMENSION_KEYS, "E-SCHEMA-CONTRACT", "schema dimensions changed")
    for name in DIMENSION_KEYS:
        require(set(schema_dimensions[name]["enum"]) == set(registry["selectionDimensions"][name]), "E-SCHEMA-CONTRACT", f"schema dimension differs: {name}")
    applicability = properties["evidenceApplicability"]
    require(applicability.get("additionalProperties") is False and set(applicability.get("required", [])) == APPLICABILITY_KEYS, "E-SCHEMA-CONTRACT", "schema applicability shape changed")
    claim_schema = defs["claimClass"]
    require(claim_schema.get("additionalProperties") is False and set(claim_schema.get("required", [])) == CLAIM_KEYS, "E-SCHEMA-CONTRACT", "schema claim-class shape changed")
    require(set(claim_schema["properties"]["claimDomain"]["enum"]) == CLAIM_DOMAINS, "E-SCHEMA-CONTRACT", "schema claim domains differ")
    require(set(claim_schema["properties"]["evaluatorClass"]["enum"]) == EVALUATOR_CLASSES, "E-SCHEMA-CONTRACT", "schema evaluator classes differ")
    require(set(claim_schema["properties"]["evaluatorMaturity"]["enum"]) == EVALUATOR_MATURITIES, "E-SCHEMA-CONTRACT", "schema evaluator maturities differ")
    require(set(applicability["properties"]["taskEffect"]["enum"]) == TASK_EFFECTS, "E-SCHEMA-CONTRACT", "schema task effects differ")
    evidence_enum = defs["evidenceItem"]["properties"]["evidenceKind"]["enum"]
    require(evidence_enum == registry["evidenceKindOrder"], "E-SCHEMA-CONTRACT", "schema evidence kinds differ")
    require(defs["escalationTrigger"]["enum"] == registry["escalationTriggers"], "E-SCHEMA-CONTRACT", "schema escalation triggers differ")
    require(defs["simplificationTrigger"]["enum"] == registry["simplificationTriggers"], "E-SCHEMA-CONTRACT", "schema simplification triggers differ")
    require(set(defs["iteration"]["required"]) == ITERATION_KEYS, "E-SCHEMA-CONTRACT", "schema does not encode all seven loop questions")


def validate_applicability(applicability: Any, dimensions: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    applicability = exact_object(applicability, APPLICABILITY_KEYS, "evidence applicability")
    claims = applicability["claims"]
    require(isinstance(claims, list) and claims, "E-APPLICABILITY", "claim domains are empty")
    claim_domains: list[str] = []
    for claim in claims:
        exact_object(claim, CLAIM_KEYS, "claim class")
        domain = claim["claimDomain"]
        evaluator_class = claim["evaluatorClass"]
        maturity = claim["evaluatorMaturity"]
        require(domain in CLAIM_DOMAINS, "E-APPLICABILITY", "claim domain is unknown")
        require(evaluator_class in EVALUATOR_CLASSES, "E-APPLICABILITY", "evaluator class is unknown")
        require(maturity in EVALUATOR_MATURITIES, "E-APPLICABILITY", "evaluator maturity is unknown")
        if evaluator_class == "exact_deterministic":
            require(maturity == "not_applicable", "E-EVALUATOR-CLASS", "exact deterministic evaluator uses fallible maturity")
        else:
            require(maturity != "not_applicable", "E-EVALUATOR-CLASS", "fallible evaluator omits maturity")
        claim_domains.append(domain)
    require(len(claim_domains) == len(set(claim_domains)), "E-APPLICABILITY", "claim domains are duplicated")
    effect = applicability["taskEffect"]
    require(effect in TASK_EFFECTS, "E-APPLICABILITY", "task effect is unknown")
    allowed_reversibility = {
        "read_only": {"easy"},
        "reversible_artifact_change": {"easy", "managed"},
        "stateful_reversible_change": {"managed", "difficult"},
        "irreversible_or_durable_external_effect": {"irreversible"},
    }
    require(dimensions.get("reversibility") in allowed_reversibility[effect], "E-EFFECT-CONTRADICTION", "task effect contradicts reversibility")
    modules = registry["evidenceModules"]
    require(set(modules["claimDomains"]) == CLAIM_DOMAINS and set(modules["taskEffects"]) == TASK_EFFECTS, "E-REGISTRY", "applicability modules changed")
    return applicability


def minimum_profile(dimensions: dict[str, Any], applicability: dict[str, Any], registry: dict[str, Any]) -> str:
    exact_object(dimensions, DIMENSION_KEYS, "decision dimensions")
    rank = 0
    floors = registry["selectionDimensions"]
    for name in DIMENSION_KEYS:
        value = dimensions[name]
        require(value in floors[name], "E-DIMENSION", f"unknown value for {name}: {value}")
        rank = max(rank, RANK[floors[name][value]])
    validate_applicability(applicability, dimensions, registry)
    for rule in registry["compoundEscalations"]:
        if all(dimensions[name] in values for name, values in rule["all"].items()):
            rank = max(rank, RANK[rule["minimumProfile"]])
    modules = registry["evidenceModules"]
    for claim in applicability["claims"]:
        rank = max(rank, RANK[modules["claimDomains"][claim["claimDomain"]]["minimumProfile"]])
        rank = max(rank, RANK[modules["evaluatorMaturity"][claim["evaluatorMaturity"]]["minimumProfile"]])
    rank = max(rank, RANK[modules["taskEffects"][applicability["taskEffect"]]["minimumProfile"]])
    return PROFILES[rank]


def validate_registry_reference(reference: Any, registry: dict[str, Any], state: str) -> None:
    reference = exact_object(reference, {"id", "path", "sha256", "schemaVersion"}, "registry reference")
    require(reference["id"] == REGISTRY_ID, "E-REGISTRY-REFERENCE", "registry ID mismatch")
    require(reference["path"] == REGISTRY_REPO_PATH, "E-REGISTRY-REFERENCE", "registry path mismatch")
    require(reference["schemaVersion"] == VERSION, "E-REGISTRY-REFERENCE", "registry version mismatch")
    digest = reference["sha256"]
    require(isinstance(digest, str) and re.fullmatch(r"[A-F0-9]{64}", digest), "E-REGISTRY-REFERENCE", "registry digest is malformed")
    if state == "template_inert":
        require(digest == "0" * 64, "E-REGISTRY-REFERENCE", "template digest is not inert")
    else:
        require(digest != "0" * 64, "E-REGISTRY-REFERENCE", "operational decision uses a placeholder digest")
        require(digest == canonical_sha256(registry), "E-REGISTRY-REFERENCE", "registry digest mismatch")


def validate_loop(loop: Any, state: str) -> None:
    require(isinstance(loop, list) and loop, "E-SCHEMA", "seven-question loop is empty")
    ids: set[str] = set()
    for index, iteration in enumerate(loop):
        exact_object(iteration, ITERATION_KEYS, f"loop iteration {index}")
        iteration_id = iteration["iterationId"]
        require(isinstance(iteration_id, str) and re.fullmatch(r"iteration:[a-z0-9][a-z0-9._-]*", iteration_id), "E-SCHEMA", "iteration ID is malformed")
        require(iteration_id not in ids, "E-SCHEMA", "iteration ID is duplicated")
        ids.add(iteration_id)
        for field in ("tryingToEstablish", "materialUncertainty", "cheapestReliableEvidence"):
            require(nonempty(iteration[field]), "E-SCHEMA", f"loop field is empty: {field}")
        require(iteration["evidenceSource"] in {"deterministic", "runtime_or_trace", "calibrated_model", "external_human", "mixed"}, "E-SCHEMA", "loop evidence source is unknown")
        for field in ("observedResult", "nextChange", "completionBasis"):
            require(iteration[field] is None or nonempty(iteration[field]), "E-SCHEMA", f"loop result field is invalid: {field}")
        observed = iteration["observedResult"] is not None
        has_next = iteration["nextChange"] is not None
        complete = iteration["completionBasis"] is not None
        require(not (has_next and complete), "E-LOOP-STATE", "iteration cannot continue and complete")
        require((not observed and not has_next and not complete) or (observed and (has_next != complete)), "E-LOOP-STATE", "iteration observation and decision are inconsistent")
        if index < len(loop) - 1:
            require(observed and has_next and not complete, "E-LOOP-STATE", "only a continuing iteration may precede another")
    last = loop[-1]
    if state in {"template_inert", "planned"}:
        require(last["observedResult"] is None and last["nextChange"] is None and last["completionBasis"] is None, "E-LOOP-STATE", "planned state claims a result")
    elif state == "observed":
        require(last["observedResult"] is not None and last["nextChange"] is not None and last["completionBasis"] is None, "E-LOOP-STATE", "observed state lacks next change")
    elif state == "complete":
        require(last["observedResult"] is not None and last["nextChange"] is None and last["completionBasis"] is not None, "E-LOOP-STATE", "complete state lacks completion basis")
    elif state != "superseded":
        raise ValidationFailure("E-SCHEMA", f"unknown decision state: {state}")


def validate_strategy(strategy: Any) -> None:
    keys = {
        "cheapestReliableEvidence",
        "whyReliable",
        "sourceClass",
        "independenceBasis",
        "nextEvidenceIfInconclusive",
    }
    exact_object(strategy, keys, "evidence strategy")
    for field in ("cheapestReliableEvidence", "whyReliable", "independenceBasis", "nextEvidenceIfInconclusive"):
        require(nonempty(strategy[field]), "E-EVIDENCE-STRATEGY", f"evidence strategy is empty: {field}")
    require(strategy["sourceClass"] in {"deterministic", "runtime_or_trace", "calibrated_model", "external_human", "mixed"}, "E-EVIDENCE-STRATEGY", "evidence source class is unknown")


def required_evidence_kinds(selected: str, dimensions: dict[str, Any], applicability: dict[str, Any], registry: dict[str, Any]) -> set[str]:
    row = next(profile for profile in registry["profiles"] if profile["name"] == selected)
    required = set(row["baseEvidenceKinds"])
    modules = registry["evidenceModules"]
    for claim in applicability["claims"]:
        required.update(modules["claimDomains"][claim["claimDomain"]]["requiredEvidenceKinds"])
        required.update(modules["evaluatorMaturity"][claim["evaluatorMaturity"]]["requiredEvidenceKinds"])
    required.update(modules["taskEffects"][applicability["taskEffect"]]["requiredEvidenceKinds"])
    return required


def validate_evidence(plan: Any, selected: str, dimensions: dict[str, Any], applicability: dict[str, Any], registry: dict[str, Any]) -> None:
    require(isinstance(plan, list) and plan, "E-EVIDENCE-MINIMUM", "evidence plan is empty")
    allowed_kinds = set(registry["evidenceKindOrder"])
    allowed_independence = {
        "predeclared_expectation",
        "existing_external_oracle",
        "independent_fixture",
        "independent_runtime_observation",
        "calibrated_evaluator",
        "external_human",
        "independent_verifier",
    }
    kinds: list[str] = []
    for index, item in enumerate(plan):
        exact_object(item, EVIDENCE_KEYS, f"evidence item {index}")
        require(item["evidenceKind"] in allowed_kinds, "E-EVIDENCE-MINIMUM", "unknown evidence kind")
        kinds.append(item["evidenceKind"])
        for field in ("sourceId", "expectedResult", "detectsFailure"):
            require(nonempty(item[field]), "E-EVIDENCE-MINIMUM", f"evidence field is empty: {field}")
        require(item["independence"] in allowed_independence, "E-EVIDENCE-MINIMUM", "unknown independence basis")
    require(len(kinds) == len(set(kinds)), "E-EVIDENCE-DUPLICATE", "evidence kinds are duplicated")
    missing = required_evidence_kinds(selected, dimensions, applicability, registry) - set(kinds)
    require(not missing, "E-EVIDENCE-MINIMUM", f"selected profile lacks: {sorted(missing)}")


def validate_triggers(decision: dict[str, Any], registry: dict[str, Any]) -> None:
    for field in ("escalationTriggers", "simplificationTriggers"):
        values = decision[field]
        require(isinstance(values, list) and values, "E-TRIGGERS", f"{field} is empty")
        require(len(values) == len(set(values)), "E-TRIGGERS", f"{field} is duplicated")
        require(set(values).issubset(registry[field]), "E-TRIGGERS", f"{field} has an unknown value")


def validate_scaffolding(scaffolding: Any) -> None:
    exact_object(scaffolding, SCAFFOLD_KEYS, "scaffolding classification")
    all_ids: list[str] = []
    for field in ("reuseExisting", "createOnceOrPeriodic", "recurForThisTask"):
        items = scaffolding[field]
        require(isinstance(items, list), "E-SCAFFOLDING", f"{field} is not an array")
        if field == "recurForThisTask":
            require(items, "E-SCAFFOLDING", "no recurring task evidence is named")
        for item in items:
            exact_object(item, {"itemId", "reason"}, f"scaffolding item in {field}")
            require(isinstance(item["itemId"], str) and re.fullmatch(r"scaffold:[a-z0-9][a-z0-9._-]*", item["itemId"]), "E-SCAFFOLDING", "scaffolding ID is malformed")
            require(nonempty(item["reason"]), "E-SCAFFOLDING", "scaffolding reason is empty")
            all_ids.append(item["itemId"])
    require(len(all_ids) == len(set(all_ids)), "E-SCAFFOLDING", "one scaffold appears in multiple cost classes")
    require(nonempty(scaffolding["proportionalityRationale"]), "E-SCAFFOLDING", "proportionality rationale is empty")


def validate_decision(decision: dict[str, Any], registry: dict[str, Any]) -> None:
    exact_object(decision, DECISION_KEYS, "task-rigor decision")
    require(decision["schemaVersion"] == VERSION, "E-SCHEMA", "decision version changed")
    require(isinstance(decision["decisionId"], str) and re.fullmatch(r"rigor-decision:[a-z0-9][a-z0-9._-]*", decision["decisionId"]), "E-SCHEMA", "decision ID is malformed")
    require(decision["state"] in {"template_inert", "planned", "observed", "complete", "superseded"}, "E-SCHEMA", "decision state is unknown")
    require(decision["authorityEffect"] == "none", "E-AUTHORITY", "rigor selector attempts to grant authority")
    validate_registry_reference(decision["registry"], registry, decision["state"])
    validate_loop(decision["loop"], decision["state"])

    computed = minimum_profile(decision["dimensions"], decision["evidenceApplicability"], registry)
    applicability = validate_applicability(decision["evidenceApplicability"], decision["dimensions"], registry)
    require(decision["recommendedMinimumProfile"] in RANK, "E-PROFILE", "recommended profile is unknown")
    require(decision["recommendedMinimumProfile"] == computed, "E-RECOMMENDATION", f"declared recommendation differs from {computed}")
    selected = decision["selectedProfile"]
    require(selected in RANK, "E-PROFILE", "selected profile is unknown")
    require(RANK[selected] >= RANK[computed], "E-PROFILE-BELOW-MINIMUM", "selected profile is below minimum")
    if RANK[selected] > RANK[computed]:
        require(nonempty(decision["higherRigorReason"]), "E-HIGHER-RIGOR-REASON", "higher rigor lacks a reason")
    else:
        require(decision["higherRigorReason"] is None, "E-HIGHER-RIGOR-REASON", "spurious higher-rigor reason")

    validate_strategy(decision["evidenceStrategy"])
    validate_evidence(decision["evidencePlan"], selected, decision["dimensions"], applicability, registry)
    validate_triggers(decision, registry)
    validate_scaffolding(decision["scaffolding"])
    require(nonempty(decision["rationale"]), "E-SCHEMA", "decision rationale is empty")


def make_evidence_item(kind: str) -> dict[str, Any]:
    independence = "predeclared_expectation"
    if kind == "deterministic_check":
        independence = "existing_external_oracle"
    elif kind == "runtime_or_trace":
        independence = "independent_runtime_observation"
    elif kind == "evaluator_check":
        independence = "calibrated_evaluator"
    elif kind in {"independent_expected_behavior", "adversarial_or_recovery"}:
        independence = "independent_fixture"
    elif kind == "independent_verification":
        independence = "independent_verifier"
    return {
        "evidenceKind": kind,
        "sourceId": f"evidence-source:{kind}",
        "expectedResult": f"{kind} meets its predeclared expectation.",
        "detectsFailure": f"A realistic {kind} failure is distinguishable from success.",
        "independence": independence,
    }


def build_case(case: dict[str, Any], template: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    decision = copy.deepcopy(template)
    decision["decisionId"] = f"rigor-decision:{case['caseId']}"
    decision["state"] = case["state"]
    decision["registry"]["sha256"] = canonical_sha256(registry)
    decision["dimensions"] = copy.deepcopy(case["dimensions"])
    decision["evidenceApplicability"] = copy.deepcopy(case["evidenceApplicability"])
    decision["recommendedMinimumProfile"] = case["expectedMinimumProfile"]
    decision["selectedProfile"] = case["selectedProfile"]
    decision["higherRigorReason"] = case["higherRigorReason"]
    decision["evidencePlan"] = [make_evidence_item(kind) for kind in case["evidenceKinds"]]
    decision["rationale"] = f"Synthetic vector {case['caseId']} grants no authority."
    iteration = decision["loop"][0]
    iteration["iterationId"] = f"iteration:{case['caseId']}_1"
    disposition = case["loopDisposition"]
    if disposition == "planned":
        iteration["observedResult"] = None
        iteration["nextChange"] = None
        iteration["completionBasis"] = None
    elif disposition == "observed":
        iteration["observedResult"] = "The evaluator produced a discriminating result."
        iteration["nextChange"] = "Change the smallest causal layer."
        iteration["completionBasis"] = None
    elif disposition == "complete":
        iteration["observedResult"] = "Evidence matched the predeclared expectation."
        iteration["nextChange"] = None
        iteration["completionBasis"] = "The selected evidence minima passed."
    else:
        raise ValidationFailure("E-VECTORS", f"unknown loop disposition: {disposition}")
    if case["selectedProfile"] in {"evaluated", "assured"}:
        decision["evidenceStrategy"]["sourceClass"] = "mixed"
    return decision


def pointer_parent(document: Any, pointer: str) -> tuple[Any, str]:
    require(isinstance(pointer, str) and pointer.startswith("/"), "E-VECTORS", "invalid JSON pointer")
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]
    current = document
    for part in parts[:-1]:
        if isinstance(current, list):
            require(part.isdigit() and int(part) < len(current), "E-VECTORS", f"invalid list pointer: {pointer}")
            current = current[int(part)]
        else:
            require(isinstance(current, dict) and part in current, "E-VECTORS", f"invalid object pointer: {pointer}")
            current = current[part]
    return current, parts[-1]


def pointer_get(document: Any, pointer: str) -> Any:
    parent, key = pointer_parent(document, pointer)
    if isinstance(parent, list):
        require(key.isdigit() and int(key) < len(parent), "E-VECTORS", "invalid list pointer")
        return parent[int(key)]
    require(isinstance(parent, dict) and key in parent, "E-VECTORS", "invalid object pointer")
    return parent[key]


def mutate(decision: dict[str, Any], mutation: dict[str, Any]) -> None:
    operation = mutation.get("operation")
    if operation in {"set", "remove", "append"}:
        if operation == "append":
            target = pointer_get(decision, mutation["jsonPointer"])
            require(isinstance(target, list), "E-VECTORS", "append target is not an array")
            target.append(copy.deepcopy(mutation.get("value")))
            return
        parent, key = pointer_parent(decision, mutation["jsonPointer"])
        if operation == "set":
            if isinstance(parent, list):
                require(key.isdigit() and int(key) < len(parent), "E-VECTORS", "invalid list set")
                parent[int(key)] = copy.deepcopy(mutation.get("value"))
            else:
                require(isinstance(parent, dict), "E-VECTORS", "set parent is not an object")
                parent[key] = copy.deepcopy(mutation.get("value"))
        else:
            if isinstance(parent, list):
                require(key.isdigit() and int(key) < len(parent), "E-VECTORS", "invalid list remove")
                parent.pop(int(key))
            else:
                require(isinstance(parent, dict) and key in parent, "E-VECTORS", "remove key is absent")
                del parent[key]
        return
    if operation == "remove_evidence_kind":
        kind = mutation["value"]
        before = len(decision["evidencePlan"])
        decision["evidencePlan"] = [item for item in decision["evidencePlan"] if item["evidenceKind"] != kind]
        require(len(decision["evidencePlan"]) == before - 1, "E-VECTORS", "evidence removal was not unique")
        return
    if operation == "duplicate_evidence_kind":
        matches = [item for item in decision["evidencePlan"] if item["evidenceKind"] == mutation["value"]]
        require(len(matches) == 1, "E-VECTORS", "evidence duplication source is not unique")
        decision["evidencePlan"].append(copy.deepcopy(matches[0]))
        return
    if operation == "copy_scaffold":
        source = pointer_get(decision, mutation["from"])
        target = pointer_get(decision, mutation["jsonPointer"])
        require(isinstance(source, dict) and isinstance(target, list), "E-VECTORS", "invalid scaffold copy")
        target.append(copy.deepcopy(source))
        return
    raise ValidationFailure("E-VECTORS", f"unknown mutation: {operation}")


def validate_vectors(vectors: dict[str, Any], template: dict[str, Any], registry: dict[str, Any]) -> tuple[int, int]:
    keys = {
        "schemaVersion",
        "vectorSetId",
        "status",
        "authority",
        "description",
        "positiveCases",
        "negativeCases",
    }
    exact_object(vectors, keys, "task-rigor vectors")
    require(vectors["schemaVersion"] == VERSION, "E-VECTORS", "vector version changed")
    require(vectors["vectorSetId"] == "vector-set:elad_task_rigor_0.3.0", "E-VECTORS", "vector-set identity changed")
    require(vectors["status"] == "reference_only" and vectors["authority"] == "none", "E-AUTHORITY", "vectors claim authority")
    positives = vectors["positiveCases"]
    negatives = vectors["negativeCases"]
    require(isinstance(positives, list) and positives, "E-VECTORS", "positive vectors are empty")
    require(isinstance(negatives, list) and negatives, "E-VECTORS", "negative vectors are empty")

    documents: dict[str, dict[str, Any]] = {}
    positive_keys = {
        "caseId",
        "state",
        "dimensions",
        "evidenceApplicability",
        "expectedMinimumProfile",
        "selectedProfile",
        "higherRigorReason",
        "loopDisposition",
        "evidenceKinds",
    }
    for case in positives:
        exact_object(case, positive_keys, "positive vector")
        case_id = case["caseId"]
        require(nonempty(case_id) and case_id not in documents, "E-VECTORS", "positive case ID is empty or duplicated")
        require(minimum_profile(case["dimensions"], case["evidenceApplicability"], registry) == case["expectedMinimumProfile"], "E-VECTORS", f"wrong expected minimum: {case_id}")
        document = build_case(case, template, registry)
        validate_decision(document, registry)
        documents[case_id] = document

    seen_negative: set[str] = set()
    for case in negatives:
        exact_object(case, {"caseId", "baseCase", "mutation", "expectedCode"}, "negative vector")
        case_id = case["caseId"]
        require(nonempty(case_id) and case_id not in seen_negative, "E-VECTORS", "negative case ID is empty or duplicated")
        seen_negative.add(case_id)
        require(case["baseCase"] in documents, "E-VECTORS", f"unknown negative base: {case_id}")
        document = copy.deepcopy(documents[case["baseCase"]])
        mutate(document, case["mutation"])
        try:
            validate_decision(document, registry)
        except ValidationFailure as exc:
            require(exc.code == case["expectedCode"], "E-VECTORS", f"{case_id} produced {exc.code}, expected {case['expectedCode']}")
        else:
            raise ValidationFailure("E-VECTORS", f"negative vector was accepted: {case_id}")
    return len(positives), len(negatives)


def validate_docs() -> None:
    try:
        doc = DOC_PATH.read_text(encoding="utf-8")
        light = LIGHT_TEMPLATE_PATH.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValidationFailure("E-DOC", f"cannot read adaptive-rigor docs: {exc}") from exc
    normalized_doc = " ".join(doc.split())
    phrases = [
        "The seven-question loop",
        "Project maturity",
        "Task rigor",
        "Effect authority",
        "cheapest reliable evidence",
        "Reusable infrastructure versus recurring work",
        "There is no mandatory JSON task-rigor decision",
        "Selecting a rigor profile never grants",
        "Evaluator maturity is classified per claim",
        "Executing a program does not by itself make a claim runtime/operational",
    ]
    for phrase in phrases:
        require(phrase.casefold() in normalized_doc.casefold(), "E-DOC", f"adaptive-rigor doc is missing: {phrase}")
    for profile in PROFILES:
        require(f"\x60{profile}\x60" in doc, "E-DOC", f"adaptive-rigor doc omits: {profile}")
    require("This file is optional" in light, "E-DOC", "light template presents itself as mandatory")
    require("No JSON packet" in light, "E-DOC", "light template does not preserve the lightweight path")
    require("never widens authority" in light, "E-DOC", "light template does not preserve authority separation")


def main() -> int:
    try:
        registry = load_json(REGISTRY_PATH)
        schema = load_json(SCHEMA_PATH)
        template = load_json(TEMPLATE_PATH)
        vectors = load_json(VECTORS_PATH)
        validate_registry(registry)
        validate_schema_contract(schema, registry)
        validate_decision(template, registry)
        positive_count, negative_count = validate_vectors(vectors, template, registry)
        validate_docs()
    except ValidationFailure as exc:
        print(f"FAIL — {exc}", file=sys.stderr)
        return 1
    print(
        "PASS — ELAD 0.3 adaptive-rigor core: "
        f"{len(PROFILES)} orthogonal task profiles, {positive_count} positive vectors, "
        f"{negative_count} malicious/contradictory vectors; true lightweight path retained. "
        "Advisory evidence selection only. No authority granted."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
