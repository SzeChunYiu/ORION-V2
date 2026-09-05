"""ME-X2 V3 lever: the identification threshold (frozen with design V3).

V1 and V2 both lost decisions to `CANNOT_IDENTIFY` declared on decidable episodes: V1's 43 (of 62
discordant against B5) were all of that kind; V2's levers recovered 26 of them and left 18 missed
escalations, where B5 — an exact finite-horizon planner — commits.  Attributed stage: the
identification rule.  When discriminators are exhausted and several hypotheses stay live, M2 abstains
unless one intervention resolves EVERY live hypothesis (the "common fix").  M3 adds a registered
threshold τ: it commits to the minimum-responsible live hypothesis c* whenever c*'s warranted fix
resolves at least a fraction τ of the live set (and is affordable and untried), and it declares
`CANNOT_IDENTIFY` otherwise.  τ = 1.0 is M2 exactly (identity, asserted); τ = 0.0 always commits
(the ablation that shows what the threshold prevents).  τ* is calibrated on a PUBLIC split and frozen
in the design JSON before the protected split exists.

Everything else — lookahead, best-hypothesis reachability, the H-EXT-3 receipts, the Jump semantics
for level ≥ 2 — is V2's code, imported read-only.
"""
from __future__ import annotations

import sys
from pathlib import Path

V1_DIR = Path(__file__).resolve().parent.parent / "me-x2"
V2_DIR = Path(__file__).resolve().parent.parent / "me-x2-v2"
for _p in (str(V2_DIR), str(V1_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from mex2_arms import DECLARE_KIND  # noqa: E402
from mex2_oracle import ArmView  # noqa: E402
from mex2v2_levers import M2LookaheadBestHypothesis  # noqa: E402

TAU_GRID: tuple[float, ...] = (0.0, 0.5, 0.6, 0.75, 0.9, 1.0)


def arm_name(tau: float) -> str:
    return f"M3_THRESHOLD_TAU_{int(round(tau * 100)):03d}"


class M3IdentificationThreshold(M2LookaheadBestHypothesis):
    """M2 + identification threshold τ (class attribute; subclassed per grid point)."""

    name = "M3_IDENTIFICATION_THRESHOLD"
    tau: float = 1.0

    def __init__(self, seed: str) -> None:
        super().__init__(seed)
        self.threshold_receipts: list[dict] = []

    def _commit_candidate(self, view: ArmView, live: tuple[str, ...]):
        """(c*, fix, share) for the minimum-responsible live hypothesis whose fix is affordable and
        untried; None when no live hypothesis has such a fix."""
        best = None
        for c in live:
            fix = self.fix_of(view, c)
            if fix is None or fix.intervention_id in self.applied(view) or fix.cost > view.budget_left:
                continue
            share = sum(1 for d in live if d in fix.resolves) / len(live)
            key = (self._responsible_rank(view, c), c)
            if best is None or key < best[0]:
                best = (key, c, fix, share)
        return None if best is None else best[1:]

    def cannot_identify(self, view: ArmView, live: tuple[str, ...]):
        if len(live) >= 2 and not self.never_escalate:
            cand = self._commit_candidate(view, live)
            if cand is not None:
                c_star, fix, share = cand
                committed = share >= self.tau
                self.threshold_receipts.append({"step": len(view.steps), "live": list(live), "candidate": c_star, "fix": fix.intervention_id,
                                                "fix_level": fix.level, "share": share, "tau": self.tau, "committed": committed})
                if committed:
                    declared = tuple(d for d in live if d in fix.resolves)
                    alternatives = [i for i in view.inst.interventions if all(d in i.resolves for d in declared)]
                    act = self._apply(view, live, fix, declared, alternatives)
                    if act is not None and act.kind in ("INTERVENE", "PROBE"):
                        return act
                    self.threshold_receipts[-1]["committed"] = False
                    self.threshold_receipts[-1]["fallback"] = "jump_semantics_declined_or_no_candidate"
        return super().cannot_identify(view, live)


def make_threshold_class(tau: float):
    return type(f"M3Tau{int(round(tau * 100)):03d}", (M3IdentificationThreshold,), {"name": arm_name(tau), "tau": tau})


THRESHOLD_CLASSES = {tau: make_threshold_class(tau) for tau in TAU_GRID}
M3_IDENTITY_ARM = arm_name(1.0)      # ≡ M2 (asserted in the selftest)
M3_ALWAYS_COMMIT_ARM = arm_name(0.0)  # ablation

__all__ = ["M3IdentificationThreshold", "THRESHOLD_CLASSES", "TAU_GRID", "arm_name", "make_threshold_class", "M3_IDENTITY_ARM", "M3_ALWAYS_COMMIT_ARM"]
