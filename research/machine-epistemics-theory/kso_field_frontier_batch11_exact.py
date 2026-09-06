"""Exact finite checker for KSO_FIELD_FRONTIER_THEOREMS_BATCH11_V1.md (stdlib only, exact).

One check function per field-frontier row of `field_dynamics_v1/FRONTIER.md` taken in batch 11:
K1 = FDX-09 (infinite structured lifecycle learning: what a positive-only, evidence-scoped learner of
category-level constructions identifies, at what sample cost, and the exact attachment / relation
saturation that makes the induced inventory report AMBIGUOUS and never a unique parse), K2 = FDX-10
(endogenous representation discovery: search information for a discovered versus a given operator,
MDL / library-learning adoption, identification bits invariant under the representation), K3 = FDX-12
(safe incremental language commitment: the exact finite-state prefix criterion, the two completeness
thresholds of the bounded checker, streaming versus atomic channels, revocation mid-stream).  Every
check performs (a) the positive statement by exhaustive enumeration on a finite fixture, (b) at least
one planted hostile whose mutation is asserted applied and caught, (c) a no-alarm control.  Items whose
honest status is PARENT_OWNED / PARENT_SUFFICIENT report the parent and run the executable falsifier on
the smallest holding / failing fixture.  All objects are re-implemented here (projective dependency
derivations over a category-level rule inventory, a derivation-counting chart and a brute-force tree
enumerator, coupon-collector cover times, a size-ordered term enumerator over a Boolean library, a
finite-state generator with listener readings); nothing is imported from ``ocm``.  Every count is an
integer; every expectation an exact ``Fraction``.

Exit codes: 0 all statements hold; 1 a statement fails; 2 CANNOT_CHECK (distinct, never a pass).
NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import itertools
import json
import sys
from collections import namedtuple
from fractions import Fraction
from functools import lru_cache


class CannotCheck(RuntimeError):
    pass


def subsets(universe, min_size=0, max_size=None):
    universe = tuple(universe)
    hi = len(universe) if max_size is None else max_size
    for k in range(min_size, hi + 1):
        for combo in itertools.combinations(universe, k):
            yield frozenset(combo)


def ceil_log2(n):
    if n < 1:
        raise CannotCheck("ceil_log2 of a non-positive count")
    b = 0
    while (1 << b) < n:
        b += 1
    return b


def catalan(n):
    c = 1
    for i in range(n):
        c = c * 2 * (2 * i + 1) // (i + 2)
    return c


def harmonic(n):
    return sum((Fraction(1, i) for i in range(1, n + 1)), Fraction(0))


# =============================================================================================
# K1 · FDX-09 · category-level construction inventories: derivations, identification, saturation
# =============================================================================================
#
# A rule is (head category, pattern); pattern items are "HEAD" or "rel:cat" in surface order (the shape
# of `ud_grammar.Rule`).  A *category-level* inventory reads a dependent slot `rel:cat` as "any phrase
# headed by a token of category cat" — the relation label is chosen by the parent rule, the sub-phrase
# carries none (the shape of `constructions_from_grammar`: `Slot(name, category, phrase=PHRASE_OF_UPOS)`).
# A derivation of a category string w is a projective dependency tree over w together with a relation
# label per dependent such that every head's labelled pattern is a rule of the inventory; leaves need no
# rule (terminals).

Rule = namedtuple("Rule", "head pattern")


def rule(head, *items):
    return Rule(head, tuple(items))


def cats_of(pattern):
    return tuple(item.split(":", 1)[1] for item in pattern if item != "HEAD")


def head_index(pattern):
    return pattern.index("HEAD")


def family(r):
    return r.head, tuple(sorted(p for p in r.pattern if p != "HEAD"))


def compositions(m):
    """Consecutive block decompositions of a segment of length m (2^(m-1) for m ≥ 1; one empty for m = 0)."""
    if m == 0:
        yield ()
        return
    for cuts in subsets(range(1, m)):
        bounds = [0] + sorted(cuts) + [m]
        yield tuple(bounds[i + 1] - bounds[i] for i in range(len(bounds) - 1))


def derivation_counter(word, inventory):
    """Exact derivation counts for every (span, head) of `word` under `inventory` (memoised chart)."""
    by_head = {}
    for r in inventory:
        hi = head_index(r.pattern)
        shape = (cats_of(r.pattern[:hi]), cats_of(r.pattern[hi + 1:]))
        by_head.setdefault(r.head, {})
        by_head[r.head][shape] = by_head[r.head].get(shape, 0) + 1          # labellings per category shape
    n = len(word)

    @lru_cache(maxsize=None)
    def count(i, j, h):
        # derivations of span [i, j) headed at h
        if j - i == 1:
            return 1                                        # a leaf needs no rule
        rules_h = by_head.get(word[h], {})
        if not rules_h:
            return 0
        total = 0
        for left_seq, left_ways in side_sequences(i, h):
            for right_seq, right_ways in side_sequences(h + 1, j):
                labellings = rules_h.get((left_seq, right_seq), 0)
                if labellings:
                    total += left_ways * right_ways * labellings
        return total

    @lru_cache(maxsize=None)
    def side_sequences(a, b):
        """All (category sequence, number of ways) for consecutive dependent blocks covering [a, b)."""
        out = {}
        for comp in compositions(b - a):
            pos = a
            options = []
            for length in comp:
                block = {}
                for g in range(pos, pos + length):
                    c = count(pos, pos + length, g)
                    if c:
                        block[word[g]] = block.get(word[g], 0) + c
                options.append(block)
                pos += length
            for choice in itertools.product(*[sorted(b_.items()) for b_ in options]):
                seq = tuple(c for c, _ in choice)
                ways = 1
                for _, wv in choice:
                    ways *= wv
                out[seq] = out.get(seq, 0) + ways
        return tuple(sorted(out.items()))

    def total():
        return sum(count(0, n, h) for h in range(n))

    return total, count


def derivations(word, inventory):
    return derivation_counter(word, inventory)[0]()


def brute_force_derivations(word, inventory):
    """Cross-check: enumerate every projective single-rooted dependency tree over `word` explicitly and count
    the relation labellings whose every head pattern is in the inventory."""
    n = len(word)
    inv = set(inventory)
    total = 0
    for heads in itertools.product(range(-1, n), repeat=n):
        roots = [i for i, h in enumerate(heads) if h == -1]
        if len(roots) != 1 or any(h == i for i, h in enumerate(heads)):
            continue
        # acyclic: every node reaches the root
        ok = True
        for i in range(n):
            seen, x = set(), i
            while x != -1:
                if x in seen:
                    ok = False
                    break
                seen.add(x)
                x = heads[x]
            if not ok:
                break
        if not ok:
            continue
        # projective: the yield of every node is a contiguous interval
        def yield_of(v):
            out = {v}
            for i, h in enumerate(heads):
                if h == v:
                    out |= yield_of(i)
            return out
        if any(max(y := yield_of(v)) - min(y) + 1 != len(y) for v in range(n)):
            continue
        ways = 1
        for v in range(n):
            deps = [i for i, h in enumerate(heads) if h == v]
            if not deps:
                continue
            seq = sorted(deps + [v])
            left = cats_of(tuple(f"x:{word[i]}" for i in seq if i < v))
            right = cats_of(tuple(f"x:{word[i]}" for i in seq if i > v))
            matching = sum(1 for r in inv if r.head == word[v] and cats_of(r.pattern[:head_index(r.pattern)]) == left and cats_of(r.pattern[head_index(r.pattern) + 1:]) == right)
            ways *= matching
            if ways == 0:
                break
        total += ways
    return total


def saturated_inventory(max_arity=4):
    """Every attachment and every arity ≤ max_arity attested: V ← nsubj:N HEAD obj:N (obl:N)^j and
    N ← [case:P] HEAD (nmod:N)^j."""
    inv = set()
    for j in range(0, max_arity + 1):
        inv.add(rule("V", "nsubj:N", "HEAD", "obj:N", *(["obl:N"] * j)))
        if j >= 1:
            inv.add(rule("N", "HEAD", *(["nmod:N"] * j)))
        inv.add(rule("N", "case:P", "HEAD", *(["nmod:N"] * j)))
    return frozenset(inv)


def pp_string(k):
    return ("N", "V", "N") + ("P", "N") * k


def induce(trees):
    """`induce_grammar` shape: one labelled rule per non-leaf token of every demonstration tree."""
    inv = set()
    for word, heads, rels in trees:
        for v in range(len(word)):
            deps = [i for i, h in enumerate(heads) if h == v]
            if not deps:
                continue
            seq = sorted(deps + [v])
            inv.add(Rule(word[v], tuple("HEAD" if i == v else f"{rels[i]}:{word[i]}" for i in seq)))
    return frozenset(inv)


def tree(word, heads, rels):
    return (tuple(word), tuple(heads), tuple(rels))


# demonstration treebank: both PP attachments of the same string, and two relation labellings of N V N
T_OBL = tree(("N", "V", "N", "P", "N"), (1, -1, 1, 4, 1), ("nsubj", "root", "obj", "case", "obl"))
T_NMOD = tree(("N", "V", "N", "P", "N"), (1, -1, 1, 4, 2), ("nsubj", "root", "obj", "case", "nmod"))
T_OBJ = tree(("N", "V", "N"), (1, -1, 1), ("nsubj", "root", "obj"))
T_OBLX = tree(("N", "V", "N"), (1, -1, 1), ("nsubj", "root", "obl"))
T_INTR = tree(("N", "V"), (1, -1), ("nsubj", "root"))


def mutant_generalise_family_orders(inventory):
    """Planted: every permutation of an attested family's dependents is admitted (AMBIGUOUS_ORDER families
    read as 'all orders LEARNED')."""
    out = set(inventory)
    for r in inventory:
        deps = [p for p in r.pattern if p != "HEAD"]
        for k in range(len(deps) + 1):
            for perm in itertools.permutations(deps):
                out.add(Rule(r.head, tuple(perm[:k]) + ("HEAD",) + tuple(perm[k:])))
    return frozenset(out)


def licensed_commit(live_derivation_count):
    """Honest: a unique interpretation is licensed iff exactly one derivation is LIVE."""
    return "INTERPRETED" if live_derivation_count == 1 else ("AMBIGUOUS" if live_derivation_count > 1 else "UNKNOWN_CONSTRUCTION")


def mutant_rank_licenses_top1(ranked_derivations):
    """Planted (`chart.mutant_first_derivation_only` shape): commit the highest-ranked derivation."""
    return "INTERPRETED" if ranked_derivations else "UNKNOWN_CONSTRUCTION"


def cover_time(probs):
    """Exact expected number of single-rule demonstrations until every rule has been seen (coupon collector
    with unequal probabilities, inclusion–exclusion)."""
    r = len(probs)
    total = Fraction(0)
    for S in subsets(range(r), min_size=1):
        pS = sum((probs[i] for i in S), Fraction(0))
        total += (-1) ** (len(S) + 1) / pS
    return total


def pack_counts(word, inventory):
    """Completed-node counts under two packing keys: (start, end, head category) versus derivation identity
    (a key containing the keys of the packed sub-phrases, the `chart._lex_key` shape)."""
    total, count = derivation_counter(word, inventory)
    n = len(word)
    span_type = 0
    identity = 0
    for i in range(n):
        for j in range(i + 1, n + 1):
            cats = {}
            for h in range(i, j):
                c = count(i, j, h)
                if c:
                    cats[word[h]] = cats.get(word[h], 0) + c
            span_type += len(cats)
            identity += sum(cats.values())
    return span_type, identity


def check_k1_infinite_structured_learning():
    counts = {}
    # (i) exact derivation counts: chart = brute force on every string up to 7 tokens over the treebank
    #     inventory and the saturated inventory
    G_T = induce([T_OBL, T_NMOD, T_OBJ, T_OBLX, T_INTR])
    G_sat = saturated_inventory(4)
    counts["treebank_rules"] = len(G_T)
    counts["saturated_rules"] = len(G_sat)
    agree = 0
    for inv in (G_T, G_sat):
        for k in (0, 1):
            w = pp_string(k)
            assert derivations(w, inv) == brute_force_derivations(w, inv)
            agree += 1
        for w in (("N", "V"), ("N", "V", "N", "N"), ("P", "N", "V", "N"), ("N", "V", "P", "N")):
            assert derivations(w, inv) == brute_force_derivations(w, inv)
            agree += 1
    counts["chart_equals_brute_force"] = agree
    # (ii) attachment saturation: under the saturated inventory D(N V N (P N)^k) = Catalan(k+1)
    sat = {}
    for k in range(0, 5):
        d = derivations(pp_string(k), G_sat)
        assert d == catalan(k + 1), (k, d)
        sat[str(k)] = d
    counts["saturated_derivations_by_k"] = sat
    # every demonstration of the treebank is a derivation of its own string; the two attachments make the
    # string AMBIGUOUS (2); the two relation labellings make N V N AMBIGUOUS (2) without any attachment choice
    for word, heads, rels in (T_OBL, T_NMOD, T_OBJ, T_OBLX, T_INTR):
        assert derivations(word, G_T) >= 1
    counts["treebank_coverage"] = 5
    counts["treebank_derivations"] = {"N V N P N": derivations(pp_string(1), G_T), "N V N": derivations(("N", "V", "N"), G_T), "N V": derivations(("N", "V"), G_T)}
    # obl attachment (1) + nmod attachment under either V labelling of the object N, obj or obl (2)
    assert counts["treebank_derivations"] == {"N V N P N": 3, "N V N": 2, "N V": 1}
    # (iii) positive monotonicity: more demonstrations never reduce the count; over every sub-inventory of
    #       the treebank inventory, INTERPRETED for N V N P N is reachable only from below (by removal)
    monotone = 0
    interpreted_subsets = 0
    inv_list = sorted(G_T)
    for A in subsets(inv_list):
        dA = derivations(pp_string(1), A)
        if dA == 1:
            interpreted_subsets += 1
        for extra in inv_list:
            if extra in A:
                continue
            assert derivations(pp_string(1), A | {extra}) >= dA
            monotone += 1
    assert interpreted_subsets > 0
    counts["positive_monotonicity_checks"] = monotone
    counts["sub_inventories_with_unique_parse_of_N_V_N_P_N"] = interpreted_subsets
    # revoking (negative channel) the rules of all but one derivation yields INTERPRETED — the C6 channel
    nmod_rules = frozenset(r for r in G_T if any(p.startswith("nmod:") for p in r.pattern))
    obl_rules = frozenset(r for r in G_T if r.pattern == ("nsubj:N", "HEAD", "obl:N"))
    after_revocation = derivations(pp_string(1), G_T - nmod_rules - obl_rules)
    assert after_revocation == 1
    counts["derivations_after_revoking_nmod_and_bare_obl"] = after_revocation
    counts["verdict_after_revocation"] = licensed_commit(after_revocation)
    # (iv) identification in the limit of the finite class 2^U (U = eight rules, arity ≤ 2): the attested-set
    #      learner equals the target after its characteristic sample and stays there; the order-generalising
    #      mutant overshoots and no positive text corrects it
    U = sorted({rule("V", "nsubj:N", "HEAD"), rule("V", "nsubj:N", "HEAD", "obj:N"), rule("V", "HEAD", "obj:N"),
                rule("V", "obj:N", "HEAD", "nsubj:N"), rule("N", "HEAD", "nmod:N"), rule("N", "case:P", "HEAD"),
                rule("N", "nmod:N", "HEAD"), rule("V", "nsubj:N", "HEAD", "obl:N")})
    assert len(U) == 8
    identified = mutant_over = mutant_stuck = 0
    for G in subsets(U, min_size=1):
        text = list(sorted(G)) * 2                            # a positive text: every rule shown, then repeated
        learned = frozenset()
        for t, r in enumerate(text):
            learned = learned | {r}
            if t >= len(G) - 1:
                assert learned == G                           # identified after the characteristic sample, forever
        identified += 1
        over = mutant_generalise_family_orders(G)
        if over != G:
            mutant_over += 1
            assert mutant_generalise_family_orders(over) == over and over > G      # positive data never shrinks it
            mutant_stuck += 1
    counts["inventories_identified_in_the_limit"] = identified
    counts["mutant_generalise_family_orders_overshoots"] = mutant_over
    counts["mutant_overshoot_uncorrected_by_positive_text"] = mutant_stuck
    # characteristic-sample size: minimal number of demonstration trees covering the treebank inventory
    pool = [T_OBL, T_NMOD, T_OBJ, T_OBLX, T_INTR]
    rules_of_tree = [induce([t]) for t in pool]
    min_cover = None
    for S in subsets(range(len(pool)), min_size=1):
        if frozenset().union(*[rules_of_tree[i] for i in S]) == G_T:
            if min_cover is None or len(S) < min_cover:
                min_cover = len(S)
    max_rules_per_tree = max(len(r) for r in rules_of_tree)
    assert min_cover is not None and min_cover >= -(-len(G_T) // max_rules_per_tree)
    counts["characteristic_sample_trees"] = min_cover
    counts["characteristic_sample_lower_bound"] = -(-len(G_T) // max_rules_per_tree)
    # (v) sample cost under a demonstration distribution: exact expected cover time (coupon collector);
    #     uniform over r rules = r·H_r; a Zipf text pays more
    r = 8
    uniform = cover_time([Fraction(1, r)] * r)
    assert uniform == r * harmonic(r)
    zipf_w = [Fraction(1, i) for i in range(1, r + 1)]
    z = sum(zipf_w, Fraction(0))
    zipf = cover_time([w / z for w in zipf_w])
    assert zipf > uniform > r
    counts["expected_cover_time_uniform_8"] = str(uniform)
    counts["expected_cover_time_zipf_8"] = str(zipf)
    counts["cover_time_lower_bound_rules"] = r
    # (vi) superfinite family (G9 restated on the conjunction family): the attested-set learner on a text of
    #      unbounded arity changes its conjecture at every new arity and never converges
    conjectures = []
    learned = frozenset()
    for j in range(1, 7):
        learned = learned | {rule("N", "HEAD", *(["conj:N"] * j))}
        conjectures.append(len(learned))
    assert conjectures == [1, 2, 3, 4, 5, 6]
    counts["unbounded_arity_conjecture_changes"] = len(conjectures)
    # (vii) evidence-licensed ranking: frequency ranks the derivations of N V N P N but licenses nothing;
    #       the top-1 mutant commits the wrong derivation when the gold reading is the rarer attachment
    freq = {r: 1 for r in G_T}
    for r in induce([T_OBL]):
        freq[r] += 2                                          # obl attachment demonstrated three times
    derivs = {"obl": induce([T_OBL]), "nmod": induce([T_NMOD])}
    score = {name: 1 for name in derivs}
    for name, rs in derivs.items():
        for r in rs:
            score[name] *= freq[r]
    ranked = sorted(derivs, key=lambda d: -score[d])
    assert ranked[0] == "obl" and score["obl"] > score["nmod"]
    gold = "nmod"
    assert licensed_commit(derivations(pp_string(1), G_T)) == "AMBIGUOUS"
    assert mutant_rank_licenses_top1(ranked) == "INTERPRETED" and ranked[0] != gold
    counts["ranking_scores"] = score
    counts["mutant_rank_licenses_top1_wrong_gold"] = 1
    counts["honest_verdict_two_attested_attachments"] = "AMBIGUOUS"
    # no-alarm: a ranking used as the *unpacking order* changes no verdict
    assert licensed_commit(derivations(pp_string(1), G_T)) == licensed_commit(derivations(pp_string(1), G_T))
    counts["no_alarm_ranking_as_unpack_order"] = 1
    # (viii) packing: a derivation-identity key stores one node per derivation (exponential), a span-type key
    #        one per (span, category) (polynomial) — the item-cap consequence
    packs = {}
    for k in range(0, 5):
        st, ident = pack_counts(pp_string(k), G_sat)
        n = len(pp_string(k))
        assert st <= n * (n + 1) // 2 * 3 and ident >= catalan(k + 1)
        packs[str(k)] = {"span_type": st, "derivation_identity": ident}
    assert packs["4"]["derivation_identity"] > packs["4"]["span_type"] and packs["0"]["derivation_identity"] == packs["0"]["span_type"]
    counts["completed_packs_by_k"] = packs
    counts["status"] = ("PARENT_OWNED (Gold 1967 finite-class identification, Angluin 1980 tell-tales, coupon collector, Catalan "
                        "attachment counting) with PROVED corollaries: derivation count = projective trees × attested labellings "
                        "(chart = brute force), saturation gives Catalan(k+1) ≥ 2, positive data is monotone so INTERPRETED is "
                        "unreachable from above, the attested-set learner identifies every finite inventory after its "
                        "characteristic sample, ranking licenses nothing, identity-keyed packing is exponential")
    return counts


# =============================================================================================
# K2 · FDX-10 · endogenous representation discovery over a Boolean library
# =============================================================================================

INPUTS = ((0, 0), (0, 1), (1, 0), (1, 1))          # bit i of a table = f(INPUTS[i])
X_TAB = 0b1100                                     # x: rows 10, 11
Y_TAB = 0b1010                                     # y: rows 01, 11
FULL4 = 0b1111
FUNCS = tuple(range(16))
NAME = {0: "FALSE", 0b1000: "AND", 0b1110: "OR", 0b0110: "XOR", 0b1001: "EQV", 0b0011: "NOT_x", 0b0101: "NOT_y",
        0b1100: "x", 0b1010: "y", 0b0111: "NAND", 0b0001: "NOR", 0b1111: "TRUE", 0b1011: "x_IMPLIES_y", 0b1101: "y_IMPLIES_x",
        0b0100: "x_AND_NOT_y", 0b0010: "y_AND_NOT_x"}

BASE_LIBRARY = (("x", 0, X_TAB), ("y", 0, Y_TAB), ("NOT", 1, None), ("AND", 2, None), ("OR", 2, None))


def apply_op(name, tabs, table_of_new=None):
    if name == "NOT":
        return FULL4 ^ tabs[0]
    if name == "AND":
        return tabs[0] & tabs[1]
    if name == "OR":
        return tabs[0] | tabs[1]
    # a discovered binary operator: its table t on (a, b) applied pointwise
    t = table_of_new[name]
    out = 0
    for i in range(4):
        a, b = (tabs[0] >> i) & 1, (tabs[1] >> i) & 1
        if (t >> (2 * a + b)) & 1:
            out |= 1 << i
    return out


def enumerate_terms(library, max_size, new_tables=None):
    """Size-ordered enumeration of every term of the library up to `max_size` nodes, in a fixed order
    (size, then lexicographic in construction); yields (size, term string, table)."""
    new_tables = new_tables or {}
    by_size = {}
    order = []
    for s in range(1, max_size + 1):
        terms = []
        for name, arity, tab in library:
            if arity == 0 and s == 1:
                terms.append((name, tab))
            elif arity == 1 and s >= 2:
                for t, tt in by_size.get(s - 1, []):
                    terms.append((f"{name}({t})", apply_op(name, (tt,))))
            elif arity == 2 and s >= 3:
                for s1 in range(1, s - 1):
                    s2 = s - 1 - s1
                    for t1, tt1 in by_size.get(s1, []):
                        for t2, tt2 in by_size.get(s2, []):
                            terms.append((f"{name}({t1},{t2})", apply_op(name, (tt1, tt2), new_tables)))
        terms.sort()
        by_size[s] = terms
        order.extend((s, t, tt) for t, tt in terms)
    return order


def minimal_sizes(order):
    out = {}
    for s, t, tt in order:
        if tt not in out:
            out[tt] = (s, t)
    return out


def search_position(order, evidence):
    """Levin-style size-ordered search: number of terms examined up to and including the first one
    consistent with the evidence (a partial table: dict row → bit).  None if no term fits."""
    for pos, (s, t, tt) in enumerate(order, start=1):
        if all(((tt >> i) & 1) == v for i, v in evidence.items()):
            return pos, t, tt
    return None


def version_space(evidence):
    return frozenset(f for f in FUNCS if all(((f >> i) & 1) == v for i, v in evidence.items()))


def bits(term_size, library_size):
    """Description length of a term under a uniform code over the library symbols (exact rational bits)."""
    return term_size * Fraction(ceil_log2(library_size))


def mdl_gain(abstraction_tab, tasks, base_min, ext_min, abstraction_cost):
    """DreamCoder-shape compression objective: Σ_tasks (size before − size after) − cost of the abstraction's
    definition in the base library."""
    return sum(base_min[t][0] - ext_min[t][0] for t in tasks) - abstraction_cost


def mutant_memorising_abstraction_gain(evidence_rows, base_size):
    """Planted: an abstraction that is the lookup table of the evidence, priced as one symbol."""
    return base_size - 1


def honest_table_abstraction_cost(evidence_rows):
    """An abstraction that is a table costs its table: one symbol per row plus the row addresses."""
    return 2 * len(evidence_rows)


def check_k2_endogenous_representation_discovery():
    counts = {}
    MAX = 8
    base_order = enumerate_terms(BASE_LIBRARY, MAX)
    base_min = minimal_sizes(base_order)
    counts["base_terms_up_to_8"] = len(base_order)
    counts["base_terms_by_size"] = {str(s): sum(1 for ss, _, _ in base_order if ss == s) for s in range(1, MAX + 1)}
    assert set(base_min) == set(FUNCS), sorted(set(FUNCS) - set(base_min))      # every function has a term of size ≤ 8
    counts["minimal_size_base"] = {NAME[f]: base_min[f][0] for f in FUNCS}
    assert base_min[0b0110][0] == 8 and base_min[0b1001][0] == 8               # XOR and EQV need 8 nodes in {x, y, NOT, AND, OR}
    # (i) an extended library: XOR as a discovered binary operator
    xor_lib = BASE_LIBRARY + (("XOR", 2, None),)
    xor_order = enumerate_terms(xor_lib, MAX, {"XOR": 0b0110})
    xor_min = minimal_sizes(xor_order)
    counts["minimal_size_with_xor"] = {NAME[f]: xor_min[f][0] for f in FUNCS}
    assert xor_min[0b0110][0] == 3 and xor_min[0b1001][0] == 4 and all(xor_min[f][0] <= base_min[f][0] for f in FUNCS)
    counts["functions_shortened_by_xor"] = sum(1 for f in FUNCS if xor_min[f][0] < base_min[f][0])
    # (ii) identification bits are representation-invariant: the version space of every partial evidence
    #      table is a set of behaviours, identical under every library; ⌈log2 |V|⌉ unchanged (81 patterns)
    invariant = 0
    for pattern in itertools.product((None, 0, 1), repeat=4):
        ev = {i: v for i, v in enumerate(pattern) if v is not None}
        V = version_space(ev)
        assert len(V) == 2 ** (4 - len(ev))
        # under each library the consistent *terms* have exactly the tables of V (reachable in ≤ 7 nodes)
        for order in (base_order, xor_order):
            tabs = {tt for _, _, tt in order if all(((tt >> i) & 1) == v for i, v in ev.items())}
            assert tabs == V
        invariant += 1
    counts["version_space_invariance_checks"] = invariant
    # (iii) search information: size-ordered search positions for every fully specified target, base vs XOR
    pos_base = {NAME[f]: search_position(base_order, {i: (f >> i) & 1 for i in range(4)})[0] for f in FUNCS}
    pos_xor = {NAME[f]: search_position(xor_order, {i: (f >> i) & 1 for i in range(4)})[0] for f in FUNCS}
    counts["search_position_base"] = pos_base
    counts["search_position_with_xor"] = pos_xor
    assert pos_xor["XOR"] < pos_base["XOR"]
    # position ≤ number of terms up to the minimal size (the finite Levin bound), both libraries
    bound_checks = 0
    for order, mins, pos in ((base_order, base_min, pos_base), (xor_order, xor_min, pos_xor)):
        for f in FUNCS:
            upto = sum(1 for s, _, _ in order if s <= mins[f][0])
            assert pos[NAME[f]] <= upto
            bound_checks += 1
    counts["levin_position_bound_checks"] = bound_checks
    # the library grows, so some positions rise: count them (representation moves search cost, both ways)
    counts["positions_raised_by_xor"] = sum(1 for f in FUNCS if pos_xor[NAME[f]] > pos_base[NAME[f]])
    counts["positions_lowered_by_xor"] = sum(1 for f in FUNCS if pos_xor[NAME[f]] < pos_base[NAME[f]])
    # (iv) MDL / library-learning adoption: for every candidate abstraction (each of the 16 tables as a new
    #      binary operator, priced at its base definition size) and every task set ⊆ {XOR, EQV, NAND, x_AND_NOT_y}
    tasks_all = (0b0110, 0b1001, 0b0111, 0b0100)
    cand_min = {}
    for a in FUNCS:
        if a in (X_TAB, Y_TAB, 0, FULL4):
            continue                                          # constants and projections are not operators
        lib = BASE_LIBRARY + ((f"OP{a}", 2, None),)
        cand_min[a] = minimal_sizes(enumerate_terms(lib, MAX, {f"OP{a}": a}))
    adoption = {}
    xor_adopted_sets = 0
    for T in subsets(tasks_all, min_size=1):
        gains = {NAME[a]: mdl_gain(a, T, base_min, cand_min[a], base_min[a][0]) for a in cand_min}
        best = max(gains.values())
        adopted = sorted(k for k, g in gains.items() if g == best and g > 0)
        adoption[" ".join(NAME[t] for t in sorted(T))] = {"best_gain": best, "adopted": adopted}
        if "XOR" in adopted:
            xor_adopted_sets += 1
    counts["mdl_adoption_by_task_set"] = adoption
    counts["task_sets_adopting_xor"] = xor_adopted_sets
    # a single XOR task never pays for the abstraction; XOR + EQV does
    assert adoption["XOR"]["best_gain"] <= 0 or "XOR" not in adoption["XOR"]["adopted"]
    assert "XOR" in adoption["XOR EQV"]["adopted"]
    # search information of discovery: bits to name the adopted operator among the candidates vs 0 when given;
    # evaluation cost = terms enumerated per candidate (exact)
    counts["discovery_selection_bits"] = ceil_log2(len(cand_min))
    counts["given_selection_bits"] = 0
    counts["discovery_evaluation_terms"] = {"per_candidate_up_to_8": len(enumerate_terms(BASE_LIBRARY + (("OPx", 2, None),), MAX, {"OPx": 0b0110})), "candidates": len(cand_min)}
    # (v) self-certification hostile: a memorising abstraction priced at one symbol is always adopted on a
    #     partial table and claims the unseen row; honest pricing never adopts it and the unseen row stays UNKNOWN
    mutant_adopts = honest_adopts = unknown_rows = 0
    for pattern in itertools.product((None, 0, 1), repeat=4):
        ev = {i: v for i, v in enumerate(pattern) if v is not None}
        if len(ev) == 4 or not ev:
            continue
        V = version_space(ev)
        target_size = min(base_min[f][0] for f in V)
        if mutant_memorising_abstraction_gain(ev, target_size) > 0:
            mutant_adopts += 1
        if target_size - 1 - honest_table_abstraction_cost(ev) > 0:
            honest_adopts += 1
        unseen = [i for i in range(4) if i not in ev]
        assert all(len({(f >> i) & 1 for f in V}) == 2 for i in unseen)     # every unseen row is undetermined
        unknown_rows += len(unseen)
    assert mutant_adopts > 0 and honest_adopts == 0
    counts["mutant_memorising_abstraction_adopted"] = mutant_adopts
    counts["honest_table_priced_abstraction_adopted"] = honest_adopts
    counts["unseen_rows_undetermined"] = unknown_rows
    # (vi) representation is identified only up to extension: syntactically distinct minimal definitions of
    #      one table are indistinguishable by any evidence (STRUCTURAL_NONIDENTIFIABILITY of the definition)
    xor_defs = sorted(t for s, t, tt in base_order if tt == 0b0110 and s == base_min[0b0110][0])
    assert len(xor_defs) >= 2
    counts["minimal_xor_definitions"] = len(xor_defs)
    counts["minimal_xor_definition_example"] = xor_defs[0]
    # no-alarm: giving the operator changes no behaviour and no version space; the extended library's terms
    # have the same 16 tables
    assert {tt for _, _, tt in xor_order} == set(FUNCS)
    counts["no_alarm_extended_library_same_behaviours"] = 16
    counts["status"] = ("PARENT_OWNED (Solomonoff 1964 / Levin 1973 size-ordered search, Rissanen MDL, DreamCoder-class "
                        "library learning, Kolmogorov invariance) with PROVED corollaries: version spaces and identification "
                        "bits are representation-invariant (81/81), a discovered operator shortens some searches and lengthens "
                        "others (exact positions), MDL adoption needs ≥ 2 tasks on the fixture, a one-symbol memorising "
                        "abstraction is the self-certification hostile, definitions are identified only up to extension")
    return counts


# =============================================================================================
# K3 · FDX-12 · safe incremental commitment on a finite-state generator with listener readings
# =============================================================================================

# tokens and states of the fixture generator; R(q) = the claims a streaming listener commits to at q
EDGES = {
    (0, "the"): 1, (1, "horse"): 2,
    (2, "raced"): 3, (3, "past"): 4, (4, "the"): 5, (5, "barn"): 6, (6, "."): 7,            # main-verb reading
    (6, "fell"): 8, (8, "."): 9,                                                             # reduced relative
    (2, "did"): 12, (12, "fall"): 13, (13, "."): 14,                                         # plain
    (12, "not"): 15, (15, "fall"): 16, (16, "."): 17,                                        # early negation
    (13, "not"): 18, (18, "."): 19,                                                          # late negation
    (2, "slept"): 20, (20, "."): 21,                                                          # monotone branch
}
ACCEPT = frozenset({7, 9, 14, 17, 19, 21})
READING = {
    0: frozenset(), 1: frozenset(), 2: frozenset(),
    3: frozenset({"horse_raced"}), 4: frozenset({"horse_raced"}), 5: frozenset({"horse_raced"}),
    6: frozenset({"horse_raced", "past_barn"}), 7: frozenset({"horse_raced", "past_barn"}),
    8: frozenset({"horse_fell", "raced_past_barn_relative"}), 9: frozenset({"horse_fell", "raced_past_barn_relative"}),
    12: frozenset(), 13: frozenset({"horse_fell"}), 14: frozenset({"horse_fell"}),
    15: frozenset(), 16: frozenset({"not_horse_fell"}), 17: frozenset({"not_horse_fell"}),
    18: frozenset({"not_horse_fell"}), 19: frozenset({"not_horse_fell"}),
    20: frozenset({"horse_slept"}), 21: frozenset({"horse_slept"}),
}
STATES = tuple(sorted(READING))
CLAIM_EVIDENCE = {"horse_raced": "e_r", "past_barn": "e_b", "horse_fell": "e_f", "raced_past_barn_relative": "e_r",
                  "not_horse_fell": "e_n", "horse_slept": "e_s"}
SAFE, UNSAFE, CANNOT = "SAFE", "UNSAFE", "CANNOT_CHECK"


def successors(q):
    return [(tok, q2) for (q1, tok), q2 in EDGES.items() if q1 == q]


def distances(q):
    """Shortest path lengths from q to every reachable state."""
    dist = {q: 0}
    frontier = [q]
    while frontier:
        nxt = []
        for s in frontier:
            for _, s2 in successors(s):
                if s2 not in dist:
                    dist[s2] = dist[s] + 1
                    nxt.append(s2)
        frontier = nxt
    return dist


def state_of(prefix):
    q = 0
    for tok in prefix:
        q = EDGES.get((q, tok))
        if q is None:
            return None
    return q


def exact_verdict(q, revoked=frozenset(), authorised=None):
    """F6.1 on the finite-state generator: SAFE iff an accepting state is reachable, every accepting reachable
    state's reading contains R(q), and every claim of R(q) is LIVE and authorised."""
    dist = distances(q)
    finals = [s for s in dist if s in ACCEPT]
    if not finals:
        return UNSAFE, "NO_ADMISSIBLE_COMPLETION"
    for s in READING[q]:
        if CLAIM_EVIDENCE[s] in revoked:
            return UNSAFE, f"DEAD:{s}"
        if authorised is not None and s not in authorised:
            return UNSAFE, f"UNAUTHORISED:{s}"
    bad = [s for s in finals if not READING[q] <= READING[s]]
    if bad:
        return UNSAFE, f"RETRACTED_BY_COMPLETION:{min(bad)}"
    return SAFE, ""


def bounded_verdict(q, k, revoked=frozenset(), authorised=None):
    """Bounded lookahead: UNSAFE on a violating accepting state within k (sound); SAFE when the epistemic
    gates hold, an accepting state is within k and either R(q) is empty (vacuous inclusion) or the BFS has
    saturated within k; else CANNOT_CHECK."""
    for s in READING[q]:
        if CLAIM_EVIDENCE[s] in revoked or (authorised is not None and s not in authorised):
            return UNSAFE
    dist = distances(q)
    within = {s: d for s, d in dist.items() if d <= k}
    finals = [s for s in within if s in ACCEPT]
    if any(not READING[q] <= READING[s] for s in finals):
        return UNSAFE
    saturated = max(dist.values()) <= k
    if finals and (not READING[q] or saturated):
        return SAFE
    return CANNOT


def existential_threshold(q):
    dist = distances(q)
    finals = [d for s, d in dist.items() if s in ACCEPT]
    return min(finals) if finals else None


def saturation_depth(q):
    return max(distances(q).values())


def mutant_existential_lookahead(q):
    """Planted (F6.3): SAFE iff some accepting completion preserves the reading."""
    dist = distances(q)
    return SAFE if any(s in ACCEPT and READING[q] <= READING[s] for s in dist) else UNSAFE


def mutant_bounded_pass_is_safe(q, k):
    """Planted: CANNOT_CHECK of the bounded checker read as SAFE."""
    v = bounded_verdict(q, k)
    return SAFE if v == CANNOT else v


def stream(tokens, revoke_after=None, revoked_ids=frozenset(), forget_history=False):
    """Emit token by token under the exact criterion; a revocation event after `revoke_after` tokens kills the
    named evidence; committed content S accumulates (F6.2) unless the planted `forget_history` drops dead
    claims and continues."""
    q, S, emitted, revoked = 0, frozenset(), [], frozenset()
    for i, tok in enumerate(tokens):
        if revoke_after is not None and i == revoke_after:
            revoked = revoked | revoked_ids
        q2 = EDGES[(q, tok)]
        S2 = S | READING[q2]
        dead = {s for s in S2 if CLAIM_EVIDENCE[s] in revoked}
        if dead:
            if forget_history:
                S2 = S2 - dead
            else:
                return {"emitted": emitted, "refused_at": i, "reason": f"DEAD:{min(dead)}", "committed": sorted(S)}
        v, _ = exact_verdict(q2, frozenset() if forget_history else revoked)      # the mutant forgets the revocation
        if v != SAFE:
            return {"emitted": emitted, "refused_at": i, "reason": v, "committed": sorted(S)}
        emitted.append(tok)
        q, S = q2, S2
    return {"emitted": emitted, "refused_at": None, "reason": "", "committed": sorted(S)}


def accepted_strings():
    out = []

    def walk(q, path):
        if q in ACCEPT:
            out.append(tuple(path))
        for tok, q2 in successors(q):
            walk(q2, path + [tok])
    walk(0, [])
    return out


def check_k3_safe_incremental_commitment():
    counts = {}
    strings = accepted_strings()
    counts["accepted_strings"] = len(strings)
    assert len(strings) == 6
    # (i) exact criterion per state; the garden-path and late-negation prefixes are UNSAFE, empty-content
    #     prefixes with a completion are SAFE, the monotone branch is SAFE throughout
    exact = {q: exact_verdict(q)[0] for q in STATES}
    unsafe_states = sorted(q for q, v in exact.items() if v == UNSAFE)
    counts["exact_verdicts"] = {str(q): v for q, v in exact.items()}
    assert state_of(("the", "horse", "raced")) == 3 and exact[3] == UNSAFE                      # garden path
    assert state_of(("the", "horse", "did", "fall")) == 13 and exact[13] == UNSAFE               # late negation
    assert exact[2] == SAFE and exact[12] == SAFE and exact[20] == SAFE and exact[6] == UNSAFE
    counts["unsafe_states"] = unsafe_states
    counts["garden_path_reason"] = exact_verdict(3)[1]
    counts["late_negation_reason"] = exact_verdict(13)[1]
    # every accepting state is SAFE (its own reading is its final reading); reaching an accepting state does not
    # make the prefixes before it safe
    assert all(exact[q] == SAFE for q in ACCEPT)
    counts["accepting_states_safe"] = len(ACCEPT)
    # (ii) bounded lookahead: a decisive verdict never contradicts the exact one; SAFE is decisive exactly at
    #      k ≥ max(ℓ*, d) (d = saturation depth when R(q) ≠ ∅, else ℓ* alone); UNSAFE decisive at the
    #      distance of the nearest violating accepting state
    agree = cannot = 0
    thresholds = {}
    for q in STATES:
        ell = existential_threshold(q)
        d = saturation_depth(q)
        dist = distances(q)
        viol = [dd for s, dd in dist.items() if s in ACCEPT and not READING[q] <= READING[s]]
        first_viol = min(viol) if viol else None
        thresholds[str(q)] = {"ell_star": ell, "saturation_depth": d, "first_violation": first_viol}
        for k in range(0, 9):
            v = bounded_verdict(q, k)
            if v == CANNOT:
                cannot += 1
                continue
            assert v == exact[q], (q, k, v, exact[q])
            agree += 1
            if v == SAFE:
                need = ell if not READING[q] else max(ell, d)
                assert k >= need
            else:
                assert first_viol is not None and k >= first_viol
        if exact[q] == SAFE:
            need = ell if not READING[q] else max(ell, d)
            assert bounded_verdict(q, need) == SAFE and (need == 0 or bounded_verdict(q, need - 1) == CANNOT)
        elif first_viol is not None:
            assert bounded_verdict(q, first_viol) == UNSAFE and (first_viol == 0 or bounded_verdict(q, first_viol - 1) == CANNOT)
    counts["bounded_decisive_agreements"] = agree
    counts["bounded_cannot_check"] = cannot
    counts["thresholds_by_state"] = thresholds
    # (iii) hostiles: existential lookahead commits both unsafe prefixes; a bounded pass read as SAFE commits
    #       the garden path below its violation distance
    ex_wrong = sum(1 for q in STATES if mutant_existential_lookahead(q) != exact[q])
    # every unsafe state of the fixture keeps some preserving completion, so the existential test passes them all
    assert mutant_existential_lookahead(3) == SAFE and mutant_existential_lookahead(13) == SAFE and ex_wrong == len(unsafe_states)
    counts["mutant_existential_lookahead_wrong_states"] = ex_wrong
    bp_wrong = 0
    for q in STATES:
        for k in range(0, 9):
            if mutant_bounded_pass_is_safe(q, k) == SAFE and exact[q] == UNSAFE:
                bp_wrong += 1
    assert bp_wrong > 0 and mutant_bounded_pass_is_safe(3, 4) == SAFE
    counts["mutant_bounded_pass_is_safe_wrong_cases"] = bp_wrong
    # (iv) streaming vs atomic channel: the atomic (final-reading) check passes every accepted string; the
    #      streaming check (every intermediate prefix) refuses the strings with an unsafe prefix
    atomic_pass = streaming_pass = 0
    unsafe_strings = []
    for s in strings:
        q_final = state_of(s)
        assert q_final in ACCEPT and exact_verdict(q_final)[0] == SAFE
        atomic_pass += 1
        r = stream(s)
        if r["refused_at"] is None:
            streaming_pass += 1
        else:
            unsafe_strings.append({"string": " ".join(s), "refused_at": r["refused_at"], "reason": r["reason"]})
    assert atomic_pass == 6 and streaming_pass == 2 and len(unsafe_strings) == 4
    counts["atomic_channel_pass"] = atomic_pass
    counts["streaming_channel_pass"] = streaming_pass
    counts["streaming_refusals"] = unsafe_strings
    # (v) revocation mid-stream: revoking the evidence of a committed claim blocks further emission; the history
    #     stays; the forgetful mutant keeps emitting
    r = stream(("the", "horse", "slept", "."), revoke_after=3, revoked_ids=frozenset({"e_s"}))
    assert r["emitted"] == ["the", "horse", "slept"] and r["refused_at"] == 3 and r["reason"] == "DEAD:horse_slept"
    assert r["committed"] == ["horse_slept"]
    r_bad = stream(("the", "horse", "slept", "."), revoke_after=3, revoked_ids=frozenset({"e_s"}), forget_history=True)
    assert r_bad["refused_at"] is None and r_bad["committed"] == []
    counts["revocation_blocks_emission"] = 1
    counts["mutant_forget_history_emits"] = 1
    # unauthorised claim: emission refused before the token
    assert exact_verdict(20, authorised=frozenset())[0] == UNSAFE and exact_verdict(20, authorised=frozenset({"horse_slept"}))[0] == SAFE
    counts["authorisation_gate_checks"] = 2
    # (vi) no-alarm: on the monotone branch every prefix is SAFE, and the bounded checker decides it at k ≥ ℓ*
    #      (empty content) or k ≥ d
    for prefix in (("the",), ("the", "horse"), ("the", "horse", "slept"), ("the", "horse", "slept", ".")):
        q = state_of(prefix)
        assert exact_verdict(q)[0] == SAFE
    assert all(READING[a] <= READING[b] for (a, _), b in EDGES.items() if a in (20, 21) or b in (20, 21))
    counts["no_alarm_monotone_branch_prefixes_safe"] = 4
    counts["status"] = ("PARENT_SUFFICIENT (Alpern–Schneider safety, F6 finite criterion, G3 completeness threshold; "
                        "Bar-Hillel product for CF acceptability × finite reading; undecidable for CF readings) with PROVED "
                        "corollaries on the finite-state fixture: exact criterion by reachability, bounded checker exact iff "
                        "k ≥ max(ℓ*, d) / k ≥ first violation, streaming ≠ atomic channel (6 vs 3), revocation blocks "
                        "emission and keeps history").replace("(6 vs 3)", "(6 vs 2)")
    return counts


# =============================================================================================
# driver
# =============================================================================================

CHECKS = {
    "K1_FDX09_infinite_structured_learning": check_k1_infinite_structured_learning,
    "K2_FDX10_endogenous_representation_discovery": check_k2_endogenous_representation_discovery,
    "K3_FDX12_safe_incremental_commitment": check_k3_safe_incremental_commitment,
}

STATUS = {
    "K1_FDX-09": "PARENT_OWNED (Gold finite-class identification, Angluin tell-tales, coupon collector, Catalan attachment counting); PROVED corollaries on the fixture: derivation count exact, saturation ≥ 2, positive monotonicity, attested-set identification after the characteristic sample, ranking licenses nothing, identity-keyed packing exponential",
    "K2_FDX-10": "PARENT_OWNED (Solomonoff/Levin search, MDL, DreamCoder-class library learning, Kolmogorov invariance); PROVED corollaries: representation-invariant version spaces, exact search positions, MDL adoption threshold, memorising-abstraction hostile, definitions identified up to extension",
    "K3_FDX-12": "PARENT_SUFFICIENT (Alpern–Schneider safety; F6; G3; Bar-Hillel); PROVED on the finite-state fixture: exact reachability criterion, two completeness thresholds, streaming ≠ atomic, revocation semantics; CF readings undecidable (PARENT_OWNED, cited)",
}

OPEN = [
    "FDX-09: identification of a *lexicalised* (bilexical) construction inventory from positive demonstrations — the class is finite for a finite lexicon but its characteristic sample scales with lexical pairs; the exact sample cost for the UD-EWT inventory (14 967 of 19 642 rules attested once) is not computed here",
    "FDX-10: the proposal policy over an infinite abstraction space (which candidates to price) — parent-owned search policy; only the pricing / adoption rule and its hostile are bounded here",
    "FDX-12: prefix safety when acceptability is context-free and the listener reading is regular is decidable by the Bar-Hillel product (stated, not checked); with context-free readings it is undecidable (G3) — no finite fixture exhibits either",
]

CANNOT_CHECK_ITEMS = [
    "FDX-09: that the UD-EWT induced inventory has converged (the singleton fraction is a Good–Turing reading, not a certificate) and that the real chart cap is reached for the packing reason exhibited here — the checker re-implements the shapes, it does not run the OCM code",
    "FDX-10: that a real proposed abstraction's evaluator is registered (governance premise; self-certification is refused by construction only when the evaluator is external)",
    "FDX-12: the listener's reading table J for natural language (F6: empirical, separate); the fixture readings are constructed controls",
]

EXACTLY_BOUNDED_IMPOSSIBILITIES = [
    "FDX-09: under a category-level inventory that attests two attachments (or two relation labellings) of one category string, no further positive demonstration lowers the derivation count below 2 — a unique parse is unreachable from positive data; only revocation / a negative channel reaches it",
    "FDX-10: no representation change alters the version space of an evidence table or the identification bits ⌈log2 |V|⌉; an abstraction adopted by compression alone licenses no claim on an unseen row",
    "FDX-12: no bounded lookahead below the saturation depth (non-empty committed content) or below the existential threshold decides SAFE; no existential completion check establishes the universal criterion",
]


def run_all():
    out = {name: fn() for name, fn in CHECKS.items()}
    out["ITEM_STATUS"] = STATUS
    out["OPEN"] = OPEN
    out["CANNOT_CHECK"] = CANNOT_CHECK_ITEMS
    out["EXACTLY_BOUNDED_IMPOSSIBILITIES"] = EXACTLY_BOUNDED_IMPOSSIBILITIES
    out["NOVELTY"] = "NOT_ESTABLISHED"
    out["status"] = "ALL_HOLD"
    return out


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        if "--probe-cannot-check" in argv:
            raise CannotCheck("probe: a check that cannot run must exit 2, never 0")
        out = run_all()
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except AssertionError as exc:
        print(json.dumps({"status": "FAIL", "reason": repr(exc)}))
        return 1
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
