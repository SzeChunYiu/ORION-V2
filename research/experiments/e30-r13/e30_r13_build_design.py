#!/usr/bin/env python3
"""Emit E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1.json.

Run once, before freeze. The contract fingerprint and the derived budget are READ from
the executable and the archived budget note rather than typed, so the design cannot
register a contract or a cap that the dispatch does not use.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
R13 = ROOT / "research" / "experiments" / "e30-r13"

spec = importlib.util.spec_from_file_location("arms", ROOT / "scripts" / "orion_claude_arms.py")
arms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arms)

note = json.loads((R13 / "results" / "E30_R13_BUDGET_NOTE_V1.json").read_text())
derivation = note["registered_contract"]["derivation"]
assert derivation["status"] == "DERIVED", derivation
PER_CALL = derivation["registered_per_call_max_tokens"]
CONTRACT = note["registered_contract"]["contract_id"]

r12 = json.loads((ROOT / "research/experiments/e30-r12/"
                  "E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json").read_text())

CALIBRATION_FILES = sorted(
    f for f in (R13 / "results").glob("E30_R13_CALIBRATION_*.json")
    if f.name != "E30_R13_CALIBRATION_PROVENANCE_V1.json")
assert len(CALIBRATION_FILES) == 4, [f.name for f in CALIBRATION_FILES]

CONTRAST = {}
for f in CALIBRATION_FILES:
    for name, summary in json.loads(f.read_text())["summary"].items():
        if name not in CONTRAST:
            CONTRAST[name] = {"calls": 0, "stop_reasons": {}, "calls_with_zero_text": 0,
                              "max_output_tokens": 0, "min_output_tokens": None,
                              "json_parseable_final_calls": [0, 0],
                              "contract_sha256": summary["contract_sha256"]}
        agg = CONTRAST[name]
        agg["calls"] += summary["calls"]
        for reason, count in summary["stop_reasons"].items():
            agg["stop_reasons"][reason] = agg["stop_reasons"].get(reason, 0) + count
        agg["calls_with_zero_text"] += summary["text_chars_zero_calls"]
        agg["max_output_tokens"] = max(agg["max_output_tokens"], summary["output_tokens"]["max"])
        low = summary["output_tokens"]["min"]
        agg["min_output_tokens"] = low if agg["min_output_tokens"] is None else min(agg["min_output_tokens"], low)
        ok, total = summary["json_parseable_final_calls"].split("/")
        agg["json_parseable_final_calls"][0] += int(ok)
        agg["json_parseable_final_calls"][1] += int(total)
for name, agg in CONTRAST.items():
    ok, total = agg.pop("json_parseable_final_calls")
    agg["json_parseable_final_calls"] = f"{ok}/{total}"

feas = note["registered_contract_feasibility"]
default_feas = note["provider_default_counterfactual"]["escalated_36000"]

design = {
    "schema_version": "orion.v2.e30-r13-design.v1",
    "study_id": "E30-R13",
    "title": "Confirmatory BugsInPy re-run under a registered channel request-body contract",
    "state_date": "2026-09-03",
    "status": "PROSPECTIVE_REGISTERED_DESIGN_NO_RESULTS",
    "class": "new prospective confirmatory study under a NEW campaign identity; not a "
             "re-analysis and not a repair of E30-R12's campaign",
    "anchor_commit": r12["anchor_commit"],
    "question": r12["question"],

    "why_this_study_exists": {
        "e30_r12_terminal": "EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ",
        "what_happened": "E30-R12 dispatched its registered chain and halted during model "
                         "dispatch with 119 of 480 responses written, 116 of them envelope "
                         "failures whose output tokens sat at or above the registered 6000 "
                         "cap with the diagnosis 'model did not return a JSON object', 0 of "
                         "480 evaluations, no gate computed and no endpoint read.",
        "measured_root_cause": "the bound z.ai Anthropic-compatible channel spends the whole "
                               "registered output budget on an extended-thinking content block "
                               "before emitting any text. The arm reads only text blocks, so it "
                               "receives nothing and records an envelope failure carrying no "
                               "model output.",
        "the_finding_that_makes_this_a_study_and_not_a_patch":
            "PINNING A SERVED MODEL ID DOES NOT PIN AN EXPERIMENTAL CONDITION. All 119 of "
            "E30-R12's envelopes recorded exactly one served model id, glm-5.3, equal to the "
            "frozen value, and its GR0c served-model condition held for every envelope "
            "written. The drift is in channel BEHAVIOUR at a FIXED served id, which no "
            "registered gate in the programme observed.",
        "the_hole_in_e30_r12s_design": "model_binding registered the channel, the base URL, "
                                       "the requested model, the frozen served model, the "
                                       "served-model assertion and the per-envelope served-id "
                                       "record. It registered NO request-body contract, so the "
                                       "condition was inherited from a provider default that "
                                       "was then free to move.",
        "why_a_new_campaign_identity": "E30-R12's 3 completed envelopes were produced under the "
                                       "provider default. Pooling them into a differently "
                                       "configured campaign would mix two channel conditions "
                                       "inside one paired contrast while every registered gate "
                                       "still passed. R13 makes its own 480 responses in its own "
                                       "campaign directory, and its setup refuses to start "
                                       "unless responses/ and evaluations/ are empty.",
    },

    "relationship_to_earlier_runs": {
        "e30_r11_endpoints": "FROZEN_TERMINAL",
        "e60_endpoints": "FROZEN_TERMINAL",
        "pc_r6_endpoints": "FROZEN_TERMINAL",
        "e30_r12_receipt": "FROZEN_TERMINAL",
        "r13_may_revise_them": False,
        "r13_is_a_reanalysis": False,
        "r11_served_model": "INFERRED_NOT_VERIFIED",
        "comparison_to_r11": "DESCRIPTIVE_ONLY",
        "why_the_r11_comparison_is_descriptive_only": [
            "E30-R11's response envelopes record no served model id, and its campaign env "
            "requested glm-5.2, which this endpoint answers with glm-5.3 at HTTP 200 and no "
            "warning (re-verified live 2026-09-02, E30_R12_SERVED_MODEL_PROBE_V1.json)",
            "E30-R11 ran under NO registered request-body contract and recorded none, so its "
            "channel condition is unknown as well as its served model",
        ],
        "r12_read_no_endpoint": True,
        "comparison_to_r12": "NOT_A_COMPARISON; E30-R12 produced 0 of 480 evaluations, computed "
                             "no gate and read no endpoint, so there is no R12 result to "
                             "compare R13 with",
        "r12_completed_envelopes_pooled_into_r13": False,
        "shared_with_r11_and_r12": r12["relationship_to_e30_r11"]["shared"],
        "changed_relative_to_r12": [
            "a registered request-body contract, frozen by sha256 over its bytes",
            "output-token budgets re-derived from measurement over every call shape, replacing "
            "the inherited 6000 / 36000 pair",
            "a per-call cap set directly, so the runner's divide-by-call-count no longer gives "
            "different arms different per-call headroom",
            "no budget escalation ladder",
            "a per-envelope channel-configuration record",
            "GR0d channel-contract homogeneity and GR0e channel-behaviour conformance",
            "a channel-behaviour probe in setup, alongside the served-model probe",
            "a setup assertion that the campaign's responses/ and evaluations/ start empty",
        ],
    },

    "substrate": r12["substrate"],
    "arms": r12["arms"],
    "repetitions": 3,
    "expected_responses": 480,
    "expected_evaluations": 480,

    "model_binding": {
        "channel": "anthropic_compatible",
        "base_url": "https://api.z.ai/api/anthropic",
        "requested_model": "glm-5.3",
        "frozen_served_model": "glm-5.3",
        "served_model_assertion": r12["model_binding"]["assertion"],
        "per_envelope_served_model_record": "resource_receipt.served_model_ids",
        "substrate_alert": r12["model_binding"]["substrate_alert"],
        "request_body_contract": {
            "contract_id": CONTRACT,
            "extra_body": arms.CHANNEL_CONTRACTS[CONTRACT],
            "system": arms.ARM_SYSTEM_PROMPT,
            "temperature": 0,
            "contract_sha256": arms.channel_contract_sha256(CONTRACT),
            "fingerprint_covers": ["contract_id", "system", "temperature", "extra_body"],
            "selected_by": "ORION_ARM_CHANNEL_CONTRACT; an unknown value raises "
                           "ChannelContractUnknown rather than falling back to the default",
            "what_is_registered_and_what_is_not":
                "What is registered is the BYTES of the request body and three GATEABLE "
                "PROPERTIES of the response: stop_reason == end_turn, text characters > 0, and "
                "output tokens below the cap. This design does NOT claim that the contract "
                "disables the provider's reasoning: under thinking:{type:disabled} the measured "
                "response still carried a thinking block (745 characters in E30-R12's probe). "
                "Claiming otherwise would be an inference where a measurement is available.",
        },
        "per_envelope_channel_record": "channel_receipt {model_calls, "
                                       "calls_reporting_a_contract, contract_ids, "
                                       "contract_sha256s, stop_reasons, "
                                       "calls_with_zero_text_chars, max_output_tokens_observed}",
        "post_hoc_homogeneity_assertion": "GR0d refuses any contrast unless every response "
                                          "envelope in both arms records exactly one contract "
                                          "sha256 and it equals the frozen one",
    },

    "execution_lane_contract": {
        "why_registered": "E30-R12 registered a primary budget of 6000 and an escalation to "
                          "36000 from pass 3. In execution 116 of 116 failures sat at or above "
                          "the primary cap, and a diagnostic run of one cell at the escalated "
                          "budget closed at 35937 output tokens with a 161644-character "
                          "thinking block and 5895 characters of text after 786 s. Because the "
                          "runner divides the registered total by the arm's call count, "
                          "F0_PARENT_FEDERATION and F2_ORION_METABOLIC_FULL would each have "
                          "received 12000 per call, a third of what one call needed to close.",
        "total_model_calls": note["campaign_arithmetic"]["total_model_calls"],
        "model_calls_per_task_repetition": note["campaign_arithmetic"]["model_calls_per_task_repetition"],
        "calls_per_task_repetition_by_arm": note["campaign_arithmetic"]["calls_per_task_repetition_by_arm"],
        "per_call_output_token_cap": PER_CALL,
        "cap_is_set_per_call_not_as_a_total": "ORION_ARM_MAX_TOKENS is set directly and "
                                              "ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET is unset, so "
                                              "every arm gets the identical per-call cap",
        "derivation": {
            "generator": "e30_r13_budget_note.py, pure arithmetic over "
                         "e30_r13_channel_calibration.py output; no outcome input",
            "rule": derivation["derivation_rule"],
            "calls_measured": derivation["calls_measured"],
            "tasks_measured": derivation["tasks_measured"],
            "arms_measured": derivation["arms_measured"],
            "replicates": derivation["replicates"],
            "calibration_output_tokens": derivation["output_tokens"],
            "calibration_output_tokens_by_stage": derivation["output_tokens_by_stage"],
            "calibration_stop_reasons": derivation["stop_reasons"],
            "calls_with_zero_text_characters": derivation["calls_with_zero_text_chars"],
            "archived_as": "results/E30_R13_BUDGET_NOTE_V1.json and "
                           "results/E30_R13_CHANNEL_CALIBRATION_V1.json",
        },
        "escalation_ladder": "NONE. The cap is derived to be non-binding; a call that stops at "
                             "max_tokens is a GR0e channel-behaviour violation to be reported, "
                             "not a resource shortfall to be topped up mid-campaign. An "
                             "escalation ladder applied after seeing failures is an "
                             "unregistered instrument change.",
        "resumability": "each pass rescans the response envelopes and re-invokes the arm ONLY "
                        "where the response is absent or carries "
                        "EXECUTION_FAILED_MODEL_RESPONSE (an envelope failure holds no model "
                        "output, so re-dispatching it is execution repair, not resampling). A "
                        "COMPLETED_PROPOSAL_ONLY response is never touched.",
        "wall_time_feasibility": {
            "registered_contract": feas,
            "provider_default_at_the_r12_escalated_budget": {
                k: v for k, v in default_feas.items() if k.startswith("concurrency_")},
            "consequence": "under the provider default at E30-R12's registered escalated budget "
                           "the 1080-call campaign does not fit in a single SLURM allocation at "
                           "any concurrency this lane uses; the registered contract is chosen on "
                           "feasibility as well as on correctness",
        },
    },

    "channel_condition_contrast_measured_pre_freeze": {
        "why": "the choice of contract is registered here as a MEASURED instrument choice, "
               "not a preference: three request bodies were run through the same frozen "
               "prompts at the same headroom, outside any campaign tree",
        "headroom_max_tokens_used_for_all_three": 16000,
        "archived_in": [f"results/{f.name}" for f in CALIBRATION_FILES],
        "aggregated_by": "research/experiments/e30-r13/e30_r13_build_design.py, re-derived "
                         "from the archived calibration files by "
                         "tests/unit/test_e30_r13_lane.py",
        "by_contract": CONTRAST,
        "what_it_shows": [
            "the provider default reaches the 16000-token headroom with ZERO text characters "
            "on 3 of 4 tasks, including the SMALLEST task in the frozen set (132571 prompt "
            "characters) -- so E30-R12's description of this signature as affecting 'the "
            "largest tasks' does not hold",
            "its one completing call still used 7418 output tokens, above E30-R12's registered "
            "6000 primary cap",
            "requesting thinking with an explicit budget_tokens of 2048 does NOT change the "
            "outcome: 3 of 4 calls still reach the headroom with zero text. The bound endpoint "
            "does not honour the requested thinking budget, so 'enabled with a small budget' is "
            "not a registrable condition on this channel",
            "under the registered contract all 108 calls ended at end_turn with text, none "
            "reached the cap, and the largest single call used 3292 output tokens",
        ],
    },

    "endpoints": r12["endpoints"],
    "task_dispositions_registered_pre_dispatch": r12["task_dispositions_registered_pre_dispatch"],
    "statistics": dict(r12["statistics"], intervals="paired task bootstrap, 10000 draws, "
                                                    "PROJECT-stratified, seed 20260903"),

    "power_note": {
        "status": "REGISTERED_PRE_DISPATCH",
        "generator": "research/experiments/e30-r12/e30_r12_power_note.py (pure arithmetic, exact "
                     "enumeration, no outcome input); its archived output is carried forward "
                     "unchanged because the substrate, the denominator and the test are "
                     "unchanged",
        "first_step_alpha": r12["power_note"]["first_step_alpha"],
        "arithmetic_floor_at_n40": r12["power_note"]["arithmetic_floor_at_n40"],
        "mde_at_n40_by_discordance": r12["power_note"]["mde_at_n40_by_discordance"],
        "tasks_required_for_80pct_power_at_the_registered_5pp_mid": [430, 863, 1287, 1708],
        "psi_values_for_those_task_counts": [0.10, 0.20, 0.30, 0.40],
        "power_against_the_registered_5pp_mid": [0.0116, 0.0185, 0.0168, 0.0157],
        "plain_statement": r12["power_note"]["plain_statement"],
        "a_non_rejection_is_not_evidence_of_equivalence": True,
        "consequence_for_r13": "E30-R13 is registered as an ESTIMATION AND DIAGNOSTIC study at "
                               "n = 40, exactly as E30-R12 was. It is NOT a powered superiority "
                               "test and a non-rejection is NOT evidence of equivalence.",
        "n_was_reconsidered_and_stays_at_40": {
            "considered": "raising n toward the 430 tasks that 80% power at the 5 pp MID would "
                          "need at psi = 0.10",
            "available_pool": r12["substrate"]["pinned_pool_for_scale_up"],
            "measured_blocker": "the frozen substrate holds prepared solver workspaces and "
                                "baseline lanes for exactly 40 tasks (counted on the campaign "
                                "tree: prepared/solver_public = 40 entries, baseline_lanes = 40 "
                                "entries). Reaching 430 tasks means building ~390 further "
                                "gold-blind workspaces, per-project offline runtimes and "
                                "baseline lanes before a single model call.",
            "decision": "n stays at 40 and the study stays an estimation and diagnostic study. "
                        "E30-R12 died without asking its question; a substrate build that "
                        "consumes the window and leaves the question unasked again reaches the "
                        "same terminal by a longer route.",
            "scale_up_is_pre_registered_as_a_separate_study": True,
            "verdict_carried_forward": r12["power_note"]
                                          ["proposed_scale_up_if_a_powered_test_is_ever_wanted"]["verdict"],
        },
        "repetitions_tradeoff": r12["power_note"]["repetitions_tradeoff"],
    },

    "evaluation_lane": dict(
        r12["evaluation_lane"],
        runner="e30_r13_fullreg_eval.py -- registers an e30r13 cell on the PC-R6 evaluator and "
               "delegates; derived from e30_r12_fullreg_eval.py by substituting the cell name "
               "and the design id, and nothing else",
        campaign_layout_required="run/confirmatory-r{1,2,3}/{responses,evaluations}/<ARM>/"
                                 "<task_id>.json plus frozen_tasks.json",
    ),

    "analysis_lane": {
        "runner": "e30_r13_analysis.py",
        "endpoint_arithmetic": "IMPORTED from research/experiments/e30-r12/e30_r12_analysis.py "
                               "under a sha256 pin asserted at run time. build_tables, family, "
                               "evaluate_gates and route are reused verbatim, so R13's endpoint "
                               "definitions are the same CODE as R12's rather than a similar "
                               "transcription of them. E30-R12's file is frozen and not "
                               "modified.",
        "added_by_r13": ["GR0d CHANNEL_CONTRACT_HOMOGENEITY", "GR0e CHANNEL_BEHAVIOUR_CONFORMANCE"],
        "exit_codes": {"0": "analysis complete, channel gates PASS",
                       "3": "a precondition refused; no endpoint read",
                       "4": "a channel gate FAILED",
                       "5": "a channel gate COULD NOT BE CHECKED"},
        "halt_is_literal": "HALT_NO_GATE_EVALUATION is implemented as a halt, not as a "
                           "routing decision taken afterwards: GR0c, GR0d and GR0e are "
                           "evaluated BEFORE any endpoint table is built, and a non-PASS on "
                           "any of them writes a refusal artifact carrying the gates and the "
                           "terminal and nothing else. A halted run that still emitted "
                           "contrast estimates would leave numbers the design forbids in the "
                           "rollup for a later reader to quote as results.",
        "could_not_check_is_not_a_pass": "GR0d and GR0e return COULD_NOT_CHECK, distinct from "
                                         "PASS and from FAIL, with a distinct process exit code; "
                                         "it routes to EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ",
        "denominators_are_published": "both gates report envelopes_expected, "
                                      "envelopes_with_a_channel_receipt and the model-call "
                                      "counts, so '0 offenders' can never be read out of "
                                      "'0 envelopes examined'",
    },

    "gates": r12["gates"] + [
        {
            "gate_id": "GR0d",
            "name": "CHANNEL_CONTRACT_HOMOGENEITY",
            "hard": True,
            "statement": "every one of the 480 response envelopes carries a channel_receipt "
                         "recording exactly one request-body contract sha256, and it equals the "
                         "registered contract's fingerprint; every model call within every "
                         "envelope reported a contract.",
            "why_it_exists": "E30-R12's GR0c held on all 119 envelopes it saw while the "
                             "experimental condition moved. A gate over the served model id "
                             "cannot see a change in the request body.",
            "compared_by": "sha256 over the contract bytes, not by the contract's label",
            "failure_action": "HALT_NO_GATE_EVALUATION; terminal CHANNEL_CONTRACT_VIOLATION",
            "cannot_check_action": "terminal EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ",
        },
        {
            "gate_id": "GR0e",
            "name": "CHANNEL_BEHAVIOUR_CONFORMANCE",
            "hard": True,
            "statement": "no model call in any response envelope stopped at max_tokens, and no "
                         "model call emitted zero text characters.",
            "why_it_exists": "this is the behavioural half of the same lesson: E30-R12's 116 "
                             "failures were exactly truncation-with-no-text at a correct served "
                             "model id under a correct-looking configuration.",
            "failure_action": "HALT_NO_GATE_EVALUATION; terminal CHANNEL_BEHAVIOUR_VIOLATION",
            "cannot_check_action": "terminal EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ",
        },
    ],

    "routing_precedence": [
        "EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ",
        "CHANNEL_CONTRACT_VIOLATION",
        "CHANNEL_BEHAVIOUR_VIOLATION",
        "LANE_DEFECT",
        "F2_HARMFUL",
        "CRITICAL_REGRESSION",
        "INTERFACE_STILL_BROKEN",
        "FIRST_REGISTERED_POSITIVE",
        "PARENT_SUFFICIENT",
        "NO_ARM_SEPARATION",
    ],
    "routing_precedence_note": "Evaluated in this order; the first matching case is the "
                               "terminal. The channel terminals precede everything because a "
                               "campaign run under an unverified or non-conformant channel "
                               "cannot support any endpoint claim. Hard-gate and adverse "
                               "terminals precede favourable ones.",
    "routing_preregistered": r12["routing_preregistered"],

    "no_rescue_clause": {
        "r13_may_not": r12["no_rescue_clause"]["r12_may_not"] + [
            "reuse E30-R12's campaign directory, or pool its 3 provider-default envelopes",
            "change the registered contract, the cap or any gate after dispatch, for any reason",
            "report a COULD_NOT_CHECK gate as a pass, a null, or an equivalence",
        ],
        "a_null_is_a_result": r12["no_rescue_clause"]["a_null_is_a_result"],
        "parent_sufficient_and_no_arm_separation_are_legitimate_terminals": True,
    },

    "custody": {
        "seed": 20260903,
        "seed_sha256": hashlib.sha256(b"20260903").hexdigest(),
        "seed_disclosure": "The seed is published in the clear here, before dispatch, AND as "
                           "its sha256. A hash-commit-then-reveal protocol would be weaker in "
                           "this study, not stronger: the seed is a bootstrap resampling seed "
                           "compiled into e30_r13_analysis.py, which is frozen and hashed by "
                           "the same pull request as this design, so it is already publicly "
                           "checkable and cannot be re-chosen after an outcome. Claiming a "
                           "commit-and-reveal that was not run would be a rendered status "
                           "standing in for the thing itself.",
        "authorization_object": "PROTECTED_RUN_AUTHORIZATION.json, written into the campaign "
                                "directory by the coordinator (not by a human) and carrying "
                                "coordinator_written: true, the verbatim operator instruction "
                                "with its source, and the exact design sha256. It does NOT "
                                "claim human authorship, because it is not human-written; what "
                                "is asserted is that the human instruction it quotes is present "
                                "and attributed. The dispatch gate refuses to run without it.",
        "authorization_archived_after_use": "the rollup step renames it to "
                                            "PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json, so the "
                                            "dispatch guard re-arms and a later resubmission "
                                            "cannot run on a spent authorization",
        "design_frozen_before_dispatch": True,
        "code_frozen_in_this_pr": [
            "research/experiments/e30-r13/e30_r13_analysis.py",
            "research/experiments/e30-r13/e30_r13_fullreg_eval.py",
            "research/experiments/e30-r13/e30_r13_budget_note.py",
            "research/experiments/e30-r13/e30_r13_channel_calibration.py",
            "research/experiments/e30-r13/e30_r13_build_design.py",
            "research/experiments/e30-r13/sbatch/*",
            "scripts/orion_claude_arms.py",
            "tests/unit/test_e30_r13_lane.py",
        ],
        "gold_blindness": r12["custody"]["gold_blindness"],
        "calibration_custody": "the channel calibration ran on frozen prompts OUTSIDE any "
                               "campaign run tree, recorded token accounting, stop reasons, "
                               "content-block shapes and a JSON-parseability boolean only, "
                               "retained no response text, evaluated no patch, read no gold "
                               "tree and read no endpoint. Its outputs are archived under "
                               "results/ and are not pooled into the campaign.",
        "outputs": ["E30_R13_FULLREG_RAW_ROLLUP_V1.json", "E30_R13_ROLLUP_V1.{json,md}",
                    "E30_R13_OUTCOME_RECEIPT.md", "JOB_IDS.env"],
    },

    "authority": {
        "grants_scientific_truth": False,
        "grants_field_status": False,
        "grants_supertheory_status": False,
        "grants_publication_readiness": False,
        "parent_sufficiency_is_valid_terminal": True,
        "no_arm_separation_is_valid_terminal": True,
    },
}

out = R13 / "E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1.json"
out.write_text(json.dumps(design, indent=2, sort_keys=True) + "\n")
print("WROTE", out)
