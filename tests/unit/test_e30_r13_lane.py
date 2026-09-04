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


def test_a_halted_run_routes_without_any_endpoint_table_existing():
    """HALT_NO_GATE_EVALUATION, taken literally: the terminal must be reachable with none."""
    fail = {"status": "FAIL", "name": "n", "offender_count": 3}
    ok = {"status": "PASS", "name": "n", "offender_count": 0}
    cannot = {"status": "COULD_NOT_CHECK", "name": "n", "offender_count": 0}
    assert analysis.hard_gate_terminal({"GR0c": ok, "GR0d": fail, "GR0e": ok})["terminal"] \
        == "CHANNEL_CONTRACT_VIOLATION"
    assert analysis.hard_gate_terminal({"GR0c": ok, "GR0d": ok, "GR0e": fail})["terminal"] \
        == "CHANNEL_BEHAVIOUR_VIOLATION"
    assert analysis.hard_gate_terminal({"GR0c": fail, "GR0d": ok, "GR0e": ok})["terminal"] \
        == "LANE_DEFECT"
    assert analysis.hard_gate_terminal({"GR0c": ok, "GR0d": cannot, "GR0e": ok})["terminal"] \
        == "EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ"
    # The channel gates precede the served-model gate, as the registered precedence says.
    assert analysis.hard_gate_terminal({"GR0c": fail, "GR0d": fail, "GR0e": ok})["terminal"] \
        == "CHANNEL_CONTRACT_VIOLATION"
    with pytest.raises(AssertionError):
        analysis.hard_gate_terminal({"GR0c": ok, "GR0d": ok, "GR0e": ok})


def test_the_refusal_artifact_carries_no_endpoint_number():
    """A halted run must not leave contrast estimates a later reader could quote."""
    refusal = {
        "routing": {"terminal": "CHANNEL_CONTRACT_VIOLATION", "detail": "d"},
        "gates": {
            "GR0c": {"name": "SERVED_MODEL_HOMOGENEITY", "status": "PASS",
                     "envelopes_read": 480, "offender_count": 0},
            "GR0d": {"name": "CHANNEL_CONTRACT_HOMOGENEITY", "status": "FAIL",
                     "envelopes_with_a_channel_receipt": 480, "envelopes_expected": 480,
                     "offender_count": 7},
            "GR0e": {"name": "CHANNEL_BEHAVIOUR_CONFORMANCE", "status": "PASS",
                     "envelopes_with_a_channel_receipt": 480, "envelopes_expected": 480,
                     "offender_count": 0},
        },
    }
    rendered = analysis.render_refusal_markdown(refusal)
    assert "None read." in rendered
    assert "evidence of equivalence" in rendered
    for forbidden in ("risk difference", "Holm", "exact p", "E1 rate", "apply rate"):
        assert forbidden not in rendered, forbidden


def test_the_rollup_driver_archives_the_authorization_even_on_a_gate_terminal():
    """Exits 4 and 5 are registered terminals; set -e must not skip the archive on them."""
    rollup = _sbatch("e30_r13_rollup_and_analysis.sbatch")
    assert "ANALYSIS_RC=0" in rollup
    assert "|| ANALYSIS_RC=$?" in rollup
    assert rollup.index("|| ANALYSIS_RC=$?") < rollup.index("PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json")
    assert rollup.rstrip().endswith('exit "$ANALYSIS_RC"')


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


# ----------------------------------------------------------------- execution tally
tally = _load("e30_r13_execution_tally", R13 / "e30_r13_execution_tally.py")


def _tally_campaign(tmp_path: Path, receipt_for, status="COMPLETED_PROPOSAL_ONLY") -> Path:
    campaign = tmp_path / "campaign"
    (campaign / "run" / "confirmatory-r1").mkdir(parents=True)
    (campaign / "run" / "confirmatory-r1" / "frozen_tasks.json").write_text(
        json.dumps({"tasks": [{"task_id": t} for t in TASKS]}))
    for rep in tally.REPS:
        for arm in tally.ARMS:
            directory = campaign / "run" / f"confirmatory-r{rep}" / "responses" / arm
            directory.mkdir(parents=True, exist_ok=True)
            for task in TASKS:
                envelope = {"task_id": task, "arm_id": arm, "status": status,
                            "resource_receipt": {"output_tokens": 900, "wall_time_seconds": 20.0,
                                                 "served_model_ids": ["glm-5.3"]}}
                receipt = receipt_for(rep, arm, task)
                if receipt is not None:
                    envelope["channel_receipt"] = receipt
                (directory / f"{task}.json").write_text(json.dumps(envelope))
    return campaign


def test_the_tally_publishes_denominators_for_every_count(tmp_path):
    campaign = _tally_campaign(tmp_path, lambda r, a, t: _clean())
    out = tmp_path / "tally.json"
    assert tally.main(["--campaign", str(campaign), "--out", str(out)]) == 0
    payload = json.loads(out.read_text())
    expected = len(tally.REPS) * len(tally.ARMS) * len(TASKS)
    assert payload["envelopes_expected"] == payload["envelopes_written"] == expected
    channel = payload["channel_receipts"]
    assert channel["envelopes_with_a_channel_receipt"] == channel["envelopes_expected"] == expected
    assert channel["model_calls_reporting_a_contract"] == channel["model_calls_seen"] == expected
    assert payload["non_completed_envelope_count"] == 0
    assert payload["computes_no_endpoint_no_contrast_no_gate"] is True


def test_the_tally_never_hides_a_missing_or_receiptless_envelope(tmp_path):
    campaign = _tally_campaign(tmp_path, lambda r, a, t: None if a == "SIMPLE_DIRECT" else _clean(),
                               status="EXECUTION_FAILED_MODEL_RESPONSE")
    (campaign / "run" / "confirmatory-r2" / "responses" / "SIMPLE_DIRECT" / f"{TASKS[0]}.json").unlink()
    out = tmp_path / "tally.json"
    assert tally.main(["--campaign", str(campaign), "--out", str(out)]) == 0
    payload = json.loads(out.read_text())
    expected = len(tally.REPS) * len(tally.ARMS) * len(TASKS)
    assert payload["statuses"]["MISSING"] == 1
    assert payload["envelopes_written"] == expected - 1
    # SIMPLE_DIRECT carries no channel receipt: the shortfall must be visible, not absorbed.
    assert payload["channel_receipts"]["envelopes_with_a_channel_receipt"] < expected - 1
    assert payload["non_completed_envelope_count"] == expected - 1


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
def test_the_contrast_block_is_re_derivable_from_the_archived_calibration_files():
    """A derived number nobody can re-derive is a claim, not a measurement.

    The block is produced by e30_r13_build_design.py. This test recomputes it from the
    archived files independently, so a builder bug or a hand-edit of the design fails
    here rather than being registered.
    """
    design = json.loads(DESIGN_PATH.read_text())
    block = design["channel_condition_contrast_measured_pre_freeze"]
    files = sorted(f for f in (R13 / "results").glob("E30_R13_CALIBRATION_*.json")
                   if f.name != "E30_R13_CALIBRATION_PROVENANCE_V1.json")
    assert [f"results/{f.name}" for f in files] == block["archived_in"]

    expected: dict[str, dict] = {}
    for path in files:
        for name, summary in json.loads(path.read_text())["summary"].items():
            row = expected.setdefault(name, {
                "calls": 0, "stop_reasons": {}, "calls_with_zero_text": 0,
                "max_output_tokens": 0, "min_output_tokens": None,
                "parsed": [0, 0], "contract_sha256": summary["contract_sha256"]})
            row["calls"] += summary["calls"]
            for reason, count in summary["stop_reasons"].items():
                row["stop_reasons"][reason] = row["stop_reasons"].get(reason, 0) + count
            row["calls_with_zero_text"] += summary["text_chars_zero_calls"]
            row["max_output_tokens"] = max(row["max_output_tokens"], summary["output_tokens"]["max"])
            low = summary["output_tokens"]["min"]
            row["min_output_tokens"] = low if row["min_output_tokens"] is None else min(row["min_output_tokens"], low)
            ok, total = summary["json_parseable_final_calls"].split("/")
            row["parsed"][0] += int(ok)
            row["parsed"][1] += int(total)
    for name, row in expected.items():
        ok, total = row.pop("parsed")
        row["json_parseable_final_calls"] = f"{ok}/{total}"
    assert block["by_contract"] == expected


@pytest.mark.skipif(not DESIGN_PATH.is_file(), reason="design not yet written")
def test_the_seed_is_published_plainly_and_its_digest_is_the_digest_of_that_seed():
    """No claim of a commit-and-reveal protocol that was not run."""
    design = json.loads(DESIGN_PATH.read_text())
    custody = design["custody"]
    assert "seed_sha256_published_pre_run" not in custody
    assert custody["seed_sha256"] == hashlib.sha256(str(custody["seed"]).encode()).hexdigest()
    assert custody["seed"] == analysis.SEED
    assert "PROTECTED_RUN_AUTHORIZATION.json" in custody["authorization_object"]
    assert "PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json" in custody["authorization_archived_after_use"]


SBATCH = R13 / "sbatch"


def _sbatch(name: str) -> str:
    return (SBATCH / name).read_text()


def test_setup_asserts_the_dispatched_cap_equals_the_registered_cap():
    """GR0e catches truncation; only this catches a cap that is simply the wrong number."""
    setup = _sbatch("e30_r13_setup.sbatch")
    assert "E30R13_PER_CALL_MAX_TOKENS" in setup
    assert 'per_call_output_token_cap' in setup
    assert "per-call cap {cap} != registered {registered_cap}" in setup


def test_the_emptiness_assertion_is_gated_so_a_resume_is_not_blocked_by_it():
    setup = _sbatch("e30_r13_setup.sbatch")
    assert "first_setup_completed" in setup
    assert setup.index('if [ -f "$FIRST_SETUP" ]') < setup.index("<<'EMPTY'")


def test_the_agents_lane_sets_a_per_call_cap_and_no_total_budget():
    agents = _sbatch("e30_r13_agents.sbatch")
    assert "export ORION_ARM_MAX_TOKENS=" in agents
    assert "unset ORION_ARM_TOTAL_OUTPUT_TOKEN_BUDGET" in agents
    # No escalation ladder: raising a budget after seeing failures is an unregistered
    # instrument change made post-dispatch.
    assert "ESCALATED_BUDGET" not in agents
    assert "ESCALATE_FROM_PASS" not in agents
    assert "PROTECTED_RUN_AUTHORIZATION.json" in agents


def test_the_rollup_lane_archives_the_authorization_so_the_guard_re_arms():
    rollup = _sbatch("e30_r13_rollup_and_analysis.sbatch")
    assert "PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json" in rollup
    assert "--channel-contract" in rollup and "--channel-contract-sha256" in rollup
    assert "--r12-analysis-sha256" in rollup


def test_the_workflow_uses_no_yaml_anchor():
    """GitHub Actions does not resolve anchors, and yaml.safe_load hides that."""
    workflow = (ROOT / ".github" / "workflows" / "e30-r13-lane.yml").read_text()
    assert "&r13paths" not in workflow and "*r13paths" not in workflow
    assert workflow.count('- "research/experiments/e30-r13/**"') == 2


@pytest.mark.skipif(not DESIGN_PATH.is_file(), reason="design not yet written")
def test_design_registers_the_contract_by_bytes_and_matches_the_executable():
    design = json.loads(DESIGN_PATH.read_text())
    binding = design["model_binding"]["request_body_contract"]
    assert binding["contract_id"] in arms.CHANNEL_CONTRACTS
    assert binding["extra_body"] == arms.CHANNEL_CONTRACTS[binding["contract_id"]]
    assert binding["contract_sha256"] == arms.channel_contract_sha256(binding["contract_id"])
    assert binding["system"] == arms.ARM_SYSTEM_PROMPT


# ------------------------------------------------------------- outcome verification
verification = _load("e30_r13_outcome_verification",
                     R13 / "e30_r13_outcome_verification.py")


def _cell(counts, applied):
    """A minimal raw-rollup cell.

    ``counts[arm][task]`` is the per-repetition critical-new-failure count (``None`` for
    uncountable); ``applied[arm]`` is the set of ``(rep, task)`` slots that applied.
    """
    evaluations = {}
    for arm in ARMS:
        for task in TASKS:
            entries = {}
            for i, rep in enumerate(REPS):
                entries[f"r{rep}"] = {
                    "critical_new_failure_count": counts[arm][task][i],
                    "patch_apply_returncode": 0 if (f"r{rep}", task) in applied[arm] else 1,
                }
            evaluations[f"{arm}/{task}"] = entries
    return {
        "arms": ARMS, "reps": REPS, "task_ids": TASKS,
        "baselines": {task: {"status": "OK"} for task in TASKS},
        "evaluations": evaluations,
        "arm_totals": {arm: {"counted": sum(
            1 for task in TASKS for v in counts[arm][task] if v is not None)} for arm in ARMS},
    }


def test_e2_denominator_helper_counts_tasks_by_majority_not_countable_evaluations():
    """One uncountable repetition still leaves a task checkable; two do not."""
    counts = {arm: {task: [0, 0, 0] for task in TASKS} for arm in ARMS}
    counts[ARMS[0]][TASKS[0]] = [0, 0, None]         # majority resolves -> still checkable
    counts[ARMS[0]][TASKS[1]] = [None, None, None]   # nothing to resolve -> not checkable
    cell = _cell(counts, {arm: set() for arm in ARMS})
    assert verification.e2_checkable_by_majority(cell, ARMS[0], []) == 2
    assert verification.e2_checkable_by_majority(cell, ARMS[1], []) == len(TASKS)
    # Countable EVALUATIONS for that arm is 5: neither the checkable-task count (2) nor
    # three times it (6).  Quoting one where the receipt means the other is the defect
    # this helper exists to prevent.
    assert cell["arm_totals"][ARMS[0]]["counted"] == 5
    # An excluded task leaves the denominator, with count.
    assert verification.e2_checkable_by_majority(cell, ARMS[1], [TASKS[0]]) == len(TASKS) - 1


def test_applied_set_helper_distinguishes_equal_counts_from_the_same_slots():
    applied = {arm: set() for arm in ARMS}
    applied[ARMS[0]] = {("r1", TASKS[0]), ("r1", TASKS[1])}
    applied[ARMS[1]] = {("r1", TASKS[0]), ("r2", TASKS[1])}   # same size, different slots
    counts = {arm: {task: [0, 0, 0] for task in TASKS} for arm in ARMS}
    cell = _cell(counts, applied)
    left = verification.applied_set(cell, ARMS[0])
    right = verification.applied_set(cell, ARMS[1])
    assert len(left) == len(right) == 2
    assert left != right and len(left & right) == 1


def test_per_arm_channel_load_reads_each_arm_separately(tmp_path):
    campaign = _campaign(tmp_path, lambda r, a, t: _clean(calls=3 if a == ARMS[0] else 1))
    load = verification.per_arm_channel_load(campaign, ARMS, REPS, TASKS)
    envelopes = len(REPS) * len(TASKS)
    assert load[ARMS[0]]["model_calls"] == 3 * envelopes
    assert load[ARMS[0]]["calls_per_envelope"] == 3.0
    assert load[ARMS[1]]["calls_per_envelope"] == 1.0
    assert all(item["envelopes"] == envelopes for item in load.values())


def test_exit_code_gives_could_not_check_its_own_code_and_never_hides_a_failure():
    assert verification.exit_code([{"status": "PASS"}]) == 0
    assert verification.exit_code([{"status": "PASS"}, {"status": "COULD_NOT_CHECK"}]) == 5
    assert verification.exit_code([{"status": "PASS"}, {"status": "FAIL"}]) == 4
    # A FAIL alongside a COULD_NOT_CHECK still reports the failure.
    assert verification.exit_code([{"status": "COULD_NOT_CHECK"}, {"status": "FAIL"}]) == 4


def _rollup(cell, *, gr1="FAIL", gr3_n=8, terminal="INTERFACE_STILL_BROKEN"):
    per_arm = {arm: {"E1_rate": 0.25 if arm == "F2_ORION_METABOLIC_FULL" else 0.15,
                     "E2_tasks_checkable": verification.e2_checkable_by_majority(cell, arm, [])}
               for arm in ARMS}
    return {
        "seed": 20260903, "denominators": {"E1": len(TASKS)}, "E2_excluded_task_ids": [],
        "per_arm": per_arm, "routing": {"terminal": terminal},
        "gates": {
            "GR0c": {"status": "PASS"},
            "GR0d": {"status": "PASS", "expected_contract_id": CONTRACT,
                     "expected_contract_sha256": CONTRACT_SHA,
                     "envelopes_read": len(REPS) * len(ARMS) * len(TASKS),
                     "model_calls_seen": len(REPS) * len(ARMS) * len(TASKS),
                     "offender_count": 0},
            "GR0e": {"status": "PASS", "offender_count": 0,
                     "stop_reason_counts": {"end_turn": len(REPS) * len(ARMS) * len(TASKS)},
                     "max_output_tokens_observed": 900},
            "GR1": {"status": gr1}, "GR2": {"status": "NULL", "direction": None},
            "GR3": {"status": "PASS", "checkable_paired_tasks": gr3_n, "margin": 0.02,
                    "one_sided_97_5_upper_bound": 0.0},
        },
    }


def _fixture(tmp_path, receipt_for=None):
    counts = {arm: {task: [0, 0, 0] for task in TASKS} for arm in ARMS}
    applied = {arm: {("r1", TASKS[0])} for arm in ARMS}
    applied[ARMS[1]] = {("r2", TASKS[0])}       # same size, different slots
    cell = _cell(counts, applied)
    campaign = _campaign(tmp_path, receipt_for or (lambda r, a, t: _clean()))
    (campaign / "PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json").write_text("{}")
    raw = {"complete": True, "cells": {"e30r13": cell}}
    design = {"execution_lane_contract": {"calls_per_task_repetition_by_arm":
                                          {arm: 1 for arm in ARMS}}}
    return campaign, _rollup(cell), raw, design


def test_the_verifier_passes_on_a_clean_fixture_and_names_every_check(tmp_path):
    campaign, rollup, raw, design = _fixture(tmp_path)
    checks = verification.run_checks(campaign, rollup, raw, analysis, None, design)
    by_id = {c["check_id"]: c for c in checks}
    # V2 has no E30-R12 archive here, and must say so rather than pass.
    assert by_id["V2_predicates_replayed_on_e30_r12"]["status"] == "COULD_NOT_CHECK"
    assert verification.exit_code(checks) == 5
    others = [c for c in checks if c["check_id"] != "V2_predicates_replayed_on_e30_r12"]
    assert {c["status"] for c in others} == {"PASS"}, [
        (c["check_id"], c["status"]) for c in others if c["status"] != "PASS"]


def test_the_verifier_fails_when_the_published_gate_does_not_reproduce(tmp_path):
    campaign, rollup, raw, design = _fixture(tmp_path)
    # The published receipt claims a larger denominator than the envelopes support.
    rollup["gates"]["GR0d"]["envelopes_read"] += 1
    checks = verification.run_checks(campaign, rollup, raw, analysis, None, design)
    by_id = {c["check_id"]: c for c in checks}
    assert by_id["V1_channel_gates_reproduce_from_envelopes"]["status"] == "FAIL"
    assert verification.exit_code(checks) == 4


def test_the_verifier_fails_when_two_arms_share_the_same_applied_slots(tmp_path):
    campaign, rollup, raw, design = _fixture(tmp_path)
    cell = raw["cells"]["e30r13"]
    for task in TASKS:                       # make F0's applied slots identical to F2's
        for rep in REPS:
            cell["evaluations"][f"F0_PARENT_FEDERATION/{task}"][f"r{rep}"][
                "patch_apply_returncode"] = cell["evaluations"][
                    f"F2_ORION_METABOLIC_FULL/{task}"][f"r{rep}"]["patch_apply_returncode"]
    checks = verification.run_checks(campaign, rollup, raw, analysis, None, design)
    by_id = {c["check_id"]: c for c in checks}
    assert by_id["V5_equal_apply_counts_are_coincidence_not_shared_state"]["status"] == "FAIL"


def test_the_verifier_fails_when_the_terminal_is_not_the_first_firing_clause(tmp_path):
    campaign, rollup, raw, design = _fixture(tmp_path)
    rollup["routing"]["terminal"] = "NO_ARM_SEPARATION"   # GR1 FAIL preempts this
    checks = verification.run_checks(campaign, rollup, raw, analysis, None, design)
    by_id = {c["check_id"]: c for c in checks}
    assert by_id["V8_terminal_is_the_first_firing_registered_clause"]["status"] == "FAIL"


def test_the_verifier_fails_when_a_live_authorization_was_left_in_place(tmp_path):
    campaign, rollup, raw, design = _fixture(tmp_path)
    (campaign / "PROTECTED_RUN_AUTHORIZATION.json").write_text("{}")
    checks = verification.run_checks(campaign, rollup, raw, analysis, None, design)
    by_id = {c["check_id"]: c for c in checks}
    assert by_id["V10_authorization_archived_and_guard_rearmed"]["status"] == "FAIL"


def test_the_verifier_fails_when_the_measured_load_contradicts_the_contract(tmp_path):
    campaign, rollup, raw, design = _fixture(tmp_path)
    design["execution_lane_contract"]["calls_per_task_repetition_by_arm"] = {
        ARMS[0]: 3, ARMS[1]: 1, ARMS[2]: 1, ARMS[3]: 1}    # contract says they differ
    checks = verification.run_checks(campaign, rollup, raw, analysis, None, design)
    by_id = {c["check_id"]: c for c in checks}
    # every fixture envelope makes one call, so the measured load contradicts the contract
    check = by_id["V4_per_arm_channel_load_matches_the_registered_contract"]
    assert check["status"] == "FAIL" and check["conforms"] is False


def test_the_verifier_reports_a_uniform_load_without_calling_it_a_violation(tmp_path):
    """Uniformity is a property of the design, not a defect the verifier invents."""
    campaign, rollup, raw, design = _fixture(tmp_path)
    checks = verification.run_checks(campaign, rollup, raw, analysis, None, design)
    check = {c["check_id"]: c for c in checks}[
        "V4_per_arm_channel_load_matches_the_registered_contract"]
    assert check["status"] == "PASS" and check["distinct_call_totals"] == 1


def test_the_verifier_replays_the_predicates_on_an_unreceipted_campaign(tmp_path):
    """The E30-R12 shape: envelopes present, no channel receipt anywhere."""
    campaign, rollup, raw, design = _fixture(tmp_path)
    r12 = _campaign(tmp_path / "r12", lambda r, a, t: None)
    checks = verification.run_checks(campaign, rollup, raw, analysis, r12, design)
    by_id = {c["check_id"]: c for c in checks}
    replay = by_id["V2_predicates_replayed_on_e30_r12"]
    assert replay["status"] == "PASS"
    assert replay["gr0d_status"] == replay["gr0e_status"] == "COULD_NOT_CHECK"
    assert replay["terminal"] == "EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ"
    assert replay["envelopes_with_a_channel_receipt"] == 0
    assert replay["envelopes_read"] == len(REPS) * len(ARMS) * len(TASKS)


def test_the_verifier_would_fail_the_replay_if_an_unreceipted_campaign_passed(tmp_path):
    """A receipted R12 stand-in must NOT reach the could-not-check terminal."""
    campaign, rollup, raw, design = _fixture(tmp_path)
    r12 = _campaign(tmp_path / "r12", lambda r, a, t: _clean())
    checks = verification.run_checks(campaign, rollup, raw, analysis, r12, design)
    by_id = {c["check_id"]: c for c in checks}
    assert by_id["V2_predicates_replayed_on_e30_r12"]["status"] == "FAIL"


def test_the_archived_verification_receipt_matches_this_module(tmp_path):
    """The committed receipt was produced by this code, with every check PASS."""
    receipt = json.loads((R13 / "results" /
                          "E30_R13_OUTCOME_VERIFICATION_V1.json").read_text())
    assert receipt["schema_version"] == verification.SCHEMA
    assert receipt["computes_no_endpoint_no_contrast_no_terminal"] is True
    assert receipt["status_counts"] == {"PASS": 12}
    assert verification.exit_code(receipt["checks"]) == 0
    assert receipt["verifier_python"].startswith("3.11")
    ids = [c["check_id"] for c in receipt["checks"]]
    assert len(ids) == len(set(ids)) == 12
