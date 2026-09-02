"""End-to-end stub tests for the frozen real-LLM Prospective Revision Audit runner.

No model download: the ``stub`` backend is pure Python. The ``planted`` variant reads
the visible representation like an ideal contract-follower and must trip GP1; the
``null`` variant answers RETAIN everywhere and must not.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "research/llm-machine-epistemics/pra_real_llm_audit.py"
DESIGN = ROOT / "research/llm-machine-epistemics/PRA_REAL_LLM_AUDIT_DESIGN_V1.json"


def load_runner():
    spec = importlib.util.spec_from_file_location("pra_real_llm_audit", RUNNER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def runner():
    return load_runner()


def run_all(runner, workdir: Path, variant: str, scale: int = 12) -> dict:
    base = ["--workdir", str(workdir), "--backend", "stub", "--stub-variant", variant, "--split", "dev", "--device", "cpu", "--design", str(DESIGN)]
    assert runner.main(["--stage", "generate-suite", "--suite-scale", str(scale)] + base) == 0
    for stage in ("present-gate", "revision", "probe", "kv-channel", "rollup"):
        assert runner.main(["--stage", stage] + base) == 0
    return json.loads((workdir / "PRA_REAL_LLM_AUDIT_ROLLUP_V1__dev.json").read_text())


def test_design_is_frozen_and_parseable(runner):
    design = runner.load_design(DESIGN)
    assert design["schema_version"] == runner.DESIGN_SCHEMA
    assert design["protected_run"]["authorized"] is False
    assert design["scientific_authority"] is False
    assert set(design["suite_generator"]["instances_per_family"]["protected"]) == set(runner.FAMILIES)
    assert sum(design["suite_generator"]["instances_per_family"]["protected"].values()) == 500
    assert {m["alias"] for m in design["models"]} == {"qwen2.5-7b-instruct", "mistral-7b-instruct-v0.3"}
    for m in design["models"]:
        assert len(m["revision"]) == 40, "HF revisions must be pinned to full commit hashes"


def test_suite_is_deterministic_and_hashed(runner, tmp_path):
    design = runner.load_design(DESIGN)
    a = runner.generate_suite(design, "dev")
    b = runner.generate_suite(design, "dev")
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert a["n_instances"] == 32
    ids = [i["instance_id"] for i in a["instances"]]
    assert len(ids) == len(set(ids))
    # canonical P2 fixture: identical R2 rendering across arms, unique current action, divergent future gold
    canon = [i for i in a["instances"] if i["family"] == "F3_P2_CANON"][0]
    hA, hB = canon["arms"]
    assert runner.render_state(canon, hA, "R2") == runner.render_state(canon, hB, "R2")
    assert runner.render_state(canon, hA, "R3") != runner.render_state(canon, hB, "R3")
    assert hA["current_gold"]["acceptable"] == hB["current_gold"]["acceptable"] == ["RETAIN"]
    assert hA["future_gold"]["acceptable"] == ["REOPEN"] and hB["future_gold"]["acceptable"] == ["RETAIN"]
    assert hA["evidence_text"] == hB["evidence_text"]
    # nonce identities: no source name is reused across instances
    names = [s["name"] for i in a["instances"] for s in i["sources"].values()]
    assert len(set(names)) > 0.9 * len(names)
    # tampering with a frozen suite is refused
    runner.main(["--stage", "generate-suite", "--workdir", str(tmp_path), "--backend", "stub", "--suite-scale", "2", "--design", str(DESIGN)])
    path = runner.suite_path(tmp_path, "dev")
    path.write_text(path.read_text().replace("SUPPORTED", "SUPPORTED "), encoding="utf-8")
    with pytest.raises(SystemExit):
        runner.load_suite(tmp_path, "dev", None)


def test_protected_split_requires_authorization(runner, tmp_path):
    base = ["--workdir", str(tmp_path), "--backend", "stub", "--design", str(DESIGN)]
    assert runner.main(["--stage", "generate-suite", "--suite-scale", "2"] + base) == 0
    with pytest.raises(SystemExit):
        runner.main(["--stage", "present-gate", "--split", "protected", "--device", "cpu"] + base)
    with pytest.raises(SystemExit):
        runner.main(["--stage", "present-gate", "--split", "protected", "--max-instances", "2", "--protected-authorization", "PROTECTED_RUN_AUTHORIZED_AFTER_DESIGN_REVIEW__ORION51_PRA_R1", "--device", "cpu"] + base)


def test_planted_signal_trips_gp1_and_gp2(runner, tmp_path):
    rollup = run_all(runner, tmp_path / "planted", "planted")
    a = rollup["models"]["stub-planted"]
    assert a["GP0"]["pass"] is True
    cb = a["GP1"]["contrast_B_R2_vs_R3_on_P2"]
    assert cb["acc_y"] > cb["acc_x"] and a["GP1"]["contrast_B_instance_level"]["acc_x"] == 0.0
    assert a["GP1"]["pass"] is True
    assert a["GP3"]["pass"] is True
    assert a["GP2"]["GP2a_true_removal_effective"] is True
    assert a["GP2"]["GP2b_kv_survival_control"] is True
    assert a["GP2"]["probe_max_test_acc"]["R0"] >= 0.8 and a["GP2"]["probe_max_test_acc"]["R2_TRUE_REMOVAL"] <= 0.65
    assert a["terminal"] == "P2_PROSPECTIVE_REVISION_STATE_REQUIRED"
    assert a["GP2"]["gate_B_causal_use"] == "CANNOT_CHECK_ALTERNATE_CHANNEL_CAUSAL_USE"
    certs = a["GP1"]["certificates"]
    assert certs["R2"]["incompatible_cells"] > 0 and certs["R3"]["incompatible_cells"] == 0 and certs["R0"]["incompatible_cells"] == 0
    assert rollup["three_history_control"]["passes"] is True
    assert rollup["scientific_authority"] is False
    assert (tmp_path / "planted" / "PRA_REAL_LLM_AUDIT_ROLLUP_V1__dev.md").exists()


def test_null_model_does_not_trip_gp1(runner, tmp_path):
    rollup = run_all(runner, tmp_path / "null", "null")
    a = rollup["models"]["stub-null"]
    cb = a["GP1"]["contrast_B_R2_vs_R3_on_P2"]
    assert cb["diff_y_minus_x"] == 0.0 and a["GP1"]["pass"] is False
    assert a["terminal"] != "P2_PROSPECTIVE_REVISION_STATE_REQUIRED"
    assert rollup["overall_terminal"].startswith("REGISTERED_NEGATIVE_OR_BOUNDARY")


def test_statistics_primitives(runner):
    assert runner.binom_two_sided_p(0, 0) == 1.0
    assert abs(runner.binom_two_sided_p(10, 10) - 2 / 1024) < 1e-12
    assert abs(runner.binom_two_sided_p(5, 10) - 1.0) < 1e-12
    m = runner.mcnemar([(False, True)] * 8 + [(True, True)] * 4)
    assert m["discordant_y_only"] == 8 and m["discordant_x_only"] == 0 and m["p_two_sided_exact"] < 0.01
    # Student t CDF sanity against known quantiles
    assert abs(runner.student_t_quantile(0.975, 10) - 2.228) < 0.01
    assert abs(runner.student_t_cdf(0.0, 5) - 0.5) < 1e-9
    t = runner.paired_tost([0.01, -0.02, 0.005, 0.0, 0.01, -0.01, 0.002, 0.003], margin=0.05)
    assert t["equivalent"] is True
    t2 = runner.paired_tost([0.3, 0.4, 0.35, 0.5, 0.2, 0.3, 0.45, 0.25], margin=0.05)
    assert t2["equivalent"] is False
    lo, hi = runner.wilson_ci(9, 10)
    assert 0.55 < lo < 0.9 < hi <= 1.0
    tr, te = runner.mass_mean_probe([[1, 0], [2, 0], [-1, 0], [-2, 0]], [1, 1, 0, 0], [[3, 0], [-3, 0]], [1, 0])
    assert tr == 1.0 and te == 1.0


def test_padding_matches_token_budget(runner):
    design = runner.load_design(DESIGN)
    backend = runner.StubBackend()
    inst = runner.generate_suite(design, "dev")["instances"][10]
    conds = runner.prepare_conditions(inst, inst["arms"][0], backend, design)
    target = max(c["tokens_unpadded"] for c in conds.values())
    for c in conds.values():
        assert abs(c["tokens_padded"] - target) <= design["token_budget"]["tolerance_tokens"]
    assert conds["R0"]["filler_lines"] == 0


def test_parse_action(runner):
    assert runner.parse_action("Answer: REOPEN.") == "REOPEN"
    assert runner.parse_action("I would RETAIN it, but the rule says otherwise.\nAnswer: REOPEN") == "REOPEN"
    assert runner.parse_action("**Answer:** ESCALATE") == "ESCALATE"
    assert runner.parse_action("retain") == "RETAIN"
    assert runner.parse_action("I am not sure") == "UNPARSEABLE"


def test_families_filter_and_strict_json(runner, tmp_path):
    base = ["--workdir", str(tmp_path), "--backend", "stub", "--design", str(DESIGN), "--device", "cpu"]
    assert runner.main(["--stage", "generate-suite"] + base) == 0
    suite = runner.load_suite(tmp_path, "dev", 8, "F3_P2_CANON,F1_P0")
    fams = {i["family"] for i in suite["instances"]}
    assert fams == {"F3_P2_CANON", "F1_P0"} and suite["n_instances"] == 8
    with pytest.raises(SystemExit):
        runner.load_suite(tmp_path, "dev", None, "NOT_A_FAMILY")
    assert runner.main(["--stage", "probe", "--split", "dev", "--max-instances", "8", "--families", "F3_P2_CANON,F1_P0"] + base) == 0
    text = (tmp_path / "runs" / "stub-planted__dev" / "probe.json").read_text()
    assert "NaN" not in text and "Infinity" not in text
    probe = json.loads(text)
    assert probe["results"]["R0"]["status"] == "OK" and probe["results"]["R0"]["max_test_acc"] >= 0.8
