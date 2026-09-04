"""Verify this research receipt's exact file bindings (not external authority)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = "research/machine-epistemics-theory/causal_verifier_v1/"
EXPECTED = {PREFIX + x for x in ("causal_verifier.py", "CALIBRATION.json", "THEORY.md", "SOURCES.md",
                               "ABSORPTION.md", "README.md", "verify_receipt.py")} | {
    "tests/unit/test_me_causal_verifier_v1.py", ".github/workflows/me-causal-verifier.yml"}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    try:
        receipt = json.loads((HERE / "RECEIPT.json").read_text())
        expected_digest = receipt.pop("receipt_payload_sha256")
        require(digest(receipt) == expected_digest, "RECEIPT_BODY_DRIFT")
        require(receipt["identity"] == "ME-CAUSAL-VERIFIER-V1", "IDENTITY_DRIFT")
        require(receipt["full_foundation_closed"] is False and
                receipt["independent_review"] == "NOT_OBTAINED", "CLAIM_PROMOTION")
        require(set(receipt["file_sha256"]) == EXPECTED, "BINDING_SET_DRIFT")
        for relative, expected in receipt["file_sha256"].items():
            target = (ROOT / relative).resolve()
            require(target.is_relative_to(ROOT), "PATH_ESCAPE")
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            require(actual == expected, "FILE_DRIFT:" + relative)
        calibration = json.loads((HERE / "CALIBRATION.json").read_text())
        stated = calibration.pop("body_sha256")
        require(digest(calibration) == stated, "CALIBRATION_BODY_DRIFT")
        require(stated == receipt["calibration_body_sha256"], "CALIBRATION_RECEIPT_DRIFT")
        print(json.dumps({"status": "PASS", "bound_files": len(EXPECTED),
                          "grants_external_authority": False}, sort_keys=True))
        return 0
    except OSError as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    except (KeyError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
