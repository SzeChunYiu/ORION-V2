"""Apply real local source mutants and demand the intended assertion failure, not a crash."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from causal_core import CannotCheck

ROOT = Path(__file__).resolve().parent
MUTANTS = (
    ("condition_in_wrong_world",
     'conditioning = model.solve(u) if self.kind == "CF" else target',
     'conditioning = target', 'test_wrong_world_conditioning_mutant'),
    ("empty_class_promoted",
     'IntervalResult("CONFLICT", None, None, (), 0)',
     'IntervalResult("IDENTIFIED", None, None, (), 0)', 'test_empty_models_are_conflict_not_vacuous_truth'),
    ("undefined_query_promoted",
     'IntervalResult("CANNOT_CHECK", None, None, (model.fingerprint,), len(vals))',
     'IntervalResult("PARTIAL", None, None, (model.fingerprint,), len(vals))',
     'test_zero_condition_model_is_not_silently_dropped'),
    ("population_drift_omitted", 'return eps + sum(', 'return sum(',
     'test_invariance_without_population_match_fails'),
    ("sample_promoted_to_exact_law",
     'if query.evaluate(m) > 0)', 'if query.evaluate(m) == 1)',
     'test_single_success_is_not_population_probability_one'),
    ("changed_dependency_ignored",
     'return "MATCH" if all(current[k] == v for k, v in bound.items()) else "REVALIDATE"',
     'return "MATCH"', 'test_dependency_drift_revalidates'),
    ("counterfactual_coupling_assumed",
     'return max(F(0), p1 - p0) / (1 - p0), min(p1, 1 - p0) / (1 - p0)',
     'return p1, p1', 'test_sharp_binary_bounds'),
    ("incompatible_marginal_accepted",
     'if tuple(observed[s] for s in projections) != target:\n            return False',
     'if tuple(observed[s] for s in projections) != target:\n            return True',
     'test_global_marginal_witness_positive_and_rejection'),
)


def audit() -> dict[str, object]:
    if not __debug__:
        raise CannotCheck("OPTIMIZED_CHECKS_NOT_ALLOWED")
    original = (ROOT / "causal_core.py").read_text(encoding="utf-8")
    reports = []
    for name, old, new, test in MUTANTS:
        if original.count(old) != 1:
            raise CannotCheck(f"MUTATION_ANCHOR_COUNT:{name}:{original.count(old)}")
        with tempfile.TemporaryDirectory(prefix="me-causal-mutant-") as tmp:
            path = Path(tmp)
            shutil.copyfile(ROOT / "test_causal_core.py", path / "test_causal_core.py")
            # First run the intended test on the unmodified source.
            (path / "causal_core.py").write_text(original, encoding="utf-8")
            command = [sys.executable, "-B", "-m", "unittest", "-q", f"test_causal_core.CausalTests.{test}"]
            baseline = subprocess.run(command, cwd=path, text=True, capture_output=True, timeout=10)
            if baseline.returncode != 0:
                raise CannotCheck(f"BASELINE_NOT_GREEN:{name}")
            mutated = original.replace(old, new, 1)
            if mutated == original:
                raise CannotCheck(f"MUTATION_NOT_APPLIED:{name}")
            (path / "causal_core.py").write_text(mutated, encoding="utf-8")
            result = subprocess.run(command, cwd=path, text=True, capture_output=True, timeout=10)
            log = result.stdout + result.stderr
            if result.returncode != 1 or "FAILED (failures=1)" not in log or f"FAIL: {test}" not in log:
                raise AssertionError(f"MUTANT_NOT_KILLED_BY_INTENDED_ASSERTION:{name}: {log}")
            reports.append({"mutant": name, "anchor_occurrences": 1, "applied": True,
                            "baseline_exit": baseline.returncode, "mutant_exit": result.returncode,
                            "test": test, "status": "KILLED_BY_ASSERTION"})
    return {"mutants": len(reports), "killed": len(reports), "reports": reports}


if __name__ == "__main__":
    try:
        print(json.dumps({"status": "PASS", "result": audit()}, sort_keys=True, indent=2))
    except (CannotCheck, OSError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}))
        sys.exit(2)
    except AssertionError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}))
        sys.exit(1)
