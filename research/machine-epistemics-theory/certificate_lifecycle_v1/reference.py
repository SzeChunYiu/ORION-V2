"""Exact research semantics, not an authenticated or concurrent production runtime.

APPLICABLE concerns a *typed certificate at a snapshot*, never unqualified truth.
External facts are explicit trusted-boundary inputs. See THEORY.md for assumptions.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Any

UNUSABLE, UNRESOLVED, APPLICABLE = 0, 1, 2
FACTS = {"INVALID": UNUSABLE, "UNKNOWN": UNRESOLVED,
         "CONFLICT": UNRESOLVED, "VALID": APPLICABLE}
KINDS = ("EXACT_OBJECT", "OPERATOR_GUARANTEE")
OPERATOR_FIELDS = tuple(sorted((
    "implementation", "model", "weights", "prompt", "decoding", "preprocessing",
    "postprocessing", "checker", "calibration_data", "calibration_protocol",
    "assumptions", "environment", "resource_policy", "scope", "epoch", "schema")))


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def digest(tag: str, value: Any) -> str:
    """Domain-separated canonical JSON on a restricted, float-free value domain."""
    def check(x: Any) -> None:
        if x is None or type(x) in (str, int, bool):
            return
        if type(x) in (tuple, list):
            for y in x:
                check(y)
            return
        if type(x) is dict and all(type(k) is str for k in x):
            for y in x.values():
                check(y)
            return
        raise ValueError("NON_CANONICAL_VALUE")
    require(type(tag) is str and bool(tag), "BAD_DOMAIN_TAG")
    check(value)
    raw = json.dumps(["me-cl/v1", tag, value], sort_keys=True,
                     ensure_ascii=True, separators=(",", ":"), allow_nan=False)
    return sha256(raw.encode("ascii")).hexdigest()


def is_hash(value: Any, length: int = 64) -> bool:
    return type(value) is str and re.fullmatch(r"[0-9a-f]{%d}" % length, value) is not None


def pairs(value: Any, hashes: bool) -> None:
    require(type(value) is tuple, "MUTABLE_PAIRS")
    require(all(type(p) is tuple and len(p) == 2 and type(p[0]) is str and p[0]
                and type(p[1]) is str for p in value), "BAD_PAIRS")
    require(value == tuple(sorted(value)) and len(dict(value)) == len(value),
            "DUPLICATE_OR_UNSORTED_KEY")
    require(all(is_hash(v) if hashes else v in FACTS for _, v in value), "BAD_VALUE")


def operator_identity(fields: dict[str, str]) -> str:
    require(type(fields) is dict and set(fields) == set(OPERATOR_FIELDS),
            "INCOMPLETE_OPERATOR_MANIFEST")
    require(all(is_hash(v) for v in fields.values()), "BAD_OPERATOR_DIGEST")
    return digest("operator", fields)


@dataclass(frozen=True)
class Certificate:
    name: str
    kind: str
    statement: str
    subject: str
    proof: str
    checker: str
    bindings: tuple[tuple[str, str], ...]
    supports: tuple[tuple[str, ...], ...]

    def __post_init__(self) -> None:
        require(type(self.name) is str and self.name.startswith("cert:")
                and len(self.name) > 5, "BAD_CERTIFICATE_NAME")
        require(self.kind in KINDS, "UNKNOWN_CERTIFICATE_KIND")
        require(all(is_hash(x) for x in (self.statement, self.subject, self.proof,
                                         self.checker)), "BAD_CERTIFICATE_DIGEST")
        pairs(self.bindings, True)
        require(type(self.supports) is tuple and all(type(a) is tuple and all(
            type(d) is str and d.startswith(("root:", "cert:")) and len(d) > 5 and (d.startswith("cert:") or is_hash(d[5:]))
            for d in a) for a in self.supports), "BAD_SUPPORTS")
        require(all(len(set(a)) == len(a) for a in self.supports)
                and len(set(self.supports)) == len(self.supports), "DUPLICATE_SUPPORT")
        if self.kind == "OPERATOR_GUARANTEE":
            require({"operator", "scope", "epoch"} <= dict(self.bindings).keys(),
                    "UNSCOPED_OPERATOR_GUARANTEE")

    @property
    def identity(self) -> str:
        return digest("certificate", asdict(self))


def registry_id(registry: tuple[Certificate, ...]) -> str:
    require(type(registry) is tuple and all(type(c) is Certificate for c in registry),
            "BAD_REGISTRY")
    names = tuple(c.name for c in registry)
    require(names == tuple(sorted(set(names))), "DUPLICATE_OR_UNSORTED_CERTIFICATE")
    return digest("registry", [asdict(c) for c in registry])


def judgment_key(registry: tuple[Certificate, ...], cert: Certificate) -> str:
    # Bind the entire frozen interpretation of symbolic dependency names.
    return "root:judgment:" + digest("judgment", [registry_id(registry), cert.identity])


def trust_key(cert: Certificate) -> str:
    return "root:checker-trust:" + digest("checker-scope", [cert.checker, cert.kind, cert.statement])


@dataclass(frozen=True)
class Snapshot:
    generation: int
    registry: str
    context: tuple[tuple[str, str], ...]
    facts: tuple[tuple[str, str], ...]
    journal: str

    def __post_init__(self) -> None:
        require(type(self.generation) is int and self.generation >= 0, "BAD_GENERATION")
        require(is_hash(self.registry) and is_hash(self.journal), "BAD_SNAPSHOT_DIGEST")
        pairs(self.context, True)
        pairs(self.facts, False)
        require(all(re.fullmatch(r"root:(?:(?:judgment|checker-trust):)?[0-9a-f]{64}", k)
                    for k, _ in self.facts), "NONROOT_FACT")

    @property
    def identity(self) -> str:
        return digest("snapshot", asdict(self))


def evaluate(registry: tuple[Certificate, ...], state: Snapshot) -> dict[str, int]:
    """Least-information fixed point of a frozen positive AND/OR dependency graph."""
    require(state.registry == registry_id(registry), "REGISTRY_DRIFT")
    facts, context = dict(state.facts), dict(state.context)
    def root(key: str) -> int:
        return FACTS[facts[key]] if key in facts else UNRESOLVED
    own = {}
    for c in registry:
        binding = APPLICABLE if all(context.get(k) == v for k, v in c.bindings) else UNRESOLVED
        own[c.name] = min(root(judgment_key(registry, c)), root(trust_key(c)), binding)
    values = {c.name: UNRESOLVED for c in registry}
    for _ in range(len(registry) + 1):
        new = {}
        for c in registry:
            alternatives = [min((values.get(d, UNRESOLVED) if d.startswith("cert:")
                                 else root(d) for d in a), default=APPLICABLE)
                            for a in c.supports]
            new[c.name] = min(own[c.name], max(alternatives, default=UNRESOLVED))
        if new == values:
            return new
        require(all(values[k] == UNRESOLVED or values[k] == new[k] for k in values),
                "NONMONOTONE_INFORMATION_UPDATE")
        values = new
    raise ValueError("FIXED_POINT_DID_NOT_CONVERGE")


def diagnostics(registry: tuple[Certificate, ...], state: Snapshot) -> dict[str, list[str]]:
    """Direct reasons, including failed alternatives; not a minimal explanation set."""
    values = evaluate(registry, state)
    facts, context = dict(state.facts), dict(state.context)
    out = {}
    for c in registry:
        reasons = [f"STALE_OR_MISSING_BINDING:{k}" for k, v in c.bindings
                   if context.get(k) != v]
        for key in (judgment_key(registry, c), trust_key(c)):
            if facts.get(key) != "VALID":
                reasons.append(f"{facts.get(key, 'MISSING')}:{key}")
        for a in c.supports:
            for dep in a:
                v = values.get(dep, UNRESOLVED) if dep.startswith("cert:") else FACTS.get(facts.get(dep), UNRESOLVED)
                if v != APPLICABLE:
                    reasons.append(f"DEPENDENCY_{v}:{dep}")
        if not c.supports:
            reasons.append("NO_DERIVATION")
        if values[c.name] == UNRESOLVED:
            reasons.append("UNRESOLVED_NOT_FALSE;CYCLE_MAY_REQUIRE_EXTERNAL_GROUND")
        out[c.name] = sorted(set(reasons))
    return out


def prepare(state: Snapshot, operation: str, payload: dict) -> dict:
    # Returned envelope is deliberately mutable/untrusted; transition validates it.
    return {"generation": state.generation, "snapshot": state.identity,
            "operation": operation, "payload": payload}


def transition(registry: tuple[Certificate, ...], state: Snapshot,
               event: dict) -> tuple[Snapshot, dict | None]:
    require(type(event) is dict and set(event) == {"generation", "snapshot", "operation", "payload"}, "BAD_EVENT")
    require(type(event["generation"]) is int, "BAD_EVENT_GENERATION")
    if event["generation"] != state.generation or event["snapshot"] != state.identity:
        raise ValueError("STALE_SNAPSHOT")
    require(state.registry == registry_id(registry), "REGISTRY_DRIFT")
    payload = event["payload"]
    require(type(payload) is dict, "BAD_PAYLOAD")
    context, facts = dict(state.context), dict(state.facts)
    receipt = None
    if event["operation"] == "IMPORT_EXTERNAL":
        require(set(payload) == {"context", "facts"}, "BAD_IMPORT")
        require(type(payload["context"]) is dict and type(payload["facts"]) is dict, "BAD_IMPORT_VALUES")
        require(all(type(k) is str for k in payload["context"] | payload["facts"]), "BAD_IMPORT_KEY")
        context.update(payload["context"])
        facts.update(payload["facts"])
    elif event["operation"] == "USE":
        require(set(payload) == {"certificate", "kind", "statement", "subject"}, "BAD_USE")
        cert = next((c for c in registry if c.name == payload["certificate"]), None)
        require(cert is not None, "MISSING_CERTIFICATE")
        require(payload["kind"] == cert.kind and payload["statement"] == cert.statement
                and payload["subject"] == cert.subject, "TYPE_OR_SUBJECT_MISMATCH")
        require(evaluate(registry, state)[cert.name] == APPLICABLE, "NOT_APPLICABLE")
        receipt = {"certificate": cert.identity, "kind": cert.kind,
                   "statement": cert.statement, "subject": cert.subject,
                   "registry": state.registry, "before": state.identity}
    else:
        raise ValueError("UNKNOWN_OPERATION")
    journal = digest("step", [state.identity, event])
    result = Snapshot(state.generation + 1, state.registry, tuple(sorted(context.items())),
                      tuple(sorted(facts.items())), journal)
    if receipt is not None:
        receipt.update(after=result.identity, event=digest("event", event))
    return result, receipt


def replay(registry: tuple[Certificate, ...], initial: Snapshot, events: list[dict],
           checkpoint: str) -> tuple[Snapshot, tuple[dict, ...]]:
    state, receipts = initial, []
    for event in events:
        state, receipt = transition(registry, state, event)
        if receipt is not None:
            receipts.append(receipt)
    require(state.identity == checkpoint, "CHECKPOINT_MISMATCH")
    return state, tuple(receipts)


ABSORPTION_FIELDS = ("source_sha", "target_sha", "statement", "artifact_manifest",
                     "terminal", "parity_receipt", "review_receipt", "scope")


def absorption_keys(record: dict) -> tuple[str, ...]:
    require(type(record) is dict and set(record) == set(ABSORPTION_FIELDS), "BAD_ABSORPTION")
    require(all(is_hash(record[k], 40 if k.endswith("_sha") else 64)
                for k in ABSORPTION_FIELDS if k != "terminal"), "BAD_ABSORPTION_DIGEST")
    require(record["terminal"] in ("PARENT_SUFFICIENT", "CORRECTED_FOUNDATION_FRAGMENT",
                                   "SCOPED_THEORY_PARENT_OWNED"), "UNRESOLVED_STUDY")
    identity = digest("absorption", record)
    return tuple("root:" + role + ":" + identity for role in
                 ("source-verified", "independent-review-verified", "parity-verified", "adoption-authorized"))


def absorption_status(record: dict, facts: dict[str, str], source_sha: str,
                      target_sha: str) -> int:
    keys = absorption_keys(record)
    require(type(facts) is dict and all(type(k) is str and type(v) is str and v in FACTS
                                     for k, v in facts.items()), "BAD_EXTERNAL_FACTS")
    require(record["source_sha"] == source_sha and record["target_sha"] == target_sha,
            "ABSORPTION_REF_DRIFT")
    return min(FACTS.get(facts.get(k), UNRESOLVED) for k in keys)
