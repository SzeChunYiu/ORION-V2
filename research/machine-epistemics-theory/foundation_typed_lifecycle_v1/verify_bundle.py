"""Verify content custody, the claim map and exact calibration. Exit 0/1/2."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys
import tempfile

FILES = {"README.md", "THEORY.md", "ATLAS_MAP.json", "SOURCES.md", "FRONTIER.md",
         "OCM_HANDOFF.md", "REVIEW.md", "POST_BASELINE_DELTA.md", "calculus.py", "check_calculus.py",
         "RESULTS.json", "verify_bundle.py", "Foundation.lean", "verify_lean.py"}
GROUPS = {"intervals", "nogoods", "substitution", "navigation", "selection",
          "adaptive_risk", "drift", "certificates", "lifecycle", "semantics", "learning"}


class Missing(Exception):
    pass


def body_digest(value: dict) -> str:
    body = {k: v for k, v in value.items() if k != "body_sha256"}
    return sha256(json.dumps(body, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def load(path: Path) -> dict:
    if not path.is_file():
        raise Missing("required artifact unavailable: " + path.name)
    return json.loads(path.read_text())


def verify_artifacts(base: Path) -> dict:
    receipt = load(base / "RECEIPT.json")
    if receipt.get("body_sha256") != body_digest(receipt):
        raise ValueError("receipt body digest mismatch")
    if set(receipt.get("files", {})) != FILES:
        raise ValueError("missing or extra bound file")
    for name, expected in receipt["files"].items():
        path = base / name
        if not path.is_file():
            raise Missing("required bound artifact unavailable: " + name)
        actual = sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError("bound artifact drift: " + name)
    registry = load(base / "ATLAS_MAP.json")
    if registry.get("full_foundation_closed") is not False:
        raise ValueError("unearned full foundation closure")
    gaps, theorems = registry["gaps"], registry["theorems"]
    ids = [row["id"] for row in gaps]
    tids = [row["id"] for row in theorems]
    if len(ids) != 35 or set(ids) != {f"MEG-{i:02d}" for i in range(1, 36)}:
        raise ValueError("gap map must cover each of the 35 IDs exactly once")
    if len(tids) != 16 or set(tids) != {f"T{i:02d}" for i in range(1, 17)}:
        raise ValueError("theorem map must cover each of the 16 IDs exactly once")
    for row in gaps:
        if row.get("programme_closed") is not False or not row.get("remaining"):
            raise ValueError("partial result silently closes a broad gap")
        if not set(row["theorems"]) <= set(tids) or not set(row["check_groups"]) <= GROUPS:
            raise ValueError("dangling gap dependency")
    statement_text = (base / "THEORY.md").read_text()
    for row in theorems:
        if row.get("statement_file") != "THEORY.md" or row.get("section") != row["id"] or ("## " + row["id"] + ".") not in statement_text:
            raise ValueError("dangling theorem statement")
        if row.get("finite_checks_are_all_size_proof") is not False:
            raise ValueError("enumeration promoted into all-size proof")
        if not row["finite_check_groups"] or not set(row["finite_check_groups"]) <= GROUPS:
            raise ValueError("missing theorem calibration binding")
    result = load(base / "RESULTS.json")
    groups = result.get("groups", {})
    if set(groups) != GROUPS or result.get("group_count") != len(GROUPS):
        raise ValueError("empty or incomplete calibration")
    if any(r.get("status") != "PASS" or r.get("checks", 0) <= 0 or not r.get("controls")
           for r in groups.values()):
        raise ValueError("missing check or discriminating control")
    counts = (sum(r["checks"] for r in groups.values()),
              sum(len(r["controls"]) for r in groups.values()))
    if counts != (result["check_count"], result["control_count"]):
        raise ValueError("calibration counts do not reconcile")
    if counts != (receipt["calibration"]["check_count"], receipt["calibration"]["control_count"]):
        raise ValueError("receipt/result count mismatch")
    if result.get("all_size_proof_authority") is not False or result.get("ocm_adoption") != "NOT_GRANTED":
        raise ValueError("unearned scientific or runtime authority")
    return receipt


def hostile_bindings(base: Path) -> list[str]:
    caught = []
    for case in ("code_drift", "proof_missing", "binding_omitted", "empty_result", "atlas_promoted"):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp)
            for name in FILES | {"RECEIPT.json"}:
                shutil.copyfile(base / name, copy / name)
            receipt = load(copy / "RECEIPT.json")
            if case == "code_drift":
                with (copy / "calculus.py").open("a") as out:
                    out.write("\n# planted drift\n")
            elif case == "proof_missing":
                (copy / "THEORY.md").unlink()
            elif case == "binding_omitted":
                del receipt["files"]["THEORY.md"]
            elif case == "empty_result":
                result = load(copy / "RESULTS.json")
                result["groups"] = {}
                (copy / "RESULTS.json").write_text(json.dumps(result))
                receipt["files"]["RESULTS.json"] = sha256((copy / "RESULTS.json").read_bytes()).hexdigest()
            else:
                registry = load(copy / "ATLAS_MAP.json")
                registry["full_foundation_closed"] = True
                (copy / "ATLAS_MAP.json").write_text(json.dumps(registry))
                receipt["files"]["ATLAS_MAP.json"] = sha256((copy / "ATLAS_MAP.json").read_bytes()).hexdigest()
            receipt["body_sha256"] = body_digest(receipt)
            (copy / "RECEIPT.json").write_text(json.dumps(receipt))
            try:
                verify_artifacts(copy)
            except Missing:
                if case != "proof_missing":
                    raise ValueError("wrong missing-input outcome for " + case)
                caught.append(case + ":CANNOT_CHECK")
            except ValueError:
                if case == "proof_missing":
                    raise ValueError("missing proof misclassified as checked defect")
                caught.append(case + ":FAIL")
            else:
                raise ValueError("hostile fixture escaped: " + case)
    return caught


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostile", action="store_true")
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    try:
        receipt = verify_artifacts(base)
        from check_calculus import run
        actual = run()
        if actual != load(base / "RESULTS.json"):
            raise ValueError("fresh exact run differs from recorded result")
        controls = hostile_bindings(base) if args.hostile else []
        print(json.dumps({"terminal": "BUNDLE_VERIFIED", "body_sha256": receipt["body_sha256"],
                          "check_count": actual["check_count"], "control_count": actual["control_count"],
                          "gap_rows": 35, "theorem_rows": 16, "custody_hostiles": controls,
                          "proof_assistant_status": "SEPARATE_EXECUTION_REQUIRED",
                          "independent_review": "NOT_OBTAINED"}, indent=2, sort_keys=True))
        return 0
    except (Missing, OSError, ModuleNotFoundError) as exc:
        print(json.dumps({"terminal": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except (ValueError, TypeError, KeyError, ArithmeticError) as exc:
        print(json.dumps({"terminal": "FAIL", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
