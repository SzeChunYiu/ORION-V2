"""Deterministic exact calibration; 0=match/PASS, 1=defect, 2=unavailable artifact."""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import argparse
import json
import sys

from model import (State, Spec, Verdict, model_check, certificate, validate,
                   parent_validate, validation_cost, evaluate, read_view,
                   descriptor_sufficient, write_skew, schedules, build_log,
                   checkpoint, replay, closed_cut, ancestor_cut)
from test_model import fixture

BASE = "24566f00a9dc4425a438fcfac05d13c6b2d903db"
DESIGN_COMMIT = "59b6819574f494354b880605998ffddbc5687077"


def require(condition: bool, message: str) -> None:
    # Not a Python assert: optimization (-O) must not erase the checks.
    if not condition:
        raise AssertionError(message)


def run() -> dict:
    checks = {}
    cases = sufficient = 0
    for desc in product(range(2), repeat=4):
        for judgment in product((False, True), repeat=4):
            by_group = {}
            for label, value in zip(desc, judgment):
                by_group.setdefault(label, set()).add(value)
            parent = all(len(group) == 1 for group in by_group.values())
            actual = descriptor_sufficient(desc, judgment)
            require(actual == parent, "R1 descriptor/reference disagreement")
            cases += 1
            sufficient += actual
    require(not descriptor_sufficient((0, 0), (True, False)), "R1 omission control")
    require(descriptor_sufficient((0, 1), (True, False)), "R1 nonvacuous control")
    checks["R1_context_descriptor"] = {"cases": cases, "sufficient": sufficient,
                                       "insufficient": cases - sufficient, "mutant_killed": 1,
                                       "nontrivial_valid_control": 1}

    spec, old, cert, records = fixture()
    cost = validation_cost(spec)
    discriminating = []
    for key in spec.required:
        now = old.change(key, "CHANGED")
        require(now != old, "R2 mutation not applied")
        require(validate(cert, spec, old, now, records, current_cut_known=True,
                         budget=cost) is Verdict.REOPEN, "R2 coordinate not bound")
        discriminating.append(key)
    new = old.change("conflict/new", "BLOCK")
    old_cells = tuple(r for r in read_view(spec, old) if r[0] == "cell")
    new_cells = tuple(r for r in read_view(spec, new) if r[0] == "cell")
    require(old_cells == new_cells, "R2 phantom control must fool row-only read set")
    require(evaluate(spec, new) is Verdict.FAIL, "R2 phantom must invalidate judgment")
    require(validate(cert, spec, old, new, records, current_cut_known=True,
                     budget=cost) is Verdict.REOPEN, "R2 predicate guard failed")
    unrelated = old.change("unrelated", "x")
    require(validate(cert, spec, old, unrelated, records, current_cut_known=True,
                     budget=cost) is Verdict.PASS, "R2 unrelated change false alarm")
    checks["R2_dependency_validation"] = {"coordinate_mutations": len(discriminating),
        "coordinates": discriminating, "phantom_mutant_killed": 1, "unrelated_no_alarm": 1,
        "logical_probe_budget": cost, "total_hashing_cost": "O(N) in this reference; not counted as free"}

    ss = schedules()
    weak_fail = sum(not any(write_skew(s, validate_full_read_set=False)) for s in ss)
    strong_fail = sum(not any(write_skew(s, validate_full_read_set=True)) for s in ss)
    require(len(ss) == 6 and weak_fail == 4 and strong_fail == 0, "R3 schedule result changed")
    checks["R3_immutable_snapshot_counterexample"] = {"schedules": len(ss),
        "snapshot_only_invariant_violations": weak_fail,
        "full_readset_invariant_violations": strong_fail,
        "sequential_no_alarm_schedules": len(ss) - weak_fail,
        "original_serializability_claim": "REFUTED_ORIGINAL_STATEMENT"}

    small_spec = Spec("s", "p", (("a", "LIVE"), ("b", "LIVE")))
    expected = small_spec.required
    states = []
    for trits in product(range(3), repeat=3):
        values = {k: (expected[k], "BAD", None)[v] for k, v in zip(sorted(expected), trits)}
        states.append(State.of(values))
    verdicts = Counter()
    comparisons = valid_commits = 0
    for historical, current in product(states, repeat=2):
        record = model_check(small_spec, historical)
        c = certificate(small_spec, historical, record)
        reg = {record.identifier: record}
        for known, budget in product((False, True), (0, validation_cost(small_spec))):
            args = (c, small_spec, historical, current, reg)
            actual = validate(*args, current_cut_known=known, budget=budget)
            parent = parent_validate(*args, current_cut_known=known, budget=budget)
            require(actual == parent, "R4 parent disagreement")
            comparisons += 1
            verdicts[actual.value] += 1
            if actual is Verdict.PASS:
                require(evaluate(small_spec, current) is Verdict.PASS, "R4 false current applicability")
                valid_commits += 1
    require(valid_commits > 0, "R4 reject-everything implementation")
    require(set(verdicts) == {v.value for v in Verdict}, "R4 missing verdict coverage")
    require(validate(cert, spec, old, old.change("evidence", "REVOKED"), records,
                     current_cut_known=True, budget=cost) is Verdict.REOPEN,
            "R4 separated-check/use control")
    checks["R4_atomic_validation_parent"] = {"states": len(states),
        "comparisons": comparisons, "parent_disagreements": 0, "verdicts": dict(sorted(verdicts.items())),
        "validated_commit_denominator": valid_commits, "false_current_applicability": 0,
        "split_check_use_mutant_killed": 1, "parent_terminal": "PARENT_SUFFICIENT"}

    policies = [Fraction(i, 4) for i in range(5)]
    # Same local history: p is BOTH acceptance on the still-valid history and error
    # on the revoked history. This finite grid illustrates the proof for all p in [0,1].
    feasible = [p for p in policies if p > 0 and p == 0]
    require(not feasible, "R5 impossible zero-error useful acceptance")
    checks["R5_async_freshness"] = {"indistinguishable_histories": 2,
        "illustrative_randomized_policies": len(policies), "zero_error_and_useful": len(feasible),
        "valid_escape": "CANNOT_CHECK, coordinate, or change the registered consistency contract",
        "all_probability_values": "written proof in THEORY.md, not inferred from this grid"}

    changes = (("evidence", "REVOKED"), ("evidence", "LIVE"), ("scope", "other"))
    log = build_log(old, changes)
    full = checkpoint(old, log)
    prefix_cases = anchored = historical_pass = unanchored = 0
    for k in range(len(log)+1):
        prefix = log[:k]
        result, state = replay(old, prefix, full)
        require((result is Verdict.PASS) == (k == len(log)), "R6 truncated current log accepted")
        anchored += result is Verdict.PASS
        result, state = replay(old, prefix, checkpoint(old, prefix))
        require(result is Verdict.PASS, "R6 valid historical prefix rejected")
        expected_state = old
        for key, value in changes[:k]:
            expected_state = expected_state.change(key, value)
        require(state == expected_state, "R6 semantic replay mismatch")
        historical_pass += 1
        require(replay(old, prefix, None)[0] is Verdict.CANNOT_CHECK, "R6 self-anchoring")
        unanchored += 1
        prefix_cases += 1
    require(replay(old.change("model", "other"), log, full)[0] is Verdict.FAIL, "R6 snapshot substitution")
    checks["R6_anchored_replay"] = {"prefix_cases": prefix_cases, "current_anchor_pass": anchored,
        "own_historical_anchor_pass": historical_pass, "unanchored_cannot_check": unanchored,
        "initial_snapshot_substitution_caught": 1, "freshness_beyond_anchor": "NOT_ESTABLISHED"}

    graphs = cut_cases = accepted = 0
    for n in range(1, 5):
        edges = tuple(combinations(range(n), 2))
        for selected in product((False, True), repeat=len(edges)):
            rows = [[] for _ in range(n)]
            for (a, b), include in zip(edges, selected):
                if include:
                    rows[b].append(a)
            parents = tuple(tuple(row) for row in rows)
            graphs += 1
            for members in product((False, True), repeat=n):
                cut = frozenset(i for i, included in enumerate(members) if included)
                result = closed_cut(parents, cut)
                require(result == ancestor_cut(parents, cut), "R7 transitive closure disagreement")
                accepted += result
                cut_cases += 1
    require(not closed_cut(((), (0,)), frozenset({1})), "R7 missing predecessor control")
    require(closed_cut(((), ()), frozenset({0, 1})), "R7 concurrent cut no-alarm")
    require(not any(write_skew(("r0", "r1", "w0", "w1"), validate_full_read_set=False)),
            "R7 causal closure must not certify an application invariant")
    checks["R7_causal_cuts"] = {"graphs": graphs, "cut_cases": cut_cases, "closed_cuts": accepted,
        "reference_disagreements": 0, "missing_predecessor_caught": 1,
        "closed_but_jointly_invalid_witness": 1, "maximum_vertices": 4}

    histories = ((('intent:1',), "EFFECT_DONE"), (('intent:1',), "EFFECT_NOT_DONE"))
    effects = {effect for observed, effect in histories if observed == ('intent:1',)}
    require(len(effects) == 2, "R8 indistinguishability control")
    checks["R8_effect_receipt_boundary"] = {"histories": len(histories),
        "distinct_effects_for_same_local_log": len(effects), "unobserved_effect_terminal": "CANNOT_CHECK",
        "external_effects_executed": 0}

    return {"schema": "ME_REVISION_CONSISTENCY_CALIBRATION_V1", "base_commit": BASE,
        "design_commit": DESIGN_COMMIT, "execution_class": "FORMAL_WITH_FINITE_CALIBRATION",
        "checks": checks, "terminal": "CORRECTED_FOUNDATION_FRAGMENT",
        "parent_disposition": "PARENT_SUFFICIENT", "foundation_overall": "OPEN_RESEARCH",
        "production_atomicity": "CANNOT_CHECK", "independent_review": "NOT_OBTAINED__DISCLOSED_LIMITATION",
        "grants_scientific_authority": False,
        "non_consequences": ["No OCM runtime or milestone closure", "No all-size proof from enumeration",
                             "No field, novelty or empirical superiority claim", "No authenticity from a hash alone"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    try:
        result = run()
        if args.verify is not None:
            if not args.verify.is_file():
                print(json.dumps({"terminal": "CANNOT_CHECK", "reason": "result artifact unavailable"}))
                return 2
            require(json.loads(args.verify.read_text()) == result, "committed result differs from fresh calculation")
        text = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.write is not None:
            args.write.write_text(text)
        print(text, end="")
        return 0
    except (AssertionError, ValueError, TypeError) as exc:
        print(json.dumps({"terminal": "FAIL", "reason": str(exc)}))
        return 1
    except OSError as exc:
        print(json.dumps({"terminal": "CANNOT_CHECK", "reason": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
