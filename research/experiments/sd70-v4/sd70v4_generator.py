#!/usr/bin/env python3
"""SD70-V4 generator: the XOR-gated two-regime policy family (registered, certified outside the linear class).

A task draws V3's dimensions (4–7 binary context features, 3–5 actions) and TWO integer weight matrices
W0, W1 (V3's ranges, distinct rows) plus a hidden gate pair (i, j); the latent policy is
    best(x) = argmax_a W_{x_i XOR x_j}[a] · x     (lowest index on ties)
so the regime a context is scored in depends on an interaction the linear parents' feature map cannot
express.  Tasks are accepted only if the full labelling carries at least one XOR-square certificate
(`sd70v4_containment`), so non-containment is a CHECKED property of every task, never assumed.  Training
episodes, query context, tokens, controls and surfaces are V3's (`sd70v3_generator`, imported read-only)
so every V3 parent and every V3 model-arm surface runs unchanged on V4 tasks.
"""
from __future__ import annotations

import hashlib
import random
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
V3 = HERE.parent / "sd70-v3"
for _p in (str(HERE), str(V3)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import sd70v3_generator as G3  # noqa: E402  (read-only)
from sd70v4_containment import xor_square_certificates  # noqa: E402

SCHEMA_PUBLIC = "orion.v2.sd70-v4.public.v1"
SCHEMA_PRIVATE = "orion.v2.sd70-v4.private.v1"
MAX_REJECTIONS_PER_TASK = 200


def gated_best_action(context: tuple[int, ...], gate: tuple[int, int], weights: tuple[list[list[int]], list[list[int]]]) -> int:
    regime = context[gate[0]] ^ context[gate[1]]
    return G3.best_action(context, weights[regime])


def gated_latent_scores(context, gate, weights) -> list[int]:
    return G3.latent_scores(context, weights[context[gate[0]] ^ context[gate[1]]])


def _distinct_rows(rng: random.Random, action_count: int, feature_count: int) -> list[list[int]]:
    weights = [[rng.randint(-3, 4) for _ in range(feature_count)] for _ in range(action_count)]
    if len({tuple(row) for row in weights}) != len(weights):
        for idx, row in enumerate(weights):
            row[idx % feature_count] += idx + 1
    return weights


def build_suite(seed: int, tasks: int, train_episodes: int, task_prefix: str = "sd70v4", *, linear_control: bool = False) -> tuple[dict, dict]:
    """V4 tasks (gated family, certificate-checked).  ``linear_control=True`` emits V3's linear family
    through the same code path (the planted no-alarm control: zero certificates expected)."""
    rng = random.Random(seed)
    public_tasks, private_tasks, rejections = [], [], 0
    task_index = 0
    while len(public_tasks) < tasks:
        feature_count = rng.randint(4, 7)
        action_count = rng.randint(3, 5)
        feature_tokens = [G3.token(rng, "ctx") for _ in range(feature_count)]
        action_tokens = [G3.token(rng, "act") for _ in range(action_count)]
        w0 = _distinct_rows(rng, action_count, feature_count)
        w1 = w0 if linear_control else _distinct_rows(rng, action_count, feature_count)
        gate = (0, 1) if linear_control else tuple(sorted(rng.sample(range(feature_count), 2)))
        weights = (w0, w1)
        policy = lambda c, g=gate, w=weights: gated_best_action(c, g, w)  # noqa: E731
        certs = xor_square_certificates(policy, feature_count)
        if not linear_control and not certs:
            rejections += 1
            if rejections > MAX_REJECTIONS_PER_TASK * tasks:
                raise RuntimeError("generator could not certify non-containment")
            continue
        training, observed = [], set()
        while len(training) < train_episodes:
            context = tuple(rng.randint(0, 1) for _ in range(feature_count))
            if not any(context) or context in observed:
                continue
            observed.add(context)
            chosen = policy(context)
            training.append({"episode_id": f"{task_prefix}-{task_index:04d}-train-{len(training):03d}", "context_features": [feature_tokens[i] for i, b in enumerate(context) if b],
                             "chosen_action": action_tokens[chosen], "validated_outcome": "SUCCESS", "resource_cost": 1 + sum(context)})
            wrong = (chosen + 1 + rng.randrange(action_count - 1)) % action_count
            training.append({"episode_id": f"{task_prefix}-{task_index:04d}-train-{len(training):03d}", "context_features": [feature_tokens[i] for i, b in enumerate(context) if b],
                             "chosen_action": action_tokens[wrong], "validated_outcome": "FAILURE", "resource_cost": 1 + sum(context)})
        training = training[:train_episodes]
        query = tuple(rng.randint(0, 1) for _ in range(feature_count))
        while not any(query) or query in observed:
            query = tuple(rng.randint(0, 1) for _ in range(feature_count))
        correct = policy(query)
        scores = gated_latent_scores(query, gate, weights)
        worst = [action_tokens[i] for i, s in enumerate(scores) if s == min(scores)]
        task_id = f"{task_prefix}-{task_index:04d}"
        public_tasks.append({"task_id": task_id, "source_domain": G3.token(rng, "domain"), "source_epoch": G3.token(rng, "epoch"), "training_episodes": training,
                             "query_context_features": [feature_tokens[i] for i, b in enumerate(query) if b], "candidate_actions": action_tokens, "instruction": G3.TASK_INSTRUCTION})
        private_tasks.append({"task_id": task_id, "correct_action": action_tokens[correct], "worst_actions": worst, "latent_query_scores": scores, "latent_feature_tokens": feature_tokens,
                              "latent_action_tokens": action_tokens, "latent_weights": [w0, w1], "latent_gate": list(gate), "query_bits": list(query), "chance_level": 1.0 / action_count,
                              "xor_square_certificates": len(certs), "first_certificate": certs[0] if certs else None, "family": "LINEAR_CONTROL" if linear_control else "XOR_GATED"})
        task_index += 1
    public = {"schema_version": SCHEMA_PUBLIC, "status": "FRESH_GENERATED_TASKS", "seed_commitment": hashlib.sha256(str(seed).encode()).hexdigest(), "task_count": len(public_tasks),
              "gold_access": "NONE", "family": "LINEAR_CONTROL" if linear_control else "XOR_GATED", "tasks": public_tasks}
    private = {"schema_version": SCHEMA_PRIVATE, "seed": seed, "task_count": len(private_tasks), "rejections": rejections, "tasks": private_tasks}
    return public, private
