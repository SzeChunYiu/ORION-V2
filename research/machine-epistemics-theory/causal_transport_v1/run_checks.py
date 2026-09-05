"""Deterministic bounded theory checks: 0=PASS, 1=defect, 2=CANNOT_CHECK.

--write-receipt creates a new receipt and refuses overwrite.
--verify checks the frozen bytes AND reruns the exact suite/mutation audit.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import io
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import unittest

from causal_core import CannotCheck, digest
from mutation_audit import audit
from test_causal_core import CausalTests, calibrate

ROOT = Path(__file__).resolve().parent
BASE_SHA = "24566f00a9dc4425a438fcfac05d13c6b2d903db"
FILES = ("README.md", "THEORY.md", "FRONTIER.md", "SOURCES.md", "CLAIMS.json",
         "causal_core.py", "test_causal_core.py", "mutation_audit.py", "run_checks.py")


def bindings() -> dict[str, str]:
    return {name: sha256((ROOT / name).read_bytes()).hexdigest() for name in FILES}


def check_claims() -> int:
    claims = json.loads((ROOT / "CLAIMS.json").read_text(encoding="utf-8"))
    theory = (ROOT / "THEORY.md").read_text(encoding="utf-8")
    sections = dict(re.findall(r"^## (CT-\d+)[^\n]*\n(.*?)(?=^## |\Z)", theory, flags=re.M | re.S))
    rows = claims["claims"]
    if {r["id"] for r in rows} != {f"CT-{i:02d}" for i in range(1, 14)} or len(rows) != 13:
        raise AssertionError("CLAIM_SET_CHANGED")
    for row in rows:
        if sha256(sections[row["id"]].encode()).hexdigest() != row["section_sha256"]:
            raise AssertionError(f"THEOREM_SECTION_DRIFT:{row['id']}")
        if row["independent_review"] != "NOT_OBTAINED" or row["novelty"] != "NOT_CLAIMED":
            raise AssertionError("UNSUPPORTED_CLAIM_PROMOTION")
        if not row["tests"] or any(not hasattr(CausalTests, t) for t in row["tests"]):
            raise AssertionError(f"MISSING_CLAIM_CHECKER:{row['id']}")
    return len(rows)


def evaluate() -> dict[str, object]:
    if not __debug__:
        raise CannotCheck("OPTIMIZED_CHECKS_NOT_ALLOWED")
    claims = check_claims()
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CausalTests))
    if not result.wasSuccessful() or result.skipped or result.testsRun == 0:
        raise AssertionError(log.getvalue())
    counts = calibrate()  # One reporting pass; counters are NOT added to the test's separate pass.
    mutations = audit()
    return {"status": "PASS", "scope": "DECLARED_FINITE_CAUSAL_TRANSPORT_FRAGMENT",
            "claim_sections": claims, "unit_tests": result.testsRun,
            "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
            "calibration": counts, "mutation_audit": mutations,
            "full_foundation_closed": False, "independent_review": "NOT_OBTAINED",
            "proof_assistant": "NOT_RUN", "empirical_validation": "NOT_RUN", "novelty": "NOT_CLAIMED"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write-receipt", action="store_true")
    action.add_argument("--verify", action="store_true")
    parser.add_argument("--receipt", type=Path, default=ROOT / "RECEIPT.json")
    args = parser.parse_args()
    try:
        if not __debug__:
            raise CannotCheck("OPTIMIZED_CHECKS_NOT_ALLOWED")
        hashed = bindings()
        old = None
        if args.verify:
            old = json.loads(args.receipt.read_text(encoding="utf-8"))
            body = {k: v for k, v in old.items() if k != "body_sha256"}
            if old.get("body_sha256") != digest(body) or old.get("bound_files") != hashed:
                raise AssertionError("RECEIPT_OR_BOUND_FILE_DRIFT")
        result = evaluate()
        if old is not None and old.get("result") != result:
            raise AssertionError("REPLAY_RESULT_MISMATCH")
        if args.write_receipt:
            record = {"schema": "ME_CAUSAL_TRANSPORT_RECEIPT_V1", "issue": 315,
                      "base_git_sha": BASE_SHA, "execution_class": "LOCAL_EXACT_CALIBRATION_NOT_PROTECTED",
                      "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                                      "platform": platform.platform()},
                      "bound_files": hashed, "result": result}
            record["body_sha256"] = digest(record)
            with args.receipt.open("x", encoding="utf-8") as stream:
                stream.write(json.dumps(record, sort_keys=True, indent=2) + "\n")
        print(json.dumps({"status": "PASS", "result": result,
                          "receipt_verified": args.verify, "receipt_written": args.write_receipt},
                         sort_keys=True, indent=2))
        return 0
    except (CannotCheck, FileNotFoundError, OSError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except (AssertionError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
