"""ME-X2 V3 arm registry (frozen with design V3).  Comparators are V1's frozen classes; M2 is V2's
frozen revival arm; the V3 additions are the threshold grid (calibration) and the frozen τ* arm."""
from __future__ import annotations

import sys
from pathlib import Path

V1_DIR = Path(__file__).resolve().parent.parent / "me-x2"
V2_DIR = Path(__file__).resolve().parent.parent / "me-x2-v2"
for _p in (str(Path(__file__).resolve().parent), str(V2_DIR), str(V1_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from mex2_arms import (  # noqa: E402
    ArmSpec, B3ModelBasedDiagnosisVoI, B5R1, B5R2, B5R3, B5R4, CNeverIntervene, CRandomPolicy, Federation,
    MLocusMinimumEscalation, Policy, make_policy,
)
from mex2v2_levers import M2LookaheadBestHypothesis  # noqa: E402
from mex2v3_levers import TAU_GRID, THRESHOLD_CLASSES, arm_name  # noqa: E402

M_V1_ARM = MLocusMinimumEscalation.name
M2_ARM = M2LookaheadBestHypothesis.name
B5_ARM = Federation.name
LADDER = [B5R1.name, B5R2.name, B5R3.name, B5R4.name, B5_ARM]
EXTRA_SEARCH_ARM = "B3_EQUAL_EXTRA_SEARCH_1_5X"


def arm_specs(taus: tuple[float, ...] = TAU_GRID) -> list[ArmSpec]:
    specs = [
        ArmSpec(B3ModelBasedDiagnosisVoI.name, B3ModelBasedDiagnosisVoI), ArmSpec(EXTRA_SEARCH_ARM, B3ModelBasedDiagnosisVoI, 1.5, "control"),
        ArmSpec(B5R1.name, B5R1, group="ladder"), ArmSpec(B5R2.name, B5R2, group="ladder"), ArmSpec(B5R3.name, B5R3, group="ladder"),
        ArmSpec(B5R4.name, B5R4, group="ladder"), ArmSpec(Federation.name, Federation, group="ladder"),
        ArmSpec(M_V1_ARM, MLocusMinimumEscalation, group="M"), ArmSpec(M2_ARM, M2LookaheadBestHypothesis, group="M2"),
    ]
    for tau in taus:
        specs.append(ArmSpec(arm_name(tau), THRESHOLD_CLASSES[tau], group="M3"))
    specs += [ArmSpec(CRandomPolicy.name, CRandomPolicy, group="control"), ArmSpec(CNeverIntervene.name, CNeverIntervene, group="control")]
    return specs


__all__ = ["ArmSpec", "Policy", "arm_specs", "make_policy", "M_V1_ARM", "M2_ARM", "B5_ARM", "LADDER", "EXTRA_SEARCH_ARM", "arm_name", "TAU_GRID"]
