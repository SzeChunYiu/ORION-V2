from orion_v2.correspondence import (
    CorrespondenceLink,
    CorrespondenceStatus,
    assess_correspondence_chain,
)


def _link(
    link_id: str,
    source: str,
    target: str,
    uncertainty: float = 0.0,
    **kwargs: object,
) -> CorrespondenceLink:
    return CorrespondenceLink(
        link_id=link_id,
        source_epoch=source,
        target_epoch=target,
        mapping_ids=(f"map:{link_id}",),
        anchor_ids=(f"anchor:{link_id}",),
        preserved_invariant_ids=("meaning", "decision"),
        uncertainty_upper_bound=uncertainty,
        valid_context_ids=("paper-comparison",),
        **kwargs,
    )


def test_multi_generation_uncertainty_accumulates() -> None:
    result = assess_correspondence_chain(
        (
            _link("a", "v1", "v2", 0.1),
            _link("b", "v2", "v3", 0.2),
        ),
        context_id="paper-comparison",
        required_invariant_ids=("meaning", "decision"),
        tolerance=0.25,
    )
    assert result.status is CorrespondenceStatus.PARTIALLY_COMPARABLE
    assert abs(result.accumulated_uncertainty_upper_bound - 0.3) < 1e-9


def test_identity_without_anchor_or_mapping_is_cannot_check() -> None:
    link = CorrespondenceLink(
        "same-id",
        "v1",
        "v2",
        (),
        (),
        ("meaning",),
        valid_context_ids=("paper-comparison",),
    )
    result = assess_correspondence_chain(
        (link,),
        context_id="paper-comparison",
        required_invariant_ids=("meaning",),
        tolerance=0,
    )
    assert result.status is CorrespondenceStatus.CANNOT_CHECK


def test_required_invariant_violation_is_noncomparable() -> None:
    link = _link("bad", "v1", "v2", violated_invariant_ids=("meaning",))
    result = assess_correspondence_chain(
        (link,),
        context_id="paper-comparison",
        required_invariant_ids=("meaning",),
        tolerance=1,
    )
    assert result.status is CorrespondenceStatus.NONCOMPARABLE
