"""Deterministic finite calibration; no assertion removal under python -O."""
from collections import Counter
from itertools import product
from temporal import (Envelope, Verdict, classify, completion_reference, kernel,
                      parent_kernel, path_reference, subsets, verify_witness, Witness)


def require(ok, label):
    if not ok:
        raise AssertionError(label)


def run():
    graph_count = kernel_cases = belief_cases = path_cases = adverse_paths = 0
    outcomes = Counter()
    for n in (1, 2, 3):
        all_edges = tuple(product(range(n), repeat=2))
        beliefs = tuple(b for b in subsets(range(n)) if b)
        for edges in subsets(all_edges):
            graph_count += 1
            for good in subsets(range(n)):
                k = kernel(n, edges, good)
                parent = parent_kernel(n, edges, good)
                require(k.safe == parent, "kernel parent disagreement")
                require(k.reverse_edge_visits <= len(edges), "nonlinear reverse visits")
                kernel_cases += 1
                env = Envelope(n, edges, edges, good, "exhaustive-exact-v2")
                for start in range(n):
                    path = k.adverse_path(start)
                    alternate = path_reference(n, edges, good, start)
                    require((path is None) == (alternate is None), "path reachability")
                    if path is not None:
                        require(len(path) == len(alternate) <= n, "shortest simple witness")
                        require(verify_witness(env, Witness(env.fingerprint, "upper", path), start), "path verification")
                        adverse_paths += 1
                    path_cases += 1
                for belief in beliefs:
                    result = classify(env, belief)
                    expected = Verdict.PERSISTENT if belief <= parent else Verdict.REFUTED
                    require(result == expected, "exact belief disagreement")
                    outcomes[result.value] += 1
                    belief_cases += 1
    edges = tuple(product(range(2), repeat=2))
    partial_counts = Counter()
    partial_cases = completion_cases = 0
    envelopes = []
    for assignment in product(range(3), repeat=len(edges)):
        lower = frozenset(e for e, v in zip(edges, assignment) if v == 2)
        upper = frozenset(e for e, v in zip(edges, assignment) if v != 0)
        envelopes.append((lower, upper))
        for good in subsets(range(2)):
            env = Envelope(2, lower, upper, good, "exhaustive-partial-v2")
            for belief in subsets(range(2)):
                if not belief:
                    continue
                actual = classify(env, belief)
                require(actual == completion_reference(env, belief), "completion disagreement")
                partial_counts[actual.value] += 1
                partial_cases += 1
                completion_cases += 1 << len(upper - lower)
    refinement_cases = 0
    for (lo, hi), (new_lo, new_hi) in product(envelopes, repeat=2):
        if not (lo <= new_lo <= new_hi <= hi):
            continue
        for good in subsets(range(2)):
            old = Envelope(2, lo, hi, good, "same-scope-v2")
            new = Envelope(2, new_lo, new_hi, good, "same-scope-v2")
            for belief in subsets(range(2)):
                if belief:
                    before, after = classify(old, belief), classify(new, belief)
                    require(before == Verdict.CANNOT_CHECK or before == after, "decisive refinement flip")
                    refinement_cases += 1
    require(graph_count == 530 and kernel_cases == 4164 and belief_cases == 28868, "exact denominator")
    require(path_cases == 12420 and partial_cases == 972 and completion_cases == 3072, "partial denominator")
    require(refinement_cases == 7500, "refinement denominator")
    return {"schema": "ME_TEMPORAL_CALIBRATION_V2", "terminal": "PARENT_SUFFICIENT",
            "scope": "REGISTERED_FINITE_REVISION_MODELS_ONLY", "foundation_overall": "OPEN_RESEARCH",
            "exact": {"graphs": graph_count, "kernel_cases": kernel_cases, "belief_cases": belief_cases,
                      "outcomes": dict(sorted(outcomes.items())), "path_cases": path_cases,
                      "adverse_paths": adverse_paths, "parent_disagreements": 0},
            "partial": {"envelopes": len(envelopes), "belief_cases": partial_cases,
                        "completion_cases": completion_cases, "outcomes": dict(sorted(partial_counts.items())),
                        "completion_disagreements": 0, "refinement_cases": refinement_cases,
                        "decisive_flips": 0},
            "all_size_proof_source": "THEORY.md written arguments, not enumeration",
            "production_model_closure": "CANNOT_CHECK", "grants_scientific_authority": False}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), sort_keys=True, indent=2))
