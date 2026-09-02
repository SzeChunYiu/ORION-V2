"""ME-X2 V2 arm registry (frozen with design V2).

Every parent, the whole H-EXT-3 ladder, both controls and the V1 rendering of M
are the **frozen V1 classes**, imported from ``research/experiments/me-x2`` and
not re-implemented here: the comparator side of the study is byte-identical to
V1 (asserted by ``mex2v2_provenance``).  The V2 additions are the revival arm
``M2`` (both levers), its two single-lever arms and its ablations.

Arm groups
  baseline / ladder / federation-variant / control : frozen V1 comparators
  M                                                 : ``M`` as V1 froze it (reference for the lever delta)
  M2 / lever                                        : the revival arm and its single-lever decompositions
  ablation                                          : protocol V2's required ablations, applied to M2
"""
from __future__ import annotations

import sys
from pathlib import Path

V1_DIR = Path(__file__).resolve().parent.parent / "me-x2"
if str(V1_DIR) not in sys.path:
    sys.path.insert(0, str(V1_DIR))

from mex2_arms import (  # noqa: E402
    ArmSpec,
    B0RetrySearch,
    B1UncertaintyAbstention,
    B2FailureTaxonomy,
    B3ModelBasedDiagnosisVoI,
    B4MDAModelExpansion,
    B5NoAbstention,
    B5R1,
    B5R2,
    B5R3,
    B5R4,
    CNeverIntervene,
    CRandomPolicy,
    Federation,
    MLocusMinimumEscalation,
    Policy,
    make_policy,
)

from mex2v2_levers import (  # noqa: E402
    M2BestHypothesisOnly,
    M2AlwaysEscalateWhenStuck,
    M2LocusLabelsShuffled,
    M2LookaheadBestHypothesis,
    M2LookaheadOnly,
    M2MinusDiagnosticEvaluatorGate,
    M2MinusLocusDiagnosis,
    M2MinusLowerLevelDisposition,
    M2MinusProspectiveDiscriminator,
    M2NeverEscalate,
)

M_V1_ARM = MLocusMinimumEscalation.name          # "M_ME_LOCUS_PLUS_MINIMUM_ESCALATION" — V1's rendering
B5_ARM = Federation.name
LADDER = [B5R1.name, B5R2.name, B5R3.name, B5R4.name, B5_ARM]
EXTRA_SEARCH_ARM = "B3_EQUAL_EXTRA_SEARCH_1_5X"


def arm_specs() -> list[ArmSpec]:
    return [
        # ---- frozen V1 comparators (classes imported, never re-implemented) ----
        ArmSpec(B0RetrySearch.name, B0RetrySearch), ArmSpec(B1UncertaintyAbstention.name, B1UncertaintyAbstention), ArmSpec(B2FailureTaxonomy.name, B2FailureTaxonomy),
        ArmSpec(B3ModelBasedDiagnosisVoI.name, B3ModelBasedDiagnosisVoI), ArmSpec(EXTRA_SEARCH_ARM, B3ModelBasedDiagnosisVoI, 1.5, "control"), ArmSpec(B4MDAModelExpansion.name, B4MDAModelExpansion),
        ArmSpec(B5R1.name, B5R1, group="ladder"), ArmSpec(B5R2.name, B5R2, group="ladder"), ArmSpec(B5R3.name, B5R3, group="ladder"), ArmSpec(B5R4.name, B5R4, group="ladder"), ArmSpec(Federation.name, Federation, group="ladder"),
        ArmSpec(B5NoAbstention.name, B5NoAbstention, group="federation-variant"),
        # ---- V1's rendering of M, unchanged: the reference for the lever delta ----
        ArmSpec(M_V1_ARM, MLocusMinimumEscalation, group="M"),
        # ---- V2 revival arm and its single-lever decompositions ----
        ArmSpec(M2LookaheadBestHypothesis.name, M2LookaheadBestHypothesis, group="M2"),
        ArmSpec(M2LookaheadOnly.name, M2LookaheadOnly, group="lever"), ArmSpec(M2BestHypothesisOnly.name, M2BestHypothesisOnly, group="lever"),
        # ---- protocol V2 required ablations, applied to the arm under test ----
        ArmSpec(M2MinusLocusDiagnosis.name, M2MinusLocusDiagnosis, group="ablation"), ArmSpec(M2LocusLabelsShuffled.name, M2LocusLabelsShuffled, group="ablation"),
        ArmSpec(M2MinusDiagnosticEvaluatorGate.name, M2MinusDiagnosticEvaluatorGate, group="ablation"), ArmSpec(M2MinusLowerLevelDisposition.name, M2MinusLowerLevelDisposition, group="ablation"),
        ArmSpec(M2MinusProspectiveDiscriminator.name, M2MinusProspectiveDiscriminator, group="ablation"),
        ArmSpec(M2AlwaysEscalateWhenStuck.name, M2AlwaysEscalateWhenStuck, group="ablation"), ArmSpec(M2NeverEscalate.name, M2NeverEscalate, group="ablation"),
        # ---- controls ----
        ArmSpec(CRandomPolicy.name, CRandomPolicy, group="control"), ArmSpec(CNeverIntervene.name, CNeverIntervene, group="control"),
    ]


__all__ = ["ArmSpec", "Policy", "arm_specs", "make_policy", "M_V1_ARM", "B5_ARM", "LADDER", "EXTRA_SEARCH_ARM"]
