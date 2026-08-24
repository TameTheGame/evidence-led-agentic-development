#!/usr/bin/env python3
"""Synthetic, dependency-free ELAD 0.3 protocol-security checks.

This Level-0 suite constructs only in-memory records. It never launches a model,
touches a target repository, grants authority, or accepts production evidence.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.3.0"
SHA = re.compile(r"^[A-F0-9]{64}$")
REF_FIELDS = {"kind", "id", "path", "bytes", "sha256", "schemaVersion", "digestMode"}


class Denied(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def require(value: bool, code: str, detail: str = "") -> None:
    if not value:
        raise Denied(code, detail)


def load(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


EXPECTED_REGISTRY = {
    "schemaVersion": VERSION,
    "registryId": "vocabulary:elad_subject_selectors_0.3.0",
    "status": "reference_only",
    "authority": "none",
    "closed": True,
    "selectors": [
        {
            "selectorId": "subject-selector:receipt_candidate_v1",
            "kind": "candidate",
            "wireSelector": "receipt_candidate",
            "resolutionRule": "receipt_candidate_v1",
            "preRunDigestRule": "must_be_null",
            "resolvedSubjectFields": ["kind", "repositoryId", "id", "baseHead", "sha256"],
        }
    ],
}


KIND_ROOT = {
    "registry": "spec/registries",
    "protocol_bundle": "protocol",
    "runtime_lock": "locks",
    "harness_lock": "locks",
    "adapter_lock": "locks",
    "json_schema": "schemas",
    "writer_profile": "profiles",
    "task_packet": "packets",
    "evidence_manifest": "evidence",
    "review_bundle": "reviews",
    "external_human_receipt": "human",
    "worker_receipt": "receipts",
    "continuation_anchor": "anchors",
    "raw_payload": "payloads",
}


EDGES = {
    "registry": [],
    "protocol_bundle": [("selectorRegistry", "registry", True)],
    "runtime_lock": [],
    "harness_lock": [],
    "adapter_lock": [],
    "json_schema": [],
    "writer_profile": [
        ("runtime", "runtime_lock", True),
        ("harness", "harness_lock", True),
        ("adapter", "adapter_lock", True),
        ("toolSchema", "json_schema", True),
    ],
    "task_packet": [
        ("protocolBundle", "protocol_bundle", True),
        ("writerProfile", "writer_profile", True),
        ("writerProfileMirror", "writer_profile", True),
    ],
    "evidence_manifest": [
        ("taskPacket", "task_packet", True),
        ("entries[].payload", "raw_payload", True),
    ],
    "review_bundle": [
        ("taskPacket", "task_packet", True),
        ("evidenceManifest", "evidence_manifest", True),
        ("artifacts[].payload", "raw_payload", True),
    ],
    "external_human_receipt": [
        ("taskPacket", "task_packet", True),
        ("reviewBundle", "review_bundle", True),
    ],
    "worker_receipt": [
        ("taskPacket", "task_packet", True),
        ("evidenceManifest", "evidence_manifest", True),
        ("externalHumanReceipt", "external_human_receipt", True),
        ("supersedes", "worker_receipt", False),
    ],
    "continuation_anchor": [("receipt", "worker_receipt", True)],
}


BUILD_ORDER = [
    "spec/registries/subject-selectors.json",
    "protocol/bundle.json",
    "locks/runtime.json",
    "locks/harness.json",
    "locks/adapter.json",
    "schemas/tools.json",
    "profiles/writer.json",
    "packets/task.json",
    "evidence/manifest.json",
    "reviews/bundle.json",
    "human/receipt.json",
    "receipts/worker.json",
    "anchors/continuation.json",
]


def reference(store: dict[str, Any], kind: str, identifier: str, path: str) -> dict[str, Any]:
    target = store[path]
    mode = "raw_bytes" if isinstance(target, bytes) else "canonical_json"
    raw = target if isinstance(target, bytes) else canonical_bytes(target)
    return {
        "kind": kind,
        "id": identifier,
        "path": path,
        "bytes": len(raw),
        "sha256": digest(raw),
        "schemaVersion": VERSION,
        "digestMode": mode,
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    store: dict[str, Any] = {
        "payloads/candidate.txt": b"candidate\n",
        "payloads/evidence-a.txt": b"evidence-a\n",
        "payloads/evidence-b.txt": b"evidence-b\n",
        "payloads/unrelated.txt": b"unrelated\n",
        "payloads/reviewer-card.md": b"reviewer-card\n",
        "spec/registries/subject-selectors.json": copy.deepcopy(EXPECTED_REGISTRY),
    }
    registry_ref = reference(store, "registry", EXPECTED_REGISTRY["registryId"], "spec/registries/subject-selectors.json")
    store["protocol/bundle.json"] = {"schemaVersion": VERSION, "id": "protocol-bundle:elad_0.3.0", "authority": "none", "selectorRegistry": registry_ref}
    for name, kind in (("runtime", "runtime_lock"), ("harness", "harness_lock"), ("adapter", "adapter_lock")):
        store[f"locks/{name}.json"] = {"schemaVersion": VERSION, "id": f"{name}-lock:synthetic", "authority": "none"}
    store["schemas/tools.json"] = {"schemaVersion": VERSION, "id": "schema:synthetic_tools", "authority": "none", "closed": True}
    store["profiles/writer.json"] = {
        "schemaVersion": VERSION,
        "id": "writer:synthetic",
        "authority": "none",
        "runtime": reference(store, "runtime_lock", "runtime-lock:synthetic", "locks/runtime.json"),
        "harness": reference(store, "harness_lock", "harness-lock:synthetic", "locks/harness.json"),
        "adapter": reference(store, "adapter_lock", "adapter-lock:synthetic", "locks/adapter.json"),
        "toolSchema": reference(store, "json_schema", "schema:synthetic_tools", "schemas/tools.json"),
    }
    candidate_ref = reference(store, "raw_payload", "payload:candidate", "payloads/candidate.txt")
    selector = {
        "kind": "candidate",
        "selector": "receipt_candidate",
        "repositoryId": "repo:synthetic",
        "id": "candidate:synthetic",
        "baseHead": "a" * 40,
        "sha256": None,
    }
    subject = {"kind": "candidate", "repositoryId": "repo:synthetic", "id": "candidate:synthetic", "baseHead": "a" * 40, "sha256": candidate_ref["sha256"]}
    writer_ref = reference(store, "writer_profile", "writer:synthetic", "profiles/writer.json")
    store["packets/task.json"] = {
        "schemaVersion": VERSION,
        "id": "packet:synthetic",
        "authority": "none",
        "repository": {"repositoryId": "repo:synthetic", "candidateId": "candidate:synthetic", "baseHead": "a" * 40},
        "protocolBundle": reference(store, "protocol_bundle", "protocol-bundle:elad_0.3.0", "protocol/bundle.json"),
        "writerProfile": writer_ref,
        "writerProfileMirror": copy.deepcopy(writer_ref),
        "claims": [
            {"claimId": "claim:machine", "acceptanceOwner": "machine", "subject": copy.deepcopy(selector), "resolvedSubject": copy.deepcopy(subject), "reviewRequirements": None},
            {"claimId": "claim:human", "acceptanceOwner": "external_human", "subject": copy.deepcopy(selector), "resolvedSubject": copy.deepcopy(subject), "reviewRequirements": {"requiredEvidenceClaimIds": ["claim:machine"], "requiredPresentationRoles": ["reviewer_card"], "eligibleReviewerIds": ["human:owner"]}},
        ],
    }
    packet_ref = reference(store, "task_packet", "packet:synthetic", "packets/task.json")
    evidence_entries = []
    for letter in ("a", "b"):
        payload = reference(store, "raw_payload", f"payload:evidence_{letter}", f"payloads/evidence-{letter}.txt")
        evidence_entries.append({"evidenceId": f"evidence:{letter}", "claimIds": ["claim:machine"], "resolvedSubject": copy.deepcopy(subject), "payload": payload})
    unrelated = reference(store, "raw_payload", "payload:unrelated", "payloads/unrelated.txt")
    evidence_entries.append({"evidenceId": "evidence:unrelated", "claimIds": [], "resolvedSubject": copy.deepcopy(subject), "payload": unrelated})
    store["evidence/manifest.json"] = {"schemaVersion": VERSION, "id": "evidence-manifest:synthetic", "authority": "none", "taskPacket": packet_ref, "subject": copy.deepcopy(subject), "entries": evidence_entries}
    evidence_ref = reference(store, "evidence_manifest", "evidence-manifest:synthetic", "evidence/manifest.json")
    artifacts = [
        {"artifactId": "artifact:candidate", "role": "candidate_subject", "evidenceId": None, "payload": candidate_ref},
        {"artifactId": "artifact:evidence_a", "role": "evidence_payload", "evidenceId": "evidence:a", "payload": copy.deepcopy(evidence_entries[0]["payload"])},
        {"artifactId": "artifact:evidence_b", "role": "evidence_payload", "evidenceId": "evidence:b", "payload": copy.deepcopy(evidence_entries[1]["payload"])},
        {"artifactId": "artifact:card", "role": "reviewer_card", "evidenceId": None, "payload": reference(store, "raw_payload", "payload:card", "payloads/reviewer-card.md")},
    ]
    store["reviews/bundle.json"] = {
        "schemaVersion": VERSION,
        "id": "review-bundle:synthetic",
        "authority": "none",
        "taskPacket": copy.deepcopy(packet_ref),
        "evidenceManifest": evidence_ref,
        "subject": copy.deepcopy(subject),
        "artifacts": artifacts,
        "claimCoverage": [{"claimId": "claim:human", "candidateArtifactIds": ["artifact:candidate"], "evidenceArtifactIds": ["artifact:evidence_a", "artifact:evidence_b"], "presentationArtifactIds": ["artifact:card"]}],
    }
    review_ref = reference(store, "review_bundle", "review-bundle:synthetic", "reviews/bundle.json")
    store["human/receipt.json"] = {"schemaVersion": VERSION, "id": "human-receipt:synthetic", "authority": "none", "taskPacket": copy.deepcopy(packet_ref), "reviewBundle": review_ref, "reviewerId": "human:owner", "claimId": "claim:human", "decision": "accepted"}
    human_ref = reference(store, "external_human_receipt", "human-receipt:synthetic", "human/receipt.json")
    store["receipts/worker.json"] = {
        "schemaVersion": VERSION,
        "id": "receipt:synthetic",
        "authority": "none",
        "taskPacket": copy.deepcopy(packet_ref),
        "evidenceManifest": copy.deepcopy(evidence_ref),
        "externalHumanReceipt": human_ref,
        "supersedes": None,
        "claims": [{"claimId": row["claimId"], "resolvedSubject": copy.deepcopy(subject), "result": "passed"} for row in store["packets/task.json"]["claims"]],
    }
    store["anchors/continuation.json"] = {"schemaVersion": VERSION, "id": "anchor:synthetic", "authority": "none", "receipt": reference(store, "worker_receipt", "receipt:synthetic", "receipts/worker.json")}
    return store, reference(store, "continuation_anchor", "anchor:synthetic", "anchors/continuation.json")


def find_refs(value: Any, prefix: str = "") -> list[tuple[str, dict[str, Any]]]:
    if isinstance(value, dict) and set(value) == REF_FIELDS:
        return [(prefix, value)]
    found: list[tuple[str, dict[str, Any]]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            found.extend(find_refs(child, f"{prefix}.{key}" if prefix else key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(find_refs(child, f"{prefix}[{index}]"))
    return found


def edge_values(document: dict[str, Any], expression: str, required: bool) -> list[tuple[str, Any]]:
    if "[]." not in expression:
        value = document.get(expression)
        require(value is not None or not required, "REF_EDGE_MISSING", expression)
        return [] if value is None else [(expression, value)]
    parent, child = expression.split("[].", 1)
    rows = document.get(parent)
    require(isinstance(rows, list), "REF_EDGE_MISSING", expression)
    return [(f"{parent}[{index}].{child}", row.get(child)) for index, row in enumerate(rows)]


class Resolver:
    def __init__(self, store: dict[str, Any], repository_path: re.Pattern[str], max_nodes: int = 32) -> None:
        self.store = store
        self.repository_path = repository_path
        self.max_nodes = max_nodes
        self.nodes = 0
        self.active: set[tuple[str, str]] = set()
        self.identities: dict[tuple[str, str], tuple[Any, ...]] = {}
        self.documents: dict[tuple[str, str], dict[str, Any]] = {}

    def resolve(self, ref: Any, expected_kind: str) -> Any:
        require(isinstance(ref, dict) and set(ref) == REF_FIELDS, "REF_FIELDS")
        require(ref["kind"] == expected_kind, "REF_KIND")
        require(ref["schemaVersion"] == VERSION and SHA.fullmatch(ref["sha256"]) is not None, "REF_FORMAT")
        require(isinstance(ref["path"], str) and self.repository_path.fullmatch(ref["path"]) is not None, "REF_PATH")
        mode = "raw_bytes" if expected_kind == "raw_payload" else "canonical_json"
        require(ref["digestMode"] == mode, "REF_MODE")
        root = KIND_ROOT[expected_kind]
        require(ref["path"].startswith(root + "/"), "REF_ROOT")
        key = (expected_kind, ref["id"])
        require(key not in self.active, "REF_CYCLE")
        identity = tuple(ref[name] for name in sorted(REF_FIELDS))
        if key in self.identities:
            require(self.identities[key] == identity, "REF_ID_SUBSTITUTION")
        else:
            self.identities[key] = identity
        if key in self.documents:
            return self.documents[key]
        require(ref["path"] in self.store, "REF_MISSING")
        target = self.store[ref["path"]]
        raw = target if isinstance(target, bytes) else canonical_bytes(target)
        require(ref["bytes"] == len(raw), "REF_BYTES")
        require(ref["sha256"] == digest(raw), "REF_DIGEST")
        if isinstance(target, bytes):
            return target
        require(target.get("schemaVersion") == VERSION and target.get("authority") == "none", "REF_DOCUMENT")
        id_field = "registryId" if expected_kind == "registry" else "id"
        require(target.get(id_field) == ref["id"], "REF_CHILD_ID")
        declared: list[tuple[str, Any, str]] = []
        for expression, child_kind, required in EDGES[expected_kind]:
            declared.extend((path, value, child_kind) for path, value in edge_values(target, expression, required))
        require({path for path, _ in find_refs(target)} == {path for path, _, _ in declared}, "REF_UNDECLARED_EDGE")
        self.nodes += 1
        require(self.nodes <= self.max_nodes, "GRAPH_BUDGET")
        self.active.add(key)
        try:
            for _, child, child_kind in declared:
                self.resolve(child, child_kind)
        finally:
            self.active.remove(key)
        self.documents[key] = target
        return target


def refresh_references(value: Any, store: dict[str, Any], protected: set[int]) -> None:
    if isinstance(value, dict) and set(value) == REF_FIELDS:
        if id(value) in protected:
            return
        target = store.get(value["path"])
        if target is not None:
            raw = target if isinstance(target, bytes) else canonical_bytes(target)
            value["bytes"] = len(raw)
            value["sha256"] = digest(raw)
        return
    if isinstance(value, dict):
        for child in value.values():
            refresh_references(child, store, protected)
    elif isinstance(value, list):
        for child in value:
            refresh_references(child, store, protected)


def reanchor(store: dict[str, Any], protected: set[int]) -> dict[str, Any]:
    for path in BUILD_ORDER:
        refresh_references(store[path], store, protected)
    return reference(store, "continuation_anchor", "anchor:synthetic", "anchors/continuation.json")


def expected_subject(packet: dict[str, Any]) -> dict[str, Any]:
    selector = packet["claims"][0]["subject"]
    require(selector["kind"] == "candidate", "SELECTOR_KIND")
    require(selector["selector"] == "receipt_candidate", "SELECTOR_UNKNOWN")
    require(selector["sha256"] is None, "SELECTOR_DIGEST")
    require(selector["repositoryId"] == packet["repository"]["repositoryId"], "SUBJECT_MISMATCH")
    require(selector["id"] == packet["repository"]["candidateId"], "SUBJECT_MISMATCH")
    require(selector["baseHead"] == packet["repository"]["baseHead"], "SUBJECT_MISMATCH")
    first = packet["claims"][0]["resolvedSubject"]
    for claim in packet["claims"]:
        require(claim["subject"] == selector and claim["resolvedSubject"] == first, "SUBJECT_MISMATCH")
    return first


def validate_semantics(resolver: Resolver, root: dict[str, Any]) -> None:
    require(resolver.store["spec/registries/subject-selectors.json"] == EXPECTED_REGISTRY, "REGISTRY_NOT_CANONICAL")
    anchor = resolver.resolve(root, "continuation_anchor")
    receipt = resolver.documents[("worker_receipt", anchor["receipt"]["id"])]
    packet = resolver.documents[("task_packet", receipt["taskPacket"]["id"])]
    manifest = resolver.documents[("evidence_manifest", receipt["evidenceManifest"]["id"])]
    human = resolver.documents[("external_human_receipt", receipt["externalHumanReceipt"]["id"])]
    review = resolver.documents[("review_bundle", human["reviewBundle"]["id"])]
    subject = expected_subject(packet)
    require(manifest["subject"] == review["subject"] == subject, "SUBJECT_MISMATCH")
    for entry in manifest["entries"]:
        require(entry["resolvedSubject"] == subject, "SUBJECT_MISMATCH")
    for row in receipt["claims"]:
        require(row["resolvedSubject"] == subject, "SUBJECT_MISMATCH")
    human_claim = next(row for row in packet["claims"] if row["acceptanceOwner"] == "external_human")
    require(human["claimId"] == human_claim["claimId"] and human["decision"] == "accepted", "REVIEW_CLAIM")
    require(human["reviewerId"] in human_claim["reviewRequirements"]["eligibleReviewerIds"], "REVIEW_CLAIM")
    coverage = [row for row in review["claimCoverage"] if row["claimId"] == human_claim["claimId"]]
    require(len(coverage) == 1, "REVIEW_CLAIM")
    coverage = coverage[0]
    artifacts = {row["artifactId"]: row for row in review["artifacts"]}
    candidate_ids = coverage["candidateArtifactIds"]
    require(len(candidate_ids) == 1 and candidate_ids[0] in artifacts, "REVIEW_CANDIDATE")
    candidate = artifacts[candidate_ids[0]]
    require(candidate["role"] == "candidate_subject" and candidate["payload"]["sha256"] == subject["sha256"], "REVIEW_CANDIDATE")
    required_claims = set(human_claim["reviewRequirements"]["requiredEvidenceClaimIds"])
    expected_ids = {row["evidenceId"] for row in manifest["entries"] if required_claims.intersection(row["claimIds"])}
    selected = []
    for artifact_id in coverage["evidenceArtifactIds"]:
        require(artifact_id in artifacts and artifacts[artifact_id]["role"] == "evidence_payload", "REVIEW_EVIDENCE")
        selected.append(artifacts[artifact_id]["evidenceId"])
    require(set(selected) == expected_ids and len(selected) == len(expected_ids), "REVIEW_EVIDENCE")
    roles = []
    for artifact_id in coverage["presentationArtifactIds"]:
        require(artifact_id in artifacts, "REVIEW_PRESENTATION")
        roles.append(artifacts[artifact_id]["role"])
    require(set(roles) == set(human_claim["reviewRequirements"]["requiredPresentationRoles"]), "REVIEW_PRESENTATION")
    mapped = set(candidate_ids + coverage["evidenceArtifactIds"] + coverage["presentationArtifactIds"])
    require(mapped == set(artifacts), "REVIEW_UNMAPPED")


def attack(name: str, store: dict[str, Any], root: dict[str, Any]) -> tuple[dict[str, Any], int, set[int]]:
    packet = store["packets/task.json"]
    manifest = store["evidence/manifest.json"]
    review = store["reviews/bundle.json"]
    receipt = store["receipts/worker.json"]
    limit = 32
    protected: set[int] = set()
    if name == "none":
        return root, limit, protected
    if name == "unknown_selector":
        for row in packet["claims"]: row["subject"]["selector"] = "invented"
    elif name == "invented_kind":
        for row in packet["claims"]: row["subject"]["kind"] = "invented"
    elif name == "selector_repository":
        for row in packet["claims"]: row["subject"]["repositoryId"] = "repo:neighbor"
    elif name == "selector_candidate":
        for row in packet["claims"]: row["subject"]["id"] = "candidate:neighbor"
    elif name == "selector_base":
        for row in packet["claims"]: row["subject"]["baseHead"] = "b" * 40
    elif name == "selector_digest":
        for row in packet["claims"]: row["subject"]["sha256"] = "0" * 64
    elif name == "invented_registry":
        store["spec/registries/subject-selectors.json"]["selectors"].append({"selectorId": "subject-selector:invented"})
    elif name == "manifest_outer_digest": receipt["evidenceManifest"]["sha256"] = "0" * 64
    elif name == "manifest_repository": manifest["subject"]["repositoryId"] = "repo:neighbor"
    elif name == "manifest_candidate": manifest["subject"]["id"] = "candidate:neighbor"
    elif name == "entry_subject": manifest["entries"][0]["resolvedSubject"]["id"] = "candidate:neighbor"
    elif name == "receipt_subject": receipt["claims"][0]["resolvedSubject"]["id"] = "candidate:neighbor"
    elif name == "typed_kind": packet["writerProfile"]["kind"] = "runtime_lock"
    elif name == "digest_mode": packet["writerProfile"]["digestMode"] = "raw_bytes"
    elif name == "byte_count":
        packet["writerProfile"]["bytes"] += 1
        protected.add(id(packet["writerProfile"]))
    elif name == "same_id_two_hashes":
        packet["writerProfileMirror"]["sha256"] = "0" * 64
        protected.add(id(packet["writerProfileMirror"]))
    elif name == "cycle": receipt["supersedes"] = copy.deepcopy(root if root["kind"] == "worker_receipt" else store["anchors/continuation.json"]["receipt"])
    elif name == "root_escape": packet["writerProfile"]["path"] = "payloads/writer.json"
    elif name == "reserved_device_path": root["path"] = "anchors/CON/file.json"
    elif name == "trailing_dot_path": root["path"] = "anchors/name./file.json"
    elif name == "trailing_space_path": root["path"] = "anchors/name /file.json"
    elif name == "absolute_path": root["path"] = "/anchors/continuation.json"
    elif name == "traversal_path": root["path"] = "anchors/../continuation.json"
    elif name == "mixed_separator_path": root["path"] = "anchors\\continuation.json"
    elif name == "hidden_edge": packet["hiddenReference"] = copy.deepcopy(store["profiles/writer.json"]["runtime"])
    elif name == "node_budget": limit = 3
    elif name == "card_only":
        review["artifacts"] = [row for row in review["artifacts"] if row["role"] == "reviewer_card"]
        review["claimCoverage"][0]["candidateArtifactIds"] = ["artifact:card"]
        review["claimCoverage"][0]["evidenceArtifactIds"] = []
    elif name == "partial_evidence":
        review["artifacts"] = [row for row in review["artifacts"] if row["artifactId"] != "artifact:evidence_b"]
        review["claimCoverage"][0]["evidenceArtifactIds"] = ["artifact:evidence_a"]
    elif name == "unrelated_evidence":
        target = next(row for row in review["artifacts"] if row["artifactId"] == "artifact:evidence_a")
        target["evidenceId"] = "evidence:unrelated"
        target["payload"] = copy.deepcopy(manifest["entries"][2]["payload"])
    elif name == "wrong_candidate":
        next(row for row in review["artifacts"] if row["role"] == "candidate_subject")["payload"] = reference(store, "raw_payload", "payload:unrelated", "payloads/unrelated.txt")
    elif name == "missing_card":
        review["artifacts"] = [row for row in review["artifacts"] if row["role"] != "reviewer_card"]
        review["claimCoverage"][0]["presentationArtifactIds"] = []
    elif name == "unmapped_artifact":
        review["artifacts"].append({"artifactId": "artifact:extra", "role": "reviewer_card", "evidenceId": None, "payload": reference(store, "raw_payload", "payload:extra", "payloads/reviewer-card.md")})
    elif name == "wrong_human_claim": review["claimCoverage"][0]["claimId"] = "claim:machine"
    else: raise Denied("UNKNOWN_ATTACK", name)
    return root, limit, protected


def main() -> int:
    registry = load("spec/registries/subject-selectors.json")
    schema = load("spec/schemas/typed-reference.schema.json")
    vectors = load("tests/protocol-security-vectors.json")
    require(registry == EXPECTED_REGISTRY, "REGISTRY_NOT_CANONICAL")
    require(schema.get("additionalProperties") is False and set(schema.get("required", [])) == REF_FIELDS, "SCHEMA_INVALID")
    repository_path_definition = schema.get("$defs", {}).get("repositoryPath", {})
    require(repository_path_definition.get("type") == "string" and isinstance(repository_path_definition.get("pattern"), str), "SCHEMA_INVALID")
    require(schema.get("properties", {}).get("path") == {"$ref": "#/$defs/repositoryPath"}, "SCHEMA_INVALID")
    repository_path = re.compile(repository_path_definition["pattern"])
    failures: list[str] = []
    accepted = rejected = 0
    for vector in vectors["vectors"]:
        store, root = build()
        try:
            root, limit, protected = attack(vector["attack"], store, root)
            if vector.get("reanchored"):
                root = reanchor(store, protected)
            resolver = Resolver(store, repository_path, limit)
            resolver.resolve(root, "continuation_anchor")
            validate_semantics(resolver, root)
            if vector["expected"] != "accept":
                failures.append(f"{vector['id']}: malicious vector accepted")
            else:
                accepted += 1
        except Denied as exc:
            if vector["expected"] == "accept" or exc.code != vector["expected"]:
                failures.append(f"{vector['id']}: expected {vector['expected']}, got {exc.code}")
            else:
                rejected += 1
    if failures:
        for item in failures: print(f"FAIL {item}", file=sys.stderr)
        return 1
    print(f"PASS — ELAD 0.3 protocol-security slice: {accepted} positive vectors, {rejected} malicious controls rejected. Level-0 inert; no authority granted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
