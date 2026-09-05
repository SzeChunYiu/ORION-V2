"""OCM-R1A: controller vs sequential federation on VSW classes — checker discipline.

Planted failure: the checker's M1 mutation (first-draft sequential-cost formula) must be caught;
a planted fake results file whose SINGLETONS_5 numbers disagree with the registered values must
route LANE_DEFECT.  No-alarm: the rectangular class ties (I = 0) and the registered instance
reproduces 8 / 9 / 9 with I = 1.  The protected stage refuses without authorization (exit 3).
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "research" / "experiments" / "ocm-r1a" / "ocm_r1a_run.py"


def load():
    spec = importlib.util.spec_from_file_location("ocm_r1a_run", RUNNER)
    assert spec and spec.loader
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


M = load()
R = M.reference()


def test_rectangular_control_ties_and_registered_instance_fires() -> None:
    lin = M.run_class("LINEAR_F2^2", R, None, None)
    assert lin["status"] == "OK" and lin["interaction_term"] == 0
    assert lin["arms"][M.M_ARM]["worst_case"] == lin["arms"][M.B5_ARM]["worst_case"] == 5
    s5 = M.run_class("SINGLETONS_5", R, None, None)
    assert s5["status"] == "OK"
    assert (s5["arms"][M.M_ARM]["worst_case"], s5["arms"][M.B5_ARM]["B_first"]["worst_case"], s5["arms"][M.B5_ARM]["Z_first"]["worst_case"]) == (8, 9, 9)
    assert s5["interaction_term"] == 1
    assert s5["paired"]["worlds_federation_better"] == 0  # the federation never identifies a world faster than the controller? not required; recorded
    assert len(s5["arms"][M.M_ARM]["per_world"]) == s5["worlds"] == 160


def test_planted_checker_mutation_fires() -> None:
    assert M.planted_mutation(R)["fired"] is True


def test_gates_route_lane_defect_on_planted_wrong_numbers() -> None:
    res = M.run_study(("LINEAR_F2^2", "SINGLETONS_5"), None, "SELFTEST")
    g = M.gates(res)
    assert g["G0a_KNOWN_ANSWER"]["pass"] and g["ROUTE"]["route"].startswith("PARENT_OWNED")
    bad = json.loads(json.dumps(res))
    for r in bad["classes"]:
        if r["class"] == "SINGLETONS_5":
            r["arms"][M.M_ARM]["worst_case"] = 7   # planted: a controller better than the counting bound
    gb = M.gates(bad)
    assert gb["G0a_KNOWN_ANSWER"]["pass"] is False and gb["ROUTE"]["route"] == "LANE_DEFECT"


def test_protected_refuses_without_authorization(tmp_path: Path) -> None:
    assert not M.AUTH_FILE.exists()
    assert M.stage_protected(tmp_path, tmp_path / "no-seed") == 3
