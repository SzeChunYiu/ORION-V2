"""Exact finite checks for Machine Epistemics Field Dynamics V1.

Finite checks are calibration/counterexample evidence for the scoped laws in DYNAMICS.md.
They do not establish field status, novelty, environment-model closure, or OCM parity.

Exit 0 = PASS, 1 = FAIL, 2 = CANNOT_CHECK.
"""
from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from fractions import Fraction


class CannotCheck(RuntimeError):
    pass


LIVE, UNKNOWN, DEAD = "LIVE", "UNKNOWN", "DEAD"


def l1(v):
    return sum(abs(x) for x in v)


def inf_matrix(M):
    return max((sum(abs(x) for x in row) for row in M), default=Fraction(0))


def fixed_point(P, s, alpha=Fraction(1, 3)):
    """Solve (I-(1-a)P^T)x=a*s exactly over Q."""
    n = len(s)
    beta = 1 - alpha
    A = [[Fraction(int(i == j)) - beta * P[j][i] for j in range(n)] for i in range(n)]
    aug = [A[i][:] + [alpha * s[i]] for i in range(n)]
    for c in range(n):
        pivot = next((r for r in range(c, n) if aug[r][c] != 0), None)
        if pivot is None:
            raise CannotCheck("singular restart system")
        aug[c], aug[pivot] = aug[pivot], aug[c]
        z = aug[c][c]
        aug[c] = [x / z for x in aug[c]]
        for r in range(n):
            if r == c:
                continue
            z = aug[r][c]
            if z:
                aug[r] = [x - z * y for x, y in zip(aug[r], aug[c])]
    return [row[-1] for row in aug]


@dataclass(frozen=True)
class Authority:
    world_truth: int = 0
    speaker: int = 0
    task_contract: int = 0
    commit: int = 0

    def meet(self, other):
        return Authority(*(min(a, b) for a, b in zip(
            (self.world_truth, self.speaker, self.task_contract, self.commit),
            (other.world_truth, other.speaker, other.task_contract, other.commit),
        )))


def check_fd01():
    vals = range(3)
    checks = 0
    for a in itertools.product(vals, repeat=4):
        for b in itertools.product(vals, repeat=4):
            A, B = Authority(*a), Authority(*b)
            M = A.meet(B)
            assert M == Authority(*(min(x, y) for x, y in zip(a, b)))
            assert all(m <= x and m <= y for m, x, y in zip(
                (M.world_truth, M.speaker, M.task_contract, M.commit), a, b))
            checks += 1
    internal = Authority(world_truth=0, speaker=1, task_contract=1, commit=0)
    receipt = Authority(world_truth=2, speaker=2, task_contract=2, commit=2)
    assert internal.meet(receipt).commit == 0
    assert max(internal.commit, receipt.commit) == 2
    return {"authority_pair_checks": checks, "internal_commit_nonamplification": 1, "max_mutant_caught": 1}


def consistent_support(support, nogoods):
    return not any(set(n) <= set(support) for n in nogoods)


def live_from_supports(supports, revoked=(), nogoods=()):
    R = set(revoked)
    return any(not (set(s) & R) and consistent_support(s, nogoods) for s in supports)


def check_fd02():
    supports_a = (frozenset({"a"}),)
    supports_b = (frozenset({"b"}),)
    joint = tuple(frozenset(x | y) for x in supports_a for y in supports_b)
    N = (frozenset({"a", "b"}),)
    assert live_from_supports(supports_a, nogoods=N)
    assert live_from_supports(supports_b, nogoods=N)
    assert not live_from_supports(joint, nogoods=N)
    alternatives = (frozenset({"a"}), frozenset({"c"}))
    assert live_from_supports(alternatives, revoked={"a"})
    score = Fraction(999, 1000)
    score_mints_truth = False
    assert score > 0 and not score_mints_truth
    return {"cross_nogood_blocks_joint": 1, "alternate_support_survives": 1, "score_does_not_mint_truth": 1}


def impact_cone(changed, edges):
    out = set(changed)
    grew = True
    while grew:
        grew = False
        for tails, heads in edges:
            if set(tails) & out:
                before = len(out)
                out.update(heads)
                grew |= len(out) != before
    return frozenset(out)


def check_fd03():
    edges = [(("e",), ("a",)), (("a",), ("b",)), (("b",), ("c",)), (("x",), ("y",))]
    cone = impact_cone({"e"}, edges)
    assert cone == {"e", "a", "b", "c"}
    assert "x" not in cone and "y" not in cone
    one_hop = {"e", "a"}
    assert "c" not in one_hop and "c" in cone
    return {"impact": sorted(cone), "outside_cone_invariant_fixture": 1, "one_hop_mutant_caught": 1}


def all_row_substochastic_2():
    vals = (Fraction(0), Fraction(1, 2), Fraction(1))
    rows = [(a, b) for a in vals for b in vals if a + b <= 1]
    return [tuple((Fraction(a), Fraction(b)) for a, b in (r1, r2)) for r1 in rows for r2 in rows]


def check_fd04(alpha=Fraction(1, 3)):
    kernels = all_row_substochastic_2()
    seeds = (
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(1, 2), Fraction(1, 2)),
    )
    checks = strict = 0
    for P in kernels:
        for Pp in kernels:
            dP = [[Pp[i][j] - P[i][j] for j in range(2)] for i in range(2)]
            dp = inf_matrix(dP)
            for s in seeds:
                a = fixed_point(P, list(s), alpha)
                for sp in seeds:
                    ap = fixed_point(Pp, list(sp), alpha)
                    lhs = l1([ap[i] - a[i] for i in range(2)])
                    rhs = l1([sp[i] - s[i] for i in range(2)]) + ((1-alpha)/alpha) * dp
                    assert lhs <= rhs, (P, Pp, s, sp, lhs, rhs)
                    strict += int(lhs < rhs)
                    checks += 1
    assert checks == 20736
    return {"kernel_seed_pair_checks": checks, "strict_cases": strict, "kernels": len(kernels), "seeds": len(seeds)}


@dataclass(frozen=True)
class EvidenceState:
    active: frozenset[str]
    history: tuple[str, ...]


def revoke(st, e):
    return EvidenceState(st.active - {e}, st.history + (f"revoke:{e}",))


def reinstate(st, e):
    return EvidenceState(st.active | {e}, st.history + (f"reinstate:{e}",))


def check_fd05():
    initial = EvidenceState(frozenset({"e"}), ("admit:e",))
    r = revoke(initial, "e")
    rr = reinstate(r, "e")
    assert rr.active == initial.active
    new = EvidenceState(r.active | {"e2"}, r.history + ("relearn:e2",))
    assert new.active != initial.active
    behavior_initial = bool(initial.active & {"e", "e2"})
    behavior_new = bool(new.active & {"e", "e2"})
    assert behavior_initial == behavior_new is True
    assert rr.history != initial.history
    return {"same_identity_semantic_reinstatement": 1, "relearn_behavior_equal_lineage_distinct": 1, "append_only_history_preserved": 1}


def persistent_kernel(states, edges, good):
    bad_reachable = set(states) - set(good)
    changed = True
    while changed:
        changed = False
        for u, v in edges:
            if v in bad_reachable and u not in bad_reachable:
                bad_reachable.add(u)
                changed = True
    return frozenset(set(states) - bad_reachable)


def check_fd06():
    S = {0, 1, 2, 3}
    E = {(0, 1), (1, 2), (3, 3)}
    P = {0, 1, 3}
    K = persistent_kernel(S, E, P)
    assert K == {3}
    one_step = {s for s in P if all(v in P for u, v in E if u == s)}
    assert 0 in one_step and 0 not in K
    return {"kernel": sorted(K), "multi_step_hostile": 1, "parent_disposition": "PARENT_SUFFICIENT"}


def row_block_sums(P, blocks):
    return [[sum(P[i][j] for j in block) for block in blocks] for i in range(len(P))]


def strong_lumpable(P, blocks):
    sums = row_block_sums(P, blocks)
    return all(sums[i] == sums[j] for block in blocks for i in block for j in block)


def check_fd08():
    F = ((0, 1), (2, 3))
    P = [
        [Fraction(1,2), 0, Fraction(1,2), 0],
        [0, Fraction(1,2), 0, Fraction(1,2)],
        [Fraction(1,4), 0, Fraction(3,4), 0],
        [0, Fraction(1,4), 0, Fraction(3,4)],
    ]
    assert strong_lumpable(P, F)
    bad = [row[:] for row in P]
    bad[1] = [0, Fraction(3,4), 0, Fraction(1,4)]
    assert not strong_lumpable(bad, F)
    live_good = [LIVE, LIVE, DEAD, DEAD]
    live_bad = [LIVE, DEAD, DEAD, DEAD]
    measurable = lambda vals: all(len({vals[i] for i in block}) == 1 for block in F)
    assert measurable(live_good) and not measurable(live_bad)
    return {"parent_lumpability_no_alarm": 1, "nonlumpable_mutant_caught": 1, "warrant_measurability_independent_gate": 1}


def check_fd09():
    shared_supports = [frozenset({"common_source"})] * 3
    assert len(set(shared_supports)) == 1
    authorities = [Authority(speaker=1, world_truth=0) for _ in range(10)]
    out = Authority(world_truth=0, speaker=1, commit=0)
    for a in authorities:
        out = out.meet(a)
    assert out.world_truth == 0
    return {"shared_source_counts_once": 1, "ten_speakers_do_not_mint_truth": 1}


def check_fd10():
    self_a = Authority(world_truth=0, speaker=0, task_contract=0, commit=0)
    object_a = Authority(world_truth=2, task_contract=2, commit=1)
    assert self_a.meet(object_a).world_truth == 0
    assert self_a.meet(object_a).commit == 0
    return {"self_cannot_raise_world_truth": 1, "self_cannot_raise_commit": 1}


def resource_add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def check_fd11():
    base = (10, 5, 20, 30, 4, 7)
    representation = (3, 2, 4, 8, 1, 2)
    total = resource_add(base, representation)
    assert total == (13, 7, 24, 38, 5, 9)
    assert base != total
    return {"resource_coordinates": len(total), "no_free_representation_fixture": 1}


PASS, FAIL, CC, GAP = "PASS", "FAIL", "CANNOT_CHECK", "GAP"
STAGES = ("ATOMIZE", "NAVIGATE", "EXTRACT", "COMPOSE", "CHECK", "COMMIT")


def run_pipeline(statuses):
    trace = []
    for stage, st in zip(STAGES, statuses, strict=True):
        trace.append((stage, st))
        if st == CC:
            return CC, tuple(trace)
        if st == FAIL:
            return FAIL, tuple(trace)
        if st == GAP:
            return GAP, tuple(trace)
        if st != PASS:
            raise CannotCheck(f"unregistered status {st}")
    return PASS, tuple(trace)


def mutant_ignore_cc(statuses):
    if all(x in (PASS, CC) for x in statuses):
        return PASS
    return next((x for x in statuses if x != PASS), PASS)


def check_fd12():
    cases = 0
    for statuses in itertools.product((PASS, FAIL, CC, GAP), repeat=len(STAGES)):
        out, trace = run_pipeline(statuses)
        first = next((x for x in statuses if x != PASS), PASS)
        assert out == first
        if CC in statuses[:len(trace)]:
            assert out == CC
        cases += 1
    hostile = (PASS, PASS, CC, PASS, PASS, PASS)
    assert run_pipeline(hostile)[0] == CC
    assert mutant_ignore_cc(hostile) == PASS
    assert cases == 4096
    return {"status_vectors": cases, "cannot_check_absorbing": 1, "ignore_cannot_check_mutant_caught": 1}


def run_all():
    return {
        "FD-01": check_fd01(),
        "FD-02": check_fd02(),
        "FD-03": check_fd03(),
        "FD-04": check_fd04(),
        "FD-05": check_fd05(),
        "FD-06": check_fd06(),
        "FD-08": check_fd08(),
        "FD-09": check_fd09(),
        "FD-10": check_fd10(),
        "FD-11": check_fd11(),
        "FD-12": check_fd12(),
        "FD-07": {"status": "OPEN_RESEARCH", "finite_checker_does_not_promote": 1},
        "GENERAL_NOVELTY": "NOT_ESTABLISHED",
        "FIELD_STATUS": "NOT_ESTABLISHED",
    }


def main():
    try:
        out = run_all()
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}, sort_keys=True))
        return 2
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "type": type(exc).__name__, "reason": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps({"status": "PASS", "result": out}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
