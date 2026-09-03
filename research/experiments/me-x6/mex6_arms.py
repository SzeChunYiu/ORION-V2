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
    capability: Callable[[FieldWindow, "ArmSpec", random.Random], str]


def _cap_untyped(w: FieldWindow, spec: "ArmSpec", rng: random.Random) -> str:
    """The science-of-science combination: one equal-weight aggregate, read for
    its trend.  Kept as B4X_INFORMATION_MATCHED_UNTYPED so the fitted parent has
    an unfitted sibling to be compared against, and as the literal B4."""
    return _dir_of(w, spec.channels)


def _cap_typed(w: FieldWindow, spec: "ArmSpec", rng: random.Random) -> str:
    """M: the same channels, read as a typed state with signed roles."""
    keys = tuple(k for k in spec.channels if k in TYPED_SIGNS)
    if not keys:
        return FLAT
    return _dir_of(w, keys, TYPED_SIGNS)


def _cap_always_rise(w, spec, rng): return RISE
def _cap_always_flat(w, spec, rng): return FLAT
def _cap_random(w, spec, rng): return rng.choice((RISE, FLAT, FALL))


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

# ---- the strongest untyped parent IN THE UNIT-SIGN CLASS -----------------------
# This header used to call B4X_FITTED the strongest FAITHFUL untyped parent.
# Neither word survives the comparator-provenance receipt.
#
# There is nothing for it to be faithful TO.  The generator emits per-period
# integer channel counts and no bibliographic objects, so no published
# science-of-science estimator is natively computable here, and no
# parent-fidelity receipt of the ME-X1 kind is possible.  B4X_FITTED is
# CONSTRUCTED FOR THIS STUDY, not a published-method parent.
#
# And it is strongest only within its own class: one weight per channel in
# {-1, 0, +1}, learned by univariate marginal screening.  fit_signs below scores
# each channel INDEPENDENTLY and then sums with UNIT weights -- it never fits a
# combination.  M's own rule is an untyped weighted aggregate of these same
# channels with weights in {-2, -1, 0, +1}, so M lies OUTSIDE this class, and
# what the study shows is that this comparator DOES NOT RECOVER the conjunction
# -- not that no untyped aggregate CAN represent it.  See
# ME_X6_COMPARATOR_PROVENANCE_AND_NON_FIDELITY_RECEIPT_V1.md sections 2-5.
#
# An equal-weight aggregate is weaker still, so fitting the signs genuinely
# strengthens the comparator, and is why B4X_FITTED rather than the equal-weight
# B4X is what G1 tests against.  Its per-channel signs are learned on the public
# DEVELOPMENT split and then FROZEN into the design JSON before the protected
# run, so it is information-matched with M, is allowed to discover the same sign
# structure M declares a priori, and cannot be tuned after any protected outcome.
# If it ties M, the registered terminal is PARENT_SUFFICIENT and X6 contracts to
# an interpretive framework -- the protocol's own contraction rule, and a
# legitimate publishable result, not a failure.
# arm name -> {channel: sign}.  Every fitted arm carries its own vector, so a
# ladder rung is the best untyped model available AT ITS OWN information level
# rather than an equal-weight sum.  That matters: with equal weights, adding a
# channel can make a rung strictly worse than the one below it -- L2's attention
# channel destroys I5_CITATION_RING, which L1 gets right -- and the ladder would
# then be measuring the arbitrariness of the weighting rather than the value of
# the information.  Fitting each rung removes that artefact and makes G4 a
# meaningful monotonicity test again.  L5 fitted is exactly the comparator.
FITTED_SIGNS: dict[str, dict[str, int]] = {}


def load_fitted_signs(signs: dict[str, dict[str, int]]) -> None:
    FITTED_SIGNS.clear()
    FITTED_SIGNS.update({k: dict(v) for k, v in signs.items()})


def fit_signs(instances, channels: tuple[str, ...] = CHANNELS) -> dict[str, int]:
    """Learn one sign per channel by agreement with the oracle capability
    direction on the split it is given.  Deterministic, no randomness, no
    hyperparameter: a channel scores +1 if its own fit-window direction matches
    the true capability direction more often than it opposes it."""
    from mex6_oracle import oracle

    score = {c: 0 for c in channels}
    for inst in instances:
        w = inst.window
        truth = oracle(w).capability
        if truth == FLAT:
            continue
        for c in channels:
            d = _dir_of(w, (c,))
            if d == FLAT:
                continue
            score[c] += 1 if d == truth else -1
    return {c: (1 if v > 0 else (-1 if v < 0 else 0)) for c, v in score.items()}


def _cap_fitted(w: FieldWindow, spec: "ArmSpec", rng: random.Random) -> str:
    signs = FITTED_SIGNS.get(spec.name)
    if signs is None:
        raise RuntimeError(f"{spec.name} used before its frozen signs were loaded")
    keys = tuple(c for c in spec.channels if signs.get(c, 0) != 0)
    if not keys:
        return FLAT
    return _dir_of(w, keys, signs)


def fit_all(instances) -> dict[str, dict[str, int]]:
    """Fit every fitted arm on the split it is given.  Called once on the public
    development split; the result is frozen into the design JSON."""
    out = {B4X_FITTED_ARM: fit_signs(instances, CHANNELS)}
    for name, chans in LADDER:
        out[name] = fit_signs(instances, chans)
    return out


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
    specs += [ArmSpec(n, c, _cap_fitted) for n, c in LADDER]
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
    return Verdict(capability=spec.capability(w, spec, rng), activity=activity)
