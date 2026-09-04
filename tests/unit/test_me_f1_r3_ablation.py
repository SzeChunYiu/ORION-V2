"""ME-F1 R3: organ ablation on the development split -- constants, routing, V1 untouched."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2] / "research" / "experiments"
R3 = HERE / "me-f1-r3"
V1 = HERE / "me-f1"


def _load():
    for p in (R3, V1):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    spec = importlib.util.spec_from_file_location("mef1r3_ablation", R3 / "mef1r3_ablation.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


RS = _load()


def test_selftest_passes():
    assert RS.selftest() == 0


def test_every_arm_is_v1_frozen_and_no_text_is_authored_here():
    src = (R3 / "mef1r3_ablation.py").read_text()
    # an authored arm text would carry V1's control-text marker; reading V1's table is allowed
    assert "YOUR PROCEDURE (" not in src
    import mef1_arms as A
    assert all(a in A.MODEL_ARMS for a in RS.ARMS)


def test_v1_is_untouched_by_this_lane():
    """The R3 lane may not edit V1; the manifest V1 froze must still describe mef1_arms.py."""
    manifest = json.loads((V1 / "ME_F1_SOURCE_MANIFEST_V1.json").read_text())
    files = manifest.get("source_files_sha256") or manifest.get("files") or {}
    key = next((k for k in files if k.endswith("mef1_arms.py")), None)
    assert key is not None, list(files)[:5]
    assert files[key] == hashlib.sha256((V1 / "mef1_arms.py").read_bytes()).hexdigest()


def test_frozen_state_if_present_matches_inputs():
    fp = RS.RESULTS / "ME_F1_R3_FREEZE_V1.json"
    if not fp.exists():
        return
    fz = json.loads(fp.read_text())
    assert fz["design_json_sha256"] == RS.sha256_file(RS.DESIGN_JSON)
    assert fz["v1_arms_py_sha256"] == RS.sha256_file(V1 / "mef1_arms.py")
    assert fz["calibration_receipt_sha256"] == RS.sha256_file(RS.CALIBRATION)
