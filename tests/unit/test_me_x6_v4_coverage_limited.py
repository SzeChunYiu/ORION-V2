"""ME-X6 V4 checker discipline: the frozen fit reproduces (D_8 = V3's refit, known answer), the
planted tie violation and the planted gap-tie both fire in the selftest, an ordinary dev run routes
to a TYPING_VALUE_EQUALS_COVERAGE_GAP terminal (no-alarm), and protected refuses without authorization."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "research" / "experiments" / "me-x6-v4" / "mex6v4_run.py"


def load():
    spec = importlib.util.spec_from_file_location("mex6v4_run", RUNNER)
    assert spec and spec.loader
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


M = load()


def test_frozen_fit_reproduces_and_d8_is_v3_refit() -> None:
    fit = M.frozen_fit()
    assert M.canonical_json(M.fit_on_development()) == M.canonical_json(fit)
    assert M.v3_known_answer(fit)["pass"] is True
    design = json.loads(M.DESIGN_JSON.read_text())
    assert design["fit_sha256"] == M.sha256_file(M.FIT_JSON)


def test_selftest_plants_fire_and_dev_route_is_coverage_gap(tmp_path: Path) -> None:
    assert M.stage_selftest(tmp_path) == 0
    rep = json.loads((tmp_path / "ME_X6_V4_SELFTEST_REPORT_V1.json").read_text())
    assert rep["planted_tie_violation_fires"] and rep["planted_untyped_recovery_fires"]
    assert M.stage_dev(tmp_path, 1) == 0
    a = json.loads((tmp_path / "ME_X6_V4_DEVELOPMENT_ANALYSIS_V1.json").read_text())
    assert a["gates"]["ROUTE"]["route"].startswith("TYPING_VALUE_EQUALS_COVERAGE_GAP")
    assert a["gates"]["G1_TIE_ON_EXERCISED_STRATA"]["pass"] is True
    curve = a["gates"]["G3_COVERAGE_CURVE"]["advantage_M_minus_refit_by_coverage"]
    assert all(curve["8"][s] == 0 for s in curve["8"])


def test_protected_refuses_without_authorization(tmp_path: Path) -> None:
    assert not M.AUTH_FILE.exists()
    assert M.stage_protected(tmp_path, 1, tmp_path / "no-seed") == 3
