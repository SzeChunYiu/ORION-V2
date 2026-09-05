"""FM80-§9-EXEC checker discipline: planted positive passes at n=70, registered n=30 is UNDERPOWERED not negative,
null fails 9.1, fidelity regression fails 9.3, A2 reproduction fails 9.5; SD80 preconditions: 3c fails on every case."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "research" / "experiments" / "fm80-exec" / "fm80_exec_gate.py"
spec = importlib.util.spec_from_file_location("fm80_exec_gate", P); M = importlib.util.module_from_spec(spec); sys.modules["fm80_exec_gate"] = M; spec.loader.exec_module(M)


def test_selftest_plants_and_no_alarm() -> None:
    rep = M.planted_and_no_alarm()
    assert all(v for k, v in rep.items() if isinstance(v, bool)), rep
    assert abs(rep["best_case_p_at_bar_n30"] - 0.25) < 1e-12 and rep["best_case_p_at_bar_n61"] < 0.05 / 3


def test_clause_census_counts() -> None:
    c = {k: sum(1 for v in M.CLAUSES.values() if v["class"] == k) for k in ("EXACT", "MODEL_PROXY", "HUMAN_ONLY")}
    assert c == {"EXACT": 12, "MODEL_PROXY": 3, "HUMAN_ONLY": 4}


def test_sd80_preconditions_3c_fails_everywhere() -> None:
    rows = M.case_table_from_sd80(ROOT / "research" / "experiments" / "sd80" / "SD80_CASE_MATRIX_CASES_V1.json")
    assert len(rows) == 455
    pre = M.preconditions(rows)
    assert pre["3c"]["n_pass"] == 0 and pre["3c"]["status"] == "SOME_FAIL" and pre["3c"]["n_checkable"] == 455
    assert pre["4.2"]["status"] == "CANNOT_CHECK"
