from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "h_ext1n_gate_study.py"
SPEC = importlib.util.spec_from_file_location("h_ext1n_gate_study", SCRIPT)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

DESIGN = ROOT / "research/experiments/h-ext1-naturalistic/H_EXT1N_DESIGN_V1.json"
ARMS = (mod.ARM_M, mod.ARM_OFF, mod.ARM_PARENT)
TOPICS = ("hypertension", "stroke")


def _record(rid: str, title: str, abstract: str, authors: list[str], grants: list[str] | None = None) -> dict:
    return {"record_id": rid, "title": title, "abstract": abstract, "authors": authors, "journal": "J", "year": "2020",
            "publication_types": ["Randomized Controlled Trial"], "grant_ids": grants or [], "mesh_major": []}


def _task(rng: random.Random, tid: str, topic: str, n: int, dependent: bool, witness: bool) -> dict:
    recs = []
    acr = "TRIAL" + "".join(rng.choice("ABCDEFGH") for _ in range(4))
    for i in range(n):
        senior = f"Senior{rng.randrange(10**6)} S"
        title = f"Effect of drug {i} on outcome {rng.randrange(1000)}"
        abstract = "Participants were randomized; outcomes were measured at follow-up."
        if dependent and witness and i < 2:
            # naturalistic witness: shared senior author + acronym in title/abstract
            senior = "Shared SS"
            title = f"{title}: the {acr} trial" if i == 0 else title
            abstract = f"Secondary analysis of the {acr} trial. " + abstract if i == 1 else abstract
        recs.append(_record(f"r{i + 1}", title, abstract, [f"First{rng.randrange(10**6)} F", senior]))
    return {"task_id": tid, "study_id": "N1", "topic": topic, "hypothesis": "H_X", "records": recs,
            "registered_decision_rule": "rule", "task": "decide",
            "answer_contract": {"decision": "string", "independent_support_family_count": "number"}}


def build_fixture(root: Path, seed: int, planted: bool, n_per_split: int = 48) -> None:
    """Two study dirs (N1-DEV, N1-EVAL) in the P-D layout.

    planted=True: dependent sets carry naturalistic witnesses, M is correct exactly on dependent
    sets and OFF exactly on independent ones (identifiable regime). planted=False: witnesses are
    absent and correctness is independent of dependence (null world)."""
    rng = random.Random(seed)
    counter = 0
    for split in ("DEV", "EVAL"):
        sdir = root / f"N1-{split}"
        tasks, strata, answers, rows = [], {}, {}, []
        for i in range(n_per_split):
            counter += 1
            n = 3 if i % 2 == 0 else 4
            dependent = (i // 2) % 2 == 0
            topic = TOPICS[i % len(TOPICS)]
            tid = f"n1-{counter:04d}"
            task = _task(rng, tid, topic, n, dependent, witness=planted)
            tasks.append(task)
            strata[tid] = {(3, True): "NS1A", (3, False): "NS1B", (4, True): "NS1C", (4, False): "NS1D"}[(n, dependent)]
            answers[tid] = {"decision": "ACCEPT_H" if not dependent else "INCONCLUSIVE_INSUFFICIENT_INDEPENDENT_SUPPORT",
                            "independent_support_family_count": n if not dependent else 2}
            if planted:
                m_ok, off_ok, parent_ok = dependent, not dependent, rng.random() < 0.7
            else:
                m_ok, off_ok, parent_ok = (rng.random() < 0.6 for _ in range(3))
            for arm, ok in ((mod.ARM_M, m_ok), (mod.ARM_OFF, off_ok), (mod.ARM_PARENT, parent_ok)):
                rows.append({"task_id": tid, "arm": arm, "correct": ok, "expected": answers[tid], "actual": {}})
                resp = sdir / "responses" / arm / f"{tid}.json"
                resp.parent.mkdir(parents=True, exist_ok=True)
                resp.write_text(json.dumps({"resource_receipt": {"model_calls": 1, "wall_time_seconds": 5.0 + rng.random()}}))
        (sdir / "public_tasks.json").write_text(json.dumps({"tasks": tasks}))
        (sdir / "private_oracle.json").write_text(json.dumps({"answers": answers, "strata": strata}))
        (sdir / "EVALUATION_ROWS.json").write_text(json.dumps(rows))
        (sdir / "FROZEN_SUITE.json").write_text(json.dumps({"seed": seed, "split": split, "corpus_freeze_sha256": "c" * 64}))


def test_naturalistic_witnesses_and_canary() -> None:
    rng = random.Random(3)
    dep = _task(rng, "t1", "stroke", 3, dependent=True, witness=True)
    f = mod.witness_features(dep)
    assert f["w_shared_root"] is True and f["w_xref_root"] is True and f["w_declared_overlap"] is True
    assert f["n_records"] == 3 and f["n_roots"] == 2 and f["root_ratio"] > 1.0
    mod.canary_check(dep)
    ind = _task(rng, "t2", "stroke", 3, dependent=False, witness=True)
    g = mod.witness_features(ind)
    assert not g["w_shared_root"] and not g["w_xref_root"] and g["n_roots"] == 3
    poisoned = dict(ind, stratum="NS1A", expected={"decision": "ACCEPT_H"}, pmid="1")
    assert mod.witness_features(poisoned) == g
    # duplicate identifier witness on shared grant ids
    ind["records"][0]["grant_ids"] = ["R01 HL000001"]
    ind["records"][2]["grant_ids"] = ["r01 hl000001"]
    assert mod.witness_features(ind)["w_dup_hash"] is True
    assert set(f) == set(mod.H1.witness_features({}))  # identical feature keys -> H-EXT-1 gate_fires reused


def _run(tmp_path: Path, planted: bool, seed: int) -> tuple[dict, dict | None]:
    build_fixture(tmp_path, seed, planted)
    dev = mod.extract_instances(tmp_path / "N1-DEV")
    freeze = mod.develop(dev, DESIGN)
    if freeze["selected_gate"] is None:
        return freeze, None
    ev = mod.extract_instances(tmp_path / "N1-EVAL")
    design = json.loads(DESIGN.read_text())
    design["null_draws"] = 300
    cell = mod.evaluate(ev, freeze, design, {r["task_id"] for r in dev["rows"]}, None)
    return freeze, cell


def test_planted_naturalistic_regime_routes_positive(tmp_path: Path) -> None:
    freeze, cell = _run(tmp_path, planted=True, seed=11)
    assert freeze["selected_gate"] in mod.CANDIDATE_GATES and freeze["gate_sha256"]
    assert cell is not None
    assert cell["terminal"] == "CONDITIONAL_ACTIVATION_IDENTIFIABLE_IN_NATURALISTIC_RECORDS", cell["gates"]
    refs = cell["references_reporting_only"]
    assert refs["activation_recall_vs_oracle"] == 1.0 and refs["activation_precision_vs_oracle"] == 1.0
    assert refs["M_vs_OFF_paired"]["mcnemar_exact_p"] <= 1.0
    roll = mod.rollup(freeze, cell, DESIGN, None)
    md = mod.rollup_markdown(roll)
    assert "H-EXT-1N" in md and roll["binding_terminal"] == cell["terminal"]


def test_null_world_does_not_route_positive(tmp_path: Path) -> None:
    freeze, cell = _run(tmp_path, planted=False, seed=12)
    if cell is None:
        assert freeze["terminal_if_none"] == "NO_CANDIDATE_GATE_ON_DEV"
    else:
        assert cell["terminal"] != "CONDITIONAL_ACTIVATION_IDENTIFIABLE_IN_NATURALISTIC_RECORDS"


def test_missing_responses_route_to_cannot_check(tmp_path: Path) -> None:
    build_fixture(tmp_path, 5, planted=True)
    rows = json.loads((tmp_path / "N1-EVAL" / "EVALUATION_ROWS.json").read_text())
    rows[0]["missing"] = True
    (tmp_path / "N1-EVAL" / "EVALUATION_ROWS.json").write_text(json.dumps(rows))
    dev = mod.extract_instances(tmp_path / "N1-DEV")
    freeze = mod.develop(dev, DESIGN)
    ev = mod.extract_instances(tmp_path / "N1-EVAL")
    cell = mod.evaluate(ev, freeze, {"null_draws": 50}, set(), None)
    assert cell["terminal"] == "CANNOT_CHECK_RUN_INVALID" and cell["n_missing"] == 1


def test_dev_eval_overlap_is_design_violation(tmp_path: Path) -> None:
    build_fixture(tmp_path, 6, planted=True)
    dev = mod.extract_instances(tmp_path / "N1-DEV")
    freeze = mod.develop(dev, DESIGN)
    ev = mod.extract_instances(tmp_path / "N1-EVAL")
    overlap = {ev["rows"][0]["task_id"]}
    cell = mod.evaluate(ev, freeze, {"null_draws": 50}, overlap, None)
    assert cell["terminal"] == "DESIGN_VIOLATION_RUN_VOID"


def test_mcnemar_exact() -> None:
    assert mod.mcnemar_exact(0, 0) == 1.0
    assert abs(mod.mcnemar_exact(10, 0) - 2 / 1024) < 1e-12
    assert mod.mcnemar_exact(5, 5) == 1.0
