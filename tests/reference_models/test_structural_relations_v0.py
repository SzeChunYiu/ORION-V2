"""Known-answer tests for the non-authorizing V0 relation reference model."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "research" / "reference_models" / "structural_relations_v0.py"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "known_answer_structural_cases_v0.json"

spec = importlib.util.spec_from_file_location("orion_v2_structural_relations_v0", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
    FIXTURES = {case["case_id"]: case for case in json.load(handle)["cases"]}


def test_local_compatibility_does_not_imply_global_consistency() -> None:
    case = FIXTURES["local-global-parity-obstruction"]
    assert module.each_constraint_satisfiable(
        case["variables"], case["domains"], case["constraints"]
    ) is case["expected"]["each_constraint_satisfiable"]
    assert module.xor_constraints_satisfiable(
        case["variables"], case["domains"], case["constraints"]
    ) is case["expected"]["global_satisfiable"]


def test_observational_equivalence_does_not_mean_structural_identity() -> None:
    case = FIXTURES["causal-observational-tie-direction-difference"]
    assert module.markov_equivalent_dags(
        case["nodes"], case["left_edges"], case["right_edges"]
    ) is case["expected"]["observationally_markov_equivalent"]
    assert case["left_edges"] != case["right_edges"]


def test_same_vocabulary_can_hide_behavioral_difference() -> None:
    case = FIXTURES["same-vocabulary-different-transition-behaviour"]
    assert module.lts_bisimilar(case["left"], case["right"]) is case["expected"]["bisimilar"]


def test_different_domains_can_share_a_role_without_semantic_identity() -> None:
    case = FIXTURES["different-vocabulary-same-relational-role"]
    assert module.role_equivalent(
        case["left_role_profile"], case["right_role_profile"]
    ) is case["expected"]["role_equivalent"]
    assert case["surface_labels"][0] != case["surface_labels"][1]
    assert case["expected"]["semantic_identity"] is False


def test_safe_quotient_is_target_and_epoch_relative() -> None:
    case = FIXTURES["safe-current-quotient-unsafe-future-query"]
    for target, expected in case["expected"]["safe_for_targets"].items():
        assert module.quotient_safe_for_target(
            case["states"], case["partition"], target
        ) is expected


def test_minimum_distinguishing_probe_set() -> None:
    case = FIXTURES["minimum-distinguishing-probe"]
    actual = module.minimum_distinguishing_probe_sets(case["hypothesis_signatures"])
    assert actual == tuple(tuple(item) for item in case["expected"]["minimum_probe_sets"])
    assert len(actual[0]) == case["expected"]["minimum_probe_count"]


def test_censored_route_is_not_nonidentifiability_evidence() -> None:
    case = FIXTURES["censored-route-not-nonidentifiability"]
    actual = module.classify_censoring_terminal(case["provider_status"])
    assert actual == case["expected"]["terminal"]
    assert actual != case["expected"]["must_not_return"]


def test_jump_chooses_minimum_tested_sufficient_level() -> None:
    results = [
        module.JumpLevelResult(1, tested=True, sufficient=False, evidence_id="e:J1"),
        module.JumpLevelResult(2, tested=True, sufficient=True, evidence_id="e:J2"),
        module.JumpLevelResult(3, tested=True, sufficient=True, evidence_id="e:J3"),
    ]
    assert module.minimum_sufficient_jump_level(
        results, incumbent_insufficiency_witnessed=True
    ) == 2


def test_jump_refuses_when_incumbent_insufficiency_is_not_identified() -> None:
    results = [module.JumpLevelResult(3, tested=True, sufficient=True, evidence_id="e:J3")]
    assert module.minimum_sufficient_jump_level(
        results, incumbent_insufficiency_witnessed=False
    ) == "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED"


def test_jump_refuses_to_learn_from_censored_coverage() -> None:
    results = [module.JumpLevelResult(3, tested=True, sufficient=True, evidence_id="e:J3")]
    assert module.minimum_sufficient_jump_level(
        results,
        incumbent_insufficiency_witnessed=True,
        coverage_censored=True,
    ) == "CANNOT_CHECK"
