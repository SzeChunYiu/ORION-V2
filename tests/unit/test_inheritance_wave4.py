import pytest

from orion_v2.inheritance import (
    ComponentContribution,
    ComponentSupportFamily,
    ComponentValidityStatus,
    InheritanceRelation,
    InheritanceStatus,
    InheritedCommitment,
    ReticulateInheritanceSystem,
    assess_reticulate_inheritance,
    revalidate_inheritance,
)


def _manuscript_system() -> ReticulateInheritanceSystem:
    return ReticulateInheritanceSystem(
        "stemmatology",
        frozenset({"exemplar-a", "exemplar-b", "copy-c"}),
        {"copy-c": frozenset({"text", "orthography"})},
        (
            ComponentContribution(
                "exemplar-a", "copy-c", "text", InheritanceRelation.COPIES
            ),
            ComponentContribution(
                "exemplar-b", "copy-c", "text", InheritanceRelation.COPIES
            ),
            ComponentContribution(
                "exemplar-a", "copy-c", "orthography", InheritanceRelation.COPIES
            ),
        ),
        (
            ComponentSupportFamily(
                "text-from-a", "copy-c", "text", frozenset({"exemplar-a"})
            ),
            ComponentSupportFamily(
                "text-from-b", "copy-c", "text", frozenset({"exemplar-b"})
            ),
            ComponentSupportFamily(
                "orthography-from-a",
                "copy-c",
                "orthography",
                frozenset({"exemplar-a"}),
            ),
        ),
        (
            InheritedCommitment("content-reading", "copy-c", frozenset({"text"})),
            InheritedCommitment(
                "scribal-style", "copy-c", frozenset({"text", "orthography"})
            ),
        ),
    )


def test_stemmatology_contamination_is_valid_multi_parent_inheritance() -> None:
    result = assess_reticulate_inheritance(_manuscript_system())
    assert result.status is InheritanceStatus.RETICULATE_INHERITANCE_VALID
    assert ("copy-c", "text") in result.multi_parent_components
    assert result.correctness_granted is False


def test_alternative_parent_preserves_text_but_reopens_style() -> None:
    receipt = revalidate_inheritance(
        _manuscript_system(), revoked_artifact_ids=("exemplar-a",)
    )
    by_component = {
        (record.artifact_id, record.component_id): record
        for record in receipt.component_records
    }
    assert (
        by_component[("copy-c", "text")].status
        is ComponentValidityStatus.PRESERVED
    )
    assert (
        by_component[("copy-c", "orthography")].status
        is ComponentValidityStatus.REOPENED
    )
    assert receipt.preserved_commitment_ids == ("content-reading",)
    assert receipt.reopened_commitment_ids == ("scribal-style",)


def _scientific_artifact_system() -> ReticulateInheritanceSystem:
    return ReticulateInheritanceSystem(
        "scientific-artifact",
        frozenset(
            {"representation-parent", "data-parent", "evaluator-parent", "result"}
        ),
        {"result": frozenset({"representation", "data", "evaluation"})},
        (
            ComponentContribution(
                "representation-parent",
                "result",
                "representation",
                InheritanceRelation.TRANSLATES,
                "map:r",
            ),
            ComponentContribution(
                "data-parent", "result", "data", InheritanceRelation.DERIVES
            ),
            ComponentContribution(
                "evaluator-parent",
                "result",
                "evaluation",
                InheritanceRelation.EVALUATED_BY,
            ),
        ),
        (
            ComponentSupportFamily(
                "representation-support",
                "result",
                "representation",
                frozenset({"representation-parent"}),
            ),
            ComponentSupportFamily(
                "data-support", "result", "data", frozenset({"data-parent"})
            ),
            ComponentSupportFamily(
                "evaluation-support",
                "result",
                "evaluation",
                frozenset({"evaluator-parent"}),
            ),
        ),
        (
            InheritedCommitment(
                "scientific-claim",
                "result",
                frozenset({"representation", "data", "evaluation"}),
            ),
            InheritedCommitment("descriptive-data", "result", frozenset({"data"})),
        ),
    )


def test_scientific_result_has_component_level_multi_parent_provenance() -> None:
    result = assess_reticulate_inheritance(_scientific_artifact_system())
    assert result.status is InheritanceStatus.RETICULATE_INHERITANCE_VALID
    assert len(result.supported_components) == 3


def test_revoked_evaluator_reopens_claim_not_data_description() -> None:
    receipt = revalidate_inheritance(
        _scientific_artifact_system(), revoked_artifact_ids=("evaluator-parent",)
    )
    assert receipt.reopened_commitment_ids == ("scientific-claim",)
    assert receipt.preserved_commitment_ids == ("descriptive-data",)


def test_missing_required_component_support_is_detected() -> None:
    system = _scientific_artifact_system()
    bad = ReticulateInheritanceSystem(
        system.system_id,
        system.artifact_ids,
        {
            "result": frozenset(
                {"representation", "data", "evaluation", "semantics"}
            )
        },
        system.contributions,
        system.support_families,
        system.commitments,
    )
    result = assess_reticulate_inheritance(bad)
    assert result.status is InheritanceStatus.MISSING_COMPONENT_SUPPORT
    assert ("result", "semantics") in result.unsupported_components


def test_translation_without_correspondence_is_rejected() -> None:
    with pytest.raises(ValueError, match="requires correspondence"):
        ComponentContribution("a", "b", "schema", InheritanceRelation.TRANSLATES)


def test_inheritance_cycle_is_rejected() -> None:
    with pytest.raises(ValueError, match="acyclic"):
        ReticulateInheritanceSystem(
            "cycle",
            frozenset({"a", "b"}),
            {},
            (
                ComponentContribution("a", "b", "x", InheritanceRelation.DERIVES),
                ComponentContribution("b", "a", "x", InheritanceRelation.DERIVES),
            ),
            (),
        )
