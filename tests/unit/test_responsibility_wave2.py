from orion_v2.responsibility import (
    DiagnosisStatus,
    DiagnosticProbe,
    ResponsibilityHypothesis,
    ResponsibilityTopology,
    assess_responsibility,
)


def test_interaction_only_failure_is_not_forced_into_one_cause() -> None:
    hypotheses = (
        ResponsibilityHypothesis(
            "network",
            frozenset({"network"}),
            ResponsibilityTopology.SINGLE,
            frozenset({"timeout"}),
        ),
        ResponsibilityHypothesis(
            "scheduler",
            frozenset({"scheduler"}),
            ResponsibilityTopology.SINGLE,
            frozenset({"delay"}),
        ),
        ResponsibilityHypothesis(
            "interaction",
            frozenset({"network", "scheduler"}),
            ResponsibilityTopology.INTERACTION_ONLY,
            frozenset({"timeout", "delay", "loss"}),
        ),
    )
    result = assess_responsibility(frozenset({"timeout", "loss"}), hypotheses)
    assert result.status is DiagnosisStatus.IDENTIFIED
    assert result.minimal_hypothesis_ids == ("interaction",)


def test_multiple_diagnoses_require_discriminating_probe() -> None:
    hypotheses = (
        ResponsibilityHypothesis(
            "sensor",
            frozenset({"sensor"}),
            ResponsibilityTopology.SINGLE,
            frozenset({"bad-reading"}),
        ),
        ResponsibilityHypothesis(
            "model",
            frozenset({"model"}),
            ResponsibilityTopology.SINGLE,
            frozenset({"bad-reading"}),
        ),
    )
    no_probe = assess_responsibility(frozenset({"bad-reading"}), hypotheses)
    assert no_probe.status is DiagnosisStatus.STRUCTURALLY_NONIDENTIFIABLE
    probe = DiagnosticProbe(
        "independent-calibration",
        {"sensor": "fails", "model": "passes"},
        cost=1,
    )
    with_probe = assess_responsibility(
        frozenset({"bad-reading"}),
        hypotheses,
        (probe,),
    )
    assert with_probe.status is DiagnosisStatus.MULTIPLE_DISCRIMINABLE
    assert with_probe.minimum_probe_ids == ("independent-calibration",)


def test_no_consistent_hypothesis_reports_contradiction() -> None:
    hypotheses = (
        ResponsibilityHypothesis(
            "a",
            frozenset({"a"}),
            ResponsibilityTopology.SINGLE,
            frozenset({"x"}),
        ),
    )
    assert (
        assess_responsibility(frozenset({"y"}), hypotheses).status
        is DiagnosisStatus.CONTRADICTION
    )
