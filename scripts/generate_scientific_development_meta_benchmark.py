#!/usr/bin/env python3
"""Generate fresh SD70 meta-policy tasks with private hidden rules/oracles."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import secrets
from pathlib import Path


def _token(rng: random.Random, prefix: str, n: int = 10) -> str:
    alphabet = "abcdefghjkmnpqrstuvwxyz23456789"
    return f"{prefix}-" + "".join(rng.choice(alphabet) for _ in range(n))


def _best_action(context: tuple[int, ...], weights: list[list[int]]) -> int:
    scores = [sum(bit * weight for bit, weight in zip(context, row, strict=True)) for row in weights]
    return max(range(len(scores)), key=lambda idx: (scores[idx], -idx))


def build_suite(seed: int, tasks: int, train_episodes: int) -> tuple[dict, dict]:
    rng = random.Random(seed)
    public_tasks = []
    private_tasks = []
    for task_index in range(tasks):
        feature_count = rng.randint(4, 7)
        action_count = rng.randint(3, 5)
        feature_tokens = [_token(rng, "ctx") for _ in range(feature_count)]
        action_tokens = [_token(rng, "act") for _ in range(action_count)]
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
            chosen = _best_action(context, weights)
            training.append(
                {
                    "episode_id": f"sd70-{task_index:04d}-train-{len(training):03d}",
                    "context_features": [feature_tokens[i] for i, bit in enumerate(context) if bit],
                    "chosen_action": action_tokens[chosen],
                    "validated_outcome": "SUCCESS",
                    "resource_cost": 1 + sum(context),
                }
            )
            wrong = (chosen + 1 + rng.randrange(action_count - 1)) % action_count
            training.append(
                {
                    "episode_id": f"sd70-{task_index:04d}-train-{len(training):03d}",
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
        correct = _best_action(query_context, weights)
        task_id = f"sd70-{task_index:04d}"
        public_tasks.append(
            {
                "task_id": task_id,
                "source_domain": _token(rng, "domain"),
                "source_epoch": _token(rng, "epoch"),
                "training_episodes": training,
                "query_context_features": [feature_tokens[i] for i, bit in enumerate(query_context) if bit],
                "candidate_actions": action_tokens,
                "instruction": "Infer a bounded action-selection principle from the success+failure trajectories and select exactly one candidate action for the held-out context. Do not invent additional actions.",
            }
        )
        private_tasks.append(
            {
                "task_id": task_id,
                "correct_action": action_tokens[correct],
                "latent_feature_tokens": feature_tokens,
                "latent_action_tokens": action_tokens,
                "latent_weights": weights,
                "query_bits": query_context,
            }
        )

    public = {
        "schema_version": "orion.v2.sd70-generated-meta-policy.public.v1",
        "status": "FRESH_GENERATED_TASKS",
        "seed_commitment": hashlib.sha256(str(seed).encode()).hexdigest(),
        "task_count": len(public_tasks),
        "gold_access": "NONE",
        "tasks": public_tasks,
    }
    private = {
        "schema_version": "orion.v2.sd70-generated-meta-policy.private.v1",
        "seed": seed,
        "task_count": len(private_tasks),
        "tasks": private_tasks,
    }
    return public, private


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", required=True)
    parser.add_argument("--private", required=True)
    parser.add_argument("--tasks", type=int, default=120)
    parser.add_argument("--train-episodes", type=int, default=16)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    if args.tasks < 8 or args.train_episodes < 6:
        raise SystemExit("tasks >= 8 and train-episodes >= 6 are required")
    seed = args.seed if args.seed is not None else secrets.randbits(63)
    public, private = build_suite(seed, args.tasks, args.train_episodes)
    Path(args.public).write_text(json.dumps(public, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.private).write_text(json.dumps(private, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"public": args.public, "private": args.private, "tasks": args.tasks, "seed_commitment": public["seed_commitment"]}, sort_keys=True))


if __name__ == "__main__":
    main()
