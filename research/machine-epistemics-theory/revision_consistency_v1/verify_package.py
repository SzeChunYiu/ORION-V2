"""Content-bound exact package runner; 0=valid, 1=defect, 2=unavailable.

No receipt hashes itself. Authenticity comes only from an independently fixed commit.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib
import io
import json
import platform
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REL = HERE.relative_to(ROOT)
FILES = ("DESIGN.md", "THEORY.md", "SOURCES.md", "README.md", "CORRECTIONS.md",
         "model.py", "study.py", "test_model.py", "verify_package.py",
         "RESULT.json", "CALIBRATION_INITIAL.json")
WORKFLOW = ".github/workflows/me-revision-consistency.yml"
DESIGN_BLOB = "ac8d1ae5fea5fb69c34ac54c68d702c905e96045"
RECEIPT = HERE / "RECEIPT.json"


class Defect(ValueError):
    pass


def check(value: bool, message: str) -> None:
    if not value:
        raise Defect(message)


def paths() -> dict[str, Path]:
    return {**{str(REL / name): HERE / name for name in FILES}, WORKFLOW: ROOT / WORKFLOW}


def bindings() -> dict[str, str]:
    out = {}
    for name, path in paths().items():
        data = path.read_bytes()  # missing source remains CANNOT_CHECK, not a pass
        out[name] = hashlib.sha256(data).hexdigest()
        if path.name == "DESIGN.md":
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            check(blob == DESIGN_BLOB, "pre-calibration design bytes changed")
    return out


def execute() -> dict:
    suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_model.py")
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output, verbosity=1).run(suite)
    summary = {"tests": result.testsRun, "failures": len(result.failures),
               "errors": len(result.errors), "skipped": len(result.skipped)}
    check(result.testsRun >= 37, "insufficient test denominator")
    check(result.wasSuccessful() and not result.skipped, output.getvalue())
    study = importlib.import_module("study")
    calculated = study.run()
    check(json.loads((HERE / "RESULT.json").read_text()) == calculated,
          "result differs from fresh exact computation")
    check(json.loads((HERE / "CALIBRATION_INITIAL.json").read_text()) == calculated,
          "initial finite result changed without a successor identity")
    return {"tests": summary, "exact_result_sha256": hashlib.sha256(
                (HERE / "RESULT.json").read_bytes()).hexdigest(),
            "terminal": calculated["terminal"],
            "parent_disposition": calculated["parent_disposition"],
            "foundation_overall": calculated["foundation_overall"],
            "grants_scientific_authority": False}


def verify() -> dict:
    record = json.loads(RECEIPT.read_text())
    check(record.get("schema") == "ME_REVISION_CONSISTENCY_RECEIPT_V1", "receipt schema")
    check(record.get("bindings") == bindings(), "binding set or source digest drift")
    check(record.get("verification") == execute(), "verification record mismatch")
    check(record.get("base_commit") == "24566f00a9dc4425a438fcfac05d13c6b2d903db", "base identity")
    check(record.get("design_commit") == "59b6819574f494354b880605998ffddbc5687077", "design identity")
    check(record.get("independent_review") == "NOT_OBTAINED__DISCLOSED_LIMITATION", "review promotion")
    check(record.get("full_local_clean_clone") is False, "clone claim promotion")
    check(record.get("production_atomicity") == "CANNOT_CHECK", "atomicity promotion")
    return record["verification"]


def selftest() -> dict:
    """Run valid, drift, missing and binding-omission cases in disposable local copies."""
    results = {}
    for case, expected in (("valid", 0), ("source_drift", 1), ("missing_source", 2),
                           ("omitted_binding", 1), ("false_independence", 1)):
        with tempfile.TemporaryDirectory(prefix="me-revision-") as tmp:
            root = Path(tmp)
            shutil.copytree(HERE, root / REL, ignore=shutil.ignore_patterns("__pycache__"))
            (root / WORKFLOW).parent.mkdir(parents=True)
            shutil.copy2(ROOT / WORKFLOW, root / WORKFLOW)
            packet = root / REL
            if case == "source_drift":
                with (packet / "model.py").open("a") as stream:
                    stream.write("\n# planted source drift\n")
            elif case == "missing_source":
                (packet / "THEORY.md").unlink()
            elif case in ("omitted_binding", "false_independence"):
                r = json.loads((packet / "RECEIPT.json").read_text())
                if case == "omitted_binding":
                    r["bindings"].pop(str(REL / "model.py"))
                else:
                    r["independent_review"] = "PASS"
                (packet / "RECEIPT.json").write_text(json.dumps(r))
            run = subprocess.run([sys.executable, str(packet / "verify_package.py"), "--verify"],
                                 text=True, capture_output=True, timeout=45)
            check(run.returncode == expected, f"receipt control {case}: {run.returncode} != {expected}")
            results[case] = run.returncode
    return {"receipt_controls": results, "cases": len(results), "passed": len(results)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--verify", action="store_true")
    mode.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    try:
        check(sys.version_info >= (3, 12), "Python >=3.12 required")
        if args.write:
            bound = bindings()
            record = {"schema": "ME_REVISION_CONSISTENCY_RECEIPT_V1",
                "base_commit": "24566f00a9dc4425a438fcfac05d13c6b2d903db",
                "design_commit": "59b6819574f494354b880605998ffddbc5687077",
                "bindings": bound, "verification": execute(),
                "environment_at_generation": {"python": platform.python_version(),
                     "implementation": platform.python_implementation(), "system": platform.system(),
                     "machine": platform.machine()},
                "full_local_clean_clone": False,
                "execution_location": "isolated Linux analysis container; not Mac/LUNARC",
                "production_atomicity": "CANNOT_CHECK",
                "independent_review": "NOT_OBTAINED__DISCLOSED_LIMITATION",
                "authority": "An external commit anchors this packet; its own hashes confer no authority."}
            RECEIPT.write_text(json.dumps(record, sort_keys=True, indent=2) + "\n")
            output = record["verification"]
        elif args.selftest:
            output = selftest()
        else:
            output = verify()
        print(json.dumps(output, sort_keys=True, indent=2))
        return 0
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"terminal": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except (ValueError, AssertionError, TypeError, KeyError, ImportError) as exc:
        print(json.dumps({"terminal": "FAIL", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
