"""End-to-end stub tests for the frozen real-LLM Prospective Revision Audit runner.

No model download: the ``stub`` backend is pure Python. The ``planted`` variant reads
the visible representation like an ideal contract-follower and must trip GP1; the
``null`` variant answers RETAIN everywhere and must not.

Design V1 and the V2 contingency (larger frozen models, sealed protected seed, GPC
competence gate, same-fibre secondary family) share the runner; both are exercised.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "research/llm-machine-epistemics/pra_real_llm_audit.py"
DESIGN = ROOT / "research/llm-machine-epistemics/PRA_REAL_LLM_AUDIT_DESIGN_V1.json"
DESIGN_V2 = ROOT / "research/llm-machine-epistemics/PRA_REAL_LLM_AUDIT_DESIGN_V2.json"
V1_FAMILIES = {"F0_ACQ", "F1_P0", "F2_P1", "F3_P2_CANON", "F3_P2_MIRROR", "F3_P2_INDEP", "F3_P2_RECON", "F3_P2_TIE"}
# Frozen V1 suite digests (archived SUITE_MANIFEST of dev smoke job 3563622): the runner must keep
# rendering the V1 design byte-identically after the V2 additions.
V1_DEV_SUITE_SHA256 = "98c8cbb54e5560d954c0a7805ae2fca37aa2777751228baf4701d30c185bf2ba"
V1_PROTECTED_SUITE_SHA256 = "21b5b0f7263a49732a9d7c6ba4c417b825e363d2ed06df66d1b3a6a26551b2ae"


def load_runner():
    spec = importlib.util.spec_from_file_location("pra_real_llm_audit", RUNNER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def runner():
    return load_runner()


def run_all(runner, workdir: Path, variant: str, scale: int = 12, design: Path = DESIGN, extra_stages: tuple[str, ...] = ()) -> dict:
    base = ["--workdir", str(workdir), "--backend", "stub", "--stub-variant", variant, "--split", "dev", "--device", "cpu", "--design", str(design)]
    assert runner.main(["--stage", "generate-suite", "--suite-scale", str(scale)] + base) == 0
    for stage in ("present-gate", "revision", "probe", "kv-channel", *extra_stages, "rollup"):
        assert runner.main(["--stage", stage] + base) == 0
    stem = runner.rollup_basename(runner.load_design(design))
    return json.loads((workdir / f"{stem}__dev.json").read_text())


def test_design_is_frozen_and_parseable(runner):
    design = runner.load_design(DESIGN)
    assert design["schema_version"] == runner.DESIGN_SCHEMA
    assert design["protected_run"]["authorized"] is False
    assert design["scientific_authority"] is False
    assert set(design["suite_generator"]["instances_per_family"]["protected"]) == V1_FAMILIES
    assert V1_FAMILIES < set(runner.FAMILIES)
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


def test_v1_suites_are_byte_identical_after_v2_additions(runner, tmp_path):
    assert runner.main(["--stage", "generate-suite", "--workdir", str(tmp_path), "--backend", "stub", "--design", str(DESIGN)]) == 0
    dev = hashlib.sha256(runner.suite_path(tmp_path, "dev").read_bytes()).hexdigest()
    prot = hashlib.sha256(runner.suite_path(tmp_path, "protected").read_bytes()).hexdigest()
    assert dev == V1_DEV_SUITE_SHA256
    assert prot == V1_PROTECTED_SUITE_SHA256


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
    assert "GPC" not in a and "contrast_B_same_fibre_R2_vs_R3" not in a["GP1"]


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


def test_zero_probe_accuracy_counts_as_removed(runner, tmp_path):
    run_all(runner, tmp_path / "z", "planted")
    probe_path = tmp_path / "z" / "runs" / "stub-planted__dev" / "probe.json"
    probe = json.loads(probe_path.read_text())
    probe["results"]["R2_TRUE_REMOVAL"]["max_test_acc"] = 0.0
    probe_path.write_text(json.dumps(probe))
    assert runner.main(["--stage", "rollup", "--workdir", str(tmp_path / "z"), "--backend", "stub", "--design", str(DESIGN)]) == 0
    rollup = json.loads((tmp_path / "z" / "PRA_REAL_LLM_AUDIT_ROLLUP_V1__dev.json").read_text())
    gp2 = rollup["models"]["stub-planted"]["GP2"]
    assert gp2["probe_R2_true_removal_at_chance"] is True and gp2["GP2a_true_removal_effective"] is True


# ------------------------------------------------------------------ design V2 (contingency)

def test_v2_design_is_frozen_and_carries_v1_verbatim(runner):
    v1 = runner.load_design(DESIGN)
    v2 = runner.load_design(DESIGN_V2)
    assert v2["schema_version"] == runner.DESIGN_SCHEMA_V2
    assert v2["protected_run"]["authorized"] is False and v2["scientific_authority"] is False
    assert v2["protected_run"]["authorization_token"] != v1["protected_run"]["authorization_token"]
    # models: two families, larger, ungated, pinned; both differ from V1
    assert {m["alias"] for m in v2["models"]} == {"qwen2.5-32b-instruct", "mistral-small-24b-instruct-2501"}
    for m in v2["models"]:
        assert len(m["revision"]) == 40 and m["gated"] is False and m["fits_one_a100_80gb_bf16"] is True
    assert {m["hf_id"] for m in v2["models"]}.isdisjoint({m["hf_id"] for m in v1["models"]})
    # carried verbatim: decoding, token budget, probe, kv channel, representation conditions, GP0-GP3, terminals
    for key in ("decoding", "token_budget", "probe", "kv_channel", "representation_conditions", "terminals", "metrics"):
        assert v2[key] == v1[key], key
    for gate in ("GP0", "GP2", "GP3"):
        assert {k: v for k, v in v2["gates"][gate].items() if k != "rule"} == {k: v for k, v in v1["gates"][gate].items() if k != "rule"}, gate
    assert {k: v for k, v in v2["gates"]["GP1"].items() if k != "rule"} == {k: v for k, v in v1["gates"]["GP1"].items() if k != "rule"}
    # V1 family counts carried verbatim; the same-fibre family is added at the canonical count
    for split in ("dev", "protected"):
        v1_counts = v1["suite_generator"]["instances_per_family"][split]
        v2_counts = v2["suite_generator"]["instances_per_family"][split]
        assert {k: v2_counts[k] for k in v1_counts} == v1_counts
        assert v2_counts["F3_P2_CANON_SF"] == v1_counts["F3_P2_CANON"]
    assert set(v2["suite_generator"]["instances_per_family"]["protected"]) == set(runner.FAMILIES)
    assert sum(v2["suite_generator"]["instances_per_family"]["protected"].values()) == 620
    # fresh seeds: dev distinct from V1; protected sealed (commitment only, never a plain integer)
    assert v2["suite_generator"]["seed"]["dev"] != v1["suite_generator"]["seed"]["dev"]
    assert "protected" not in v2["suite_generator"]["seed"]
    assert isinstance(v2["suite_generator"]["seed"]["protected_commitment_sha256"], str)
    # GPC registered
    gpc = v2["gates"]["GPC"]
    assert gpc["split"] == "dev" and gpc["condition"] == "R0"
    assert gpc["min_maintain_accuracy_R0"] == 0.75 and gpc["min_update_accuracy_R0"] == 0.75


def test_v2_same_fibre_family_properties(runner):
    v2 = runner.load_design(DESIGN_V2)
    suite = runner.generate_suite(v2, "dev")
    assert suite["n_instances"] == 36
    sf = [i for i in suite["instances"] if i["family"] == "F3_P2_CANON_SF"]
    canon = [i for i in suite["instances"] if i["family"] == "F3_P2_CANON"]
    assert len(sf) == 4 and len(canon) == 4
    inst = sf[0]
    hA, hB = inst["arms"]
    # same histories/gold structure as the canonical fixture
    assert hA["current_gold"]["acceptable"] == hB["current_gold"]["acceptable"] == ["RETAIN"]
    assert hA["future_gold"]["acceptable"] == ["REOPEN"] and hB["future_gold"]["acceptable"] == ["RETAIN"]
    assert runner.render_state(inst, hA, "R2") == runner.render_state(inst, hB, "R2")
    assert runner.render_state(inst, hA, "R3") != runner.render_state(inst, hB, "R3")
    # identical evidence across arms; the retraction is of A; both arms list A on file
    assert hA["evidence_text"] == hB["evidence_text"]
    assert inst["sources"]["A"]["id"] in hA["evidence_text"] and "FLAGGED" in hA["evidence_text"]
    # same successor fibre: the registered successor status line is identical across arms
    assert hA["successor_linguistic_target"]["continuation"] == hB["successor_linguistic_target"]["continuation"]
    assert hA["successor_linguistic_target"]["same_fibre_across_arms"] is True
    assert hA["successor_linguistic_target"]["continuation"] == f"Claim {inst['claim_id']} is currently listed as FLAGGED."
    # the canonical fixture does not carry the field (its successors sit in distinct fibres)
    assert "successor_linguistic_target" not in canon[0]["arms"][0]
    # the planted stub still resolves the same-fibre evidence exactly like the canonical one
    stub = runner.StubBackend()
    for arm, gold in ((hA, "REOPEN"), (hB, "RETAIN")):
        m = runner.build_messages(runner.render_state(inst, arm, "R3"), "future_action", arm["evidence_text"], inst["claim_id"])
        assert runner.parse_action(stub.generate(m, 8)) == gold


def test_v2_sealed_protected_seed(runner, tmp_path):
    v2 = runner.load_design(DESIGN_V2)
    # without the seed file: dev generated, protected skipped with the commitment recorded
    base = ["--workdir", str(tmp_path / "a"), "--backend", "stub", "--design", str(DESIGN_V2)]
    assert runner.main(["--stage", "generate-suite"] + base) == 0
    manifest = json.loads((tmp_path / "a" / "suite" / "SUITE_MANIFEST.json").read_text())
    assert manifest["splits"]["dev"]["n_instances"] == 36
    assert manifest["splits"]["protected"]["status"].startswith("SEALED_SEED_NOT_SUPPLIED")
    assert not runner.suite_path(tmp_path / "a", "protected").exists()
    with pytest.raises(SystemExit):
        runner.generate_suite(v2, "protected")
    # a seed file that does not hash to the commitment is refused
    bad = tmp_path / "bad.sealed"
    bad.write_text("123456:deadbeef\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        runner.resolve_split_seed(v2, "protected", str(bad))
    # a matching commitment unlocks a deterministic protected suite with the frozen counts
    sealed = tmp_path / "good.sealed"
    sealed.write_text("424242:0123456789abcdef\n", encoding="utf-8")
    design_copy = json.loads(DESIGN_V2.read_text())
    design_copy["suite_generator"]["seed"]["protected_commitment_sha256"] = hashlib.sha256(sealed.read_bytes()).hexdigest()
    dpath = tmp_path / "design_v2_unsealed_test.json"
    dpath.write_text(json.dumps(design_copy), encoding="utf-8")
    assert runner.resolve_split_seed(design_copy, "protected", str(sealed)) == 424242
    assert runner.main(["--stage", "generate-suite", "--workdir", str(tmp_path / "b"), "--backend", "stub", "--design", str(dpath), "--protected-seed-file", str(sealed)]) == 0
    prot = json.loads(runner.suite_path(tmp_path / "b", "protected").read_text())
    assert prot["n_instances"] == 620 and prot["generator_seed"] == 424242
    assert prot["instances_per_family"]["F3_P2_CANON_SF"] == 120
    # the protected split still requires the V2 authorization token
    with pytest.raises(SystemExit):
        runner.main(["--stage", "present-gate", "--split", "protected", "--device", "cpu", "--workdir", str(tmp_path / "b"), "--backend", "stub", "--design", str(dpath)])


def test_v2_competence_gate_planted_passes_null_fails(runner, tmp_path):
    rollup = run_all(runner, tmp_path / "planted", "planted", design=DESIGN_V2, extra_stages=("competence-gate",))
    a = rollup["models"]["stub-planted"]
    assert rollup["rollup_basename"] == "PRA_REAL_LLM_AUDIT_ROLLUP_V2"
    assert (tmp_path / "planted" / "PRA_REAL_LLM_AUDIT_ROLLUP_V2__dev.md").exists()
    gpc = json.loads((tmp_path / "planted" / "runs" / "stub-planted__dev" / "competence_gate.json").read_text())
    assert gpc["pass"] is True and gpc["verdict"] == "COMPETENT__MODEL_RETAINED"
    assert gpc["maintain_accuracy_R0"]["acc"] == 1.0 and gpc["update_accuracy_R0"]["acc"] == 1.0
    assert "F3_P2_CANON_SF" in gpc["by_family"]
    assert a["GPC"]["pass"] is True
    # GPC is reported, never gated: V1 gates and terminal are unchanged by it
    assert a["GP1"]["pass"] is True and a["terminal"] == "P2_PROSPECTIVE_REVISION_STATE_REQUIRED"
    # the same-fibre secondary contrast is reported beside the primary with the same shape
    sf = a["GP1"]["contrast_B_same_fibre_R2_vs_R3"]
    assert sf["acc_y"] > sf["acc_x"] and a["GP1"]["contrast_B_same_fibre_instance_level"]["acc_x"] == 0.0
    assert a["GP1"]["same_fibre_r3_competence_floor_met"] is True
    assert "F3_P2_CANON_SF" in a["GP1"]["metrics_by_family_condition"]
    md = (tmp_path / "planted" / "PRA_REAL_LLM_AUDIT_ROLLUP_V2__dev.md").read_text()
    assert "Contrast B-SF" in md and "GPC competence" in md and "rollup V2" in md

    null = run_all(runner, tmp_path / "null", "null", design=DESIGN_V2, extra_stages=("competence-gate",))
    b = null["models"]["stub-null"]
    assert b["GPC"]["pass"] is False and b["GPC"]["verdict"].startswith("INCOMPETENT_ON_DEV")
    assert b["GPC"]["maintain_accuracy_R0"]["acc"] == 1.0 and b["GPC"]["update_accuracy_R0"]["acc"] == 0.0
    assert b["GP1"]["pass"] is False


def test_v2_competence_gate_refuses_v1_design_and_protected_split(runner, tmp_path):
    base = ["--workdir", str(tmp_path), "--backend", "stub", "--device", "cpu"]
    assert runner.main(["--stage", "generate-suite", "--suite-scale", "2", "--design", str(DESIGN)] + base) == 0
    assert runner.main(["--stage", "revision", "--design", str(DESIGN)] + base) == 0
    with pytest.raises(SystemExit):
        runner.main(["--stage", "competence-gate", "--design", str(DESIGN)] + base)
    with pytest.raises(SystemExit):
        runner.main(["--stage", "competence-gate", "--split", "protected", "--design", str(DESIGN_V2), "--protected-authorization", "PROTECTED_RUN_AUTHORIZED_AFTER_DESIGN_REVIEW__ORION51_PRA_V2_R1"] + base)
