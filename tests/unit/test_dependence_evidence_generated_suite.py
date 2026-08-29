from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUITE = ROOT / "scripts/run_dependence_evidence_generated_suite.py"
ARMS = ROOT / "scripts/orion_pd_arms.py"

OFFLINE_ARMS = [
    "CURRENT_INDEPENDENT_COUNTING",
    "PROVENANCE_TRACKING",
    "STANDARD_DEPENDENCE_META_ANALYSIS",
    "ARGUMENT_ACCEPTABILITY",
    "SIMPLE_DIRECT_CONTROL",
]
MODEL_ARM = "P_D_FULL"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def load_suite():
    return load_module(SUITE, "orion_pd_generated_suite")


def load_arms():
    return load_module(ARMS, "orion_pd_arms_lib")


def tiny_strata(suite) -> dict[str, dict[str, int]]:
    return {
        "PD-S1-DEPENDENT-CORROBORATION": {s: 2 for s in ("PDS1A", "PDS1B", "PDS1C", "PDS1D")},
        "PD-S2-ARGUMENT-AND-ADEQUACY": {s: 2 for s in ("PDS2A", "PDS2B", "PDS2C", "PDS2D")},
        "PD-S3-REVOCATION-AND-UPTAKE": {s: 2 for s in ("PDS3A", "PDS3B", "PDS3C", "PDS3D")},
        "PD-S4-AUTHORITY-AND-RESPONSE": {s: 2 for s in ("PDS4A", "PDS4B", "PDS4C", "PDS4D")},
    }


def run_offline_campaign(suite, tmp_path: Path, per_stratum: int = 2):
    root = tmp_path / "campaign"
    arms = OFFLINE_ARMS + [MODEL_ARM]
    for study, strata in tiny_strata(suite).items():
        counts = {s: per_stratum for s in strata}
        suite.prepare(root / study, study, counts, 12345, arms, False)
        suite.FMFG.dispatch(root / study, arms, 2, True)
        suite.FMFG.evaluate(root / study, arms)
    return root


def test_prepare_hides_strata_and_answers(tmp_path):
    suite = load_suite()
    root = tmp_path / "hide"
    suite.prepare(root, "PD-S1-DEPENDENT-CORROBORATION",
                  {"PDS1A": 3, "PDS1B": 2, "PDS1C": 2, "PDS1D": 1}, 99, OFFLINE_ARMS, False)
    public_text = (root / "public_tasks.json").read_text()
    private = json.loads((root / "private_oracle.json").read_text())
    freeze = json.loads((root / "FROZEN_SUITE.json").read_text())
    for stratum in ("PDS1A", "PDS1B", "PDS1C", "PDS1D"):
        assert stratum not in public_text and stratum.lower() not in public_text
    assert "answers" not in json.loads(public_text)
    assert set(private["strata"]) == {t["task_id"] for t in json.loads(public_text)["tasks"]}
    assert len(private["answers"]) == 8
    for value in freeze["authority"].values():
        assert value is False
    assert freeze["strata_visible_in_public_tasks"] is False


def test_offline_dispatch_constructed_ceiling_and_missing_model(tmp_path, monkeypatch):
    suite = load_suite()
    monkeypatch.setenv("ORION_FORMAL_ARM_COMMAND", f"{sys.executable} {ARMS}")
    monkeypatch.setenv("ORION_PD_OFFLINE_ONLY", "1")
    root = run_offline_campaign(suite, tmp_path)
    s1 = root / "PD-S1-DEPENDENT-CORROBORATION"
    strata = json.loads((s1 / "private_oracle.json").read_text())["strata"]
    summary = json.loads((s1 / "EVALUATION_SUMMARY.json").read_text())["summary"]
    rows = json.loads((s1 / "EVALUATION_ROWS.json").read_text())
    for arm in OFFLINE_ARMS:
        assert summary[arm]["run_valid"] is True and summary[arm]["missing_or_invalid"] == 0
    assert summary[MODEL_ARM]["run_valid"] is False
    assert all(r["missing"] for r in rows if r["arm"] == MODEL_ARM)
    by = {(r["arm"], strata[r["task_id"]]): r for r in rows}
    for task_id, stratum in strata.items():
        if stratum == "PDS1A":
            # counting accepts planted dependent corroboration (false corroboration 1.0)
            assert by[("CURRENT_INDEPENDENT_COUNTING", stratum)]["actual"]["decision"] == "ACCEPT_H" or \
                by[("CURRENT_INDEPENDENT_COUNTING", stratum)]["task_id"] != task_id
    pds1a_rows = [r for r in rows if r["arm"] == "CURRENT_INDEPENDENT_COUNTING" and strata[r["task_id"]] == "PDS1A"]
    assert pds1a_rows and all(r["actual"]["decision"] == "ACCEPT_H" and not r["correct"] for r in pds1a_rows)
    pds1c_rows = [r for r in rows if r["arm"] == "PROVENANCE_TRACKING" and strata[r["task_id"]] == "PDS1C"]
    assert pds1c_rows and all(r["correct"] for r in pds1c_rows)
    receipt = json.loads((s1 / "DISPATCH_RECEIPT.json").read_text())
    assert receipt["all_returncodes_zero"] and receipt["oracle_restored_hash_match"]
    s2 = root / "PD-S2-ARGUMENT-AND-ADEQUACY"
    s2_rows = json.loads((s2 / "EVALUATION_ROWS.json").read_text())
    s2_strata = json.loads((s2 / "private_oracle.json").read_text())["strata"]
    af_circ = [r for r in s2_rows if r["arm"] == "ARGUMENT_ACCEPTABILITY" and s2_strata[r["task_id"]] == "PDS2B"]
    assert af_circ and all(r["correct"] for r in af_circ)


def test_oracle_absent_during_dispatch(tmp_path, monkeypatch):
    suite = load_suite()
    stub = tmp_path / "stub_arm.py"
    stub.write_text(
        "import json, sys\n"
        "from pathlib import Path\n"
        "args = sys.argv[1:]\n"
        "req = Path(args[args.index('--request') + 1])\n"
        "resp = Path(args[args.index('--response') + 1])\n"
        "workdir = resp.parent.parent.parent\n"
        "with (workdir / 'STUB_PROBE.log').open('a') as fh:\n"
        "    fh.write(str((workdir / 'private_oracle.json').exists()) + '\\n')\n"
        "resp.write_text(json.dumps({'status': 'COMPLETED_PROPOSAL_ONLY', 'answer': {},\n"
        "    'resource_receipt': {'model_calls': 0}}))\n"
    )
    monkeypatch.setenv("ORION_FORMAL_ARM_COMMAND", f"{sys.executable} {stub}")
    workdir = tmp_path / "probe"
    suite.prepare(workdir, "PD-S1-DEPENDENT-CORROBORATION",
                  {"PDS1A": 1, "PDS1B": 1, "PDS1C": 1, "PDS1D": 1}, 5, ["STUB"], False)
    suite.FMFG.dispatch(workdir, ["STUB"], 2, True)
    probes = [line == "False\n" for line in (workdir / "STUB_PROBE.log").read_text().splitlines(True)]
    assert probes and all(probes)
    commitment = json.loads((workdir / "PRIVATE_ORACLE_COMMITMENT.json").read_text())
    assert commitment["private_removed_before_dispatch"] is True
    receipt = json.loads((workdir / "DISPATCH_RECEIPT.json").read_text())
    assert receipt["oracle_restored_hash_match"] is True


def test_offline_constructed_rates_by_stratum():
    suite = load_suite()
    arms = load_arms()
    correct: dict[tuple[str, str, str], int] = {}
    total: dict[tuple[str, str, str], int] = {}
    for study, strata in suite.PD_GENERATORS.items():
        for stratum, gen in strata.items():
            for seed in (0, 1, 2):
                for index in range(6):
                    public, answer = gen(__import__("random").Random(seed * 100 + index), index)
                    for arm in OFFLINE_ARMS:
                        key = (study, stratum, arm)
                        total[key] = total.get(key, 0) + 1
                        correct[key] = correct.get(key, 0) + int(
                            arms.offline_answer(arm, public) == answer)
    def right(study, stratum, arm):
        return correct[(study, stratum, arm)] == total[(study, stratum, arm)]
    def wrong(study, stratum, arm):
        return correct[(study, stratum, arm)] == 0
    s1 = "PD-S1-DEPENDENT-CORROBORATION"
    for stratum in ("PDS1A", "PDS1C"):
        assert wrong(s1, stratum, "CURRENT_INDEPENDENT_COUNTING")
    for stratum in ("PDS1B", "PDS1D"):
        assert right(s1, stratum, "CURRENT_INDEPENDENT_COUNTING")
    for arm in ("PROVENANCE_TRACKING", "STANDARD_DEPENDENCE_META_ANALYSIS", "SIMPLE_DIRECT_CONTROL"):
        assert wrong(s1, "PDS1A", arm)
        for stratum in ("PDS1B", "PDS1C", "PDS1D"):
            assert right(s1, stratum, arm), (arm, stratum)
    s2 = "PD-S2-ARGUMENT-AND-ADEQUACY"
    for arm in ("ARGUMENT_ACCEPTABILITY",):
        assert right(s2, "PDS2B", arm) and right(s2, "PDS2D", arm)
        assert wrong(s2, "PDS2A", arm) and wrong(s2, "PDS2C", arm)
    for arm in ("CURRENT_INDEPENDENT_COUNTING", "SIMPLE_DIRECT_CONTROL"):
        assert right(s2, "PDS2D", arm) and wrong(s2, "PDS2A", arm) and wrong(s2, "PDS2B", arm)
    s3 = "PD-S3-REVOCATION-AND-UPTAKE"
    for arm in ("CURRENT_INDEPENDENT_COUNTING", "ARGUMENT_ACCEPTABILITY",
                "PROVENANCE_TRACKING", "STANDARD_DEPENDENCE_META_ANALYSIS"):
        assert wrong(s3, "PDS3A", arm) and right(s3, "PDS3B", arm) and right(s3, "PDS3C", arm)
    assert correct[(s3, "PDS3D", "SIMPLE_DIRECT_CONTROL")] == total[(s3, "PDS3D", "SIMPLE_DIRECT_CONTROL")] // 3
    s4 = "PD-S4-AUTHORITY-AND-RESPONSE"
    for arm in ("CURRENT_INDEPENDENT_COUNTING", "PROVENANCE_TRACKING",
                "STANDARD_DEPENDENCE_META_ANALYSIS", "ARGUMENT_ACCEPTABILITY"):
        assert right(s4, "PDS4B", arm)
        for stratum in ("PDS4A", "PDS4C", "PDS4D"):
            assert wrong(s4, stratum, arm), (arm, stratum)
    for stratum in ("PDS4A", "PDS4B", "PDS4C", "PDS4D"):
        assert wrong(s4, stratum, "SIMPLE_DIRECT_CONTROL")


def test_seed_determinism(tmp_path):
    suite = load_suite()
    calls = 0

    def public(seed: int) -> str:
        nonlocal calls
        calls += 1
        workdir = tmp_path / f"d{seed}-{calls}"
        suite.prepare(workdir, "PD-S2-ARGUMENT-AND-ADEQUACY",
                      {"PDS2A": 2, "PDS2B": 2, "PDS2C": 2, "PDS2D": 2}, seed, ["STUB"], False)
        return (workdir / "public_tasks.json").read_text()
    first = public(20260903)
    assert first == public(20260903)
    assert first != public(20260904)


def test_analyze_stratified_metrics_and_authority(tmp_path, monkeypatch):
    suite = load_suite()
    monkeypatch.setenv("ORION_FORMAL_ARM_COMMAND", f"{sys.executable} {ARMS}")
    monkeypatch.setenv("ORION_PD_OFFLINE_ONLY", "1")
    root = run_offline_campaign(suite, tmp_path)
    plan = tmp_path / "tiny_plan.json"
    plan.write_text(json.dumps({"seed": 1, "studies": {s: {"strata": c, "arms": OFFLINE_ARMS + [MODEL_ARM]}
                                                        for s, c in tiny_strata(suite).items()}}))
    suite.cmd_analyze(plan, root, list(tiny_strata(suite)))
    out = json.loads((root / "CAMPAIGN_ANALYSIS_SUMMARY.json").read_text())
    assert all(v is False for v in out["authority"].values())
    s1 = out["studies"]["PD-S1-DEPENDENT-CORROBORATION"]
    assert s1["CURRENT_INDEPENDENT_COUNTING"]["PDS1A"]["false_corroboration_rate"] == 1.0
    assert s1["CURRENT_INDEPENDENT_COUNTING"]["PDS1B"]["independent_support_preservation"] == 1.0
    assert s1["PROVENANCE_TRACKING"]["PDS1C"]["accuracy"] == 1.0
    model = s1[MODEL_ARM]["PDS1A"]
    assert model["missing"] == 2 and "accuracy" not in model and model["false_corroboration_rate"] is None
    s4 = out["studies"]["PD-S4-AUTHORITY-AND-RESPONSE"]
    assert s4["ARGUMENT_ACCEPTABILITY"]["PDS4A"]["false_authority_rate"] == 1.0


def test_latent_dependence_inferable_only_from_method_text():
    suite = load_suite()
    gen = suite.PD_GENERATORS["PD-S1-DEPENDENT-CORROBORATION"]["PDS1A"]
    for index in range(4):
        public, answer = gen(__import__("random").Random(index), index)
        text = json.dumps(public)
        assert "PDS1A" not in text
        methods = [item["method_text"] for item in public["items"]]
        conv = next(m.split("calibration convention ", 1)[1].split()[0]
                    for m in methods if m.startswith("We introduce"))
        adopters = [m for m in methods if "adopt calibration convention" in m]
        assert len(adopters) == 2 and all(conv in m for m in adopters)
        assert sum(conv in m for m in methods) == 3  # latent dependence stated in prose, never labelled
        assert len({item["lineage_root"] for item in public["items"]}) == 4  # invisible to provenance
        assert answer["decision"] == "INCONCLUSIVE_INSUFFICIENT_INDEPENDENT_SUPPORT"


def test_model_arm_offline_guard(tmp_path):
    suite = load_suite()
    workdir = tmp_path / "guard"
    suite.prepare(workdir, "PD-S1-DEPENDENT-CORROBORATION",
                  {"PDS1A": 1, "PDS1B": 1, "PDS1C": 1, "PDS1D": 1}, 3, [MODEL_ARM], False)
    request = next((workdir / "requests" / MODEL_ARM).glob("*.json"))
    response = tmp_path / "response.json"
    env = {**__import__("os").environ, "ORION_PD_OFFLINE_ONLY": "1"}
    proc = subprocess.run([sys.executable, str(ARMS), "--request", str(request), "--response", str(response)],
                          env=env, text=True, capture_output=True)
    assert proc.returncode == 0
    out = json.loads(response.read_text())
    assert out["status"].startswith("EXECUTION_FAILED")
    assert out["answer"] is None
    assert out["resource_receipt"]["model_calls"] == 0
