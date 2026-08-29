from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/run_formal_discovery_generated_suite.py"


def load_suite():
    spec = importlib.util.spec_from_file_location("orion_formal_generated_suite", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_all_generated_fm_fg_studies_have_hidden_exact_oracle(tmp_path):
    suite = load_suite()
    workdir = tmp_path / "suite"
    suite.prepare(workdir, list(suite.STUDIES), 2, 12345, ["TEST"], False)
    public = json.loads((workdir / "public_tasks.json").read_text())
    private = json.loads((workdir / "private_oracle.json").read_text())
    freeze = json.loads((workdir / "FROZEN_SUITE.json").read_text())
    assert len(public["tasks"]) == len(suite.STUDIES) * 2
    assert set(task["study_id"] for task in public["tasks"]) == set(suite.STUDIES)
    assert set(private["answers"]) == {task["task_id"] for task in public["tasks"]}
    assert "answers" not in json.dumps(public)
    assert freeze["private_oracle_visible_to_solver"] is False
    assert all(value is False for value in freeze["authority"].values())


def test_exact_answers_score_one_without_promoting_science(tmp_path):
    suite = load_suite()
    workdir = tmp_path / "suite"
    suite.prepare(
        workdir,
        ["FM10", "FM20", "FM30", "FM40", "FM50", "FM60", "FG10", "FG40", "FG70", "FG80"],
        2,
        7,
        ["TEST"],
        False,
    )
    answers = json.loads((workdir / "private_oracle.json").read_text())["answers"]
    for task_id, answer in answers.items():
        path = workdir / "responses" / "TEST" / f"{task_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"answer": answer}))
    suite.evaluate(workdir, ["TEST"])
    summary = json.loads((workdir / "EVALUATION_SUMMARY.json").read_text())
    assert summary["summary"]["TEST"]["accuracy"] == 1.0
    assert all(value is False for value in summary["authority"].values())


def test_dispatch_removes_private_oracle_during_child_execution(tmp_path, monkeypatch):
    suite = load_suite()
    workdir = tmp_path / "suite"
    suite.prepare(workdir, ["FM10", "FG10", "FG70"], 1, 99, ["TEST"], False)
    stub = tmp_path / "stub.py"
    stub.write_text(
        "import argparse,json,os\n"
        "from pathlib import Path\n"
        "p=argparse.ArgumentParser();p.add_argument('--request');p.add_argument('--response');a=p.parse_args()\n"
        "req=Path(a.request); root=req.parents[2]\n"
        "assert not (root/'private_oracle.json').exists()\n"
        "assert os.environ.get('ORION_GOLD_ACCESS')=='NONE'\n"
        "out={'answer':{}}\n"
        "Path(a.response).parent.mkdir(parents=True,exist_ok=True);Path(a.response).write_text(json.dumps(out))\n"
    )
    monkeypatch.setenv("ORION_FORMAL_ARM_COMMAND", f"{sys.executable} {stub}")
    suite.dispatch(workdir, ["TEST"], 2, False)
    receipt = json.loads((workdir / "DISPATCH_RECEIPT.json").read_text())
    commitment = json.loads((workdir / "PRIVATE_ORACLE_COMMITMENT.json").read_text())
    assert commitment["private_removed_before_dispatch"] is True
    assert receipt["all_returncodes_zero"] is True
    assert receipt["oracle_restored_hash_match"] is True
    assert (workdir / "private_oracle.json").exists()


def test_generation_is_seed_deterministic(tmp_path):
    suite = load_suite()
    a = tmp_path / "a"
    b = tmp_path / "b"
    suite.prepare(a, ["FM10", "FM30", "FG10", "FG40"], 3, 20260829, ["TEST"], False)
    suite.prepare(b, ["FM10", "FM30", "FG10", "FG40"], 3, 20260829, ["TEST"], False)
    assert (a / "public_tasks.json").read_bytes() == (b / "public_tasks.json").read_bytes()
    assert (a / "private_oracle.json").read_bytes() == (b / "private_oracle.json").read_bytes()


def test_fg30_operation_oracle_is_unique():
    suite = load_suite()
    for seed in range(30):
        public, answer = suite.gen_fg30(random.Random(seed))
        consistent = []
        for candidate in public["candidate_operation_ids"]:
            if all(
                suite.operation_value(candidate, x, y, public["modulus"]) == z
                for x, y, z in public["examples"]
            ):
                consistent.append(candidate)
        assert consistent == [answer["operation_id"]]


def test_fg40_axiom_oracle_is_unique_minimum():
    suite = load_suite()
    for seed in range(30):
        public, answer = suite.gen_fg40(random.Random(seed))
        features = public["feature_ids"]
        valid = []
        for size in range(len(features) + 1):
            for subset in itertools.combinations(features, size):
                chosen = list(subset)
                if all(suite.conjunction_holds(row, chosen) for row in public["positive_models"]) and all(
                    not suite.conjunction_holds(row, chosen) for row in public["negative_countermodels"]
                ):
                    valid.append(tuple(sorted(chosen)))
            if valid:
                break
        assert valid == [tuple(answer["axiom_feature_ids"])]


def test_fg80_representation_feature_is_unique():
    suite = load_suite()
    for seed in range(30):
        public, answer = suite.gen_fg80(random.Random(seed))
        features = list(public["target"])
        consistent = [
            feature
            for feature in features
            if all(
                ("YES" if row[feature] else "NO") == row["decision"]
                for row in public["demonstrations"]
            )
        ]
        assert consistent == [answer["representation_feature"]]


def test_fm50_generated_objects_are_complete_walking_arrow_categories():
    suite = load_suite()
    for seed in range(10):
        public, _ = suite.gen_fm50(random.Random(seed))
        for category in (public["source_category"], public["target_category"]):
            endpoints = category["endpoints"]
            composition = {(left, right): result for left, right, result in category["composition"]}
            expected_pairs = {
                (left, right)
                for left in category["morphisms"]
                for right in category["morphisms"]
                if endpoints[left][1] == endpoints[right][0]
            }
            assert set(composition) == expected_pairs
            for obj, identity in category["identities"].items():
                assert endpoints[identity] == [obj, obj]
