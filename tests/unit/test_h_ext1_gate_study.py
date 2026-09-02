from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "h_ext1_gate_study.py"
SPEC = importlib.util.spec_from_file_location("h_ext1_gate_study", SCRIPT)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

DESIGN = ROOT / "research/experiments/h-ext1/H_EXT1_CONDITIONAL_ACTIVATION_DESIGN_V1.json"
ARMS = (mod.ARM_M, mod.ARM_OFF, mod.ARM_PARENT)


def _record(rng: random.Random, root: str, text: str) -> dict:
    return {"item_id": "e" + str(rng.randrange(10**6)), "lineage_root": root, "source_type": "data",
            "method_text": text, "replay_hash": "rh_" + "".join(rng.choice("0123456789abcdef") for _ in range(12))}


def _task(rng: random.Random, task_id: str, study: str, dependent: bool) -> dict:
    roots = ["R_" + "".join(rng.choice("ABCDEFGH") for _ in range(6)) for _ in range(4)]
    if dependent:
        # planted witness: two records share a lineage root (arm-visible structure)
        items = [_record(rng, roots[0], "primary"), _record(rng, roots[0], "replication"),
                 _record(rng, roots[1], "other"), _record(rng, roots[2], "third")]
    else:
        items = [_record(rng, roots[i], f"independent {i}") for i in range(3)]
    return {"task_id": task_id, "study_id": study, "items": items, "task": "decide",
            "answer_contract": {"decision": "<enum>"}}


def build_fixture(root: Path, seed: int, planted: bool, n_per_study: int = 40) -> None:
    """Campaign-root fixture in the P-D suite layout.

    planted=True: M is correct exactly where the witness is present, OFF is correct
    exactly where it is absent (an identifiable activation regime). planted=False:
    correctness is independent of the witness (null world).
    """
    rng = random.Random(seed)
    for study in ("PD-S1-DEPENDENT-CORROBORATION", "PD-S2-ARGUMENT-AND-ADEQUACY"):
        sdir = root / study
        tasks, strata, rows = [], {}, []
        for i in range(n_per_study):
            dependent = (i % 2 == 0) if study.startswith("PD-S1") else False
            tid = f"{study[:5].lower()}-{i + 1:04d}"
            task = _task(rng, tid, study, dependent)
            tasks.append(task)
            strata[tid] = "PDS1A" if dependent else ("PDS1B" if study.startswith("PD-S1") else "PDS2D")
            if planted:
                m_ok, off_ok = dependent, not dependent
                parent_ok = rng.random() < 0.7
            else:
                m_ok, off_ok, parent_ok = (rng.random() < 0.6 for _ in range(3))
            for arm, ok in ((mod.ARM_M, m_ok), (mod.ARM_OFF, off_ok), (mod.ARM_PARENT, parent_ok)):
                rows.append({"task_id": tid, "arm": arm, "correct": ok, "expected": {}, "actual": {}})
                resp = sdir / "responses" / arm / f"{tid}.json"
                resp.parent.mkdir(parents=True, exist_ok=True)
                resp.write_text(json.dumps({"resource_receipt": {"model_calls": 1, "wall_time_seconds": 5.0 + rng.random()}}))
        (sdir / "public_tasks.json").write_text(json.dumps({"tasks": tasks}))
        (sdir / "private_oracle.json").write_text(json.dumps({"answers": {}, "strata": strata}))
        (sdir / "EVALUATION_ROWS.json").write_text(json.dumps(rows))
        (sdir / "FROZEN_SUITE.json").write_text(json.dumps({"seed": seed * 7 + len(study)}))


def test_witness_features_and_canary_ignore_oracle_keys() -> None:
    rng = random.Random(1)
    task = _task(rng, "t1", "PD-S1-X", dependent=True)
    feats = mod.witness_features(task)
    assert feats["w_shared_root"] is True and feats["n_records"] == 4 and feats["n_roots"] == 3
    mod.canary_check(task)  # must not raise
    poisoned = dict(task, stratum="PDS1A", expected={"decision": "ACCEPT_H"})
    assert mod.witness_features(poisoned) == feats


def test_xref_and_shared_token_witnesses() -> None:
    rng = random.Random(2)
    a = _record(rng, "R_AAAAAA", "We introduce calibration convention CVQWER here.")
    b = _record(rng, "R_BBBBBB", "We adopt calibration convention CVQWER from R_AAAAAA.")
    f = mod.witness_features({"items": [a, b]})
    assert f["w_xref_root"] and f["w_shared_token"] and not f["w_shared_root"]
    assert mod.witness_features({"no": "records"})["n_records"] == 0


def test_planted_gate_passes_g1_to_g3_end_to_end(tmp_path: Path) -> None:
    retro, pro, out = tmp_path / "retro", tmp_path / "pro", tmp_path / "out"
    build_fixture(retro, seed=11, planted=True)
    build_fixture(pro, seed=23, planted=True)
    rc = mod.main(["all", "--retro-root", str(retro), "--prospective-root", str(pro), "--design", str(DESIGN),
                   "--out-dir", str(out)])
    assert rc == 0
    freeze = json.loads((out / "H_EXT1_GATE_FREEZE.json").read_text())
    assert freeze["selected_gate"] in {"G_A_PROVENANCE_WITNESS", "G_F_ROOT_RATIO_GT1"}
    roll = json.loads((out / "H_EXT1_ROLLUP_V1.json").read_text())
    for cell in ("RETROSPECTIVE_EVAL", "PROSPECTIVE"):
        gates = roll["cells"][cell]["gates"]
        assert gates["G0_VALIDITY"]["pass"]
        assert gates["G1_DOMINATES_ALWAYS_ON"]["pass"]
        assert gates["G2_DOMINATES_ALWAYS_OFF_AND_PARENT"]["pass"]
        assert gates["G3_BEATS_SHUFFLE_NULL"]["pass"]
        assert gates["G3S_BEATS_WITHIN_STUDY_NULL"]["pass"]
        assert gates["G4_SIGN_CONSISTENCY"]["pass"]
    assert roll["binding_terminal"] == "CONDITIONAL_ACTIVATION_IDENTIFIABLE_FROM_EVIDENCE_STRUCTURE"
    # dev / eval disjointness by construction of the parity split
    inst = json.loads((out / "data" / "RETROSPECTIVE_instances.json").read_text())
    dev = {r["task_id"] for r in mod.dev_rows(inst)}
    ev = {r["task_id"] for r in mod.eval_rows_retro(inst)}
    assert dev and ev and not (dev & ev)
    assert (out / "H_EXT1_ROLLUP_V1.md").read_text().startswith("# H-EXT-1 Rollup V1")


def test_null_world_does_not_pass_g3(tmp_path: Path) -> None:
    retro, pro, out = tmp_path / "retro", tmp_path / "pro", tmp_path / "out"
    build_fixture(retro, seed=5, planted=False, n_per_study=60)
    build_fixture(pro, seed=9, planted=False, n_per_study=60)
    rc = mod.main(["all", "--retro-root", str(retro), "--prospective-root", str(pro), "--design", str(DESIGN),
                   "--out-dir", str(out)])
    roll = json.loads((out / "H_EXT1_ROLLUP_V1.json").read_text())
    if rc == 4:
        assert roll["binding_terminal"] == "NO_CANDIDATE_GATE_ON_DEV"
        return
    pro_cell = roll["cells"]["PROSPECTIVE"]
    assert pro_cell["terminal"] != "CONDITIONAL_ACTIVATION_IDENTIFIABLE_FROM_EVIDENCE_STRUCTURE"
    assert not (pro_cell["gates"]["G3_BEATS_SHUFFLE_NULL"]["pass"] and pro_cell["gates"]["G1_DOMINATES_ALWAYS_ON"]["pass"]
                and pro_cell["gates"]["G2_DOMINATES_ALWAYS_OFF_AND_PARENT"]["pass"])


def test_missing_prospective_responses_route_to_cannot_check(tmp_path: Path) -> None:
    retro, pro, out = tmp_path / "retro", tmp_path / "pro", tmp_path / "out"
    build_fixture(retro, seed=11, planted=True)
    build_fixture(pro, seed=23, planted=True)
    # drop one arm response row from the prospective cell -> missing -> CANNOT_CHECK
    sdir = pro / "PD-S1-DEPENDENT-CORROBORATION"
    rows = json.loads((sdir / "EVALUATION_ROWS.json").read_text())
    rows = [r for r in rows if not (r["arm"] == mod.ARM_M and r["task_id"].endswith("0001"))]
    (sdir / "EVALUATION_ROWS.json").write_text(json.dumps(rows))
    mod.main(["all", "--retro-root", str(retro), "--prospective-root", str(pro), "--design", str(DESIGN),
              "--out-dir", str(out)])
    roll = json.loads((out / "H_EXT1_ROLLUP_V1.json").read_text())
    assert roll["binding_terminal"] == "CANNOT_CHECK_PROSPECTIVE_RUN_INVALID"
    assert roll["cells"]["PROSPECTIVE"]["gates"] == {}


def test_evaluate_refuses_without_frozen_gate() -> None:
    with pytest.raises(mod.DesignViolation):
        mod.evaluate_cell({"rows": [], "study_seeds": {}}, {"selected_gate": None, "gate_sha256": None},
                          "PROSPECTIVE", json.loads(DESIGN.read_text()))
