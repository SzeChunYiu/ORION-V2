"""Execute every authored test and retain exact native packets in a fresh directory."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import unittest

import test_adapter
from verify_sources import verify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    binding = verify()
    args.output.mkdir(parents=True, exist_ok=False)
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_adapter)
    with (args.output / "tests.log").open("x") as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    outputs = getattr(test_adapter.NativeParentTests, "outputs", {})
    identities = []
    for name, packet in sorted(outputs.items()):
        raw = (json.dumps(packet, indent=2, sort_keys=True) + "\n").encode()
        path = args.output / (name + ".json")
        with path.open("xb") as stream:
            stream.write(raw)
        identities.append({"file": path.name, "sha256": hashlib.sha256(raw).hexdigest(),
                           "input_sha256": packet.get("execution", {}).get("input_sha256", packet.get("input_sha256")),
                           "status": packet["status"]})
    good = (result.wasSuccessful() and result.testsRun == 20 and not result.skipped
            and len(outputs) == 7 and all(p["status"] == "OBSERVED" for p in outputs.values()))
    report = {"schema": "PUBLIC_PARENT_NATIVE_FIT_RUN_V1",
              "terminal": "PUBLIC_ENGINEERING_FIT_PASS" if good else "PUBLIC_ENGINEERING_FIT_NOT_PASSED",
              "python": sys.version, "platform": platform.platform(),
              "source_bindings": binding, "tests": result.testsRun,
              "failures": len(result.failures), "errors": len(result.errors),
              "skips": len(result.skipped), "public_cases": identities,
              "paired_subject_outcomes_accessed": False,
              "strongest_parent_bound": False, "protected_parity_run": False,
              "scientific_terminal": "CANNOT_CHECK"}
    with (args.output / "REPORT.json").open("x") as stream:
        json.dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps(report, sort_keys=True))
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main())
