"""ME-X6 arms.

Every arm sees the *fit window* channels only -- never a latent coordinate,
never a holdout period.  Arms differ in two ways and only two: which channels
they receive (the ladder), and whether they combine them as an untyped
aggregate or as a typed state (the study's question).
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, Sequence

from mex6_model import (
    ACTIVITY_CHANNELS,
    ATTENTION_CHANNELS,
    B4_LITERAL_CHANNELS,
    CHANNELS,
    FALL,
    FLAT,
    NETWORK_CHANNELS,
    RISE,
    SEMANTIC_CHANNELS,
    VALIDATION_CHANNELS,
    FieldWindow,
    Period,
    Verdict,
)

# ---- the shared, frozen direction rule ----------------------------------------


def _halves(w: FieldWindow) -> tuple[Sequence[Period], Sequence[Period]]:
    h = w.fit_len // 2
    return w.fit_periods[:h], w.fit_periods[h:]


def _dir_of(w: FieldWindow, keys: Sequence[str], signs: dict[str, int] | None = None) -> str:
    a, b = _halves(w)
    sg = signs or {}
    before = sum(sg.get(k, 1) * p.channels[k] for p in a for k in keys)
    after = sum(sg.get(k, 1) * p.channels[k] for p in b for k in keys)
    return RISE if after > before else (FALL if after < before else FLAT)


# ---- the typed capability score (M's registered hypothesis) --------------------
# Validated capability rises with independently checkable evidence and falls with
# invalidation.  The retraction weight is 2 because a retraction withdraws a
# claim rather than merely qualifying it (protocol I4: the model must support
# negative revision).  Cost enters negatively: the same validated result reached
# more cheaply is a capability gain (validation target V4).
TYPED_SIGNS: dict[str, int] = {
    "formal_artifacts": +1,
    "replications_passed": +1,
    "downstream_reuse": +1,
    "independent_rederivations": +1,
    "replications_failed": -1,
    "corrections": -1,
    "retractions": -2,
    "solution_cost": -1,
}


@dataclass(frozen=True, slots=True)
class ArmSpec:
    name: str
    channels: tuple[str, ...]
    capability: Callable[[FieldWindow, tuple[str, ...], random.Random], str]


def _cap_untyped(w: FieldWindow, chans: tuple[str, ...], rng: random.Random) -> str:
    """The science-of-science combination: one aggregate, read for its trend."""
    return _dir_of(w, chans)


def _cap_typed(w: FieldWindow, chans: tuple[str, ...], rng: random.Random) -> str:
    """M: the same channels, read as a typed state with signed roles."""
    keys = tuple(k for k in chans if k in TYPED_SIGNS)
    if not keys:
        return FLAT
    return _dir_of(w, keys, TYPED_SIGNS)


def _cap_always_rise(w, chans, rng): return RISE
def _cap_always_flat(w, chans, rng): return FLAT
def _cap_random(w, chans, rng): return rng.choice((RISE, FLAT, FALL))


LADDER = (
    ("L1_ACTIVITY_ONLY", ACTIVITY_CHANNELS),
    ("L2_PLUS_ATTENTION", ACTIVITY_CHANNELS + ATTENTION_CHANNELS),
    ("L3_PLUS_SEMANTIC", ACTIVITY_CHANNELS + ATTENTION_CHANNELS + SEMANTIC_CHANNELS),
    ("L4_PLUS_NETWORK", B4_LITERAL_CHANNELS),
    ("L5_PLUS_VALIDATION", CHANNELS),
)

# M's ablations: drop one typed validation group at a time.
ABLATION_GROUPS: dict[str, tuple[str, ...]] = {
    "M_MINUS_FORMAL": ("formal_artifacts",),
    "M_MINUS_REPLICATION": ("replications_passed", "replications_failed"),
    "M_MINUS_CORRECTION_RETRACTION": ("corrections", "retractions"),
    "M_MINUS_REUSE": ("downstream_reuse",),
    "M_MINUS_REDERIVATION": ("independent_rederivations",),
    "M_MINUS_COST": ("solution_cost",),
}

# ---- the strongest faithful untyped parent ------------------------------------
# An equal-weight aggregate is a strawman: a real science-of-science modeller
# given the validation channels would FIT the combination rather than sum it.
# B4X_FITTED is that parent.  Its per-channel signs are learned on the public
# DEVELOPMENT split and then FROZEN into the design JSON before the protected
# run, so it is information-matched with M, is allowed to discover the same sign
# structure M declares a priori, and cannot be tuned after any protected outcome.
# If it ties M, the registered terminal is PARENT_SUFFICIENT and X6 contracts to
# an interpretive framework -- the protocol's own contraction rule, and a
# legitimate publishable result, not a failure.
FITTED_SIGNS: dict[str, int] = {}


def load_fitted_signs(signs: dict[str, int]) -> None:
    FITTED_SIGNS.clear()
    FITTED_SIGNS.update(signs)


def fit_signs(instances) -> dict[str, int]:
    """Learn one sign per channel by agreement with the oracle capability
    direction on the split it is given.  Deterministic, no randomness, no
    hyperparameter: a channel scores +1 if its own fit-window direction matches
    the true capability direction more often than it opposes it."""
    from mex6_oracle import oracle

    score = {c: 0 for c in CHANNELS}
    for inst in instances:
        w = inst.window
        truth = oracle(w).capability
        if truth == FLAT:
            continue
        for c in CHANNELS:
            d = _dir_of(w, (c,))
            if d == FLAT:
                continue
            score[c] += 1 if d == truth else -1
    return {c: (1 if v > 0 else (-1 if v < 0 else 0)) for c, v in score.items()}


def _cap_fitted(w: FieldWindow, chans: tuple[str, ...], rng: random.Random) -> str:
    if not FITTED_SIGNS:
        raise RuntimeError("B4X_FITTED used before its frozen signs were loaded")
    keys = tuple(c for c in chans if FITTED_SIGNS.get(c, 0) != 0)
    if not keys:
        return FLAT
    return _dir_of(w, keys, FITTED_SIGNS)


M_ARM = "M_TYPED_COLLECTIVE_STATE"
B4X_ARM = "B4X_INFORMATION_MATCHED_UNTYPED"
B4_LITERAL_ARM = "B4_SCIENCE_OF_SCIENCE_LITERAL"
B4X_FITTED_ARM = "B4X_FITTED_UNTYPED"


def arm_specs() -> tuple[ArmSpec, ...]:
    specs: list[ArmSpec] = [
        ArmSpec("B0_PUBLICATION_VOLUME", ACTIVITY_CHANNELS, _cap_untyped),
        ArmSpec("B1_CITATION_IMPACT", ATTENTION_CHANNELS, _cap_untyped),
        ArmSpec("B2_SEMANTIC_NOVELTY", SEMANTIC_CHANNELS, _cap_untyped),
        ArmSpec("B3_DISRUPTION_TURNOVER", NETWORK_CHANNELS, _cap_untyped),
        ArmSpec(B4_LITERAL_ARM, B4_LITERAL_CHANNELS, _cap_untyped),
        ArmSpec(B4X_ARM, CHANNELS, _cap_untyped),
        ArmSpec(B4X_FITTED_ARM, CHANNELS, _cap_fitted),
        ArmSpec(M_ARM, CHANNELS, _cap_typed),
    ]
    specs += [ArmSpec(n, c, _cap_untyped) for n, c in LADDER]
    for name, drop in ABLATION_GROUPS.items():
        specs.append(ArmSpec(name, tuple(c for c in CHANNELS if c not in drop), _cap_typed))
    specs += [
        ArmSpec("C_ALWAYS_RISE", CHANNELS, _cap_always_rise),
        ArmSpec("C_ALWAYS_FLAT", CHANNELS, _cap_always_flat),
        ArmSpec("C_RANDOM", CHANNELS, _cap_random),
    ]
    return tuple(specs)


def run_arm(spec: ArmSpec, w: FieldWindow, rng: random.Random) -> Verdict:
    """The activity half is not the contested question: any arm holding the
    activity channels reads them directly, so no arm is crippled on a half it
    plainly has the information for.  The contest is capability."""
    act_keys = tuple(k for k in ACTIVITY_CHANNELS if k in spec.channels)
    activity = _dir_of(w, act_keys) if act_keys else _dir_of(w, spec.channels)
    return Verdict(capability=spec.capability(w, spec.channels, rng), activity=activity)
