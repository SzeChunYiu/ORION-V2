"""ME-X6 — collective epistemics as a noisy measurement problem: frozen types.

Every quantity is an integer.  The study is an exact known-answer design: the
latent trajectory and the observable channels are planted, so the correct joint
verdict is computable by construction and no estimation is involved anywhere in
the oracle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

# ---- verdict vocabulary --------------------------------------------------------

RISE = "RISE"
FLAT = "FLAT"
FALL = "FALL"
DIRECTIONS = (RISE, FLAT, FALL)

# ---- scales (protocol section 3: more than one unit of analysis) ---------------

SCALE_SUBFIELD = "SCALE_SUBFIELD"
SCALE_PROBLEM_FAMILY = "SCALE_PROBLEM_FAMILY"
SCALES = (SCALE_SUBFIELD, SCALE_PROBLEM_FAMILY)

# ---- typed latent coordinates (protocol section 4) -----------------------------
# R validated reach, V verification/reproducibility depth, D epistemic diversity,
# T transport/reuse scope, G generative repertoire, U unresolved frontier,
# C solution cost, E dependence/concentration.
LATENT_COORDS = ("R", "V", "D", "T", "G", "U", "C", "E")

# The capability coordinates.  Declared here, before any outcome exists: the
# joint verdict's capability half is a function of R and V only.  D/T/G/U/C/E are
# reported and are moved by the perturbations, but they do not define capability.
CAPABILITY_COORDS = ("R", "V")

# ---- observable channels (protocol section 2 / the .json observable_channels) --

ACTIVITY_CHANNELS = ("preprints", "journal_papers", "authors")
ATTENTION_CHANNELS = ("citations",)
SEMANTIC_CHANNELS = ("semantic_novelty", "topic_spread")
NETWORK_CHANNELS = ("disruption", "concentration")
VALIDATION_CHANNELS = (
    "formal_artifacts",
    "replications_passed",
    "replications_failed",
    "corrections",
    "retractions",
    "downstream_reuse",
    "independent_rederivations",
    "solution_cost",
)
CHANNELS = (
    ACTIVITY_CHANNELS
    + ATTENTION_CHANNELS
    + SEMANTIC_CHANNELS
    + NETWORK_CHANNELS
    + VALIDATION_CHANNELS
)

# The protocol's literal B4 covariate set (section 6): output, citation,
# semantic, network, team and field size.  It does NOT include the validation /
# reproducibility / correction channels -- those are what M adds.  This is why
# the design registers a second, information-matched comparator (design 1.1).
B4_LITERAL_CHANNELS = ACTIVITY_CHANNELS + ATTENTION_CHANNELS + SEMANTIC_CHANNELS + NETWORK_CHANNELS


@dataclass(frozen=True, slots=True)
class Period:
    """One time step of one field window: the latent state and what was observed."""

    index: int
    latent: Mapping[str, int]
    channels: Mapping[str, int]


@dataclass(frozen=True, slots=True)
class FieldWindow:
    """A field observed over a fit window and a holdout window.

    `periods` covers the whole trajectory.  An arm sees the channels of the first
    `fit_len` periods only; the verdict concerns the holdout periods that follow.
    No arm ever sees a latent coordinate or a holdout period.
    """

    window_id: str
    scale: str
    fit_len: int
    horizon: int
    periods: tuple[Period, ...]

    @property
    def fit_periods(self) -> tuple[Period, ...]:
        return self.periods[: self.fit_len]

    @property
    def holdout_periods(self) -> tuple[Period, ...]:
        return self.periods[self.fit_len : self.fit_len + self.horizon]


@dataclass(frozen=True, slots=True)
class Verdict:
    """The joint typed verdict.

    Two directions, decided together.  Reporting them jointly is the whole point:
    a surface that reads volume gets `activity` right and `capability` wrong on
    every perturbation stratum, which is the protocol's
    PAPER_COUNT = ACTIVITY_NOT_KNOWLEDGE turned into a measurement.
    """

    capability: str
    activity: str

    def as_tuple(self) -> tuple[str, str]:
        return (self.capability, self.activity)

    def as_dict(self) -> dict[str, str]:
        return {"capability": self.capability, "activity": self.activity}


@dataclass(frozen=True, slots=True)
class Instance:
    window: FieldWindow
    stratum: str
    scale: str
    instance_id: str
    facts: tuple[tuple[str, str], ...] = field(default=())
