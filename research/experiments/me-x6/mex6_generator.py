"""ME-X6 generator: planted latent trajectories and their noisy channel readouts.

Fourteen strata.  Each plants a *known* joint verdict -- a capability direction
and an activity direction -- and then emits channels consistent with it.  Ten of
the strata are the protocol's hostile invariances (long section 7 I1-I10), one is
the short protocol's X6-I7, and three are the non-perturbed controls without
which an always-FLAT arm would score well.
"""

from __future__ import annotations

import hashlib
import random

from mex6_model import (
    ACTIVITY_CHANNELS,
    CHANNELS,
    FALL,
    FLAT,
    LATENT_COORDS,
    RISE,
    SCALES,
    FieldWindow,
    Instance,
    Period,
)

FIT_LEN = 8
HORIZON = 4
MAX_ATTEMPTS = 64

# Per-instance structural variation.  There is still no additive jitter -- every
# direction remains a strict integer comparison with no deadband -- but three
# structural quantities are drawn per instance so that two instances of the same
# cell are genuinely different windows rather than copies:
#
#   * a per-channel baseline level.  Each half of a window has the same number of
#     periods, so a baseline contributes equally to both and cannot move a
#     direction;
#   * a per-instance step magnitude.  All channels share it, so every relative
#     weight in the typed score (notably I4's retraction dominance) is preserved
#     exactly;
#   * the period at which the step lands, inside the second half of the fit
#     window, so the size of the observed difference varies while its sign
#     cannot.
#
# The two scales draw from different ranges, so a result that only holds at one
# unit of analysis can actually fail G6.  Without this the scale field never
# reached the window and cross-scale transfer would have been a contrast that
# could not exist.
SCALE_PARAMS: dict[str, dict[str, tuple[int, int]]] = {
    "SCALE_SUBFIELD": {"base": (120, 240), "step": (8, 15)},
    "SCALE_PROBLEM_FAMILY": {"base": (20, 60), "step": (3, 7)},
}

# ---- strata: (capability direction, activity direction) ------------------------
# Registered before any outcome exists.  The capability half is what the study is
# about; the activity half is included so that a volume-reading surface is
# *right about something*, and a joint exact match is not a one-bit test.
STRATA: dict[str, tuple[str, str]] = {
    # controls -- not perturbations
    "NO_CHANGE": (FLAT, FLAT),
    "GENUINE_CAPABILITY_GAIN": (RISE, RISE),
    "GENUINE_CAPABILITY_LOSS": (FALL, FALL),
    # protocol section 7 hostile invariances
    "I1_DUPLICATES": (FLAT, RISE),
    "I2_PARAPHRASE": (FLAT, RISE),
    "I3_MASS_LOW_INFORMATION": (FLAT, RISE),
    "I4_RETRACTED_WORK": (FALL, RISE),
    "I5_CITATION_RING": (FLAT, FLAT),
    "I6_VENUE_MIGRATION": (FLAT, FLAT),
    "I7_FIELD_SIZE_SCALING": (FLAT, RISE),
    "I8_FASHION_CONCENTRATION": (FLAT, RISE),
    "I9_DELAYED_VALIDATION": (RISE, FLAT),
    "I10_INDEPENDENT_REDISCOVERY": (RISE, RISE),
    # short protocol X6-I7
    "X6I7_ONE_BREAKTHROUGH": (RISE, FLAT),
}
# Which validated channel CARRIES the capability direction, per stratum.
# Declared before any outcome exists.  This is what makes the omission gate
# non-vacuous: if every validated channel moved together on every stratum, no
# single ablation could ever be load-bearing and G3 would be a gate that cannot
# fail.  Each capability-moving stratum is given a distinct carrier so the
# mechanism is separable.
DEFAULT_CARRIERS = ("formal_artifacts", "replications_passed", "downstream_reuse")
CAPABILITY_CARRIERS: dict[str, tuple[str, ...]] = {
    "NO_CHANGE": DEFAULT_CARRIERS,
    "GENUINE_CAPABILITY_GAIN": DEFAULT_CARRIERS,
    "GENUINE_CAPABILITY_LOSS": DEFAULT_CARRIERS,
    "I1_DUPLICATES": DEFAULT_CARRIERS,
    "I2_PARAPHRASE": DEFAULT_CARRIERS,
    "I3_MASS_LOW_INFORMATION": DEFAULT_CARRIERS,
    # the work looks good on every ordinary validated channel; only the
    # retraction channel reveals that it was later invalidated (protocol I4:
    # the model must support negative revision)
    "I4_RETRACTED_WORK": (),
    "I5_CITATION_RING": DEFAULT_CARRIERS,
    "I6_VENUE_MIGRATION": DEFAULT_CARRIERS,
    "I7_FIELD_SIZE_SCALING": DEFAULT_CARRIERS,
    "I8_FASHION_CONCENTRATION": DEFAULT_CARRIERS,
    # the validation arrives late and only through replication
    "I9_DELAYED_VALIDATION": ("replications_passed",),
    # the gain is carried solely by genuinely independent rederivation
    "I10_INDEPENDENT_REDISCOVERY": ("independent_rederivations",),
    # one deep result: the gain shows up only as a formal artifact
    "X6I7_ONE_BREAKTHROUGH": ("formal_artifacts",),
}

PERTURBATION_STRATA = tuple(s for s in STRATA if s.startswith(("I", "X6I")))
CONTROL_STRATA = tuple(s for s in STRATA if not s.startswith(("I", "X6I")))
CELLS = tuple((s, sc) for s in STRATA for sc in SCALES)


def sha256_text(t: str) -> str:
    return hashlib.sha256(t.encode()).hexdigest()


def instance_seed(split_seed: str, stratum: str, scale: str, index: int) -> int:
    return int(sha256_text(f"{split_seed}|{stratum}|{scale}|{index}")[:12], 16)


def _delta(direction: str, amount: int) -> int:
    return amount if direction == RISE else (-amount if direction == FALL else 0)


def _levels(direction: str, n: int, base: int, amount: int, onset: int) -> list[int]:
    """A step integer series whose compared halves move in `direction`.

    There is deliberately **no additive jitter**.  ME-X6's noise is structural,
    not stochastic: a channel is a noisy readout of the latent state because
    perturbations *decouple* it (duplicates raise volume without capability, a
    citation ring raises attention without either), and those perturbations are
    modelled explicitly as strata.  Sampling noise on top would force a deadband,
    which would reintroduce exactly the threshold constant the gates avoid.

    `onset` is the period at which the step lands.  It sits inside the second
    half of the fit window, so both the arms' comparison (fit halves) and the
    oracle's (opening baseline against the holdout) see the full step, and only
    the magnitude of the difference varies.
    """
    per = _delta(direction, amount)
    return [max(0, base + (per if i >= onset else 0)) for i in range(n)]


def build_window(rng: random.Random, stratum: str, scale: str, window_id: str) -> FieldWindow:
    cap_dir, act_dir = STRATA[stratum]
    n = FIT_LEN + HORIZON
    par = SCALE_PARAMS[scale]
    step = rng.randrange(*par["step"])
    # the step lands inside the second half of the fit window
    onset = rng.randrange(FIT_LEN // 2, FIT_LEN)
    bases = {c: rng.randrange(*par["base"]) for c in CHANNELS}
    lat_bases = {c: rng.randrange(*par["base"]) for c in LATENT_COORDS}
    ch: dict[str, list[int]] = {}

    def _apply(store, name, direction, amount, base_map):
        store[name] = _levels(direction, n, base_map[name], amount, onset)

    STEP = step

    # --- the two registered drivers -------------------------------------------
    # activity channels follow the activity direction; validated channels follow
    # the capability direction.  Everything else is stratum-specific decoration.
    for name in ACTIVITY_CHANNELS:
        _apply(ch, name, act_dir, STEP, bases)
    carriers = CAPABILITY_CARRIERS[stratum]
    for name in ("formal_artifacts", "replications_passed", "downstream_reuse",
                 "independent_rederivations"):
        _apply(ch, name, cap_dir if name in carriers else FLAT, STEP, bases)
    # cost is inverted: capability rising means the same result gets cheaper.
    # It only moves when the ordinary validated channels do.
    _apply(ch, "solution_cost",
           {RISE: FALL, FALL: RISE, FLAT: FLAT}[cap_dir] if carriers == DEFAULT_CARRIERS else FLAT,
           STEP, bases)
    for name in ("citations", "semantic_novelty", "topic_spread", "disruption",
                 "concentration", "replications_failed", "corrections", "retractions"):
        _apply(ch, name, FLAT, 0, bases)

    # --- stratum-specific channel signatures -----------------------------------
    if stratum == "I1_DUPLICATES" or stratum == "I2_PARAPHRASE":
        # identical or restated content: volume and attention move, nothing
        # independent is rederived and no new validation appears
        _apply(ch, "citations", RISE, STEP, bases)
        if stratum == "I2_PARAPHRASE":
            _apply(ch, "semantic_novelty", RISE, STEP // 2, bases)
    elif stratum == "I3_MASS_LOW_INFORMATION":
        _apply(ch, "semantic_novelty", RISE, STEP, bases)
        _apply(ch, "topic_spread", RISE, STEP, bases)
    elif stratum == "I4_RETRACTED_WORK":
        # novel-looking work that is later invalidated.  Every ordinary validated
        # channel RISES -- the work looked good -- and only the retraction channel
        # carries the truth.  The retraction rise is large enough that the typed
        # score's negative revision flips the direction, so dropping the
        # correction/retraction group is load-bearing for exactly this stratum.
        _apply(ch, "citations", RISE, STEP, bases)
        _apply(ch, "semantic_novelty", RISE, STEP, bases)
        for name in DEFAULT_CARRIERS:
            _apply(ch, name, RISE, STEP, bases)
        _apply(ch, "retractions", RISE, STEP * 3, bases)
        _apply(ch, "corrections", RISE, STEP, bases)
    elif stratum == "I5_CITATION_RING":
        _apply(ch, "citations", RISE, STEP * 2, bases)
        _apply(ch, "concentration", RISE, STEP, bases)
    elif stratum == "I6_VENUE_MIGRATION":
        # the same work moves preprint -> journal: no new epistemic gain
        _apply(ch, "preprints", FALL, STEP, bases)
        _apply(ch, "journal_papers", RISE, STEP, bases)
        _apply(ch, "authors", FLAT, 0, bases)
    elif stratum == "I7_FIELD_SIZE_SCALING":
        _apply(ch, "authors", RISE, STEP * 2, bases)
    elif stratum == "I8_FASHION_CONCENTRATION":
        _apply(ch, "topic_spread", FALL, STEP, bases)
        _apply(ch, "concentration", RISE, STEP, bases)
        _apply(ch, "citations", RISE, STEP, bases)
    elif stratum == "I9_DELAYED_VALIDATION":
        # activity flat; the validation arrives inside the fit window and only
        # through replication (the carrier declared above)
        pass
    elif stratum == "I10_INDEPENDENT_REDISCOVERY":
        # looks duplicated in the activity channels, but the rederivations are
        # genuinely independent: duplicate detection must not erase this.  The
        # gain is carried solely by the rederivation channel (declared above).
        _apply(ch, "semantic_novelty", FLAT, 0, bases)
    elif stratum == "X6I7_ONE_BREAKTHROUGH":
        # one deep result rather than many incremental ones
        _apply(ch, "disruption", RISE, STEP, bases)

    # --- the latent trajectory (never shown to any arm) ------------------------
    lat: dict[str, list[int]] = {}
    lat["R"] = _levels(cap_dir, n, lat_bases["R"], STEP, onset)
    lat["V"] = _levels(cap_dir, n, lat_bases["V"], STEP, onset)
    lat["D"] = _levels(FALL if stratum == "I8_FASHION_CONCENTRATION" else FLAT,
                       n, lat_bases["D"], STEP, onset)
    lat["T"] = _levels(cap_dir, n, lat_bases["T"], max(1, STEP // 2), onset)
    lat["G"] = _levels(FLAT, n, lat_bases["G"], 0, onset)
    lat["U"] = _levels(FLAT, n, lat_bases["U"], 0, onset)
    lat["C"] = _levels({RISE: FALL, FALL: RISE, FLAT: FLAT}[cap_dir], n, lat_bases["C"], STEP, onset)
    lat["E"] = _levels(RISE if stratum == "I5_CITATION_RING" else FLAT,
                       n, lat_bases["E"], STEP, onset)

    periods = tuple(
        Period(
            index=i,
            latent={k: lat[k][i] for k in LATENT_COORDS},
            channels={k: ch[k][i] for k in CHANNELS},
        )
        for i in range(n)
    )
    return FieldWindow(window_id=window_id, scale=scale, fit_len=FIT_LEN,
                       horizon=HORIZON, periods=periods)


def generate_instance(prefix: str, split_seed: str, stratum: str, scale: str, index: int) -> Instance:
    from mex6_oracle import planter_agrees

    rng = random.Random(instance_seed(split_seed, stratum, scale, index))
    iid = f"{prefix}-{stratum}-{scale}-{index:04d}"
    for _ in range(MAX_ATTEMPTS):
        w = build_window(random.Random(rng.randrange(2**62)), stratum, scale,
                         window_id=f"fw-{sha256_text(iid)[:16]}")
        ok, why = planter_agrees(w, stratum)
        if ok:
            return Instance(window=w, stratum=stratum, scale=scale, instance_id=iid,
                            facts=(("planted_capability", STRATA[stratum][0]),
                                   ("planted_activity", STRATA[stratum][1])))
    raise RuntimeError(f"generator could not satisfy the planter check for {iid}: {why}")


def generate_split(prefix: str, split_seed: str, per_cell: int) -> list[Instance]:
    return [
        generate_instance(prefix, split_seed, stratum, scale, i)
        for stratum, scale in CELLS
        for i in range(per_cell)
    ]
