#!/usr/bin/env python3
"""Exact finite checker for the WLL strict observation-interface hierarchy."""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from typing import Callable, Hashable, Iterable


@dataclass(frozen=True)
class World:
    theta: tuple[int, ...]
    known_backup: tuple[int, ...]
    unseen_backup: tuple[int, ...]

    def __post_init__(self) -> None:
        p = len(self.theta)
        if len(self.known_backup) != p or len(self.unseen_backup) != p:
            raise ValueError("world vector lengths disagree")
        if any(
            bit not in (0, 1)
            for vector in (self.theta, self.known_backup, self.unseen_backup)
            for bit in vector
        ):
            raise ValueError("world values must be binary")

    @property
    def endpoint(self) -> int:
        return self.theta[0] ^ self.theta[1]

    @property
    def actual_backup(self) -> tuple[int, ...]:
        return tuple(
            known | unseen
            for known, unseen in zip(self.known_backup, self.unseen_backup)
        )

    @property
    def lifecycle_target(self) -> tuple[int, ...]:
        return self.theta + self.actual_backup


def enumerate_worlds(module_count: int = 3, endpoint_value: int = 0):
    worlds = []
    for theta in itertools.product((0, 1), repeat=module_count):
        if (theta[0] ^ theta[1]) != endpoint_value:
            continue
        for known in itertools.product((0, 1), repeat=module_count):
            for unseen in itertools.product((0, 1), repeat=module_count):
                worlds.append(World(theta, known, unseen))
    return tuple(worlds)


def obs_i0(world: World) -> Hashable:
    return (world.endpoint,)


def obs_i1(world: World) -> Hashable:
    return (world.endpoint, world.theta)


def obs_i2(world: World) -> Hashable:
    return (world.endpoint, world.theta, world.known_backup)


def obs_i3(world: World) -> Hashable:
    return (
        world.endpoint,
        world.theta,
        world.known_backup,
        world.actual_backup,
        "CLOSED_SCOPE_EPOCH",
    )


INTERFACES: tuple[tuple[str, Callable[[World], Hashable]], ...] = (
    ("I0_ENDPOINT_ONLY", obs_i0),
    ("I1_RAW_LOCAL_TRACE", obs_i1),
    ("I2_POSITIVE_CERTIFIED_SUPPORT", obs_i2),
    ("I3_CLOSURE_CERTIFIED_WARRANT", obs_i3),
)


def fibers(worlds: Iterable[World], observation: Callable[[World], Hashable]):
    out: dict[Hashable, list[World]] = {}
    for world in worlds:
        out.setdefault(observation(world), []).append(world)
    return {key: tuple(group) for key, group in out.items()}


def target_profiles(group: Iterable[World]):
    return frozenset(world.lifecycle_target for world in group)


def constant_target_coordinates(group: tuple[World, ...]) -> tuple[int, ...]:
    if not group:
        raise ValueError("empty observation fiber")
    width = len(group[0].lifecycle_target)
    return tuple(
        index
        for index in range(width)
        if len({world.lifecycle_target[index] for world in group}) == 1
    )


def interface_metrics(
    worlds: tuple[World, ...], observation: Callable[[World], Hashable]
):
    partition = fibers(worlds, observation)
    profile_counts = [len(target_profiles(group)) for group in partition.values()]
    constant_counts = [
        len(constant_target_coordinates(group)) for group in partition.values()
    ]
    target_width = len(worlds[0].lifecycle_target)
    return {
        "observation_classes": len(partition),
        "max_lifecycle_profiles_per_observation": max(profile_counts),
        "min_lifecycle_profiles_per_observation": min(profile_counts),
        "exact_lifecycle_identification": max(profile_counts) == 1,
        "minimum_guaranteed_answerable_coordinates": min(constant_counts),
        "maximum_required_abstentions_zero_error": target_width - min(constant_counts),
        "target_width": target_width,
    }


def find_strict_witness(
    worlds: tuple[World, ...],
    lower: Callable[[World], Hashable],
    upper: Callable[[World], Hashable],
):
    for lower_obs, group in fibers(worlds, lower).items():
        for left, right in itertools.combinations(group, 2):
            if upper(left) != upper(right) and left.lifecycle_target != right.lifecycle_target:
                return {
                    "lower_observation": repr(lower_obs),
                    "left_world": {
                        "theta": left.theta,
                        "known_backup": left.known_backup,
                        "unseen_backup": left.unseen_backup,
                        "target": left.lifecycle_target,
                    },
                    "right_world": {
                        "theta": right.theta,
                        "known_backup": right.known_backup,
                        "unseen_backup": right.unseen_backup,
                        "target": right.lifecycle_target,
                    },
                }
    raise AssertionError("no strict hierarchy witness found")


def interface_refines(
    worlds: tuple[World, ...],
    lower: Callable[[World], Hashable],
    upper: Callable[[World], Hashable],
) -> bool:
    seen: dict[Hashable, Hashable] = {}
    for world in worlds:
        upper_observation = upper(world)
        lower_observation = lower(world)
        if upper_observation in seen and seen[upper_observation] != lower_observation:
            return False
        seen[upper_observation] = lower_observation
    return True


def run_exact_calibration():
    worlds = enumerate_worlds()
    if len(worlds) != 256:
        raise AssertionError("world-count drift")

    metrics = {
        name: interface_metrics(worlds, observation)
        for name, observation in INTERFACES
    }
    strict_witnesses = {}
    for (lower_name, lower), (upper_name, upper) in zip(
        INTERFACES, INTERFACES[1:]
    ):
        if not interface_refines(worlds, lower, upper):
            raise AssertionError(f"{upper_name} does not refine {lower_name}")
        strict_witnesses[f"{lower_name}_TO_{upper_name}"] = find_strict_witness(
            worlds, lower, upper
        )

    expected = {
        "I0_ENDPOINT_ONLY": (False, 1, 5),
        "I1_RAW_LOCAL_TRACE": (False, 3, 3),
        "I2_POSITIVE_CERTIFIED_SUPPORT": (False, 3, 3),
        "I3_CLOSURE_CERTIFIED_WARRANT": (True, 6, 0),
    }
    for name, (
        exact,
        answerable,
        abstentions,
    ) in expected.items():
        if metrics[name]["exact_lifecycle_identification"] != exact:
            raise AssertionError(f"{name} exactness drift")
        if metrics[name]["minimum_guaranteed_answerable_coordinates"] != answerable:
            raise AssertionError(f"{name} coverage drift")
        if metrics[name]["maximum_required_abstentions_zero_error"] != abstentions:
            raise AssertionError(f"{name} abstention drift")

    positive_world = next(
        world
        for world in worlds
        if world.theta == (0, 0, 0)
        and world.known_backup == (1, 0, 0)
        and world.unseen_backup == (0, 0, 0)
    )
    i1_group = fibers(worlds, obs_i1)[obs_i1(positive_world)]
    i2_group = fibers(worlds, obs_i2)[obs_i2(positive_world)]
    i1_constants = set(constant_target_coordinates(i1_group))
    i2_constants = set(constant_target_coordinates(i2_group))
    backup_coordinate = len(positive_world.theta)
    if backup_coordinate in i1_constants:
        raise AssertionError("I1 incorrectly knows a backup support")
    if backup_coordinate not in i2_constants:
        raise AssertionError("I2 failed to use a positive support certificate")
    if not i1_constants < i2_constants:
        raise AssertionError("I2 witness did not improve this fiber")

    ambiguous_left = World((0, 0, 0), (0, 0, 0), (0, 0, 0))
    ambiguous_right = World((0, 0, 0), (0, 0, 0), (1, 0, 0))
    if obs_i2(ambiguous_left) != obs_i2(ambiguous_right):
        raise AssertionError("ambiguous worlds should share I2 observation")
    if ambiguous_left.lifecycle_target == ambiguous_right.lifecycle_target:
        raise AssertionError("ambiguous worlds should require different action")

    return {
        "schema": "orion.ocm.wll-interface-hierarchy.exact-results.v1",
        "terminal": "PASS_STRICT_INTERFACE_HIERARCHY_FINITE_MODEL",
        "world_count": len(worlds),
        "interface_order": [name for name, _ in INTERFACES],
        "metrics": metrics,
        "strict_refinement_witnesses": strict_witnesses,
        "positive_certificate_local_gain": {
            "world": {
                "theta": positive_world.theta,
                "known_backup": positive_world.known_backup,
                "unseen_backup": positive_world.unseen_backup,
            },
            "I1_constant_coordinates": sorted(i1_constants),
            "I2_constant_coordinates": sorted(i2_constants),
            "newly_answerable_backup_coordinate": backup_coordinate,
        },
        "planted_false_completion": {
            "rule": "treat missing observed positive support as proof of no support",
            "I2_observation_identical": True,
            "left_required_backup_action": ambiguous_left.actual_backup[0],
            "right_required_backup_action": ambiguous_right.actual_backup[0],
            "fired": True,
        },
        "authority": {
            "finite_hierarchy": True,
            "general_literature_novelty": False,
            "architecture_separation": False,
            "natural_language_transfer": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = run_exact_calibration()
    except (AssertionError, ValueError, IndexError) as exc:
        print(json.dumps({"terminal": "FAIL", "error": str(exc)}, indent=2))
        return 1
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS strict WLL interface hierarchy on 256 finite worlds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
