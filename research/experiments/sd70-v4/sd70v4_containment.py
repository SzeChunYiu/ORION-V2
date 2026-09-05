#!/usr/bin/env python3
"""SD70-V4 non-containment certificate: the XOR square.

THEOREM (frozen argmax rule).  Let A = {0..A-1} be the actions, x ∈ {0,1}^f \\ {0} the contexts, and
`policy(x) = argmax_a (W_a · [x, 1])` with ties broken to the LOWEST index (sd70v3_generator.best_action /
sd70v3_parents.argmax_frozen).  Take two coordinates p ≠ q and four contexts x00, x01, x10, x11 that agree
outside {p, q} and take bits (0,0), (0,1), (1,0), (1,1) on (p, q).  Then, as vectors with the bias
appended, x00 + x11 = x01 + x10.  Suppose the labelling has policy(x00) = policy(x11) = a and
policy(x01) = policy(x10) = b with a ≠ b.  Put d = W_a − W_b.  Then d·x00 ≥ 0 and d·x11 ≥ 0 (a is a
maximiser at both), and d·x01 ≤ 0, d·x10 ≤ 0 (b is a maximiser at both); summing, d·(x00+x11) ≥ 0 and
d·(x01+x10) ≤ 0, and the two sums are equal, so every one of the four inner products is exactly 0.  Hence
a and b tie at all four contexts.  At x00 the label is a, so a is the lowest index in the argmax set, which
contains b: a < b.  At x01 the label is b with a in the argmax set: b < a.  Contradiction.  Therefore NO
linear multiclass argmax policy (any W, any bias) realises a labelling that contains an "aabb" XOR square,
and each such square is a checkable certificate of non-containment.  The V3 generator family is linear,
so its labellings contain zero such squares — the no-alarm control.  ∎

The checker enumerates every (p, q, base) square inside the nonzero-context domain and counts the
certificates; `MUTANT_IGNORE_LABELS` is the planted checker defect (counts every square) that the
selftest must catch.
"""
from __future__ import annotations

from itertools import combinations, product
from typing import Callable


def all_contexts(f: int) -> list[tuple[int, ...]]:
    return [c for c in product((0, 1), repeat=f) if any(c)]


def xor_square_certificates(policy: Callable[[tuple[int, ...]], int], f: int, *, mutant_ignore_labels: bool = False) -> list[dict]:
    """Every XOR square (p, q, base) in the nonzero-context domain whose labels form the aabb pattern."""
    out: list[dict] = []
    for p, q in combinations(range(f), 2):
        rest = [k for k in range(f) if k not in (p, q)]
        for base_bits in product((0, 1), repeat=len(rest)):
            def ctx(bp: int, bq: int) -> tuple[int, ...]:
                c = [0] * f
                for k, b in zip(rest, base_bits):
                    c[k] = b
                c[p], c[q] = bp, bq
                return tuple(c)
            square = [ctx(0, 0), ctx(0, 1), ctx(1, 0), ctx(1, 1)]
            if not all(any(c) for c in square):
                continue  # the all-zero context is outside the domain
            labels = [policy(c) for c in square]
            fires = (labels[0] == labels[3] and labels[1] == labels[2] and labels[0] != labels[1]) or mutant_ignore_labels
            if fires:
                out.append({"p": p, "q": q, "base": list(base_bits), "labels": labels})
    return out


def linear_containment_verdict(policy: Callable[[tuple[int, ...]], int], f: int) -> dict:
    certs = xor_square_certificates(policy, f)
    return {"xor_square_certificates": len(certs), "outside_linear_multiclass_class": len(certs) > 0,
            "first_certificate": certs[0] if certs else None,
            "note": "certificate = aabb XOR square; theorem in sd70v4_containment.py; zero certificates does NOT prove containment"}
