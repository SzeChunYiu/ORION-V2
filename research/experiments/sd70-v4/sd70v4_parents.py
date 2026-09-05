#!/usr/bin/env python3
"""SD70-V4 parents: V3's seven parents and F0 federation imported read-only, plus the generator-faithful
parent for the new family and the federation that contains it.

GATED_MAXMARGIN_PARENT — the strongest faithful parent for the XOR-gated family: it knows the family FORM
(two linear regimes selected by the XOR of two context bits) but not the gate or the weights.  For every
candidate gate pair (i, j) over the surface vocabulary it splits the training episodes by regime, fits V3's
max-margin parent on each half (frozen hyper-parameters, unchanged), scores the pair by training
consistency (SUCCESS episodes reproduced + FAILURE episodes not chosen), and predicts the query with the
best pair's regime model (ties → lexicographic pair; an empty regime falls back to the pooled max-margin).
F0_PLUS_FEDERATION — plurality over the seven V3 parents and the gated parent; ties → the strongest parent.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
V3 = HERE.parent / "sd70-v3"
for _p in (str(HERE), str(V3)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import sd70v3_parents as P3  # noqa: E402  (read-only)

GATED_PARENT = "GATED_MAXMARGIN_PARENT"
F0_PLUS = "F0_PLUS_FEDERATION"
PARENT_IDS_V4 = P3.PARENT_IDS + (GATED_PARENT,)
GENERATOR_FAITHFUL_CANDIDATES_V4 = P3.GENERATOR_FAITHFUL_CANDIDATES + (GATED_PARENT,)


def _sub_surface(surface: dict[str, Any], keep: list[dict]) -> dict[str, Any]:
    s = dict(surface)
    s["training_episodes"] = keep
    return s


def gated_maxmargin(surface: dict[str, Any]) -> tuple[list[float], dict[str, Any]]:
    enc = P3.Encoded(surface)
    vocab = enc.vocab
    episodes = list(surface.get("training_episodes", []))
    pooled = P3.maxmargin_weights(enc)
    best = None
    for i in range(len(vocab)):
        for j in range(i + 1, len(vocab)):
            fi, fj = vocab[i], vocab[j]
            halves = {0: [], 1: []}
            for ep in episodes:
                cs = set(ep["context_features"])
                halves[int((fi in cs) ^ (fj in cs))].append(ep)
            models = {}
            for r in (0, 1):
                models[r] = P3.maxmargin_weights(P3.Encoded(_sub_surface(surface, halves[r]))) if halves[r] else pooled
            # training consistency under the gated model
            score = 0
            for ep in episodes:
                cs = set(ep["context_features"])
                r = int((fi in cs) ^ (fj in cs))
                x = enc.vector(cs)
                pred = P3.argmax_frozen([P3.dot(models[r][b], x) for b in range(enc.A)])
                chosen = enc.cand_index.get(ep["chosen_action"])
                if ep["validated_outcome"] == "SUCCESS":
                    score += int(pred == chosen)
                else:
                    score += int(pred != chosen)
            key = (score, -i, -j)
            if best is None or key > best[0]:
                best = (key, (fi, fj), models)
    if best is None:  # fewer than two vocabulary features: no gate expressible
        return [P3.dot(pooled[b], enc.query) for b in range(enc.A)], {"gate": None, "fallback": "pooled_maxmargin"}
    _, (fi, fj), models = best
    r = int((fi in enc.query_set) ^ (fj in enc.query_set))
    return [P3.dot(models[r][b], enc.query) for b in range(enc.A)], {"gate": [fi, fj], "query_regime": r, "training_consistency": best[0][0]}


def select(parent_id: str, surface: dict[str, Any]) -> tuple[str, list[float]]:
    if parent_id == GATED_PARENT:
        scores, _ = gated_maxmargin(surface)
        enc = P3.Encoded(surface)
        return enc.candidates[P3.argmax_frozen(scores)], scores
    return P3.select(parent_id, surface)


def federation_plus(surface: dict[str, Any], strongest_parent: str) -> tuple[str, dict[str, str]]:
    enc = P3.Encoded(surface)
    picks = {pid: select(pid, surface)[0] for pid in PARENT_IDS_V4}
    tally = [0] * enc.A
    for a in picks.values():
        tally[enc.cand_index[a]] += 1
    top = max(tally)
    winners = [i for i, t in enumerate(tally) if t == top]
    if len(winners) == 1:
        return enc.candidates[winners[0]], picks
    strong = picks[strongest_parent]
    if enc.cand_index[strong] in winners:
        return strong, picks
    return enc.candidates[winners[0]], picks


def fidelity_selftest() -> dict[str, Any]:
    """Planted gated policy on a FULL-information surface (every nonzero context as a SUCCESS episode
    minus one held-out query): the gated parent must recover the gate and the held-out action; V3's
    max-margin parent, fitted on the same surface, is reported beside it."""
    import random
    from itertools import product
    rng = random.Random(7)
    f, A = 4, 3
    feats = [f"ctx-{k}" for k in range(f)]
    acts = [f"act-{k}" for k in range(A)]
    w0 = [[2, -1, 0, 1], [-1, 2, 1, 0], [0, 0, 3, -2]]
    w1 = [[-2, 1, 1, 0], [1, -2, 0, 2], [3, 0, -1, -1]]
    gate = (0, 2)
    def pol(c):
        w = (w0, w1)[c[gate[0]] ^ c[gate[1]]]
        return P3.argmax_frozen([sum(a * b for a, b in zip(w[a_], c)) for a_ in range(A)])
    ctxs = [c for c in product((0, 1), repeat=f) if any(c)]
    query = ctxs[-1]
    eps = [{"episode_id": f"e{i}", "context_features": [feats[k] for k in range(f) if c[k]], "chosen_action": acts[pol(c)], "validated_outcome": "SUCCESS", "resource_cost": 1}
           for i, c in enumerate(ctxs) if c != query]
    surface = {"training_episodes": eps, "query_context_features": [feats[k] for k in range(f) if query[k]], "candidate_actions": acts, "instruction": ""}
    scores, meta = gated_maxmargin(surface)
    gated_pick = acts[P3.argmax_frozen(scores)]
    mm_pick, _ = P3.select("MAXMARGIN_PARENT", surface)
    truth = acts[pol(query)]
    return {"gate_recovered": meta.get("gate") == [feats[gate[0]], feats[gate[1]]], "gated_pick_correct": gated_pick == truth, "maxmargin_pick_correct": mm_pick == truth,
            "gate_found": meta.get("gate"), "training_consistency": meta.get("training_consistency"), "n_training": len(eps), "rng_unused": rng.random() >= 0}
