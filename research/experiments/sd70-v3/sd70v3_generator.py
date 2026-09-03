#!/usr/bin/env python3
"""SD70-V3 generator: frozen synthetic hidden-policy family, negative-control
variants, and physically sanitized per-arm request surfaces.

The task family is byte-identical to the V1 generator
(`scripts/generate_scientific_development_meta_benchmark.py`, `build_suite`):
a hidden integer linear multiclass rule over binary context features with
lowest-index tie break, 8 paired SUCCESS/FAILURE training contexts, and one
unseen held-out context. V2 adds (a) the private worst-action set used by the
critical-false-direction outcome, (b) two solver-facing negative-control
variants, and (c) per-arm request surfaces whose top-level keys are physically
restricted to the arm's registered information.

Stdlib only; deterministic given the seed.
"""
from __future__ import annotations

import hashlib
import json
import random
from typing import Any

SCHEMA_PUBLIC = "orion.v2.sd70-v3.public.v1"
SCHEMA_PRIVATE = "orion.v2.sd70-v3.private.v1"
SCHEMA_REQUEST = "orion.v2.sd70-v3.request.v1"

TASK_INSTRUCTION = (
    "Infer a bounded action-selection principle from the success+failure "
    "trajectories and select exactly one candidate action for the held-out "
    "context. Do not invent additional actions."
)
TARGET_ONLY_INSTRUCTION = (
    "Select exactly one candidate action for the held-out context. No "
    "trajectories are available. Do not invent additional actions."
)

# Registered information surfaces (top-level keys of `surface` in a request).
SURFACE_COMMON = ("training_episodes", "query_context_features", "candidate_actions", "instruction")
SURFACE_TARGET_ONLY = ("query_context_features", "candidate_actions", "instruction")
SURFACE_WITH_ADVISORY = SURFACE_COMMON + ("parent_advisory",)


def token(rng: random.Random, prefix: str, n: int = 10) -> str:
    alphabet = "abcdefghjkmnpqrstuvwxyz23456789"
    return f"{prefix}-" + "".join(rng.choice(alphabet) for _ in range(n))


def best_action(context: tuple[int, ...], weights: list[list[int]]) -> int:
    scores = [sum(bit * weight for bit, weight in zip(context, row)) for row in weights]
    return max(range(len(scores)), key=lambda idx: (scores[idx], -idx))


def latent_scores(context: tuple[int, ...], weights: list[list[int]]) -> list[int]:
    return [sum(bit * weight for bit, weight in zip(context, row)) for row in weights]


def build_suite(seed: int, tasks: int, train_episodes: int, task_prefix: str = "sd70") -> tuple[dict, dict]:
    """V1-identical task family (same RNG consumption order), V2 private extras."""
    rng = random.Random(seed)
    public_tasks = []
    private_tasks = []
    for task_index in range(tasks):
        feature_count = rng.randint(4, 7)
        action_count = rng.randint(3, 5)
        feature_tokens = [token(rng, "ctx") for _ in range(feature_count)]
        action_tokens = [token(rng, "act") for _ in range(action_count)]
        weights = [[rng.randint(-3, 4) for _ in range(feature_count)] for _ in range(action_count)]
        if len({tuple(row) for row in weights}) != len(weights):
            weights = [row[:] for row in weights]
            for idx, row in enumerate(weights):
                row[idx % feature_count] += idx + 1

        training = []
        observed_contexts: set[tuple[int, ...]] = set()
        while len(training) < train_episodes:
            context = tuple(rng.randint(0, 1) for _ in range(feature_count))
            if not any(context) or context in observed_contexts:
                continue
            observed_contexts.add(context)
            chosen = best_action(context, weights)
            training.append(
                {
                    "episode_id": f"{task_prefix}-{task_index:04d}-train-{len(training):03d}",
                    "context_features": [feature_tokens[i] for i, bit in enumerate(context) if bit],
                    "chosen_action": action_tokens[chosen],
                    "validated_outcome": "SUCCESS",
                    "resource_cost": 1 + sum(context),
                }
            )
            wrong = (chosen + 1 + rng.randrange(action_count - 1)) % action_count
            training.append(
                {
                    "episode_id": f"{task_prefix}-{task_index:04d}-train-{len(training):03d}",
                    "context_features": [feature_tokens[i] for i, bit in enumerate(context) if bit],
                    "chosen_action": action_tokens[wrong],
                    "validated_outcome": "FAILURE",
                    "resource_cost": 1 + sum(context),
                }
            )
        training = training[:train_episodes]

        query_context = tuple(rng.randint(0, 1) for _ in range(feature_count))
        while not any(query_context) or query_context in observed_contexts:
            query_context = tuple(rng.randint(0, 1) for _ in range(feature_count))
        correct = best_action(query_context, weights)
        scores = latent_scores(query_context, weights)
        worst = [action_tokens[i] for i, s in enumerate(scores) if s == min(scores)]
        task_id = f"{task_prefix}-{task_index:04d}"
        public_tasks.append(
            {
                "task_id": task_id,
                "source_domain": token(rng, "domain"),
                "source_epoch": token(rng, "epoch"),
                "training_episodes": training,
                "query_context_features": [feature_tokens[i] for i, bit in enumerate(query_context) if bit],
                "candidate_actions": action_tokens,
                "instruction": TASK_INSTRUCTION,
            }
        )
        private_tasks.append(
            {
                "task_id": task_id,
                "correct_action": action_tokens[correct],
                "worst_actions": worst,
                "latent_query_scores": scores,
                "latent_feature_tokens": feature_tokens,
                "latent_action_tokens": action_tokens,
                "latent_weights": weights,
                "query_bits": list(query_context),
                "chance_level": 1.0 / action_count,
            }
        )

    public = {
        "schema_version": SCHEMA_PUBLIC,
        "status": "FRESH_GENERATED_TASKS",
        "seed_commitment": hashlib.sha256(str(seed).encode()).hexdigest(),
        "task_count": len(public_tasks),
        "gold_access": "NONE",
        "tasks": public_tasks,
    }
    private = {
        "schema_version": SCHEMA_PRIVATE,
        "seed": seed,
        "task_count": len(private_tasks),
        "tasks": private_tasks,
    }
    return public, private


# ---------------------------------------------------------------------------
# Negative controls (solver-facing; derived deterministically from a control seed)
# ---------------------------------------------------------------------------

def control_seed(master_seed: int, label: str) -> int:
    return int(hashlib.sha256(f"SD70-V3-CONTROL|{label}|{master_seed}".encode()).hexdigest()[:15], 16)


def label_permutation_controls(public: dict, private: dict, master_seed: int) -> tuple[dict, dict]:
    """Label permutation: a uniformly random bijection pi on the candidate
    actions (identity included) is applied to `chosen_action` of every training
    episode of the task. Contexts, SUCCESS/FAILURE labels, the candidate list,
    the held-out context and the private answer are untouched. Every learner
    that is equivariant under relabelling then predicts pi(g) where g is its
    protected prediction, so P(pi(g) = correct) = 1/|candidates| exactly: the
    expected accuracy of every arm is the chance level, with all marginal and
    structural statistics of the training preserved."""
    rng = random.Random(control_seed(master_seed, "LP"))
    pub_tasks, priv_tasks = [], []
    priv_by_id = {t["task_id"]: t for t in private["tasks"]}
    for task in public["tasks"]:
        cands = list(task["candidate_actions"])
        image = cands[:]
        rng.shuffle(image)
        pi = dict(zip(cands, image))
        episodes = []
        for ep in task["training_episodes"]:
            item = dict(ep)
            item["chosen_action"] = pi[ep["chosen_action"]]
            episodes.append(item)
        new = dict(task)
        new["task_id"] = task["task_id"] + "-LP"
        new["training_episodes"] = episodes
        pub_tasks.append(new)
        p = dict(priv_by_id[task["task_id"]])
        p["task_id"] = new["task_id"]
        p["control"] = "LABEL_PERMUTATION"
        p["label_bijection"] = pi
        priv_tasks.append(p)
    return (
        {**public, "task_count": len(pub_tasks), "tasks": pub_tasks, "control": "LABEL_PERMUTATION"},
        {**private, "task_count": len(priv_tasks), "tasks": priv_tasks, "control": "LABEL_PERMUTATION"},
    )


def query_shuffle_controls(public: dict, private: dict, master_seed: int) -> tuple[dict, dict]:
    """Query-to-task shuffle. Task i keeps its own training trajectories and
    vocabulary; its held-out context is replaced by the query bits of task
    sigma(i) (a fixed derangement), mapped positionally into task i's feature
    tokens, and the private correct action is the argmax of task sigma(i)'s
    hidden rule on those bits, mapped positionally into task i's candidates
    (index modulo candidate count). The answer is therefore independent of
    anything learnable from task i's training; expected accuracy is the chance
    level (a small tie-break bias toward low indices is shared by all arms)."""
    rng = random.Random(control_seed(master_seed, "QS"))
    n = len(public["tasks"])
    order = list(range(n))
    if n > 1:
        for _ in range(1000):
            rng.shuffle(order)
            if all(order[i] != i for i in range(n)):
                break
        else:
            order = [(i + 1) % n for i in range(n)]
    priv_list = private["tasks"]
    pub_tasks, priv_tasks = [], []
    for i, task in enumerate(public["tasks"]):
        src_priv = priv_list[order[i]]
        own_priv = priv_list[i]
        own_features = own_priv["latent_feature_tokens"]
        bits = list(src_priv["query_bits"])[: len(own_features)]
        bits += [0] * (len(own_features) - len(bits))
        if not any(bits):
            bits[0] = 1
        src_bits = tuple(src_priv["query_bits"])
        src_best = best_action(src_bits, src_priv["latent_weights"])
        target_idx = src_best % len(task["candidate_actions"])
        new = dict(task)
        new["task_id"] = task["task_id"] + "-QS"
        new["query_context_features"] = [own_features[k] for k, b in enumerate(bits) if b]
        pub_tasks.append(new)
        scores = latent_scores(tuple(bits), own_priv["latent_weights"])
        p = dict(own_priv)
        p["task_id"] = new["task_id"]
        p["control"] = "QUERY_TO_TASK_SHUFFLE"
        p["correct_action"] = task["candidate_actions"][target_idx]
        p["query_bits"] = bits
        p["latent_query_scores"] = scores
        p["worst_actions"] = [task["candidate_actions"][k] for k, s in enumerate(scores) if s == min(scores)]
        p["shuffle_source_task_id"] = src_priv["task_id"]
        priv_tasks.append(p)
    return (
        {**public, "task_count": len(pub_tasks), "tasks": pub_tasks, "control": "QUERY_TO_TASK_SHUFFLE"},
        {**private, "task_count": len(priv_tasks), "tasks": priv_tasks, "control": "QUERY_TO_TASK_SHUFFLE"},
    )


# ---------------------------------------------------------------------------
# Physically sanitized per-arm request surfaces
# ---------------------------------------------------------------------------

def surface_for(arm_surface: str, task: dict, advisory: dict | None) -> dict[str, Any]:
    """Return the physical request surface for one arm. Only registered keys
    are present; nothing else from the task is copied."""
    if arm_surface == "TARGET_ONLY":
        return {
            "query_context_features": list(task["query_context_features"]),
            "candidate_actions": list(task["candidate_actions"]),
            "instruction": TARGET_ONLY_INSTRUCTION,
        }
    if arm_surface == "COMMON":
        return {
            "training_episodes": [dict(ep) for ep in task["training_episodes"]],
            "query_context_features": list(task["query_context_features"]),
            "candidate_actions": list(task["candidate_actions"]),
            "instruction": task["instruction"],
        }
    if arm_surface == "COMMON_SUCCESS_ONLY":
        return {
            "training_episodes": [dict(ep) for ep in task["training_episodes"] if ep["validated_outcome"] == "SUCCESS"],
            "query_context_features": list(task["query_context_features"]),
            "candidate_actions": list(task["candidate_actions"]),
            "instruction": task["instruction"],
        }
    if arm_surface in ("COMMON_WITH_ADVISORY", "COMMON_SUCCESS_ONLY_WITH_ADVISORY"):
        base = surface_for(arm_surface.replace("_WITH_ADVISORY", ""), task, None)
        if advisory is None:
            raise ValueError("advisory surface requires a parent advisory")
        base["parent_advisory"] = advisory
        return base
    raise ValueError(f"unknown arm surface: {arm_surface}")


def build_request(task_id: str, arm_id: str, surface: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_REQUEST,
        "task_id": task_id,
        "arm_id": arm_id,
        "surface": surface,
        "surface_keys": sorted(surface),
        "gold_access": "NONE",
        "outcome_access": "NONE",
        "scientific_truth_authorized": False,
    }


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256_of(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def surface_tokens(surface: dict[str, Any]) -> set[str]:
    """Every token string reachable from a request surface (for leak checks)."""
    out: set[str] = set()

    def walk(v: Any) -> None:
        if isinstance(v, str):
            out.add(v)
        elif isinstance(v, dict):
            for k, x in v.items():
                out.add(str(k))
                walk(x)
        elif isinstance(v, (list, tuple)):
            for x in v:
                walk(x)

    walk(surface)
    return out
