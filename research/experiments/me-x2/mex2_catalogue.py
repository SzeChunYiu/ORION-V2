"""ME-X2 registered template catalogue (frozen with design V1).

Five symptom templates (protocol V2 paired hostile families A-D plus the
plateau signature of fixture X2-DEV-016).  Each template registers: a shared
symptom and trajectory pattern, cause hypotheses (obstruction class, locus,
canonical minimal fix), probes with exact outcome tables (``nominal`` is the
outcome for every cause not listed), and intervention kinds with a Jump level,
base ``resolves`` and optional ``also`` sets (over-cost resolution, included
per instance with probability 1/2 by the generator).

Effective-table rule (meta-evaluator separation): an ``evaluator_mediated``
probe returns its nominal outcome under every cause whose locus is
``EVALUATOR_VALIDATION`` - a blind scientific evaluator launders the check.
The catalogue registers the *designed* row (what the check would report if
the evaluator were valid, e.g. PPC REJECT under EVALUATOR_BLIND); the generator
derives the *effective* table by laundering those rows to nominal.  Both are
registered on the instance: information-matched arms use the effective table
(the diagnostic-evaluator contract); B5 ladder rungs below the evaluator
contract use the designed table (the scientific evaluator trusted).
"""
from __future__ import annotations

from mex2_model import Cause

# cause tuples: (cause_id, obstruction_class, locus, typical_fix_kind)
# probe tuples: (kind, (cost_lo, cost_hi), mediated, nominal, {cause_id: outcome})
# intervention tuples: (kind, level, [resolves], [also])

TEMPLATES: dict[str, dict] = {
    "A_RESIDUAL": {
        "symptom": "systematic model-observation residual after t0",
        "pattern": "PREDICTIVE_RESIDUAL_AFTER_T0",
        "causes": [
            ("TARGET_SHIFT_REFIT", "NO_ESCALATION_NEEDED", "TARGET_WORLD", "refit_post_t0"),
            ("TARGET_NEW_REGIME", "MODEL_FAMILY_INADEQUATE", "TARGET_WORLD", "expand_model_family"),
            ("SENSOR_DRIFT_RECAL", "NO_ESCALATION_NEEDED", "OBSERVATION_MEASUREMENT", "recalibrate"),
            ("SENSOR_BLIND_NO_STANDARD", "MEASUREMENT_OR_EVALUATOR_BLIND", "OBSERVATION_MEASUREMENT", "build_calibration_instrument"),
            ("MODEL_INADEQUATE", "MODEL_FAMILY_INADEQUATE", "EPISTEMIC_MODEL", "expand_model_family"),
            ("PREPROCESS_BUG", "NO_ESCALATION_NEEDED", "PROCESS_TOOL_WORKFLOW", "fix_unit_conversion"),
            ("MISSING_COVARIATE", "MISSING_PREMISE_OR_DATA", "OBSERVATION_MEASUREMENT", "measure_covariate"),
            ("EVALUATOR_BLIND", "MEASUREMENT_OR_EVALUATOR_BLIND", "EVALUATOR_VALIDATION", "build_validated_evaluator"),
            ("STALE_CACHE", "NO_ESCALATION_NEEDED", "PROCESS_TOOL_WORKFLOW", "refresh_cache"),
        ],
        "probes": [
            ("changepoint_raw", (2, 4), False, "STABLE", {"TARGET_SHIFT_REFIT": "SHIFT", "TARGET_NEW_REGIME": "SHIFT"}),
            ("calibration_standard", (3, 5), False, "OK", {"SENSOR_DRIFT_RECAL": "DRIFT", "SENSOR_BLIND_NO_STANDARD": "OUT_OF_RANGE", "EVALUATOR_BLIND": "OUT_OF_RANGE"}),
            ("ppc_via_evaluator", (1, 2), True, "ACCEPT", {"TARGET_NEW_REGIME": "REJECT", "MODEL_INADEQUATE": "REJECT", "PREPROCESS_BUG": "REJECT", "MISSING_COVARIATE": "REJECT", "EVALUATOR_BLIND": "REJECT"}),
            ("preprocess_unit_audit", (1, 2), False, "OK", {"PREPROCESS_BUG": "MISMATCH"}),
            ("covariate_availability", (1, 1), False, "PRESENT", {"MISSING_COVARIATE": "MISSING"}),
            ("evaluator_gold_audit", (3, 6), False, "OK", {"EVALUATOR_BLIND": "BLIND"}),
            ("provenance_freshness_audit", (1, 2), False, "FRESH", {"STALE_CACHE": "STALE"}),
        ],
        "interventions": [
            ("refit_post_t0", 0, ["TARGET_SHIFT_REFIT"], []),
            ("measure_covariate", 0, ["MISSING_COVARIATE"], []),
            ("recalibrate", 1, ["SENSOR_DRIFT_RECAL"], []),
            ("fix_unit_conversion", 1, ["PREPROCESS_BUG"], []),
            ("refresh_cache", 1, ["STALE_CACHE"], []),
            ("expand_model_family", 2, ["MODEL_INADEQUATE", "TARGET_NEW_REGIME"], ["TARGET_SHIFT_REFIT", "SENSOR_DRIFT_RECAL"]),
            ("change_representation", 3, [], ["MODEL_INADEQUATE", "TARGET_NEW_REGIME"]),
            ("reformulate_objective", 4, [], []),
            ("build_calibration_instrument", 5, ["SENSOR_BLIND_NO_STANDARD"], ["SENSOR_DRIFT_RECAL"]),
            ("build_validated_evaluator", 5, ["EVALUATOR_BLIND"], []),
            ("revise_workflow", 6, [], ["PREPROCESS_BUG", "STALE_CACHE"]),
        ],
    },
    "A_PLATEAU": {
        "symptom": "evaluator score stops improving",
        "pattern": "SCORE_PLATEAU",
        "causes": [
            ("LOCAL_OPTIMUM_MORE_SEARCH", "SEARCH_INSUFFICIENT", "PROCESS_TOOL_WORKFLOW", "continue_search"),
            ("MODEL_INADEQUATE_P", "MODEL_FAMILY_INADEQUATE", "EPISTEMIC_MODEL", "expand_model_family"),
            ("STATES_COLLAPSED", "REPRESENTATION_INSUFFICIENT", "REPRESENTATION_REGIME", "change_representation"),
            ("EVALUATOR_SATURATED", "MEASUREMENT_OR_EVALUATOR_BLIND", "EVALUATOR_VALIDATION", "build_validated_evaluator"),
            ("CRITERION_MET", "NO_ESCALATION_NEEDED", "NO_MATERIAL_DISCREPANCY", "stop_warranted_terminal"),
            ("OBJECTIVE_OMITS_CRITERION", "PROBLEM_OBJECTIVE_MISSPECIFIED", "PROBLEM_CRITERION", "reformulate_objective"),
            ("HYPERPARAM_MISSET", "NO_ESCALATION_NEEDED", "PROCESS_TOOL_WORKFLOW", "reset_registered_parameters"),
        ],
        "probes": [
            ("search_coverage_audit", (1, 2), False, "SATURATED", {"LOCAL_OPTIMUM_MORE_SEARCH": "SHALLOW"}),
            ("obligation_ledger_audit", (1, 1), False, "OPEN", {"CRITERION_MET": "ALL_DISCHARGED"}),
            ("separability_test", (3, 5), False, "SEPARABLE", {"STATES_COLLAPSED": "COLLAPSED"}),
            ("ppc_via_evaluator", (1, 2), True, "ACCEPT", {"MODEL_INADEQUATE_P": "REJECT", "EVALUATOR_SATURATED": "REJECT"}),
            ("evaluator_gold_audit", (3, 6), False, "OK", {"EVALUATOR_SATURATED": "BLIND"}),
            ("decision_outcome_review", (4, 6), False, "ALIGNED", {"OBJECTIVE_OMITS_CRITERION": "MISALIGNED"}),
            ("config_audit", (1, 2), False, "OK", {"HYPERPARAM_MISSET": "MISSET"}),
        ],
        "interventions": [
            ("continue_search", 0, ["LOCAL_OPTIMUM_MORE_SEARCH"], []),
            ("stop_warranted_terminal", 0, ["CRITERION_MET"], []),
            ("reset_registered_parameters", 0, ["HYPERPARAM_MISSET"], []),
            ("expand_model_family", 2, ["MODEL_INADEQUATE_P"], ["LOCAL_OPTIMUM_MORE_SEARCH"]),
            ("change_representation", 3, ["STATES_COLLAPSED"], ["MODEL_INADEQUATE_P"]),
            ("reformulate_objective", 4, ["OBJECTIVE_OMITS_CRITERION"], []),
            ("build_validated_evaluator", 5, ["EVALUATOR_SATURATED"], []),
            ("revise_workflow", 6, [], ["HYPERPARAM_MISSET"]),
        ],
    },
    "B_PROOF": {
        "symptom": "proof search fails on the registered theorem",
        "pattern": "PROOF_SEARCH_FAILURE",
        "causes": [
            ("SEARCH_SHALLOW", "SEARCH_INSUFFICIENT", "PROCESS_TOOL_WORKFLOW", "continue_search"),
            ("MISSING_LEMMA", "MISSING_PREMISE_OR_DATA", "EPISTEMIC_MODEL", "retrieve_lemma"),
            ("ENCODING_INSUFFICIENT", "REPRESENTATION_INSUFFICIENT", "REPRESENTATION_REGIME", "change_encoding"),
            ("OPERATOR_MISSING", "FORMALISM_OR_OPERATOR_INSUFFICIENT", "REPRESENTATION_REGIME", "extend_formalism_operator"),
            ("SPEC_WRONG", "PROBLEM_OBJECTIVE_MISSPECIFIED", "PROBLEM_CRITERION", "reformulate_specification"),
            ("SEMANTIC_EVAL_CANNOT_ALIGN", "MEASUREMENT_OR_EVALUATOR_BLIND", "EVALUATOR_VALIDATION", "build_semantic_alignment_evaluator"),
            ("TRANSIENT_TOOL_FAILURE", "NO_ESCALATION_NEEDED", "PROCESS_TOOL_WORKFLOW", "rerun_stable_tolerance"),
            ("PROVER_VERSION_INADEQUATE", "TOOL_INSTRUMENT_INADEQUATE", "PROCESS_TOOL_WORKFLOW", "adopt_capable_prover"),
        ],
        "probes": [
            ("search_coverage_audit", (1, 2), False, "EXHAUSTED", {"SEARCH_SHALLOW": "SHALLOW"}),
            ("library_retrieval_audit", (1, 2), False, "NONE", {"MISSING_LEMMA": "UNRETRIEVED_LEMMA"}),
            ("expressivity_check", (3, 5), False, "OK", {"ENCODING_INSUFFICIENT": "CEILING", "OPERATOR_MISSING": "CEILING"}),
            ("operator_availability_audit", (2, 3), False, "OK", {"OPERATOR_MISSING": "OPERATOR_MISSING"}),
            ("spec_intent_review", (4, 6), False, "ALIGNED", {"SPEC_WRONG": "MISMATCH", "SEMANTIC_EVAL_CANNOT_ALIGN": "UNDECIDABLE"}),
            ("tactic_retry_via_checker", (1, 2), True, "STUCK", {"SEARCH_SHALLOW": "PROGRESS", "TRANSIENT_TOOL_FAILURE": "PROGRESS"}),
            ("tool_log_audit", (1, 1), False, "CLEAN", {"TRANSIENT_TOOL_FAILURE": "TRANSIENT_ERROR", "PROVER_VERSION_INADEQUATE": "UNSUPPORTED_FEATURE"}),
        ],
        "interventions": [
            ("continue_search", 0, ["SEARCH_SHALLOW"], []),
            ("rerun_stable_tolerance", 0, ["TRANSIENT_TOOL_FAILURE"], []),
            ("retrieve_lemma", 1, ["MISSING_LEMMA"], []),
            ("invent_lemma", 2, [], ["MISSING_LEMMA"]),
            ("change_encoding", 3, ["ENCODING_INSUFFICIENT"], ["MISSING_LEMMA", "SEARCH_SHALLOW"]),
            ("extend_formalism_operator", 3, ["OPERATOR_MISSING"], []),
            ("reformulate_specification", 4, ["SPEC_WRONG"], []),
            ("build_semantic_alignment_evaluator", 5, ["SEMANTIC_EVAL_CANNOT_ALIGN"], []),
            ("adopt_capable_prover", 5, ["PROVER_VERSION_INADEQUATE"], ["TRANSIENT_TOOL_FAILURE"]),
            ("revise_proof_workflow", 6, [], ["TRANSIENT_TOOL_FAILURE", "SEARCH_SHALLOW"]),
        ],
    },
    "C_NONDISCRIM": {
        "symptom": "competing hypotheses remain undiscriminated after the experiment",
        "pattern": "EXPERIMENT_NONDISCRIMINATION",
        "causes": [
            ("MORE_SAMPLES", "SEARCH_INSUFFICIENT", "OBSERVATION_MEASUREMENT", "collect_more_samples"),
            ("CHANNEL_INSENSITIVE", "TOOL_INSTRUMENT_INADEQUATE", "OBSERVATION_MEASUREMENT", "switch_instrument"),
            ("HYPOTHESIS_FAMILY_INADEQUATE", "MODEL_FAMILY_INADEQUATE", "EPISTEMIC_MODEL", "expand_hypothesis_family"),
            ("INTERVENTION_NEEDED", "PROBE_ACTION_INSUFFICIENT", "OBSERVATION_MEASUREMENT", "run_discriminating_intervention"),
            ("CRITERION_UNIDENTIFIABLE", "PROBLEM_OBJECTIVE_MISSPECIFIED", "PROBLEM_CRITERION", "reformulate_criterion"),
            ("EVALUATOR_BLIND_C", "MEASUREMENT_OR_EVALUATOR_BLIND", "EVALUATOR_VALIDATION", "build_validated_evaluator"),
            ("ANALYSIS_BUG", "NO_ESCALATION_NEEDED", "PROCESS_TOOL_WORKFLOW", "fix_analysis_script"),
        ],
        "probes": [
            ("power_analysis", (1, 2), False, "ADEQUATE", {"MORE_SAMPLES": "UNDERPOWERED"}),
            ("channel_sensitivity_check", (3, 5), False, "SENSITIVE", {"CHANNEL_INSENSITIVE": "INSENSITIVE"}),
            ("passive_equivalence_analysis", (2, 3), False, "DISTINGUISHABLE", {"INTERVENTION_NEEDED": "EQUIVALENT_UNDER_PASSIVE", "CRITERION_UNIDENTIFIABLE": "EQUIVALENT_UNDER_PASSIVE"}),
            ("model_criticism_via_evaluator", (1, 2), True, "SOME_FIT", {"HYPOTHESIS_FAMILY_INADEQUATE": "ALL_REJECTED", "ANALYSIS_BUG": "ALL_REJECTED", "EVALUATOR_BLIND_C": "ALL_REJECTED"}),
            ("identifiability_analysis", (4, 6), False, "IDENTIFIABLE", {"CRITERION_UNIDENTIFIABLE": "NONIDENTIFIABLE"}),
            ("evaluator_sensitivity_audit", (3, 5), False, "OK", {"EVALUATOR_BLIND_C": "BLIND"}),
            ("analysis_reproduction_audit", (1, 2), False, "REPRODUCED", {"ANALYSIS_BUG": "DISCREPANT"}),
        ],
        "interventions": [
            ("collect_more_samples", 0, ["MORE_SAMPLES"], []),
            ("run_discriminating_intervention", 0, ["INTERVENTION_NEEDED"], []),
            ("fix_analysis_script", 1, ["ANALYSIS_BUG"], []),
            ("expand_hypothesis_family", 2, ["HYPOTHESIS_FAMILY_INADEQUATE"], []),
            ("new_representation", 3, [], ["HYPOTHESIS_FAMILY_INADEQUATE"]),
            ("reformulate_criterion", 4, ["CRITERION_UNIDENTIFIABLE"], []),
            ("switch_instrument", 5, ["CHANNEL_INSENSITIVE"], ["MORE_SAMPLES"]),
            ("build_validated_evaluator", 5, ["EVALUATOR_BLIND_C"], []),
            ("revise_workflow", 6, [], ["ANALYSIS_BUG"]),
        ],
    },
    "D_WORKFLOW": {
        "symptom": "pipeline output invalid; downstream comparison corrupted",
        "pattern": "PIPELINE_STAGE_MISMATCH",
        "causes": [
            ("LOCAL_TOOL_BUG", "NO_ESCALATION_NEEDED", "PROCESS_TOOL_WORKFLOW", "patch_tool"),
            ("METADATA_LOSS", "WORKFLOW_INADEQUATE", "PROCESS_TOOL_WORKFLOW", "workflow_state_contract"),
            ("METADATA_LOSS_LOCAL_FIXABLE", "NO_ESCALATION_NEEDED", "PROCESS_TOOL_WORKFLOW", "add_metadata_passthrough"),
            ("INVALID_EVALUATOR", "MEASUREMENT_OR_EVALUATOR_BLIND", "EVALUATOR_VALIDATION", "replace_validate_evaluator"),
            ("WRONG_MODEL", "MODEL_FAMILY_INADEQUATE", "EPISTEMIC_MODEL", "expand_model_family"),
            ("WRONG_CRITERION", "PROBLEM_OBJECTIVE_MISSPECIFIED", "PROBLEM_CRITERION", "reformulate_criterion"),
            ("TRANSIENT_ENV", "NO_ESCALATION_NEEDED", "PROCESS_TOOL_WORKFLOW", "rerun_clean"),
            ("TOOL_CAPABILITY_MISSING", "TOOL_INSTRUMENT_INADEQUATE", "PROCESS_TOOL_WORKFLOW", "adopt_capable_tool"),
        ],
        "probes": [
            ("unit_test_local_tool", (1, 2), False, "PASS", {"LOCAL_TOOL_BUG": "FAIL_LOGIC", "TOOL_CAPABILITY_MISSING": "FAIL_UNSUPPORTED"}),
            ("dependency_provenance_audit", (2, 3), False, "INTACT", {"METADATA_LOSS": "LOST_METADATA", "METADATA_LOSS_LOCAL_FIXABLE": "LOST_METADATA"}),
            ("stage_contract_audit", (3, 5), False, "CONSISTENT", {"METADATA_LOSS": "CROSS_STAGE", "METADATA_LOSS_LOCAL_FIXABLE": "SINGLE_STAGE"}),
            ("evaluator_validity_audit", (3, 5), False, "VALID", {"INVALID_EVALUATOR": "INVALID"}),
            ("model_check_via_evaluator", (1, 2), True, "ACCEPT", {"WRONG_MODEL": "REJECT", "INVALID_EVALUATOR": "REJECT"}),
            ("criterion_review", (3, 5), False, "OK", {"WRONG_CRITERION": "MISSPECIFIED"}),
            ("clean_env_reproduction", (1, 2), False, "PERSISTS", {"TRANSIENT_ENV": "TRANSIENT"}),
        ],
        "interventions": [
            ("rerun_clean", 0, ["TRANSIENT_ENV"], []),
            ("patch_tool", 1, ["LOCAL_TOOL_BUG"], []),
            ("add_metadata_passthrough", 1, ["METADATA_LOSS_LOCAL_FIXABLE"], []),
            ("expand_model_family", 2, ["WRONG_MODEL"], []),
            ("reformulate_criterion", 4, ["WRONG_CRITERION"], []),
            ("replace_validate_evaluator", 5, ["INVALID_EVALUATOR"], []),
            ("adopt_capable_tool", 5, ["TOOL_CAPABILITY_MISSING"], ["LOCAL_TOOL_BUG"]),
            ("workflow_state_contract", 6, ["METADATA_LOSS"], ["METADATA_LOSS_LOCAL_FIXABLE", "LOCAL_TOOL_BUG", "TRANSIENT_ENV"]),
        ],
    },
}

# ARFT-equivalent process-failure pattern vocabulary (frozen; ARFT itself is not licensed/used:
# an equivalently strong pattern -> standard-fix taxonomy stands in, see design S4 B2).
TAXONOMY_PATTERNS: dict[str, dict] = {
    "PREDICTIVE_RESIDUAL_AFTER_T0": {"standard_fix_kind": "expand_model_family", "orion_mapping": "MANY_TO_ONE", "orion_classes": ["MODEL_FAMILY_INADEQUATE", "NO_ESCALATION_NEEDED", "MISSING_PREMISE_OR_DATA", "MEASUREMENT_OR_EVALUATOR_BLIND"]},
    "SCORE_PLATEAU": {"standard_fix_kind": "change_representation", "orion_mapping": "ONE_TO_MANY", "orion_classes": ["REPRESENTATION_INSUFFICIENT", "SEARCH_INSUFFICIENT", "MODEL_FAMILY_INADEQUATE", "NO_ESCALATION_NEEDED", "PROBLEM_OBJECTIVE_MISSPECIFIED", "MEASUREMENT_OR_EVALUATOR_BLIND"]},
    "PROOF_SEARCH_FAILURE": {"standard_fix_kind": "change_encoding", "orion_mapping": "MULTI_CAUSAL", "orion_classes": ["SEARCH_INSUFFICIENT", "MISSING_PREMISE_OR_DATA", "REPRESENTATION_INSUFFICIENT", "FORMALISM_OR_OPERATOR_INSUFFICIENT", "PROBLEM_OBJECTIVE_MISSPECIFIED", "MEASUREMENT_OR_EVALUATOR_BLIND", "NO_ESCALATION_NEEDED", "TOOL_INSTRUMENT_INADEQUATE"]},
    "EXPERIMENT_NONDISCRIMINATION": {"standard_fix_kind": "expand_hypothesis_family", "orion_mapping": "MANY_TO_ONE", "orion_classes": ["SEARCH_INSUFFICIENT", "TOOL_INSTRUMENT_INADEQUATE", "MODEL_FAMILY_INADEQUATE", "PROBE_ACTION_INSUFFICIENT", "PROBLEM_OBJECTIVE_MISSPECIFIED", "MEASUREMENT_OR_EVALUATOR_BLIND", "NO_ESCALATION_NEEDED"]},
    "PIPELINE_STAGE_MISMATCH": {"standard_fix_kind": "workflow_state_contract", "orion_mapping": "MANY_TO_ONE", "orion_classes": ["WORKFLOW_INADEQUATE", "NO_ESCALATION_NEEDED", "MEASUREMENT_OR_EVALUATOR_BLIND", "MODEL_FAMILY_INADEQUATE", "PROBLEM_OBJECTIVE_MISSPECIFIED", "TOOL_INSTRUMENT_INADEQUATE"]},
    "UNMAPPED_AGENT_LOOP_PATTERN": {"standard_fix_kind": None, "orion_mapping": "NO_MAPPING", "orion_classes": [], "note": "hostile counterexample to universality: an agent-loop pattern (e.g. tool-call formatting loop) with no ORION obstruction class; not instantiated by the generator, registered so the mapping table is honest"},
}


def template_causes(name: str) -> tuple[Cause, ...]:
    return tuple(Cause(*c) for c in TEMPLATES[name]["causes"])


def templates_with_class(cls: str) -> list[str]:
    return [t for t, d in TEMPLATES.items() if any(c[1] == cls for c in d["causes"])]
