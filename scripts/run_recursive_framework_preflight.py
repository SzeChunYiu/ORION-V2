#!/usr/bin/env python3
"""Reference-only preflight for the integrated ORION-V2 development hierarchy."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from orion_v2.development_controller import (
    DevelopmentMode,
    DevelopmentModeProposal,
    ModeAssessmentContext,
    ModeWitnessBundle,
    RegisteredAlternative,
    assess_mode_proposal,
    framework_layers,
)
from orion_v2.recursive_generalization import RecursiveGeneralizationStatus
from orion_v2.scientific_development import ScientificDevelopmentStatus


def proposal(identifier: str, mode: DevelopmentMode, cost: float) -> DevelopmentModeProposal:
    return DevelopmentModeProposal(
        proposal_id=identifier,
        episode_id="preflight-episode",
        mode=mode,
        target_obligation_ids=("registered-obligation",),
        prospective_identity_frozen=True,
        expected_resource_cost=cost,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    parent_blocks = assess_mode_proposal(
        proposal("parent-blocks-formalism", DevelopmentMode.FORMALISM_GENESIS, 5.0),
        ModeAssessmentContext(
            alternatives=(
                RegisteredAlternative("strong-parent", DevelopmentMode.STRONGEST_PARENT, 1.0, True, True),
                RegisteredAlternative("more-data", DevelopmentMode.EMPIRICAL_EXPANSION, 2.0, True, False),
            ),
            witnesses=ModeWitnessBundle(
                representational_deficit_witness_ids=("collision",),
                semantic_validation_plan_ids=("semantics",),
                predecessor_recovery_plan_ids=("recovery",),
                counterexample_or_obstruction_ids=("counterexample",),
            ),
            authority_ceiling=1,
            resource_budget=10,
        ),
    )
    formalism_allowed = assess_mode_proposal(
        proposal("formalism-after-controls", DevelopmentMode.FORMALISM_GENESIS, 5.0),
        ModeAssessmentContext(
            alternatives=(
                RegisteredAlternative("strong-parent", DevelopmentMode.STRONGEST_PARENT, 1.0, True, False),
                RegisteredAlternative("more-data", DevelopmentMode.EMPIRICAL_EXPANSION, 2.0, True, False),
            ),
            witnesses=ModeWitnessBundle(
                representational_deficit_witness_ids=("collision",),
                semantic_validation_plan_ids=("semantics",),
                predecessor_recovery_plan_ids=("recovery",),
                counterexample_or_obstruction_ids=("counterexample",),
            ),
            authority_ceiling=1,
            resource_budget=10,
        ),
    )
    recursive_allowed = assess_mode_proposal(
        proposal("recursive-after-saturation", DevelopmentMode.RECURSIVE_META_LEARNING, 5.0),
        ModeAssessmentContext(
            alternatives=(),
            witnesses=ModeWitnessBundle(
                population_episode_ids=("episode-a", "episode-b"),
                lower_level_saturation_receipt_ids=("bounded-lower-terminal",),
                heldout_route_ids=("new-field", "new-epoch"),
            ),
            authority_ceiling=1,
            resource_budget=10,
        ),
    )

    value = {
        "schema_version": "orion.v2.recursive-framework-preflight.v1",
        "status": "REFERENCE_FRAMEWORK_INTEGRATION_PREFLIGHT_ONLY",
        "layer_count": len(framework_layers()),
        "layers": [item.value for item in framework_layers()],
        "checks": {
            "parent_sufficiency_blocks_formalism": parent_blocks.status.value == "SIMPLE_OR_PARENT_SUFFICIENT",
            "formalism_admissible_only_after_parent_and_data_controls_fail": formalism_allowed.status.value == "ADMISSIBLE",
            "recursive_meta_learning_requires_population_and_lower_level_terminal": recursive_allowed.status.value == "ADMISSIBLE",
            "scientific_development_non_authorizing_status_surface_present": ScientificDevelopmentStatus.POPULATION_REGULARITY_ONLY.value == "POPULATION_REGULARITY_ONLY",
            "recursive_stability_non_ultimate_terminal_present": RecursiveGeneralizationStatus.RECURSIVE_STABILITY_CANDIDATE.value == "RECURSIVE_STABILITY_CANDIDATE",
        },
        "authority": {
            "grants_scientific_truth": False,
            "grants_F2_superiority": False,
            "grants_theory_revision": False,
            "grants_recursive_stability": False,
            "grants_ultimate_truth": False,
            "grants_submission_readiness": False,
        },
    }
    value["all_reference_checks_pass"] = all(value["checks"].values())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if value["all_reference_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
