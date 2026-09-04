"""Verify the additive temporal package: 0=checked, 1=defect, 2=unavailable."""
from __future__ import annotations

import argparse
import hashlib
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
ROOT = HERE.parents[3]
REL = HERE.relative_to(ROOT)
WORKFLOW = ".github/workflows/me-temporal-validity.yml"
FILES = ("DESIGN.md", "THEORY.md", "SOURCES.md", "README.md", "temporal.py",
         "calibrate.py", "test_temporal.py", "run.py", "RESULT.json")
DESIGN_BLOB = "2312e6ab77cb89212d9e8ceea51b083041662db5"
DESIGN_COMMIT = "81beff7df934d4502d01d252353d7a213e9f0a61"
PREDECESSOR = "97d35a13c3213fbbfb0c090923bf4271bddbf757"
RECEIPT = HERE / "RECEIPT.json"


def check(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)


def bindings() -> dict[str, str]:
    paths = {**{str(REL / name): HERE / name for name in FILES}, WORKFLOW: ROOT / WORKFLOW}
    out = {}
    for name, path in paths.items():
        data = path.read_bytes()
        out[name] = hashlib.sha256(data).hexdigest()
        if path.name == "DESIGN.md":
            git_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            check(git_blob == DESIGN_BLOB, "registered design changed")
    return out


def execute() -> dict:
    suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_temporal.py")
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    check(result.testsRun == 28 and result.wasSuccessful() and not result.skipped, stream.getvalue())
    import calibrate
    calculated = calibrate.run()
    check(calculated == json.loads((HERE / "RESULT.json").read_text()), "fresh calculation differs")
    return {"tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
            "skipped": len(result.skipped), "result": calculated}


def verify() -> dict:
    record = json.loads(RECEIPT.read_text())
    check(record.get("schema") == "ME_TEMPORAL_RECEIPT_V2", "receipt schema")
    check(record.get("design_commit") == DESIGN_COMMIT, "design identity")
    check(record.get("predecessor_commit") == PREDECESSOR, "predecessor identity")
    check(record.get("bindings") == bindings(), "binding omission or source drift")
    check(record.get("independent_review") == "NOT_OBTAINED__DISCLOSED_LIMITATION", "review promotion")
    check(record.get("production_model_closure") == "CANNOT_CHECK", "closure promotion")
    check(record.get("full_local_clean_clone") is False, "clone promotion")
    check(record.get("grants_scientific_authority") is False, "authority promotion")
    check(record.get("verification") == execute(), "verification record drift")
    return record["verification"]


def selftest() -> dict:
    results = {}
    for case, expected in (("valid", 0), ("source_drift", 1), ("missing_source", 2),
                           ("omitted_binding", 1), ("false_independence", 1)):
        with tempfile.TemporaryDirectory(prefix="me-temporal-") as tmp:
            root = Path(tmp)
            packet = root / REL
            shutil.copytree(HERE, packet, ignore=shutil.ignore_patterns("__pycache__"))
            (root / WORKFLOW).parent.mkdir(parents=True)
            shutil.copy2(ROOT / WORKFLOW, root / WORKFLOW)
            if case == "source_drift":
                with (packet / "temporal.py").open("a") as f:
                    f.write("\n# deliberately planted drift\n")
            elif case == "missing_source":
                (packet / "THEORY.md").unlink()
            elif case in ("omitted_binding", "false_independence"):
                record = json.loads((packet / "RECEIPT.json").read_text())
                if case == "omitted_binding":
                    record["bindings"].pop(str(REL / "temporal.py"))
                else:
                    record["independent_review"] = "PASS"
                (packet / "RECEIPT.json").write_text(json.dumps(record))
            run = subprocess.run([sys.executable, str(packet / "run.py"), "--verify"],
                                 capture_output=True, text=True, timeout=45)
            check(run.returncode == expected, f"{case}: exit {run.returncode}, expected {expected}")
            results[case] = run.returncode
    return {"cases": len(results), "controls": results}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--verify", action="store_true")
    mode.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    try:
        if sys.version_info < (3, 12):
            raise OSError("Python >=3.12 unavailable")
        if args.write:
            record = {"schema": "ME_TEMPORAL_RECEIPT_V2", "design_commit": DESIGN_COMMIT,
                      "predecessor_commit": PREDECESSOR, "bindings": bindings(),
                      "verification": execute(), "environment": {"python": platform.python_version(),
                      "system": platform.system(), "machine": platform.machine()},
                      "execution_location": "isolated Linux analysis container; not Mac/LUNARC",
                      "independent_review": "NOT_OBTAINED__DISCLOSED_LIMITATION",
                      "production_model_closure": "CANNOT_CHECK", "full_local_clean_clone": False,
                      "grants_scientific_authority": False}
            RECEIPT.write_text(json.dumps(record, sort_keys=True, indent=2) + "\n")
            output = record["verification"]
        elif args.selftest:
            output = selftest()
        else:
            output = verify()
        print(json.dumps(output, sort_keys=True, indent=2))
        return 0
    except (OSError, subprocess.TimeoutExpired, ImportError) as exc:
        print(json.dumps({"terminal": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except (ValueError, AssertionError, TypeError, KeyError) as exc:
        print(json.dumps({"terminal": "FAIL", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
