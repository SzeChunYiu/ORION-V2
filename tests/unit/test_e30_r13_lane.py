"""Known-answer controls for the E30-R13 lane.

The controls that matter most here are the NEGATIVE ones.  E30-R12 failed because a
condition moved underneath a gate that was only watching the served model id, and the
programme's recurring defect is a check that reports "0 violations" because it never
ran.  So every gate in this lane is tested three ways: it PASSES on a clean fixture, it
FAILS on a fixture that violates exactly the thing it claims to watch, and it reports
COULD_NOT_CHECK -- with its own exit code -- when there is nothing to read.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
R13 = ROOT / "research" / "experiments" / "e30-r13"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


arms = _load("orion_claude_arms_r13", ROOT / "scripts" / "orion_claude_arms.py")
analysis = _load("e30_r13_analysis", R13 / "e30_r13_analysis.py")
budget = _load("e30_r13_budget_note", R13 / "e30_r13_budget_note.py")
calibration = _load("e30_r13_channel_calibration", R13 / "e30_r13_channel_calibration.py")

ARMS = ["F2_ORION_METABOLIC_FULL", "F0_PARENT_FEDERATION", "SAME_MODEL_REFLECTION", "SIMPLE_DIRECT"]
REPS = ["1", "2", "3"]
TASKS = [f"bugsinpy-t-{i}" for i in range(1, 4)]
CONTRACT = "thinking_disabled"
CONTRACT_SHA = arms.channel_contract_sha256(CONTRACT)


# ------------------------------------------------------------------ channel contract
def test_default_contract_is_the_historical_one_so_no_existing_lane_changes(monkeypatch):
    monkeypatch.delenv("ORION_ARM_CHANNEL_CONTRACT", raising=False)
    assert arms.channel_contract_id() == "provider_default"
    assert arms.CHANNEL_CONTRACTS["provider_default"] == {}


def test_an_unknown_contract_fails_closed_rather_than_falling_back(monkeypatch):
    monkeypatch.setenv("ORION_ARM_CHANNEL_CONTRACT", "thinking_disbaled")  # typo on purpose
    with pytest.raises(arms.ChannelContractUnknown):
        arms.channel_contract_id()


def test_contract_fingerprint_separates_contracts_and_is_stable():
    seen = {name: arms.channel_contract_sha256(name) for name in arms.CHANNEL_CONTRACTS}
    assert len(set(seen.values())) == len(seen)
    assert seen == {name: arms.channel_contract_sha256(name) for name in arms.CHANNEL_CONTRACTS}
    assert all(len(v) == 64 for v in seen.values())


def test_the_calibration_probe_measures_the_bytes_the_campaign_will_send():
    """A budget derived from a body different from the dispatched one is worthless."""
    assert calibration.CONTRACTS == arms.CHANNEL_CONTRACTS
    assert calibration.SYSTEM_PROMPT == arms.ARM_SYSTEM_PROMPT
    for name in arms.CHANNEL_CONTRACTS:
        assert calibration.contract_fingerprint(name) == arms.channel_contract_sha256(name)


# -------------------------------------------------------------------- envelope receipt
def _request(arm: str = "SIMPLE_DIRECT") -> dict:
    return {"task_id": "bugsinpy-t-1", "arm_id": arm, "task": {}}


def _usage(**kw):
    base = {"input_tokens": 10, "output_tokens": 20, "_served_model": "glm-5.3",
            "_channel_contract_id": CONTRACT, "_channel_contract_sha256": CONTRACT_SHA,
            "_stop_reason": "end_turn", "_text_chars": 300}
    base.update(kw)
    return base


def test_completed_envelope_carries_the_channel_receipt():
    payload = json.dumps({"patch": "", "diagnosis": "d", "assumptions": [],
                          "uncertainty": "u", "discriminator_or_tests": [], "falsifier": "f"})
    response = arms.run_arm(_request(), call=lambda p: (payload, _usage()),
                            workspace_context="{}")
    receipt = response["channel_receipt"]
    assert receipt["contract_ids"] == [CONTRACT]
    assert receipt["contract_sha256s"] == [CONTRACT_SHA]
    assert receipt["model_calls"] == receipt["calls_reporting_a_contract"] == 1
    assert receipt["stop_reasons"] == ["end_turn"]
    assert receipt["calls_with_zero_text_chars"] == 0


def test_failed_envelope_also_carries_the_channel_receipt():
    """A failure is where the channel record is most diagnostic; R12 had none."""
    response = arms.run_arm(
        _request(), call=lambda p: ("no json here", _usage(_stop_reason="max_tokens",
                                                           _text_chars=0, output_tokens=6000)),
        workspace_context="{}")
    assert response["status"] == "EXECUTION_FAILED_MODEL_RESPONSE"
    receipt = response["channel_receipt"]
    assert receipt["stop_reasons"] == ["max_tokens"]
    assert receipt["calls_with_zero_text_chars"] == 1
    assert receipt["max_output_tokens_observed"] == 6000


def test_a_call_reporting_no_contract_publishes_a_zero_denominator_not_a_pass():
    response = arms.run_arm(
        _request(), call=lambda p: ("no json", {"input_tokens": 1, "output_tokens": 2}),
        workspace_context="{}")
    receipt = response["channel_receipt"]
    assert receipt["model_calls"] == 1
    assert receipt["calls_reporting_a_contract"] == 0
    assert receipt["contract_ids"] == []


# --------------------------------------------------------------------- GR0d / GR0e
def _campaign(tmp_path: Path, receipt_for) -> Path:
    campaign = tmp_path / "campaign"
    for rep in REPS:
        for arm in ARMS:
            directory = campaign / "run" / f"confirmatory-r{rep}" / "responses" / arm
            directory.mkdir(parents=True, exist_ok=True)
            for task in TASKS:
                receipt = receipt_for(rep, arm, task)
                envelope = {"task_id": task, "arm_id": arm, "status": "COMPLETED_PROPOSAL_ONLY"}
                if receipt is not None:
                    envelope["channel_receipt"] = receipt
                (directory / f"{task}.json").write_text(json.dumps(envelope))
    return campaign


def _clean(calls: int = 1, **over):
    receipt = {"model_calls": calls, "calls_reporting_a_contract": calls,
               "contract_ids": [CONTRACT], "contract_sha256s": [CONTRACT_SHA],
               "stop_reasons": ["end_turn"], "calls_with_zero_text_chars": 0,
               "max_output_tokens_observed": 900}
    receipt.update(over)
    return receipt


def _gr0d(campaign: Path):
    return analysis.channel_contract_homogeneity(campaign, ARMS, REPS, TASKS, CONTRACT, CONTRACT_SHA)


def _gr0e(campaign: Path):
    return analysis.channel_behaviour_conformance(campaign, ARMS, REPS, TASKS)


def test_gr0d_passes_on_a_homogeneous_campaign_and_publishes_denominators(tmp_path):
    gate = _gr0d(_campaign(tmp_path, lambda r, a, t: _clean()))
    assert gate["status"] == "PASS"
    assert gate["envelopes_read"] == gate["envelopes_expected"] == len(REPS) * len(ARMS) * len(TASKS)
    assert gate["envelopes_with_a_channel_receipt"] == gate["envelopes_expected"]
    assert gate["model_calls_reporting_a_contract"] == gate["model_calls_seen"] > 0
    assert gate["offender_count"] == 0


def test_gr0d_fails_when_one_envelope_used_a_different_contract(tmp_path):
    other = arms.channel_contract_sha256("provider_default")

    def receipt_for(rep, arm, task):
        if (rep, arm, task) == ("2", "SIMPLE_DIRECT", TASKS[1]):
            return _clean(contract_ids=["provider_default"], contract_sha256s=[other])
        return _clean()

    gate = _gr0d(_campaign(tmp_path, receipt_for))
    assert gate["status"] == "FAIL"
    assert len(gate["contract_sha256_counts"]) == 2
    reasons = {o["reason"] for o in gate["offenders"]}
    assert {"CONTRACT_ID_MISMATCH", "CONTRACT_SHA256_MISMATCH"} <= reasons


def test_gr0d_fails_when_an_envelope_mixes_two_contracts_within_itself(tmp_path):
    other = arms.channel_contract_sha256("provider_default")
    mixed = _clean(calls=3, contract_ids=[CONTRACT, "provider_default"],
                   contract_sha256s=[CONTRACT_SHA, other])
    gate = _gr0d(_campaign(tmp_path, lambda r, a, t: mixed if a == "SIMPLE_DIRECT" else _clean()))
    assert gate["status"] == "FAIL"
    assert "CONTRACT_IDS_NOT_A_SINGLETON" in {o["reason"] for o in gate["offenders"]}


def test_gr0d_fails_when_some_calls_reported_no_contract_at_all(tmp_path):
    partial = _clean(calls=3, calls_reporting_a_contract=2)
    gate = _gr0d(_campaign(tmp_path, lambda r, a, t: partial if a == "F0_PARENT_FEDERATION" else _clean()))
    assert gate["status"] == "FAIL"
    assert "CALLS_WITHOUT_A_REPORTED_CONTRACT" in {o["reason"] for o in gate["offenders"]}


def test_gr0d_reports_could_not_check_rather_than_pass_when_no_receipt_exists(tmp_path):
    gate = _gr0d(_campaign(tmp_path, lambda r, a, t: None))
    assert gate["status"] == "COULD_NOT_CHECK"
    assert gate["envelopes_read"] == gate["envelopes_expected"]
    assert gate["envelopes_with_a_channel_receipt"] == 0


def test_gr0d_flags_missing_responses_instead_of_shrinking_its_denominator(tmp_path):
    campaign = _campaign(tmp_path, lambda r, a, t: _clean())
    (campaign / "run" / "confirmatory-r1" / "responses" / "SIMPLE_DIRECT" / f"{TASKS[0]}.json").unlink()
    gate = _gr0d(campaign)
    assert gate["status"] == "FAIL"
    assert gate["envelopes_read"] == gate["envelopes_expected"] - 1
    assert "RESPONSE_MISSING" in {o["reason"] for o in gate["offenders"]}


def test_gr0e_passes_on_a_conformant_campaign(tmp_path):
    gate = _gr0e(_campaign(tmp_path, lambda r, a, t: _clean()))
    assert gate["status"] == "PASS"
    assert gate["envelopes_with_a_channel_receipt"] == gate["envelopes_expected"]
    assert gate["model_calls_checked"] > 0
    assert gate["stop_reason_counts"] == {"end_turn": gate["envelopes_expected"]}


def test_gr0e_fails_on_the_exact_r12_signature_truncated_with_no_text(tmp_path):
    starved = _clean(stop_reasons=["max_tokens"], calls_with_zero_text_chars=1,
                     max_output_tokens_observed=6000)
    gate = _gr0e(_campaign(tmp_path, lambda r, a, t: starved if t == TASKS[0] else _clean()))
    assert gate["status"] == "FAIL"
    reasons = {o["reason"] for o in gate["offenders"]}
    assert {"CALL_TRUNCATED_AT_MAX_TOKENS", "CALL_EMITTED_ZERO_TEXT_CHARACTERS"} <= reasons


def test_gr0e_reports_could_not_check_when_there_is_nothing_to_read(tmp_path):
    gate = _gr0e(_campaign(tmp_path, lambda r, a, t: None))
    assert gate["status"] == "COULD_NOT_CHECK"
    assert gate["model_calls_checked"] == 0


# ------------------------------------------------------------------------- routing
class _R12Stub:
    @staticmethod
    def route(gates, per_arm):
        return {"terminal": "DELEGATED_TO_R12", "detail": "reached the imported routing"}


def test_a_could_not_check_channel_gate_is_not_a_null(tmp_path):
    routing = analysis.route_with_channel_gates(
        _R12Stub, {"GR0d": {"status": "COULD_NOT_CHECK", "name": "n", "offender_count": 0,
                            "envelopes_with_a_channel_receipt": 0},
                   "GR0e": {"status": "PASS", "name": "n", "offender_count": 0,
                            "envelopes_with_a_channel_receipt": 1}}, {})
    assert routing["terminal"] == "EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ"


def test_channel_gate_failures_route_to_their_own_terminals():
    fail = {"status": "FAIL", "name": "n", "offender_count": 3, "envelopes_with_a_channel_receipt": 9}
    ok = {"status": "PASS", "name": "n", "offender_count": 0, "envelopes_with_a_channel_receipt": 9}
    assert analysis.route_with_channel_gates(_R12Stub, {"GR0d": fail, "GR0e": ok}, {})["terminal"] \
        == "CHANNEL_CONTRACT_VIOLATION"
    assert analysis.route_with_channel_gates(_R12Stub, {"GR0d": ok, "GR0e": fail}, {})["terminal"] \
        == "CHANNEL_BEHAVIOUR_VIOLATION"
    assert analysis.route_with_channel_gates(_R12Stub, {"GR0d": ok, "GR0e": ok}, {})["terminal"] \
        == "DELEGATED_TO_R12"


def test_could_not_check_and_fail_do_not_share_an_exit_code():
    codes = {analysis.EXIT_OK, analysis.EXIT_PRECONDITION_REFUSED,
             analysis.EXIT_GATE_FAIL, analysis.EXIT_GATE_COULD_NOT_CHECK}
    assert len(codes) == 4


# ------------------------------------------------------- imported R12 arithmetic pin
def test_the_r12_analysis_import_is_sha_pinned(tmp_path):
    path = ROOT / "research" / "experiments" / "e30-r12" / "e30_r12_analysis.py"
    real = hashlib.sha256(path.read_bytes()).hexdigest()
    module, got = analysis.load_r12_analysis(path, real)
    assert got == real and hasattr(module, "build_tables") and hasattr(module, "route")
    with pytest.raises(analysis.AnalysisRefused):
        analysis.load_r12_analysis(path, "0" * 64)


# ------------------------------------------------------------------- budget note
def test_the_campaign_issues_1080_model_calls_not_480():
    assert budget.CALLS_PER_TASK_REPETITION == 1 + 2 + 3 + 3 == 9
    assert budget.TOTAL_CALLS == 9 * 40 * 3 == 1080


def _call(out: int, stop: str = "end_turn", stage: str = "final", arm: str = "SIMPLE_DIRECT"):
    return {"contract_id": CONTRACT, "output_tokens": out, "stop_reason": stop,
            "stage_id": stage, "arm_id": arm, "task_id": "bugsinpy-t-1", "replicate": 1,
            "text_chars": 100, "json_object_parseable": True, "wall_seconds": 20.0}


def test_budget_refuses_to_derive_from_a_censored_distribution():
    """A draw that hit the headroom is a floor, not a maximum; 4x a floor means nothing."""
    result = budget.derive([_call(500), _call(16000, stop="max_tokens")])
    assert result["status"] == "COULD_NOT_DERIVE"
    assert "censored" in result["reason"]


def test_budget_refuses_when_there_is_nothing_to_derive_from():
    assert budget.derive([])["status"] == "COULD_NOT_DERIVE"


def test_budget_applies_the_registered_rule_to_the_observed_maximum():
    result = budget.derive([_call(500), _call(2620), _call(1100)])
    assert result["status"] == "DERIVED"
    assert result["output_tokens"]["max"] == 2620
    assert result["registered_per_call_max_tokens"] == 1000 * ((4 * 2620 + 999) // 1000) == 11000


def test_feasibility_arithmetic_is_over_calls_not_envelopes():
    fast = budget.feasibility(20.0, 4)
    assert fast["total_model_calls"] == 1080
    assert fast["fits_in_one_slurm_allocation"] is True
    slow = budget.feasibility(785.810107, 2)
    assert slow["wall_hours_at_concurrency"] > budget.SLURM_TIME_LIMIT_HOURS
    assert slow["fits_in_one_slurm_allocation"] is False


# --------------------------------------------------------------------- design freeze
DESIGN_PATH = R13 / "E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1.json"


@pytest.mark.skipif(not DESIGN_PATH.is_file(), reason="design not yet written")
def test_design_is_prospective_and_carries_the_registered_power_boundary():
    design = json.loads(DESIGN_PATH.read_text())
    assert design["status"] == "PROSPECTIVE_REGISTERED_DESIGN_NO_RESULTS"
    power = design["power_note"]
    assert power["arithmetic_floor_at_n40"]["min_all_one_directional_discordant_tasks"] == 7
    assert power["arithmetic_floor_at_n40"]["implied_minimum_observable_risk_difference"] == 0.175
    assert power["tasks_required_for_80pct_power_at_the_registered_5pp_mid"] == [430, 863, 1287, 1708]
    assert power["a_non_rejection_is_not_evidence_of_equivalence"] is True
    assert design["authority"]["parent_sufficiency_is_valid_terminal"] is True
    assert design["authority"]["no_arm_separation_is_valid_terminal"] is True
    assert design["relationship_to_earlier_runs"]["r11_served_model"] == "INFERRED_NOT_VERIFIED"
    assert design["relationship_to_earlier_runs"]["comparison_to_r11"] == "DESCRIPTIVE_ONLY"
    assert design["substrate"]["task_count"] == 40


@pytest.mark.skipif(not DESIGN_PATH.is_file(), reason="design not yet written")
def test_design_carries_the_three_way_channel_contrast_it_claims_to_have_measured():
    """The contract is registered as a measured choice; the measurement must be there."""
    design = json.loads(DESIGN_PATH.read_text())
    contrast = design["channel_condition_contrast_measured_pre_freeze"]["by_contract"]
    assert set(contrast) == set(arms.CHANNEL_CONTRACTS)
    registered = design["model_binding"]["request_body_contract"]["contract_id"]
    winner = contrast[registered]
    # The registered contract is the one measured to end its turns and emit text.
    assert winner["stop_reasons"] == {"end_turn": winner["calls"]}
    assert winner["calls_with_zero_text"] == 0
    assert winner["calls"] >= 100
    for name, row in contrast.items():
        assert row["contract_sha256"] == arms.channel_contract_sha256(name)
    # The derived cap must sit strictly above the largest call actually measured.
    cap = design["execution_lane_contract"]["per_call_output_token_cap"]
    assert cap > winner["max_output_tokens"]


@pytest.mark.skipif(not DESIGN_PATH.is_file(), reason="design not yet written")
def test_design_registers_the_contract_by_bytes_and_matches_the_executable():
    design = json.loads(DESIGN_PATH.read_text())
    binding = design["model_binding"]["request_body_contract"]
    assert binding["contract_id"] in arms.CHANNEL_CONTRACTS
    assert binding["extra_body"] == arms.CHANNEL_CONTRACTS[binding["contract_id"]]
    assert binding["contract_sha256"] == arms.channel_contract_sha256(binding["contract_id"])
    assert binding["system"] == arms.ARM_SYSTEM_PROMPT
