import pytest

from orion_v2.closure import CloseoutInputs, CloseoutStatus, assess_closeout


def _ready_inputs(**overrides: object) -> CloseoutInputs:
    values = dict(
        v1_handoff_bound=True,
        v1_parity_complete=True,
        paper_contraction_frozen=True,
        minimal_kernel_frozen=True,
        parent_baselines_complete=True,
        protected_evaluation_complete=True,
        no_material_change_passes=2,
        all_declared_routes_dispositioned=True,
        open_critical_failures=0,
        external_authority_complete=True,
    )
    values.update(overrides)
    return CloseoutInputs(**values)


def test_v1_parity_blocks_even_after_handoff() -> None:
    result = assess_closeout(_ready_inputs(v1_parity_complete=False))
    assert result.status is CloseoutStatus.BLOCKED_V1_PARITY


def test_paper_proliferation_is_a_closeout_blocker() -> None:
    result = assess_closeout(_ready_inputs(paper_contraction_frozen=False))
    assert result.status is CloseoutStatus.BLOCKED_PAPER_CONTRACTION


def test_one_flat_pass_is_not_saturation() -> None:
    result = assess_closeout(_ready_inputs(no_material_change_passes=1))
    assert result.status is CloseoutStatus.BLOCKED_SATURATION


def test_censored_or_unresolved_route_blocks_saturation() -> None:
    result = assess_closeout(
        _ready_inputs(all_declared_routes_dispositioned=False, no_material_change_passes=3)
    )
    assert result.status is CloseoutStatus.BLOCKED_SATURATION


def test_critical_failure_cannot_be_compensated_by_other_green_gates() -> None:
    result = assess_closeout(_ready_inputs(open_critical_failures=1))
    assert result.status is CloseoutStatus.BLOCKED_FAILURES


def test_local_convergence_does_not_mint_external_authority() -> None:
    result = assess_closeout(_ready_inputs(external_authority_complete=False))
    assert result.status is CloseoutStatus.EXTERNAL_AUTHORITY_REQUIRED
    assert result.locally_ready is True
    assert result.grants_scientific_truth is False
    assert result.grants_novelty is False
    assert result.grants_publication_authority is False


def test_ready_terminal_still_grants_no_scientific_authority() -> None:
    result = assess_closeout(_ready_inputs())
    assert result.status is CloseoutStatus.READY_FOR_V2_CLOSEOUT
    assert result.grants_scientific_truth is False
    assert result.grants_novelty is False
    assert result.grants_publication_authority is False


def test_invalid_negative_counts_fail_closed() -> None:
    with pytest.raises(ValueError):
        _ready_inputs(open_critical_failures=-1)
