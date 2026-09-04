"""Exact rational checker for MEG-09 parent reduction to strong lumpability/intertwining.

Exit 0 PASS, 1 FAIL, 2 CANNOT_CHECK. No novelty claim.
"""
from __future__ import annotations

import json
from fractions import Fraction

LIVE, DEAD, UNKNOWN = "LIVE", "DEAD", "UNKNOWN"


def row_block_sums(P, blocks):
    return [[sum(P[i][j] for j in block) for block in blocks] for i in range(len(P))]


def strong_lumpable(P, blocks):
    sums = row_block_sums(P, blocks)
    for block in blocks:
        for i in block:
            for j in block:
                if sums[i] != sums[j]:
                    return False
    return True


def quotient(P, blocks):
    if not strong_lumpable(P, blocks):
        raise ValueError("NON_LUMPABLE")
    sums = row_block_sums(P, blocks)
    return [[sums[block[0]][b] for b in range(len(blocks))] for block in blocks]


def push(vec, blocks):
    return [sum(vec[i] for i in block) for block in blocks]


def fixed_point(P, seed, alpha=Fraction(1, 3), max_steps=1000):
    # exact iteration; for the small triangular-ish witness it stabilizes only asymptotically,
    # so use closed form Gaussian solve of (I-(1-a)P^T)x = a s.
    n = len(seed)
    A = [[Fraction(int(i == j)) - (1-alpha)*P[j][i] for j in range(n)] for i in range(n)]
    b = [alpha*x for x in seed]
    # Gauss-Jordan over Q
    aug = [A[i][:] + [b[i]] for i in range(n)]
    for c in range(n):
        pivot = next((r for r in range(c, n) if aug[r][c] != 0), None)
        if pivot is None:
            raise ValueError("SINGULAR")
        aug[c], aug[pivot] = aug[pivot], aug[c]
        z = aug[c][c]
        aug[c] = [x/z for x in aug[c]]
        for r in range(n):
            if r == c: continue
            z = aug[r][c]
            if z:
                aug[r] = [x-z*y for x, y in zip(aug[r], aug[c])]
    return [aug[i][-1] for i in range(n)]


def measurable(blocks, values):
    return all(len({values[i] for i in block}) <= 1 for block in blocks)


def cemetery_embed(P):
    n = len(P)
    out = [[Fraction(0) for _ in range(n+1)] for _ in range(n+1)]
    for i,row in enumerate(P):
        for j,x in enumerate(row): out[i][j] = x
        missing = Fraction(1) - sum(row)
        if missing < 0: raise ValueError("SUPERSTOCHASTIC")
        out[i][n] = missing
    out[n][n] = Fraction(1)
    return out


def check_meg09():
    F = ((0,1),(2,3))
    P = [
        [Fraction(1,2),0,Fraction(1,2),0],
        [0,Fraction(1,2),0,Fraction(1,2)],
        [Fraction(1,4),0,Fraction(3,4),0],
        [0,Fraction(1,4),0,Fraction(3,4)],
    ]
    assert strong_lumpable(P,F)
    Q = quotient(P,F)
    assert Q == [[Fraction(1,2),Fraction(1,2)],[Fraction(1,4),Fraction(3,4)]]
    s = [Fraction(1),0,0,0]
    a = fixed_point(P,s)
    aq = fixed_point(Q,push(s,F))
    assert push(a,F) == aq

    bad = [row[:] for row in P]
    bad[1] = [0,Fraction(3,4),0,Fraction(1,4)]
    assert not strong_lumpable(bad,F)
    try:
        quotient(bad,F)
    except ValueError as e:
        assert str(e) == "NON_LUMPABLE"
    else:
        raise AssertionError("non-lumpable cross-fibre mutant accepted")

    good_live = [LIVE,LIVE,DEAD,DEAD]
    bad_live = [LIVE,DEAD,DEAD,DEAD]
    assert measurable(F,good_live)
    assert not measurable(F,bad_live)

    # Substochastic parent: missing mass becomes a cemetery state without changing live-state solve.
    Psub = [
        [Fraction(1,4),0,Fraction(1,4),0],
        [0,Fraction(1,4),0,Fraction(1,4)],
        [Fraction(1,4),0,Fraction(3,4),0],
        [0,Fraction(1,4),0,Fraction(3,4)],
    ]
    assert strong_lumpable(Psub,F)
    sub = fixed_point(Psub,s)
    Pcem = cemetery_embed(Psub)
    cem = fixed_point(Pcem,s+[Fraction(0)])
    assert cem[:4] == sub
    Fcem = ((0,1),(2,3),(4,))
    assert strong_lumpable(Pcem,Fcem)

    return {
        "fine_states":4,"fibres":2,"lumpable":1,"pushforward_fixed_point_exact":1,
        "cross_fibre_nonlumpable_mutant_caught":1,"warrant_measurable_no_alarm":1,
        "warrant_nonmeasurable_refine_required":1,"substochastic_cemetery_live_projection_equal":1,
        "terminal":"PARENT_LUMPABILITY_SUFFICIENT__KSO_ADDS_WARRANT_AND_ANSWER_MEASURABILITY",
        "GENERAL_NOVELTY":"NOT_ESTABLISHED"
    }


def main():
    try: out=check_meg09()
    except Exception as e:
        print(json.dumps({"status":"FAIL","type":type(e).__name__,"reason":str(e)},sort_keys=True)); return 1
    print(json.dumps({"status":"PASS","result":out},sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())
