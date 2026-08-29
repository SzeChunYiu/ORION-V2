"""Shared exact finite-probability / partition utilities for #51 mechanical execution.

Two independent entropy implementations:
  * exact  — prime-exponent log-linear arithmetic over Fractions
             (ln p for distinct primes p are Q-linearly independent, so a
              rational-coefficient combination vanishes iff all coefficients
              are zero: exponentiate Π p^{c_p} = 1 and use unique factorisation)
  * decimal — Decimal at >= 90 significant digits via Decimal.ln()
Everything entropy-identity-shaped is checked with BOTH; structural partition
facts use only integer arithmetic.
"""
from __future__ import annotations

import json
from fractions import Fraction
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 110

LN2 = Decimal(2).ln()

# ---------------------------------------------------------------- partitions


def rgs_partitions(n: int):
    """All set partitions of {0..n-1} as restricted-growth sequences (tuples).

    Canonical form: class ids 0,1,2,... in order of first occurrence.
    """
    if n == 0:
        yield ()
        return
    a = [0] * n
    while True:
        yield tuple(a)
        i = n - 1
        while i >= 0:
            a[i] += 1
            if a[i] <= max(a[:i], default=-1) + 1:
                break
            a[i] = 0
            i -= 1
        else:
            return
        if i < 0:
            return


BELL_REFERENCE = {1: 1, 2: 2, 3: 5, 4: 15, 5: 52, 6: 203, 7: 877}


def check_bell(n: int, count: int) -> None:
    ref = BELL_REFERENCE[n]
    if count != ref:
        raise RuntimeError(f"Bell mismatch n={n}: enumerated {count} != reference {ref}")


def n_blocks(part) -> int:
    return len(set(part))


def intersect_all(sets):
    """Intersection over an iterable of set/frozenset objects (frozenset)."""
    it = iter(sets)
    try:
        out = frozenset(next(it))
    except StopIteration:
        return frozenset()
    for s in it:
        out &= frozenset(s)
    return out


def block_of(part):
    """dict element -> frozenset(block members)."""
    blocks = {}
    for i, c in enumerate(part):
        blocks.setdefault(c, set()).add(i)
    return {c: frozenset(m) for c, m in blocks.items()}


def refines(finer, coarser) -> bool:
    """True iff every block of `finer` lies inside one block of `coarser`."""
    mapping = {}
    for f, c in zip(finer, coarser):
        if f in mapping and mapping[f] != c:
            return False
        mapping[f] = c
    return True


def tuple_partition(*parts):
    """Common refinement: same class iff same class in every argument."""
    seen = {}
    out = []
    for key in zip(*parts):
        if key not in seen:
            seen[key] = len(seen)
        out.append(seen[key])
    return tuple(out)


DISCRETE = None  # sentinel filled per-n by callers


def discrete_partition(n: int):
    return tuple(range(n))


# ------------------------------------------------------- exact log algebra


def _factorize(m: int):
    out = {}
    d = 2
    while d * d <= m:
        while m % d == 0:
            out[d] = out.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        out[m] = out.get(m, 0) + 1
    return out


def log_vector(x: Fraction):
    """Prime-exponent vector e with  ln(x) == sum_p e_p ln p  (exact)."""
    x = Fraction(x)
    if x <= 0:
        raise ValueError("log of nonpositive rational")
    if x == 1:
        return {}
    num = _factorize(x.numerator)
    den = _factorize(x.denominator)
    out = {p: Fraction(e) for p, e in num.items()}
    for p, e in den.items():
        out[p] = out.get(p, Fraction(0)) - Fraction(e)
    return {p: e for p, e in out.items() if e != 0}


def expr_add(target: dict, coeff: Fraction, x: Fraction) -> None:
    """target += coeff * ln(x)"""
    for p, e in log_vector(x).items():
        target[p] = target.get(p, Fraction(0)) + coeff * e


def expr_is_zero(expr: dict) -> bool:
    return all(v == 0 for v in expr.values())


def expr_diff(a: dict, b: dict) -> dict:
    out = dict(a)
    for p, e in b.items():
        out[p] = out.get(p, Fraction(0)) - e
    return {p: e for p, e in out.items() if e != 0}


# --------------------------------------- joint tables over labelled samples


def joint_from_marginal(samples, probs):
    """samples: list of hashable tuples (one per history), probs: list[Fraction]."""
    table = {}
    for s, p in zip(samples, probs):
        key = tuple(s)
        table[key] = table.get(key, Fraction(0)) + p
    return table


def marginal(table, keep_idxs):
    out = {}
    for key, p in table.items():
        k = tuple(key[i] for i in keep_idxs)
        out[k] = out.get(k, Fraction(0)) + p
    return out


def h_expr(table: dict, idxs) -> dict:
    """Exact nats expression of H(variables at idxs) from a joint table."""
    m = marginal(table, idxs)
    expr = {}
    for p in m.values():
        expr_add(expr, p, 1 / p)
    return expr


def cond_h_expr(table: dict, cond_idxs, var_idxs) -> dict:
    """Exact nats expression of H(var | cond) from a joint table.

    H(Y|X) = sum_{xy} p_xy * ln( p_x / p_xy )
    """
    mx = marginal(table, cond_idxs)
    expr = {}
    for key, pxy in table.items():
        px = mx[tuple(key[i] for i in cond_idxs)]
        expr_add(expr, pxy, px / pxy)
    return expr


def cmi_expr(table: dict, a_idxs, b_idxs, cond_idxs) -> dict:
    """I(A;B|C) = H(A|C) - H(A|B,C)."""
    return expr_diff(
        cond_h_expr(table, cond_idxs, a_idxs),
        cond_h_expr(table, sorted(set(cond_idxs) | set(b_idxs)), a_idxs),
    )


# --------------------------------------------------- decimal cross-checking


def _dec_frac(f: Fraction) -> Decimal:
    return Decimal(f.numerator) / Decimal(f.denominator)


def h_dec(table: dict, idxs) -> Decimal:
    m = marginal(table, idxs)
    total = Decimal(0)
    for p in m.values():
        if p > 0:
            total += _dec_frac(p) * (_dec_frac(1 / p)).ln() / LN2
    return total


def cond_h_dec(table: dict, cond_idxs, var_idxs) -> Decimal:
    mx = marginal(table, cond_idxs)
    total = Decimal(0)
    for key, pxy in table.items():
        px = mx[tuple(key[i] for i in cond_idxs)]
        total += _dec_frac(pxy) * (_dec_frac(px / pxy)).ln() / LN2
    return total


def expr_to_dec(expr: dict) -> Decimal:
    """Evaluate a prime-exponent nats expression to bits (Decimal)."""
    total = Decimal(0)
    for p, e in expr.items():
        total += _dec_frac(e) * Decimal(p).ln() / LN2
    return total


# ------------------------------------------------------------------ worlds


def composition_vectors(total: int, length: int):
    """All positive integer vectors of given length summing to total."""
    if length == 1:
        yield (total,)
        return
    for first in range(1, total - length + 2):
        for rest in composition_vectors(total - first, length - 1):
            yield (first,) + rest


def rational_distributions(n: int, dmin: int = 2, dmax: int = 8):
    seen = set()
    for d in range(max(dmin, n), dmax + 1):
        for ks in composition_vectors(d, n):
            vec = tuple(Fraction(k, d) for k in ks)
            if vec not in seen:
                seen.add(vec)
                yield vec


# ------------------------------------------------------------------ output


def dump_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    class Enc(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Fraction):
                return {"__fraction__": [str(o.numerator), str(o.denominator)]}
            if isinstance(o, Decimal):
                return {"__decimal__": str(o)}
            if isinstance(o, frozenset):
                return sorted(o)
            if isinstance(o, set):
                return sorted(o)
            return super().default(o)

    path.write_text(json.dumps(obj, indent=2, sort_keys=True, cls=Enc) + "\n",
                    encoding="utf-8")
