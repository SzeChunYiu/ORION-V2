"""ME-X6 exact oracle and generator-validity check.

The oracle reads the *planted latent trajectory* over the holdout window.  No arm
ever sees a latent coordinate or a holdout period, so the oracle is not
reachable from any arm's surface.
"""

from __future__ import annotations

from typing import Iterable, Sequence

from mex6_model import (
    ACTIVITY_CHANNELS,
    CAPABILITY_COORDS,
    FALL,
    FLAT,
    RISE,
    FieldWindow,
    Period,
    Verdict,
)

# Every series is an exact integer step function (the generator plants no
# additive jitter), so a direction is a strict integer comparison and there is no
# threshold to tune.  A deadband would be a free parameter; there is none.


def _sum(periods: Sequence[Period], keys: Iterable[str], latent: bool) -> int:
    ks = tuple(keys)
    src = (lambda p: p.latent) if latent else (lambda p: p.channels)
    return sum(src(p)[k] for p in periods for k in ks)


def _direction(before: int, after: int) -> str:
    if after > before:
        return RISE
    if after < before:
        return FALL
    return FLAT


def oracle(w: FieldWindow) -> Verdict:
    """The true joint verdict.

    Capability: the direction of the capability coordinates (R, V) from the
    opening baseline of the fit window into the holdout window.
    Activity: the same comparison on the activity channels.

    Both use the first `horizon` periods of the fit window as the baseline, so
    the two halves being compared are the same length.
    """
    base = w.periods[: w.horizon]
    hold = w.holdout_periods
    cap = _direction(_sum(base, CAPABILITY_COORDS, True), _sum(hold, CAPABILITY_COORDS, True))
    act = _direction(_sum(base, ACTIVITY_CHANNELS, False), _sum(hold, ACTIVITY_CHANNELS, False))
    return Verdict(capability=cap, activity=act)


# ---- generator validity -------------------------------------------------------
# ME-X7's protected run failed because a generator-validity invariant was stated
# as a COUNT ("exactly one censored check") that was false for a mechanism which
# legitimately affected two.  The offending instances were then re-drawn away and
# the gate went green by deletion.  That lesson is built in here from the start:
# the check compares the recomputed effect against a DECLARED per-stratum
# expected effect, never against a count.


def expected_effect(stratum: str) -> tuple[str, str]:
    from mex6_generator import STRATA

    return STRATA[stratum]


def planter_agrees(w: FieldWindow, stratum: str) -> tuple[bool, str]:
    """Independent full-structure recomputation of what the planter claims.

    The oracle verdict recomputed from the planted trajectory must equal the
    stratum's declared (capability, activity) effect exactly -- both halves.  A
    stratum that fails to plant, or plants the wrong direction, cannot enter a
    split.
    """
    want_cap, want_act = expected_effect(stratum)
    got = oracle(w)
    if got.capability != want_cap:
        return False, f"{stratum}: capability {got.capability} != declared {want_cap}"
    if got.activity != want_act:
        return False, f"{stratum}: activity {got.activity} != declared {want_act}"
    return True, ""


def decidable_from_fit_window(w: FieldWindow) -> bool:
    """The registered generative assumption, made checkable.

    The study is only a known-answer design because the holdout direction is
    determined by the fit window: the planted step lands inside the fit window
    and continues.  This asserts that property instance by instance rather than
    leaving it as prose -- the fit window's own second-half movement in the
    capability coordinates must already carry the holdout's direction.
    """
    h = w.fit_len // 2
    fit_before = _sum(w.fit_periods[:h], CAPABILITY_COORDS, True)
    fit_after = _sum(w.fit_periods[h:], CAPABILITY_COORDS, True)
    return _direction(fit_before, fit_after) == oracle(w).capability
