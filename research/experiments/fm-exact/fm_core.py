#!/usr/bin/env python3
"""Shared exact-study harness for the FM series (formal transfer mechanics, L4).

House style is inherited from `research/experiments/me-x{1,2,4}`: exact
generator, exhaustive oracle cross-checked by an independent algorithm, seed
commitment under `~/.orion-custody/fm/`, a development split that is separate
from the protected split, and pre-registered gates.

Two additions are made here on purpose, both learned from defects found on
2026-09-02:

1.  **Every gate reports how many instances it actually evaluated.**  A gate
    that reports zero violations because it never ran on the relevant cases is
    the recurring defect of this programme, so `GateResult` carries
    `n_evaluated` and a gate that evaluated nothing is `CANNOT_CHECK`, never
    `pass`.
2.  **Every no-alarm assertion is paired with a planted positive.**  A suite
    registers decoys/planted violations per family; `decoy_coverage` fails the
    G0 block when a family that must contain a trip-wire contains none.

The module is content-neutral: suites supply a `SuiteSpec` and the runner does
generation, dispatch, scoring, gates and receipts identically for all of them.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

# --------------------------------------------------------------------------
# hashing / canonical serialisation
# --------------------------------------------------------------------------


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canonical_json(obj: Any) -> str:
    """Deterministic serialisation used for every artifact that is hashed."""
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


# --------------------------------------------------------------------------
# exact statistics
# --------------------------------------------------------------------------


def exact_binomial_two_sided(b: int, c: int) -> float:
    """Exact two-sided sign (McNemar) test on discordant pairs."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / 2**n
    return min(1.0, 2 * p)


def paired_summary(x: Sequence[bool], y: Sequence[bool]) -> dict:
    """Paired comparison of two arms' per-instance exactness indicators."""
    n = len(x)
    b = sum(1 for a, bb in zip(x, y) if a and not bb)
    c = sum(1 for a, bb in zip(x, y) if bb and not a)
    diff = (b - c) / n if n else 0.0
    se = math.sqrt(max(0.0, (b + c) - (b - c) ** 2 / n)) / n if n else 0.0
    return {
        "n": n,
        "x_only": b,
        "y_only": c,
        "discordant": b + c,
        "diff_x_minus_y": diff,
        "wald_ci95": [diff - 1.96 * se, diff + 1.96 * se],
        "exact_p_two_sided": exact_binomial_two_sided(b, c),
    }


def holm(pvalues: dict[str, float]) -> dict[str, dict]:
    """Holm-Bonferroni step-down adjustment across a family of tests."""
    items = sorted(pvalues.items(), key=lambda kv: kv[1])
    m = len(items)
    out: dict[str, dict] = {}
    running = 0.0
    for i, (k, p) in enumerate(items):
        adj = min(1.0, max(running, (m - i) * p))
        running = adj
        out[k] = {"raw_p": p, "holm_p": adj, "rank": i + 1, "m": m}
    return out


# --------------------------------------------------------------------------
# gates
# --------------------------------------------------------------------------


@dataclass
class GateResult:
    """A gate verdict that always carries its own denominator.

    `n_evaluated` is the number of instances the gate's rule was actually
    applied to.  `verdict` is PASS / FAIL / CANNOT_CHECK; a gate with
    `n_evaluated == 0` can never be PASS.
    """

    name: str
    rule: str
    n_evaluated: int
    n_violations: int
    hard: bool = True
    detail: dict = field(default_factory=dict)
    requires_evaluated: int = 1
    applicable: bool = True
    verdict_labels: tuple[str, str] = ("PASS", "FAIL")

    @property
    def verdict(self) -> str:
        if not self.applicable:
            return "NOT_APPLICABLE"
        if self.n_evaluated < self.requires_evaluated:
            return "CANNOT_CHECK"
        ok, bad = self.verdict_labels
        return ok if self.n_violations == 0 else bad

    @property
    def passed(self) -> bool | None:
        v = self.verdict
        if v == self.verdict_labels[0]:
            return True
        if v == self.verdict_labels[1]:
            return False
        return None

    def as_dict(self) -> dict:
        return {
            "gate": self.name,
            "verdict": self.verdict,
            "rule": self.rule,
            "n_evaluated": self.n_evaluated,
            "n_violations": self.n_violations,
            "min_required_evaluated": self.requires_evaluated,
            "hard": self.hard,
            "applicable": self.applicable,
            "detail": self.detail,
        }


def gate_block_ok(gates: Sequence[GateResult]) -> bool:
    """A block of hard gates passes only if every hard gate is PASS.

    A gate that could not be evaluated (`CANNOT_CHECK`) never counts as a pass:
    "could not check" is not "checked and fine".
    """
    return all(g.verdict == "PASS" for g in gates if g.hard and g.applicable)


# --------------------------------------------------------------------------
# planted-positive registry (trip-wire discipline)
# --------------------------------------------------------------------------


@dataclass
class PlantedPositive:
    """A case constructed so that a named gate MUST fire on it.

    Registering one is how a no-alarm assertion earns the right to be believed:
    the same predicate that reports `0 violations` on the study is shown to
    report `>= 1` on the planted case.
    """

    gate: str
    name: str
    description: str
    fired: bool | None = None

    def as_dict(self) -> dict:
        return {
            "gate": self.gate,
            "name": self.name,
            "description": self.description,
            "fired": self.fired,
        }


def decoy_coverage_gate(counts: dict[str, int], minimum: int) -> GateResult:
    """Gate: each registered decoy family carries at least `minimum` members."""
    short = {k: v for k, v in counts.items() if v < minimum}
    return GateResult(
        name="G0d_DECOY_COVERAGE",
        rule=f"every registered decoy family carries >= {minimum} instances in the split",
        n_evaluated=len(counts),
        n_violations=len(short),
        detail={"counts": counts, "minimum": minimum, "below_minimum": short},
    )


def discrimination_gate(
    per_arm_exact: dict[str, float],
    *,
    weak_arms: Sequence[str],
    strong_arm: str,
    max_weak: float,
    min_strong: float,
) -> GateResult:
    """Gate against an uninformative task family.

    The FM/FG R2 registered-scale campaign (2026-08-30) produced eight studies
    at ceiling and one at floor: every arm scored the same and the comparison
    could not have detected a difference had one existed.  A family that cannot
    separate a deliberately weak arm from the strongest parent is a defect of
    the generator, not a null result, so it is gated explicitly.
    """
    strong = per_arm_exact.get(strong_arm)
    viol = []
    if strong is None or strong < min_strong:
        viol.append(f"{strong_arm}={strong}")
    if not any(per_arm_exact.get(a, 1.0) <= max_weak for a in weak_arms):
        viol.append("no weak arm below max_weak")
    return GateResult(
        name="G0f_FAMILY_DISCRIMINATION",
        rule=(
            f"the split is non-degenerate: {strong_arm} >= {min_strong} and at "
            f"least one of {list(weak_arms)} <= {max_weak} (guards against the "
            "ceiling/floor families that made FM/FG R2 uninformative)"
        ),
        n_evaluated=len(per_arm_exact),
        n_violations=len(viol),
        detail={
            "per_arm_exact": per_arm_exact,
            "weak_arms": list(weak_arms),
            "strong_arm": strong_arm,
            "max_weak": max_weak,
            "min_strong": min_strong,
            "violations": viol,
        },
    )


# --------------------------------------------------------------------------
# null calibration
# --------------------------------------------------------------------------


def shuffled_label_null(
    labels: Sequence[str], predictions: Sequence[str], *, seed: int
) -> dict:
    """Exactness of an arm against within-split shuffled oracle labels.

    A mechanic that scores well against shuffled labels is scoring on something
    other than the answer.
    """
    rng = random.Random(seed)
    shuffled = list(labels)
    rng.shuffle(shuffled)
    hits = sum(1 for p, s in zip(predictions, shuffled) if p == s)
    return {
        "n": len(labels),
        "exact_against_shuffled": hits,
        "rate": hits / len(labels) if labels else 0.0,
        "seed": seed,
    }


def null_calibration_gate(
    *,
    constant_arm_rates: dict[str, float],
    random_rate: float,
    shuffle: dict,
    max_constant: float,
    max_random: float,
    max_shuffle: float,
) -> GateResult:
    viol: list[str] = []
    for arm, rate in constant_arm_rates.items():
        if rate > max_constant:
            viol.append(f"{arm}={rate:.4f}>{max_constant}")
    if random_rate > max_random:
        viol.append(f"random={random_rate:.4f}>{max_random}")
    if shuffle["rate"] > max_shuffle:
        viol.append(f"shuffled_label={shuffle['rate']:.4f}>{max_shuffle}")
    n_eval = len(constant_arm_rates) + 1 + (1 if shuffle["n"] else 0)
    return GateResult(
        name="G0c_NULL_CALIBRATION",
        rule=(
            f"constant-response arms <= {max_constant}, random arm <= {max_random}, "
            f"M against within-split shuffled oracle labels <= {max_shuffle}"
        ),
        n_evaluated=n_eval,
        n_violations=len(viol),
        detail={
            "constant_arm_rates": constant_arm_rates,
            "random_rate": random_rate,
            "shuffled_label_null": shuffle,
            "violations": viol,
        },
    )


# --------------------------------------------------------------------------
# suite specification
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ArmSpec:
    name: str
    kind: str  # PARENT | FEDERATION | MECHANIC | ABLATION | CONTROL
    description: str = ""

    def as_dict(self) -> dict:
        return {"name": self.name, "kind": self.kind, "description": self.description}


@dataclass(frozen=True)
class SuiteSpec:
    """Everything the shared runner needs to execute one FM suite."""

    suite_id: str  # e.g. "FM10"
    title: str
    families: tuple[str, ...]
    arms: tuple[ArmSpec, ...]
    mechanic_arm: str
    strongest_parent_arm: str
    federation_arm: str
    weak_arms: tuple[str, ...]
    constant_arms: tuple[str, ...]
    random_arm: str
    ablation_for_family: dict[str, str]
    default_ablation: str
    decoy_families: tuple[str, ...]
    min_tasks: int
    dev_per_family: int
    protected_per_family: int
    design_json: str  # filename of the frozen design JSON
    seed_commitment_key: str = "protected_seed_sha256"

    # callables supplied by the suite module
    generate: Callable[[str, str, dict[str, int]], list] = None  # type: ignore[assignment]
    oracle: Callable[[Any], Any] = None  # type: ignore[assignment]
    cross_check: Callable[[Any], Any] = None  # type: ignore[assignment]
    run_arm: Callable[[str, Any], Any] = None  # type: ignore[assignment]
    parent_fidelity: Callable[[], list[dict]] = None  # type: ignore[assignment]
    known_answer_fixtures: Callable[[], list[dict]] = None  # type: ignore[assignment]
    planted_positives: Callable[[], list[PlantedPositive]] = None  # type: ignore[assignment]

    def arm_names(self) -> list[str]:
        return [a.name for a in self.arms]


__all__ = [
    "ArmSpec",
    "GateResult",
    "PlantedPositive",
    "SuiteSpec",
    "canonical_json",
    "decoy_coverage_gate",
    "discrimination_gate",
    "exact_binomial_two_sided",
    "gate_block_ok",
    "holm",
    "null_calibration_gate",
    "paired_summary",
    "sha256_bytes",
    "sha256_text",
    "shuffled_label_null",
]
