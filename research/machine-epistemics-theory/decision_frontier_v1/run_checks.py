"""Content-bound finite-calibration receipt; exit 0=match, 1=defect, 2=unavailable.

No protected study is run. This checks only this directory's theoretical fixtures.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import io
import json
from pathlib import Path
import platform
import sys
import unittest

from frontier import CannotCheck, memory_frontier, observed_memory_frontier, Solver
from test_frontier import FrontierTests, calibrate, model, query

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / "RESULTS_V1.json"
BOUND = ("README.md", "THEORY.md", "frontier.py", "test_frontier.py", "run_checks.py",
         "SOURCES_AND_REVIEW.md", "OCM_ABSORPTION.md", "INTEGRATION_V1.json")


def scientific_payload() -> dict:
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FrontierTests)
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    if not result.wasSuccessful():
        raise AssertionError(stream.getvalue())
    counts = calibrate()
    bits = model((("00",), ("01",), ("10",), ("11",)),
                 (query("x", (0, 0, 1, 1), 2), query("y", (0, 1, 0, 1), 3)))
    triple = model(("ab", "bc", "ac"))
    return {
        "unit_tests": {"run": result.testsRun, "failures": len(result.failures),
                       "errors": len(result.errors), "skipped": len(result.skipped)},
        "finite_corpus": counts,
        "two_bit_frontier": memory_frontier(bits),
        "overlap_frontier": memory_frontier(triple),
        "partial_signal_frontier": observed_memory_frontier(bits, ("0", "1", "0", "1")),
        "constant_signal_no_query": observed_memory_frontier(model(("a", "b")), ("same", "same")),
        "correlated_joint_cost": str(Solver(model((("00",), ("11",)),
                                            (query("x", (0, 1), 2), query("y", (0, 1), 3)))).solve()[0]),
        "counterexamples": ["pairwise compatibility is not whole-set compatibility",
                            "no unique coarsest sufficient partition for set-valued acceptable actions",
                            "correlation invalidates unrestricted direct sum",
                            "revoked observation can invalidate an old decision",
                            "unobserved history cannot be encoded as free advice"],
        "undetectable_assumption_failures": ["omitted actual world despite declared closure",
                                            "wrong observation from a supposedly deterministic trusted channel"],
        "independent_review": "NOT_OBTAINED", "proof_assistant": "NOT_RUN",
        "novelty": "NOT_ESTABLISHED", "ocm_adoption": False,
        "full_foundation_complete": False,
    }


def bindings() -> dict:
    return {name: sha256((ROOT / name).read_bytes()).hexdigest() for name in BOUND}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Create an initial receipt; refuses overwrite")
    mode.add_argument("--verify", action="store_true", help="Recheck bytes and all finite results")
    args = parser.parse_args()
    try:
        if args.write and RECEIPT.exists():
            raise ValueError("receipt exists; create a successor identity instead of overwriting")
        h = bindings()
        if args.verify:
            saved = json.loads(RECEIPT.read_text())
            if saved.get("schema") != "ME-DF-RECEIPT-1" or saved.get("bound_sha256") != h:
                raise ValueError("receipt schema or source binding mismatch")
        payload = scientific_payload()
        if args.write:
            out = {"schema": "ME-DF-RECEIPT-1", "task": "ME-DECISION-FRONTIER-V1", "issue": 314,
                   "base_sha": "24566f00a9dc4425a438fcfac05d13c6b2d903db",
                   "execution_class": "EXACT_FORMAL_CALIBRATION_NOT_PROTECTED_EMPIRICAL",
                   "record_environment": {"python": platform.python_version(), "platform": platform.platform(),
                                          "host_class": "isolated Linux analysis container; not operator compute"},
                   "proof_grade": "WRITTEN_FINITE_FAMILY_PROOFS_PLUS_FINITE_CALIBRATION",
                   "bound_sha256": h, "scientific_payload": payload,
                   "commands": ["python -m unittest -v test_frontier", "python run_checks.py --verify"],
                   "limitations": ["whole repository tests not run", "no proof assistant", "no independent review",
                                   "no OCM adapter parity", "no authorized protected study", "no main merge"]}
            RECEIPT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        elif saved.get("scientific_payload") != payload:
            raise ValueError("fresh result differs from committed receipt")
        print(json.dumps({"status": "PASS", "mode": "write" if args.write else "verify",
                          "tests": payload["unit_tests"], "counts": payload["finite_corpus"],
                          "current_python": platform.python_version()}, sort_keys=True))
        return 0
    except (FileNotFoundError, CannotCheck) as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
