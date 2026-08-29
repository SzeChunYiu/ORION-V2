#!/usr/bin/env python3
"""Run non-scientific reference checks for the SD recursive-development semantics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from orion_v2.recursive_generalization import GeneralizationEvidence, RecursiveGeneralizationStatus, RecursiveStabilityEvidence, assess_higher_abstraction, assess_recursive_stability
from orion_v2.scientific_development import DevelopmentOutcomeClass, DevelopmentStep, MetaPrincipleEvidence, ScientificDevelopmentEpisode, ScientificDevelopmentStatus, assess_meta_principle, discover_operator_contrasts


def _ep(ep_id: str, outcome: DevelopmentOutcomeClass, action: str, domain: str):
    return ScientificDevelopmentEpisode(
        episode_id=ep_id,
        domain_id=domain,
        epoch_id="epoch-calibration",
        outcome_class=outcome,
        steps=(DevelopmentStep(ep_id + "-0", 0, ("s:open",), (action,), resource_cost=1.0),),
        source_mode_ids=("synthetic-calibration", "independent-oracle"),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    episodes = (
        _ep("p1", DevelopmentOutcomeClass.VALIDATED_SUCCESS, "opaque-action-X", "domain-a"),
        _ep("p2", DevelopmentOutcomeClass.VALIDATED_SUCCESS, "opaque-action-X", "domain-b"),
        _ep("n1", DevelopmentOutcomeClass.VALIDATED_FAILURE, "opaque-action-Y", "domain-a"),
        _ep("n2", DevelopmentOutcomeClass.ABANDONED, "opaque-action-Y", "domain-c"),
    )
    operators = discover_operator_contrasts(episodes, minimum_positive_support=2, maximum_feature_order=1)
    population = assess_meta_principle(operators[0].operator_id, MetaPrincipleEvidence(True, True, True, False, True, True, None, False, True))
    higher = assess_higher_abstraction("calibration-higher", from_level=2, evidence=GeneralizationEvidence(True, False, 0.1, 0.1, 0.1, False, 0.1, 0.0, True))
    stability = assess_recursive_stability(RecursiveStabilityEvidence(3, True, False, True, True, True))
    checks = {
        "operator_discovery": bool(operators and operators[0].feature_ids == ("ACTION:opaque-action-X",)),
        "population_stays_noncausal_without_prospective_test": population.status is ScientificDevelopmentStatus.POPULATION_REGULARITY_ONLY,
        "higher_level_prospective_residual": higher.status is RecursiveGeneralizationStatus.PROSPECTIVE_HIGHER_LEVEL_RESIDUAL,
        "recursive_stability_is_bounded_terminal": stability.status is RecursiveGeneralizationStatus.RECURSIVE_STABILITY_CANDIDATE and not stability.ultimate_truth_authorized,
    }
    receipt = {
        "schema_version": "orion.v2.scientific-development-reference.v1",
        "status": "REFERENCE_SEMANTICS_CALIBRATION_ONLY",
        "checks": checks,
        "all_reference_checks_pass": all(checks.values()),
        "authority": {"grants_scientific_truth": False, "grants_causal_law": False, "grants_recursive_ultimate_truth": False},
    }
    Path(args.output).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
