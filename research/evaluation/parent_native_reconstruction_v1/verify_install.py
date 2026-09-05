"""Check pip's actual installation report against every prospective version/hash."""
import json
from pathlib import Path
import re
import sys

from adapter import PINS, ROOT


def verify(report_path):
    document = json.loads(Path(report_path).read_text())
    expected = {d["name"]: d for d in json.loads((ROOT / "DEPENDENCY_SOURCES.json").read_text())["dependencies"]}
    seen = {}
    for installed in document["install"]:
        metadata = installed["metadata"]
        name = metadata["name"].lower().replace("_", "-")
        if name in seen or name not in PINS or metadata["version"] != PINS[name]:
            raise ValueError("unexpected_or_duplicate_installed_distribution:" + name)
        archive = installed["download_info"]["archive_info"]["hashes"]["sha256"]
        if not re.fullmatch("[a-f0-9]{64}", archive):
            raise ValueError("missing_actual_archive_digest:" + name)
        pinned = expected[name]["wheel_sha256"]
        if pinned is not None and pinned != archive:
            raise ValueError("upstream_wheel_digest_mismatch:" + name)
        seen[name] = {"version": metadata["version"], "archive_sha256": archive}
    if set(seen) != set(PINS):
        raise ValueError("installed_dependency_closure_mismatch")
    return {"status": "EXACT_NATIVE_DEPENDENCY_INSTALLATION_VERIFIED", "distributions": seen}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python verify_install.py PIP_REPORT.json")
    print(json.dumps(verify(sys.argv[1]), sort_keys=True))
