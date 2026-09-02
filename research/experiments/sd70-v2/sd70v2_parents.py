#!/usr/bin/env python3
"""SD70-V2 deterministic mature parent baselines, the fixed meta lesson, the
frozen parent federation, the parent advisory block, and native known-answer
fidelity tests.

Every parent consumes ONLY a request surface (training episodes, held-out
context, candidate actions). Every parent uses the single frozen tie break:
highest score, ties resolved by candidate-list order (the generator's own
lowest-index tie break, which is public through the candidate list).

Stdlib only; fully deterministic; no numeric constant below is tuned on any
protected task.
"""
from __future__ import annotations

import math
import random
from typing import Any, Callable

# Frozen hyper-parameters (development-only; recorded in the design JSON).
PERCEPTRON_EPOCHS = 50
PERCEPTRON_MARGIN = 1.0
MAXMARGIN_ITERS = 200
MAXMARGIN_STEP = 0.1
MAXMARGIN_L2 = 0.01
DECISION_LIST_MAX_LITERALS = 2
NB_LAPLACE = 1.0
KERNEL_BANDWIDTH = 1.0  # w = 1 / (1 + d * bandwidth)

PARENT_IDS = (
    "SIMPLE_FREQUENCY_PARENT",
    "MATCHED_CASE_PARENT",
    "NAIVE_BAYES_PARENT",
    "DECISION_LIST_PARENT",
    "PERCEPTRON_PARENT",
    "MAXMARGIN_PARENT",
    "PAIRWISE_LINEAR_PARENT",
)
# Candidates for the strongest generator-faithful parent (mature linear or
# rule learners whose hypothesis class contains the generator family).
GENERATOR_FAITHFUL_CANDIDATES = (
    "PERCEPTRON_PARENT",
    "MAXMARGIN_PARENT",
    "PAIRWISE_LINEAR_PARENT",
    "DECISION_LIST_PARENT",
    "NAIVE_BAYES_PARENT",
)


# ---------------------------------------------------------------------------
# Encoding
# ---------------------------------------------------------------------------

class Encoded:
    def __init__(self, surface: dict[str, Any]):
        self.candidates: list[str] = list(surface["candidate_actions"])
        self.cand_index = {a: i for i, a in enumerate(self.candidates)}
        episodes = list(surface.get("training_episodes", []))
        vocab: set[str] = set(surface.get("query_context_features", []))
        for ep in episodes:
            vocab.update(ep["context_features"])
        self.vocab: list[str] = sorted(vocab)
        self.vindex = {f: i for i, f in enumerate(self.vocab)}
        self.query_set = set(surface.get("query_context_features", []))
        self.query = self.vector(self.query_set)
        self.episodes: list[tuple[frozenset[str], tuple[float, ...], int, bool]] = []
        for ep in episodes:
            if ep["chosen_action"] not in self.cand_index:
                continue  # out-of-candidate evidence is ignored (never occurs in the generator)
            cs = frozenset(ep["context_features"])
            self.episodes.append(
                (cs, self.vector(cs), self.cand_index[ep["chosen_action"]], ep["validated_outcome"] == "SUCCESS")
            )
        # paired success action per context (for FAILURE episodes)
        self.success_by_context: dict[frozenset[str], int] = {}
        for cs, _x, a, ok in self.episodes:
            if ok and cs not in self.success_by_context:
                self.success_by_context[cs] = a

    def vector(self, features) -> tuple[float, ...]:
        x = [0.0] * (len(self.vocab) + 1)
        for f in features:
            if f in self.vindex:
                x[self.vindex[f]] = 1.0
        x[-1] = 1.0  # bias
        return tuple(x)

    @property
    def A(self) -> int:
        return len(self.candidates)


def argmax_frozen(scores: list[float]) -> int:
    best = 0
    for i in range(1, len(scores)):
        if scores[i] > scores[best]:
            best = i
    return best


def dot(w: list[float], x: tuple[float, ...]) -> float:
    return sum(a * b for a, b in zip(w, x))


# ---------------------------------------------------------------------------
# Parents. Each returns (scores per candidate in candidate order).
# ---------------------------------------------------------------------------

def simple_frequency(enc: Encoded) -> list[float]:
    s = [0.0] * enc.A
    for _cs, _x, a, ok in enc.episodes:
        s[a] += 1.0 if ok else -1.0
    return s


def matched_case(enc: Encoded) -> list[float]:
    s = [0.0] * enc.A
    for cs, _x, a, ok in enc.episodes:
        d = len(cs.symmetric_difference(enc.query_set))
        w = 1.0 / (1.0 + KERNEL_BANDWIDTH * d)
        s[a] += w if ok else -w
    return s


def naive_bayes(enc: Encoded) -> list[float]:
    """log P_S(a | c) - log P_F(a | c): naive-Bayes log odds that `a` is the
    validated-success action rather than the validated-failure action for the
    held-out context. Laplace(1) smoothing; class prior over actions."""
    V = len(enc.vocab)

    def loglik(subset: list[tuple[frozenset[str], tuple[float, ...], int, bool]]) -> list[float]:
        n_a = [0] * enc.A
        cnt = [[0] * V for _ in range(enc.A)]
        for cs, _x, a, _ok in subset:
            n_a[a] += 1
            for f in cs:
                cnt[a][enc.vindex[f]] += 1
        out = []
        for a in range(enc.A):
            ll = math.log((n_a[a] + NB_LAPLACE) / (len(subset) + NB_LAPLACE * enc.A))
            for f_idx in range(V):
                p = (cnt[a][f_idx] + NB_LAPLACE) / (n_a[a] + 2 * NB_LAPLACE)
                present = enc.query[f_idx] > 0
                ll += math.log(p if present else 1.0 - p)
            out.append(ll)
        return out

    succ = [e for e in enc.episodes if e[3]]
    fail = [e for e in enc.episodes if not e[3]]
    ls = loglik(succ)
    lf = loglik(fail)
    return [ls[a] - lf[a] for a in range(enc.A)]


def _literals(enc: Encoded) -> list[tuple[str, bool]]:
    return [(f, True) for f in enc.vocab] + [(f, False) for f in enc.vocab]


def _matches(cond: tuple[tuple[str, bool], ...], cs: frozenset[str]) -> bool:
    return all((f in cs) == present for f, present in cond)


def decision_list_rules(enc: Encoded) -> list[tuple[tuple[tuple[str, bool], ...], int]]:
    """Sequential covering (Rivest decision lists over conjunctions of up to
    DECISION_LIST_MAX_LITERALS literals). Positive examples of action a are
    SUCCESS episodes with a; SUCCESS episodes with other actions and FAILURE
    episodes with a are negatives. Greedy best-rule-first; deterministic."""
    lits = _literals(enc)
    conds: list[tuple[tuple[str, bool], ...]] = []
    for i, l1 in enumerate(lits):
        conds.append((l1,))
        if DECISION_LIST_MAX_LITERALS >= 2:
            for l2 in lits[i + 1:]:
                if l1[0] == l2[0]:
                    continue
                conds.append((l1, l2))
    remaining = [e for e in enc.episodes if e[3]]
    fails = [e for e in enc.episodes if not e[3]]
    rules: list[tuple[tuple[tuple[str, bool], ...], int]] = []
    while remaining:
        best = None
        for cond in conds:
            covered = [e for e in remaining if _matches(cond, e[0])]
            if not covered:
                continue
            for a in range(enc.A):
                pos = sum(1 for e in covered if e[2] == a)
                if pos == 0:
                    continue
                neg = (len(covered) - pos) + sum(1 for e in fails if e[2] == a and _matches(cond, e[0]))
                score = pos - neg
                key = (score, pos, -len(cond), -a)
                if score > 0 and (best is None or key > best[0]):
                    best = (key, cond, a)
        if best is None:
            break
        _key, cond, a = best
        rules.append((cond, a))
        remaining = [e for e in remaining if not _matches(cond, e[0])]
    return rules


def decision_list(enc: Encoded) -> list[float]:
    rules = decision_list_rules(enc)
    base = simple_frequency(enc)
    # Default = frequency parent; a fired rule dominates by a large offset.
    s = [b / (1.0 + 4.0 * len(enc.episodes)) for b in base]
    for cond, a in rules:
        if _matches(cond, enc.query_set):
            s[a] += 10.0
            break
    return s


def _kesler_update_target(enc: Encoded, cs: frozenset[str], a_wrong: int, W: list[list[float]], x) -> int:
    if cs in enc.success_by_context:
        return enc.success_by_context[cs]
    scores = [dot(W[b], x) if b != a_wrong else -math.inf for b in range(enc.A)]
    return argmax_frozen(scores)


def perceptron_weights(enc: Encoded) -> list[list[float]]:
    D = len(enc.vocab) + 1
    W = [[0.0] * D for _ in range(enc.A)]
    Wsum = [[0.0] * D for _ in range(enc.A)]
    steps = 0
    for _epoch in range(PERCEPTRON_EPOCHS):
        for cs, x, a, ok in enc.episodes:
            scores = [dot(W[b], x) for b in range(enc.A)]
            if ok:
                other = max((scores[b] for b in range(enc.A) if b != a), default=-math.inf)
                if scores[a] - other < PERCEPTRON_MARGIN:
                    b_max = argmax_frozen([scores[b] if b != a else -math.inf for b in range(enc.A)])
                    for k in range(D):
                        W[a][k] += x[k]
                        W[b_max][k] -= x[k]
            else:
                target = _kesler_update_target(enc, cs, a, W, x)
                if scores[target] - scores[a] < PERCEPTRON_MARGIN:
                    for k in range(D):
                        W[target][k] += x[k]
                        W[a][k] -= x[k]
            steps += 1
            for b in range(enc.A):
                for k in range(D):
                    Wsum[b][k] += W[b][k]
    if steps == 0:
        return W
    return [[v / steps for v in row] for row in Wsum]


def perceptron(enc: Encoded) -> list[float]:
    W = perceptron_weights(enc)
    return [dot(W[b], enc.query) for b in range(enc.A)]


def maxmargin_weights(enc: Encoded) -> list[list[float]]:
    """Crammer-Singer multiclass hinge + L2, full-batch subgradient descent
    with a fixed step; FAILURE episodes contribute a pairwise hinge against the
    paired SUCCESS action of the same context (when present)."""
    D = len(enc.vocab) + 1
    W = [[0.0] * D for _ in range(enc.A)]
    for _it in range(MAXMARGIN_ITERS):
        G = [[MAXMARGIN_L2 * W[b][k] for k in range(D)] for b in range(enc.A)]
        for cs, x, a, ok in enc.episodes:
            scores = [dot(W[b], x) for b in range(enc.A)]
            if ok:
                if enc.A == 1:
                    continue
                b_max = argmax_frozen([scores[b] if b != a else -math.inf for b in range(enc.A)])
                if scores[a] - scores[b_max] < 1.0:
                    for k in range(D):
                        G[a][k] -= x[k]
                        G[b_max][k] += x[k]
            else:
                if cs not in enc.success_by_context:
                    continue
                t = enc.success_by_context[cs]
                if t == a:
                    continue
                if scores[t] - scores[a] < 1.0:
                    for k in range(D):
                        G[t][k] -= x[k]
                        G[a][k] += x[k]
        for b in range(enc.A):
            for k in range(D):
                W[b][k] -= MAXMARGIN_STEP * G[b][k]
    return W


def maxmargin(enc: Encoded) -> list[float]:
    W = maxmargin_weights(enc)
    return [dot(W[b], enc.query) for b in range(enc.A)]


def pairwise_linear(enc: Encoded) -> list[float]:
    """One averaged binary perceptron per candidate pair (a < b), trained on
    SUCCESS episodes labelled a (+1) or b (-1) plus FAILURE episodes of a whose
    paired SUCCESS action is b (-1) and vice versa. Each pair casts one vote;
    ties fall to candidate order via the frozen argmax."""
    D = len(enc.vocab) + 1
    votes = [0.0] * enc.A
    for a in range(enc.A):
        for b in range(a + 1, enc.A):
            data: list[tuple[tuple[float, ...], int]] = []
            for cs, x, act, ok in enc.episodes:
                if ok and act == a:
                    data.append((x, 1))
                elif ok and act == b:
                    data.append((x, -1))
                elif not ok and act == a and enc.success_by_context.get(cs) == b:
                    data.append((x, -1))
                elif not ok and act == b and enc.success_by_context.get(cs) == a:
                    data.append((x, 1))
            w = [0.0] * D
            wsum = [0.0] * D
            steps = 0
            for _epoch in range(PERCEPTRON_EPOCHS):
                for x, y in data:
                    if y * dot(w, x) < PERCEPTRON_MARGIN:
                        for k in range(D):
                            w[k] += y * x[k]
                    steps += 1
                    for k in range(D):
                        wsum[k] += w[k]
            wavg = [v / steps for v in wsum] if steps else w
            margin = dot(wavg, enc.query)
            if margin >= 0:
                votes[a] += 1.0
            else:
                votes[b] += 1.0
    return votes


def fixed_meta_lesson(enc: Encoded) -> list[float]:
    """Fixed, non-recursive heuristic: additive per-feature evidence. For each
    held-out feature f, credit action a with (successes of a under f minus
    failures of a under f) / (episodes containing f). Ties -> global
    success-minus-failure frequency, then candidate order. No tuning."""
    s = [0.0] * enc.A
    for f in enc.query_set:
        with_f = [e for e in enc.episodes if f in e[0]]
        if not with_f:
            continue
        for _cs, _x, a, ok in with_f:
            s[a] += (1.0 if ok else -1.0) / len(with_f)
    freq = simple_frequency(enc)
    scale = 1.0 / (1.0 + 4.0 * max(1, len(enc.episodes)))
    return [s[a] + scale * freq[a] * 1e-3 for a in range(enc.A)]


def target_only_deterministic(enc: Encoded) -> list[float]:
    return [0.0] * enc.A  # frozen argmax -> first candidate


PARENT_FUNCTIONS: dict[str, Callable[[Encoded], list[float]]] = {
    "SIMPLE_FREQUENCY_PARENT": simple_frequency,
    "MATCHED_CASE_PARENT": matched_case,
    "NAIVE_BAYES_PARENT": naive_bayes,
    "DECISION_LIST_PARENT": decision_list,
    "PERCEPTRON_PARENT": perceptron,
    "MAXMARGIN_PARENT": maxmargin,
    "PAIRWISE_LINEAR_PARENT": pairwise_linear,
    "FIXED_META_LESSON": fixed_meta_lesson,
    "TARGET_ONLY_DETERMINISTIC": target_only_deterministic,
}


def select(parent_id: str, surface: dict[str, Any]) -> tuple[str, list[float]]:
    enc = Encoded(surface)
    scores = PARENT_FUNCTIONS[parent_id](enc)
    return enc.candidates[argmax_frozen(scores)], scores


def federation(surface: dict[str, Any], strongest_parent: str, members: tuple[str, ...] = PARENT_IDS) -> tuple[str, dict[str, str]]:
    """F0: plurality vote over the parents' selections; ties broken by the
    strongest parent's selection. No information beyond the parents' outputs."""
    enc = Encoded(surface)
    picks: dict[str, str] = {}
    for pid in members:
        picks[pid] = enc.candidates[argmax_frozen(PARENT_FUNCTIONS[pid](enc))]
    tally = [0] * enc.A
    for pid, a in picks.items():
        tally[enc.cand_index[a]] += 1
    top = max(tally)
    winners = [i for i, t in enumerate(tally) if t == top]
    if len(winners) == 1:
        return enc.candidates[winners[0]], picks
    strong = picks[strongest_parent]
    if enc.cand_index[strong] in winners:
        return strong, picks
    return enc.candidates[winners[0]], picks


def advisory(surface: dict[str, Any], strongest_parent: str) -> dict[str, Any]:
    """Parent advisory block for F2 surfaces: derived from the SAME surface the
    arm sees; contains no private information."""
    enc = Encoded(surface)
    out: dict[str, Any] = {"parents": {}, "note": "deterministic parent outputs computed from this request's own surface"}
    for pid in PARENT_IDS:
        scores = PARENT_FUNCTIONS[pid](enc)
        order = sorted(range(enc.A), key=lambda i: (-scores[i], i))
        out["parents"][pid] = {
            "selected_action": enc.candidates[order[0]],
            "ranked_actions": [enc.candidates[i] for i in order],
            "scores": [round(scores[i], 4) for i in range(enc.A)],
        }
    fed, _ = federation(surface, strongest_parent)
    out["strongest_parent"] = strongest_parent
    out["federation_selected_action"] = fed
    return out


# ---------------------------------------------------------------------------
# Native known-answer fidelity tests
# ---------------------------------------------------------------------------

def _planted_surface(rng: random.Random, feature_count: int, action_count: int, weights, contexts, with_failures=True):
    feats = [f"ctx-{i}" for i in range(feature_count)]
    acts = [f"act-{i}" for i in range(action_count)]
    episodes = []
    from sd70v2_generator import best_action  # local import keeps module standalone-importable

    for ctx in contexts:
        best = best_action(ctx, weights)
        episodes.append({"episode_id": f"e{len(episodes)}", "context_features": [feats[i] for i, b in enumerate(ctx) if b],
                         "chosen_action": acts[best], "validated_outcome": "SUCCESS", "resource_cost": 1})
        if with_failures and action_count > 1:
            wrong = (best + 1 + rng.randrange(action_count - 1)) % action_count
            episodes.append({"episode_id": f"e{len(episodes)}", "context_features": [feats[i] for i, b in enumerate(ctx) if b],
                             "chosen_action": acts[wrong], "validated_outcome": "FAILURE", "resource_cost": 1})
    return feats, acts, episodes


def _all_contexts(f: int):
    out = []
    for m in range(1, 2 ** f):
        out.append(tuple((m >> i) & 1 for i in range(f)))
    return out


def fidelity_selftests() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    def rec(parent: str, name: str, passed: bool, detail: str = "") -> None:
        results.append({"parent": parent, "test": name, "passed": bool(passed), "detail": detail})

    # 1. SIMPLE_FREQUENCY: planted majority; tie -> candidate order.
    surf = {"candidate_actions": ["act-x", "act-y", "act-z"], "query_context_features": ["ctx-0"],
            "training_episodes": [
                {"context_features": ["ctx-1"], "chosen_action": "act-y", "validated_outcome": "SUCCESS"},
                {"context_features": ["ctx-2"], "chosen_action": "act-y", "validated_outcome": "SUCCESS"},
                {"context_features": ["ctx-1"], "chosen_action": "act-x", "validated_outcome": "SUCCESS"},
                {"context_features": ["ctx-2"], "chosen_action": "act-z", "validated_outcome": "FAILURE"},
                {"context_features": ["ctx-0"], "chosen_action": "act-z", "validated_outcome": "SUCCESS"},
            ]}
    rec("SIMPLE_FREQUENCY_PARENT", "planted majority act-y", select("SIMPLE_FREQUENCY_PARENT", surf)[0] == "act-y")
    tie = {"candidate_actions": ["act-b", "act-a"], "query_context_features": ["ctx-0"], "training_episodes": []}
    rec("SIMPLE_FREQUENCY_PARENT", "empty evidence -> first candidate", select("SIMPLE_FREQUENCY_PARENT", tie)[0] == "act-b")

    # 2. MATCHED_CASE: identical-context success beats a globally more frequent action.
    surf = {"candidate_actions": ["act-x", "act-y"], "query_context_features": ["ctx-0", "ctx-1"],
            "training_episodes": [
                {"context_features": ["ctx-0", "ctx-1"], "chosen_action": "act-y", "validated_outcome": "SUCCESS"},
                {"context_features": ["ctx-2"], "chosen_action": "act-x", "validated_outcome": "SUCCESS"},
                {"context_features": ["ctx-3"], "chosen_action": "act-x", "validated_outcome": "SUCCESS"},
                {"context_features": ["ctx-2", "ctx-3"], "chosen_action": "act-x", "validated_outcome": "SUCCESS"},
            ]}
    rec("MATCHED_CASE_PARENT", "identical context wins over global frequency", select("MATCHED_CASE_PARENT", surf)[0] == "act-y")
    rec("SIMPLE_FREQUENCY_PARENT", "same fixture: frequency picks act-x (separation)", select("SIMPLE_FREQUENCY_PARENT", surf)[0] == "act-x")

    # 3. NAIVE_BAYES: feature ctx-0 planted as a perfect indicator of act-a.
    eps = []
    for i in range(6):
        eps.append({"context_features": ["ctx-0", f"ctx-{2 + (i % 3)}"], "chosen_action": "act-a", "validated_outcome": "SUCCESS"})
        eps.append({"context_features": ["ctx-1", f"ctx-{2 + (i % 3)}"], "chosen_action": "act-b", "validated_outcome": "SUCCESS"})
        eps.append({"context_features": ["ctx-0", f"ctx-{2 + (i % 3)}"], "chosen_action": "act-b", "validated_outcome": "FAILURE"})
    surf = {"candidate_actions": ["act-b", "act-a"], "query_context_features": ["ctx-0", "ctx-4"], "training_episodes": eps}
    rec("NAIVE_BAYES_PARENT", "planted indicator feature -> act-a", select("NAIVE_BAYES_PARENT", surf)[0] == "act-a")
    surf2 = dict(surf, query_context_features=["ctx-1", "ctx-4"])
    rec("NAIVE_BAYES_PARENT", "planted indicator feature -> act-b", select("NAIVE_BAYES_PARENT", surf2)[0] == "act-b")

    # 4. DECISION_LIST: planted list "if ctx-0 then act-a; elif ctx-1 then act-b; else act-c" over all 7 contexts of 3 features.
    def planted_dl(ctx):
        if ctx[0]:
            return 0
        if ctx[1]:
            return 1
        return 2
    feats = ["ctx-0", "ctx-1", "ctx-2"]
    acts = ["act-a", "act-b", "act-c"]
    eps = []
    for ctx in _all_contexts(3):
        eps.append({"context_features": [feats[i] for i, b in enumerate(ctx) if b], "chosen_action": acts[planted_dl(ctx)], "validated_outcome": "SUCCESS"})
    ok = True
    for ctx in _all_contexts(3):
        surf = {"candidate_actions": acts, "query_context_features": [feats[i] for i, b in enumerate(ctx) if b], "training_episodes": eps}
        if select("DECISION_LIST_PARENT", surf)[0] != acts[planted_dl(ctx)]:
            ok = False
    rec("DECISION_LIST_PARENT", "recovers planted 3-rule decision list on every context", ok)
    rules = decision_list_rules(Encoded({"candidate_actions": acts, "query_context_features": [], "training_episodes": eps}))
    rec("DECISION_LIST_PARENT", "first induced rule is a single literal on ctx-0 -> act-a",
        bool(rules) and rules[0][1] == 0 and len(rules[0][0]) == 1 and rules[0][0][0] == ("ctx-0", True), str(rules[:2]))

    # 5. Linear learners: planted generator-family rule, all contexts observed -> exact reproduction.
    rng = random.Random(20260902)
    for parent in ("PERCEPTRON_PARENT", "MAXMARGIN_PARENT", "PAIRWISE_LINEAR_PARENT"):
        exact_total = 0
        n_total = 0
        for trial in range(5):
            f = 4 + trial % 3
            a = 3 + trial % 3
            weights = [[rng.randint(-3, 4) for _ in range(f)] for _ in range(a)]
            for idx, row in enumerate(weights):
                row[idx % f] += idx + 1
            contexts = _all_contexts(f)
            feats, acts, eps = _planted_surface(rng, f, a, weights, contexts)
            from sd70v2_generator import best_action
            for ctx in contexts:
                surf = {"candidate_actions": acts, "query_context_features": [feats[i] for i, b in enumerate(ctx) if b], "training_episodes": eps}
                n_total += 1
                exact_total += select(parent, surf)[0] == acts[best_action(ctx, weights)]
        if parent == "PAIRWISE_LINEAR_PARENT":
            # Documented boundary: pairwise voting can cycle (Condorcet), so exact
            # reproduction is not guaranteed even when every pair is separable.
            rec(parent, "reproduces planted linear argmax rule on >= 97% of observed contexts (pairwise-vote cycle boundary)",
                exact_total >= 0.97 * n_total, f"{exact_total}/{n_total}")
        else:
            rec(parent, "reproduces planted linear argmax rule when all contexts are observed (training consistency)",
                exact_total == n_total, f"{exact_total}/{n_total}")

    # 6. Null behaviour: label-permuted planted data must sit at chance for every parent.
    rng = random.Random(7)
    from sd70v2_generator import best_action
    for parent in PARENT_IDS + ("FIXED_META_LESSON",):
        hits = 0
        chance = 0.0
        n = 60
        for trial in range(n):
            f = rng.randint(4, 7)
            a = rng.randint(3, 5)
            weights = [[rng.randint(-3, 4) for _ in range(f)] for _ in range(a)]
            contexts = rng.sample(_all_contexts(f), 8)
            feats, acts, eps = _planted_surface(rng, f, a, weights, contexts)
            image = acts[:]
            rng.shuffle(image)
            pi = dict(zip(acts, image))
            for e in eps:
                e["chosen_action"] = pi[e["chosen_action"]]
            q = rng.choice([c for c in _all_contexts(f) if c not in contexts])
            surf = {"candidate_actions": acts, "query_context_features": [feats[i] for i, b in enumerate(q) if b], "training_episodes": eps}
            hits += select(parent, surf)[0] == acts[best_action(q, weights)]
            chance += 1.0 / a
        rate = hits / n
        rec(parent, "label-permuted (candidate bijection) planted data stays within +0.12 of chance", rate <= chance / n + 0.12, f"rate={rate:.3f} chance={chance / n:.3f}")

    # 7. Frozen tie break for every scorer: all-zero scores -> first candidate.
    empty = {"candidate_actions": ["act-q", "act-p"], "query_context_features": ["ctx-9"], "training_episodes": []}
    for parent in PARENT_IDS + ("FIXED_META_LESSON", "TARGET_ONLY_DETERMINISTIC"):
        rec(parent, "no evidence -> first candidate (frozen tie break)", select(parent, empty)[0] == "act-q")

    # 8. Federation: unanimous parents -> that action; strongest breaks a tie.
    fed, picks = federation(surf2, "PERCEPTRON_PARENT")
    rec("F0_PARENT_FEDERATION", "returns a candidate and records every member pick", fed in surf2["candidate_actions"] and set(picks) == set(PARENT_IDS))
    return results
