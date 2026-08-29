from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json"
FM_PROTOCOL = ROOT / "research/experiments/CONCEPTUAL_TRANSFER_FORMAL_MECHANICS_PROTOCOL_V1.json"
FG_PROTOCOL = ROOT / "research/experiments/FORMALISM_GENESIS_PROTOCOL_V1.json"
RUNNER = ROOT / "scripts/run_formal_discovery_campaign.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("orion_formal_campaign", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_campaign_task_counts_match_registered_generated_studies():
    plan = json.loads(PLAN.read_text())
    fm = json.loads(FM_PROTOCOL.read_text())
    fg = json.loads(FG_PROTOCOL.read_text())
    fm_min = {item["id"]: item["minimum_tasks"] for item in fm["studies"] if "minimum_tasks" in item}
    fg_min = {item["id"]: item["minimum_tasks"] for item in fg["studies"] if "minimum_tasks" in item}
    for study_id in ("FM10", "FM20", "FM30", "FM40", "FM50", "FM60"):
        assert plan["studies"][study_id]["tasks"] == fm_min[study_id]
    for study_id in ("FG10", "FG20", "FG30", "FG40", "FG50", "FG60", "FG70", "FG80"):
        assert plan["studies"][study_id]["tasks"] == fg_min[study_id]


def test_campaign_keeps_non_synthetic_studies_outside_generated_lane():
    plan = json.loads(PLAN.read_text())
    excluded = plan["excluded_from_generated_campaign"]
    assert set(excluded) == {"FM70", "FM80", "FG90"}
    assert "naturalistic" in excluded["FM80"].lower()
    assert "exploratory" in excluded["FG90"].lower()


def test_every_generated_study_has_parent_and_integrated_comparators():
    plan = json.loads(PLAN.read_text())
    for study_id, spec in plan["studies"].items():
        arms = set(spec["arms"])
        assert "STRONGEST_DOMAIN_FORMAL_PARENT" in arms
        if study_id.startswith("FM"):
            assert "F0_PARENT_FEDERATION" in arms
            assert "F2_STATIC_NO_TRANSFER_DISCOVERY" in arms
            assert "F2_TRANSFER_DISCOVERY_FULL" in arms
        else:
            assert "F0_FORMAL_PARENT_FEDERATION" in arms
            assert "F2_STATIC_NO_FORMALISM_GENESIS" in arms
            assert "F2_FORMALISM_GENESIS_FULL" in arms


def test_specialized_parent_arms_are_bound_where_applicable():
    plan = json.loads(PLAN.read_text())
    assert "STRUCTURE_MAPPING_PARENT" in plan["studies"]["FM10"]["arms"]
    assert "ANTI_UNIFICATION_OR_MDL_PARENT_WHEN_APPLICABLE" in plan["studies"]["FM20"]["arms"]
    assert "FCA_PARENT_WHEN_APPLICABLE" in plan["studies"]["FM30"]["arms"]


def test_campaign_prepare_materializes_study_specific_counts_and_hashes(tmp_path):
    runner = load_runner()
    campaign = tmp_path / "campaign"
    plan = json.loads(PLAN.read_text())
    runner.prepare(PLAN, campaign, ["FM30", "FG80"], False)
    manifest = json.loads((campaign / "CAMPAIGN_FREEZE_MANIFEST.json").read_text())
    rows = {row["study_id"]: row for row in manifest["studies"]}
    assert rows["FM30"]["task_count"] == plan["studies"]["FM30"]["tasks"]
    assert rows["FG80"]["task_count"] == plan["studies"]["FG80"]["tasks"]
    assert rows["FM30"]["arms"] == plan["studies"]["FM30"]["arms"]
    assert rows["FG80"]["arms"] == plan["studies"]["FG80"]["arms"]
    assert len(rows["FM30"]["private_oracle_sha256"]) == 64
    assert len(rows["FG80"]["freeze_sha256"]) == 64
    assert manifest["private_oracle_visible_to_solver"] is False
    assert all(value is False for value in manifest["authority"].values())
