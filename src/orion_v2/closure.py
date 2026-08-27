from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CloseoutStatus(str, Enum):
    BLOCKED_V1_HANDOFF = "BLOCKED_V1_HANDOFF"
    BLOCKED_V1_PARITY = "BLOCKED_V1_PARITY"
    BLOCKED_PAPER_CONTRACTION = "BLOCKED_PAPER_CONTRACTION"
    BLOCKED_KERNEL_FREEZE = "BLOCKED_KERNEL_FREEZE"
    BLOCKED_PARENT_BASELINES = "BLOCKED_PARENT_BASELINES"
    BLOCKED_PROTECTED_EVALUATION = "BLOCKED_PROTECTED_EVALUATION"
    BLOCKED_SATURATION = "BLOCKED_SATURATION"
    BLOCKED_FAILURES = "BLOCKED_FAILURES"
    EXTERNAL_AUTHORITY_REQUIRED = "EXTERNAL_AUTHORITY_REQUIRED"
    READY_FOR_V2_CLOSEOUT = "READY_FOR_V2_CLOSEOUT"


@dataclass(frozen=True)
class CloseoutInputs:
    v1_handoff_bound: bool
    v1_parity_complete: bool
    paper_contraction_frozen: bool
    minimal_kernel_frozen: bool
    parent_baselines_complete: bool
    protected_evaluation_complete: bool
    no_material_change_passes: int
    all_declared_routes_dispositioned: bool
    open_critical_failures: int
    external_authority_complete: bool

    def __post_init__(self) -> None:
        if self.no_material_change_passes < 0:
            raise ValueError("no_material_change_passes cannot be negative")
        if self.open_critical_failures < 0:
            raise ValueError("open_critical_failures cannot be negative")


@dataclass(frozen=True)
class CloseoutAssessment:
    status: CloseoutStatus
    blockers: tuple[str, ...]
    grants_scientific_truth: bool = False
    grants_novelty: bool = False
    grants_publication_authority: bool = False

    @property
    def locally_ready(self) -> bool:
        return self.status in {
            CloseoutStatus.EXTERNAL_AUTHORITY_REQUIRED,
            CloseoutStatus.READY_FOR_V2_CLOSEOUT,
        }


def assess_closeout(inputs: CloseoutInputs) -> CloseoutAssessment:
    """Return the first fail-closed convergence blocker.

    The ordering encodes dependency, not research priority. Contraction and
    kernel work may proceed while later protected gates remain open.
    """

    gates: tuple[tuple[bool, CloseoutStatus, str], ...] = (
        (
            inputs.v1_handoff_bound,
            CloseoutStatus.BLOCKED_V1_HANDOFF,
            "exact non-retroactive V1 handoff is not bound",
        ),
        (
            inputs.v1_parity_complete,
            CloseoutStatus.BLOCKED_V1_PARITY,
            "frozen V1 capability parity/non-regression is incomplete",
        ),
        (
            inputs.paper_contraction_frozen,
            CloseoutStatus.BLOCKED_PAPER_CONTRACTION,
            "paper candidates have not all reached merge/keep/drop dispositions",
        ),
        (
            inputs.minimal_kernel_frozen,
            CloseoutStatus.BLOCKED_KERNEL_FREEZE,
            "minimal kernel/API has not been reduced and frozen",
        ),
        (
            inputs.parent_baselines_complete,
            CloseoutStatus.BLOCKED_PARENT_BASELINES,
            "strongest parent-composed baselines are incomplete",
        ),
        (
            inputs.protected_evaluation_complete,
            CloseoutStatus.BLOCKED_PROTECTED_EVALUATION,
            "prospectively frozen protected evaluation is incomplete",
        ),
        (
            inputs.all_declared_routes_dispositioned
            and inputs.no_material_change_passes >= 2,
            CloseoutStatus.BLOCKED_SATURATION,
            "two complete post-contraction no-material-change passes are not established",
        ),
        (
            inputs.open_critical_failures == 0,
            CloseoutStatus.BLOCKED_FAILURES,
            "critical correctness/integrity/authority failures remain open",
        ),
    )

    for passed, status, reason in gates:
        if not passed:
            return CloseoutAssessment(status=status, blockers=(reason,))

    if not inputs.external_authority_complete:
        return CloseoutAssessment(
            status=CloseoutStatus.EXTERNAL_AUTHORITY_REQUIRED,
            blockers=(
                "local convergence is complete but external scientific/publication authority is unresolved",
            ),
        )

    return CloseoutAssessment(status=CloseoutStatus.READY_FOR_V2_CLOSEOUT, blockers=())
