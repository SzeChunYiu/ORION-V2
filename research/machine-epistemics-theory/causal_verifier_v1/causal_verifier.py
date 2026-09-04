"""Finite causal/verifier foundation: exact semantics, not an OCM runtime.

No external packages, network, model calls, random sampling, or hidden solver
access. All distributions use exact Fraction arithmetic. See THEORY.md for
assumptions: finite-class coverage and truthful evidence are not inferred from
registration, hashes, agreement, or successful execution of this checker.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import cache
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
from typing import Iterable, Sequence

Bit = int
Intervention = tuple[int | None, int | None]
Distribution = tuple[Q, Q, Q, Q]
INTERVENTIONS: tuple[Intervention, ...] = tuple(product((None, 0, 1), repeat=2))
VALUES = (Q(0), Q(1, 2), Q(1))
QUERIES = ("Y1_do_X0", "Y1_do_X1", "Y0_equals_Y1", "natural_X1")


class CannotCheck(Exception):
    """Missing coverage/scope/tool assumptions, never a successful check."""


def require(condition: bool, message: str) -> None:
    # Unlike assert, load-bearing validation survives python -O.
    if not condition:
        raise ValueError(message)


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def powerset(xs: Sequence) -> Iterable[tuple]:
    for size in range(len(xs) + 1):
        yield from combinations(xs, size)


@dataclass(frozen=True)
class SCM:
    """X=f(U), Y=g(X,U), U uniform on {0,1}; g indexed by 2*X+U."""
    f: tuple[int, int]
    g: tuple[int, int, int, int]

    def __post_init__(self) -> None:
        require(len(self.f) == 2 and len(self.g) == 4, "SCM table shape")
        require(all(type(b) is int and b in (0, 1) for b in self.f + self.g), "SCM bits")

    def run(self, u: int, intervention: Intervention = (None, None)) -> tuple[int, int]:
        require(type(u) is int and u in (0, 1), "exogenous bit")
        require(len(intervention) == 2 and all(v is None or (type(v) is int and v in (0, 1))
                                               for v in intervention), "intervention")
        x = self.f[u] if intervention[0] is None else intervention[0]
        y = self.g[2 * x + u] if intervention[1] is None else intervention[1]
        return x, y

    @cache
    def distribution(self, intervention: Intervention = (None, None)) -> Distribution:
        counts = Counter(self.run(u, intervention) for u in (0, 1))
        return tuple(Q(counts[(x, y)], 2) for x, y in product((0, 1), repeat=2))

    @cache
    def interventional_signature(self) -> tuple:
        return tuple(self.distribution(i) for i in INTERVENTIONS)

    @cache
    def response_law(self) -> tuple[Q, ...]:
        # Joint law of natural X, Y(do X=0), Y(do X=1), with SAME U.
        counts = Counter((self.f[u], self.g[u], self.g[2 + u]) for u in (0, 1))
        return tuple(Q(counts[r], 2) for r in product((0, 1), repeat=3))

    def as_dict(self) -> dict:
        return {"f": list(self.f), "g": list(self.g)}


@cache
def models() -> tuple[SCM, ...]:
    return tuple(SCM(f, g) for f in product((0, 1), repeat=2)
                 for g in product((0, 1), repeat=4))


@cache
def query_value(model: SCM, query: str) -> Q:
    if query == "Y1_do_X0":
        d = model.distribution((0, None))
        return d[1] + d[3]
    if query == "Y1_do_X1":
        d = model.distribution((1, None))
        return d[1] + d[3]
    if query == "Y0_equals_Y1":
        return Q(sum(model.g[u] == model.g[2 + u] for u in (0, 1)), 2)
    if query == "natural_X1":
        return Q(sum(model.f), 2)
    raise CannotCheck("UNREGISTERED_QUERY:" + query)


def distribution_from_response_law(law: tuple[Q, ...], intervention: Intervention) -> Distribution:
    """Alternate pushforward evaluator: does not call SCM.run/distribution."""
    require(len(law) == 8 and all(isinstance(p, Q) and p >= 0 for p in law)
            and sum(law) == 1, "response law")
    require(len(intervention) == 2 and all(v is None or (type(v) is int and v in (0, 1))
                                          for v in intervention), "intervention")
    out = [Q(0)] * 4
    for mass, (natural_x, y0, y1) in zip(law, product((0, 1), repeat=3)):
        x = natural_x if intervention[0] is None else intervention[0]
        y = (y0 if x == 0 else y1) if intervention[1] is None else intervention[1]
        out[2 * x + y] += mass
    return tuple(out)


def check_alternate_oracle() -> dict:
    comparisons = 0
    for model, intervention in product(models(), INTERVENTIONS):
        a = model.distribution(intervention)
        b = distribution_from_response_law(model.response_law(), intervention)
        require(a == b, "STRUCTURAL_VS_RESPONSE_ORACLE_DISAGREEMENT")
        comparisons += 1
    return {"structural_vs_response_pushforward": comparisons,
            "independent_implementation_paths": True,
            "independent_author_or_external_reviewer": False}


@dataclass(frozen=True)
class Evidence:
    """Typed mathematical evidence predicate, NOT a self-authenticating record.

    EXACT_DISTRIBUTION requires an externally valid full-law certificate;
    OBSERVED_EVENT only certifies occurrence of one event. RESPONSE_LAW is a
    stronger, explicitly charged oracle/certificate, not a field observation.
    """
    evidence_id: str
    kind: str
    payload: tuple
    intervention: Intervention = (None, None)
    scope: str = "source"

    def __post_init__(self) -> None:
        require(bool(self.evidence_id) and bool(self.scope), "empty evidence identity/scope")
        require(self.kind in {"EXACT_DISTRIBUTION", "OBSERVED_EVENT", "RESPONSE_LAW"}, "evidence kind")
        require(len(self.intervention) == 2 and all(v is None or (type(v) is int and v in (0, 1))
                                                   for v in self.intervention), "intervention")
        if self.kind == "OBSERVED_EVENT":
            require(len(self.payload) == 2 and all(type(v) is int and v in (0, 1)
                                                   for v in self.payload), "event payload")
        else:
            n = 4 if self.kind == "EXACT_DISTRIBUTION" else 8
            require(len(self.payload) == n and all(isinstance(v, Q) and v >= 0
                                                    for v in self.payload), "distribution payload")
            require(sum(self.payload) == 1, "distribution normalization")
        if self.kind == "RESPONSE_LAW":
            require(self.intervention == (None, None), "response law is not one intervention")

    def matches(self, model: SCM) -> bool:
        if self.kind == "EXACT_DISTRIBUTION":
            return model.distribution(self.intervention) == self.payload
        if self.kind == "RESPONSE_LAW":
            return model.response_law() == self.payload
        x, y = self.payload
        return model.distribution(self.intervention)[2 * x + y] > 0

    def as_dict(self) -> dict:
        return {"id": self.evidence_id, "kind": self.kind, "payload": list(map(str, self.payload)),
                "intervention": self.intervention, "scope": self.scope}


def validate_evidence(evidence: Sequence[Evidence], scope: str) -> None:
    identities: dict[str, dict] = {}
    for e in evidence:
        if e.scope != scope:
            raise CannotCheck("SCOPE_MISMATCH:" + e.evidence_id)
        content = e.as_dict()
        if e.evidence_id in identities:
            require(identities[e.evidence_id] == content, "EVIDENCE_ID_COLLISION")
        identities[e.evidence_id] = content


def compatible(evidence: Sequence[Evidence], *, scope: str = "source",
               family: Sequence[SCM] | None = None) -> tuple[SCM, ...]:
    validate_evidence(evidence, scope)
    fam = models() if family is None else tuple(family)
    if not fam:
        raise CannotCheck("NO_REGISTERED_MODEL_CLASS")
    return tuple(m for m in fam if all(e.matches(m) for e in evidence))


def classify_family(family: Sequence[SCM], query: str, value: Q) -> str:
    if not family:
        return "INCONSISTENT"
    answers = {query_value(m, query) == value for m in family}
    return "SUPPORTED" if answers == {True} else "REFUTED" if answers == {False} else "UNKNOWN"


def assess(evidence: Sequence[Evidence], query: str, value: Q, *, scope: str = "source") -> str:
    return classify_family(compatible(evidence, scope=scope), query, value)


def minimal_supports(evidence: Sequence[Evidence], query: str, value: Q, *,
                     polarity: bool = True) -> tuple[frozenset[str], ...]:
    """Exact minimal sufficient supports over a CONSISTENT finite record set."""
    validate_evidence(evidence, "source")
    unique = tuple({e.evidence_id: e for e in evidence}.values())
    require(bool(compatible(unique)), "INCONSISTENT_BASE_FOR_MONOTONE_PROVENANCE")
    wanted = "SUPPORTED" if polarity else "REFUTED"
    out: list[frozenset[str]] = []
    for subset in powerset(unique):
        ids = frozenset(e.evidence_id for e in subset)
        if any(s <= ids for s in out):
            continue
        if assess(subset, query, value) == wanted:
            out.append(ids)
    return tuple(out)


def survives(supports: Sequence[frozenset[str]], revoked: Iterable[str]) -> bool:
    removed = frozenset(revoked)
    return any(not (s & removed) for s in supports)


def direct_mask(evidence: Sequence[Evidence]) -> int:
    """Separate bitset intersection evaluator; not an independent reviewer."""
    mask = (1 << len(models())) - 1
    for e in evidence:
        local = sum(1 << j for j, m in enumerate(models()) if e.matches(m))
        mask &= local
    return mask


def classify_mask(mask: int, query: str, value: Q) -> str:
    if mask == 0:
        return "INCONSISTENT"
    true_mask = sum(1 << j for j, m in enumerate(models()) if query_value(m, query) == value)
    return "SUPPORTED" if mask & true_mask == mask else "REFUTED" if mask & true_mask == 0 else "UNKNOWN"


def coupling_table(p: Q, q: Q, joint: Q) -> tuple[Q, Q, Q, Q]:
    """Joint law of binary error events A,B; order 00,01,10,11."""
    require(0 <= p <= 1 and 0 <= q <= 1, "marginal probabilities")
    table = (1 - p - q + joint, q - joint, p - joint, joint)
    require(all(x >= 0 for x in table), "INCOMPATIBLE_COUPLING")
    return table


def joint_bounds(p: Q, q: Q, event: tuple[int, int, int, int]) -> tuple[Q, Q]:
    require(len(event) == 4 and all(type(b) is int and b in (0, 1) for b in event), "joint event")
    lo, hi = max(Q(0), p + q - 1), min(p, q)
    vals = [sum(x * b for x, b in zip(coupling_table(p, q, t), event)) for t in (lo, hi)]
    return min(vals), max(vals)


def law_evidence(m: SCM) -> tuple[Evidence, ...]:
    return (Evidence("obs", "EXACT_DISTRIBUTION", m.distribution()),
            Evidence("do0", "EXACT_DISTRIBUTION", m.distribution((0, None)), (0, None)),
            Evidence("do1", "EXACT_DISTRIBUTION", m.distribution((1, None)), (1, None)),
            Evidence("joint", "RESPONSE_LAW", m.response_law()))


def check_hierarchy() -> dict:
    # Cause vs latent common cause: same observational law, different intervention.
    cause = SCM((0, 1), (0, 0, 1, 1))
    confound = SCM((0, 1), (0, 1, 0, 1))
    require(cause.distribution() == confound.distribution(), "observational witness")
    require(query_value(cause, "Y1_do_X1") == 1 and
            query_value(confound, "Y1_do_X1") == Q(1, 2), "interventional separation")
    # Same entire family of single-world interventional laws, different coupling.
    same = SCM((0, 0), (0, 1, 0, 1))
    flip = SCM((0, 0), (0, 1, 1, 0))
    require(same.interventional_signature() == flip.interventional_signature(), "intervention witness")
    require(query_value(same, "Y0_equals_Y1") == 1 and
            query_value(flip, "Y0_equals_Y1") == 0, "counterfactual separation")
    pairs = 0
    for a, b in product(models(), repeat=2):
        if a.response_law() == b.response_law():
            require(a.interventional_signature() == b.interventional_signature(), "response sufficiency")
        if a.interventional_signature() == b.interventional_signature():
            require(a.distribution() == b.distribution(), "intervention includes observation")
        pairs += 1
    fibres: dict[tuple, set[tuple]] = {}
    for model in models():
        fibres.setdefault(model.interventional_signature(), set()).add(model.response_law())
    fibre_sizes = Counter(len(f) for f in fibres.values())
    require(fibre_sizes == {1: 32, 2: 2}, "counterfactual fibre histogram")
    return {"counterfactual_classes_per_interventional_class":
            {str(k): v for k, v in sorted(fibre_sizes.items())},
            "models": len(models()), "model_pairs": pairs,
            "observational_classes": len({m.distribution() for m in models()}),
            "interventional_classes": len({m.interventional_signature() for m in models()}),
            "counterfactual_response_classes": len({m.response_law() for m in models()}),
            "obs_not_do": {"models": [cause.as_dict(), confound.as_dict()], "P_Y1_do_X1": ["1", "1/2"]},
            "do_not_counterfactual": {"models": [same.as_dict(), flip.as_dict()], "P_equal": ["1", "0"]}}


def check_lifecycle() -> dict:
    verdicts: Counter = Counter()
    comparisons = revocations = retention = 0
    for hidden in models():
        evidence = law_evidence(hidden)
        subsets = tuple(powerset(evidence))
        families = {tuple(e.evidence_id for e in s): compatible(s) for s in subsets}
        masks = {tuple(e.evidence_id for e in s): direct_mask(s) for s in subsets}
        for query, value in product(QUERIES, VALUES):
            positive = minimal_supports(evidence, query, value)
            negative = minimal_supports(evidence, query, value, polarity=False)
            for s in subsets:
                key = tuple(e.evidence_id for e in s)
                family = families[key]
                result = classify_family(family, query, value)
                require(result == classify_mask(masks[key], query, value), "two evaluators disagree")
                require(hidden in family, "truthful evidence excluded hidden model")
                if result == "SUPPORTED":
                    require(query_value(hidden, query) == value, "unsound positive")
                if result == "REFUTED":
                    require(query_value(hidden, query) != value, "unsound negative")
                removed = {e.evidence_id for e in evidence} - set(key)
                require(survives(positive, removed) == (result == "SUPPORTED"), "positive retraction")
                require(survives(negative, removed) == (result == "REFUTED"), "negative retraction")
                verdicts[result] += 1
                comparisons += 1
                revocations += 2
            # Reinstate the exact records: reconstruction gives the original result.
            require(assess(tuple(reversed(evidence)), query, value) == assess(evidence, query, value),
                    "order/instate mismatch")
            retention += 1
    return {"hidden_models": 64, "evidence_records_per_model": 4,
            "active_subsets_per_model": 16, "query_value_claims_per_subset": 12,
            "list_vs_bitset_comparisons": comparisons, "positive_negative_retraction_checks": revocations,
            "reinstatement_permutation_checks": retention, "verdict_counts": dict(sorted(verdicts.items()))}


def check_couplings() -> dict:
    comparisons = tables = 0
    for n in range(1, 9):
        for pc, qc in product(range(n + 1), repeat=2):
            p, q = Q(pc, n), Q(qc, n)
            laws = tuple(coupling_table(p, q, Q(t, n))
                         for t in range(max(0, pc + qc - n), min(pc, qc) + 1))
            tables += len(laws)
            for event in product((0, 1), repeat=4):
                values = [sum(x * b for x, b in zip(law, event)) for law in laws]
                require((min(values), max(values)) == joint_bounds(p, q, event), "sharp coupling bounds")
                comparisons += 1
    marginal = Q(1, 20)
    lo, hi = joint_bounds(marginal, marginal, (0, 0, 0, 1))
    require((lo, hi) == (0, marginal), "dependent verifier bound")
    independent = marginal * marginal
    require(independent < hi, "independence laundering control")
    return {"denominator_range": [1, 8], "feasible_integer_tables": tables,
            "all_16_boolean_event_bound_checks": comparisons,
            "verifier_example": {"marginals": ["1/20", "1/20"],
                                 "joint_error_interval": [str(lo), str(hi)],
                                 "independence_only_value": str(independent)}}


def check_boundaries() -> dict:
    cause = SCM((0, 1), (0, 0, 1, 1))
    confound = SCM((0, 1), (0, 1, 0, 1))
    q = "Y1_do_X1"
    # A single event does not establish its generating distribution.
    sample = Evidence("sample", "OBSERVED_EVENT", (1, 1))
    e = law_evidence(cause)[0]
    require(len(compatible((sample,))) > len(compatible((e,))), "sample/distribution distinction")
    require(assess((sample,), q, Q(1)) == "UNKNOWN", "sample minted causal truth")
    # Contradictory exact laws: never true because all([]) happens to be True.
    zero = Evidence("zero", "EXACT_DISTRIBUTION", (Q(1), Q(0), Q(0), Q(0)))
    one = Evidence("one", "EXACT_DISTRIBUTION", (Q(0), Q(0), Q(0), Q(1)))
    require(assess((zero, one), q, Q(1)) == "INCONSISTENT", "vacuous certainty")
    # Same evidence repeated carries the same logical constraint, not new corroboration.
    require(compatible((e, e)) == compatible((e,)), "duplicate constraint")
    # Registration of an inaccurate law excludes the actual model: truthfulness matters.
    false_registered = Evidence("registered_but_false", "EXACT_DISTRIBUTION",
                                cause.distribution((1, None)), (1, None))
    require(not false_registered.matches(confound), "measurement fidelity counterexample")
    require(assess((false_registered,), q, Q(1)) == "SUPPORTED" and query_value(confound, q) != 1,
            "registration alone sufficient mutant")
    # Scope must be checked, not inferred by identical words/schema.
    try:
        assess((e,), q, Q(1), scope="target")
    except CannotCheck:
        pass
    else:
        raise ValueError("source evidence applied to target")
    # Source is identical in two environments; target is not constrained to match it.
    environments = ((cause, cause), (cause, confound))
    require(environments[0][0].interventional_signature() == environments[1][0].interventional_signature()
            and query_value(environments[0][1], q) != query_value(environments[1][1], q), "transport witness")
    # Agreement observations carry no relationship to the proposition truth bit.
    worlds = ((True, ("PASS", "PASS")), (False, ("PASS", "PASS")))
    require(worlds[0][1] == worlds[1][1] and worlds[0][0] != worlds[1][0], "verifier agreement witness")
    # Identical marginal component laws, opposite joint behavior.
    corr = coupling_table(Q(1, 2), Q(1, 2), Q(1, 2))
    anti = coupling_table(Q(1, 2), Q(1, 2), Q(0))
    require(corr[0] + corr[3] == 1 and anti[0] + anti[3] == 0, "component coupling witness")
    return {"sample_compatible_models": len(compatible((sample,))),
            "full_observation_law_compatible_models": len(compatible((e,))),
            "inconsistent_no_vacuity": 1, "duplicate_no_new_logical_information": 1,
            "registration_without_fidelity_refuted": 1, "scope_mismatch_refused": 1,
            "source_only_transport_refuted": 1, "agreement_without_truth_link_refuted": 1,
            "marginal_component_composition_refuted": 1}


def revision_trace() -> list[dict]:
    """A readable certificate revocation demonstration, not a runtime/action log."""
    model = SCM((0, 0), (0, 1, 0, 1))
    records = law_evidence(model)
    stages = (("single_world_laws", records[:3]), ("joint_certificate_added", records),
              ("joint_certificate_revoked", records[:3]), ("joint_certificate_reinstated", records))
    rows = [{"phase": phase, "active_evidence_ids": [e.evidence_id for e in active],
             "P_Y0_equals_Y1_is_1": assess(active, "Y0_equals_Y1", Q(1)),
             "P_Y1_do_X1_is_half": assess(active, "Y1_do_X1", Q(1, 2))}
            for phase, active in stages]
    require([r["P_Y0_equals_Y1_is_1"] for r in rows] ==
            ["UNKNOWN", "SUPPORTED", "UNKNOWN", "SUPPORTED"], "counterfactual reopens")
    require(all(r["P_Y1_do_X1_is_half"] == "SUPPORTED" for r in rows), "unrelated effect retained")
    return rows


def calibration() -> dict:
    return {"identity": "ME-CAUSAL-VERIFIER-V1", "calibration_class": "EXACT_FINITE_NOT_EMPIRICAL",
            "hierarchy": check_hierarchy(), "alternate_oracle": check_alternate_oracle(),
            "lifecycle": check_lifecycle(),
            "couplings": check_couplings(), "boundaries": check_boundaries(),
            "revision_trace": revision_trace(),
            "scientific_terminal": "PARENT_OWNED_FORMAL_FOUNDATION",
            "full_foundation_closed": False, "independent_review": "NOT_OBTAINED",
            "general_causal_discovery_or_real_llm_claim": False}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path, help="Compare exact body with a committed calibration JSON")
    parser.add_argument("--control", choices=("normal", "fail", "cannot-check"), default="normal")
    args = parser.parse_args(argv)
    try:
        if args.control == "cannot-check":
            raise CannotCheck("PLANTED_UNAVAILABLE_CERTIFICATE")
        if args.control == "fail":
            require(False, "PLANTED_FALSE_GREEN_CHECK")
        result = calibration()
        result["body_sha256"] = digest(result)
        if args.verify:
            old = json.loads(args.verify.read_text())
            require(old == result, "CALIBRATION_DRIFT")
        text = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(text)
        else:
            print(text, end="")
        return 0
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except (ValueError, OSError, TypeError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
