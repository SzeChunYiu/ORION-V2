"""ME-X2 V2 provenance: the V1 lane is imported, never edited.

V2 changes the arm under test and nothing else.  The instance stream, the exact
oracle, the registered templates, the parent implementations and V1's rendering
of ``M`` are the frozen V1 files, whose sha256 were published in
``research/experiments/me-x2/ME_X2_PARENT_FIDELITY_RECEIPT_V1.md`` §1 before any
protected outcome existed.  ``check()`` re-verifies them; gate G0d fails the
lane if any byte moved, so a V2 result can never be a comparison against a
silently different world.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

V1_DIR = Path(__file__).resolve().parent.parent / "me-x2"

# sha256 as published in the V1 parent-fidelity receipt §1 (frozen 2026-09-02, main 704d379).
V1_FROZEN_SHA256 = {
    "mex2_model.py": "f43462b2d50dda48e9a731ae8f1136807651c18c78a58bdfc10c2040d432db86",
    "mex2_catalogue.py": "f809870ae4a20c8df2a8a72db545684e99b64386e146b64997c7ba19c4b1f294",
    "mex2_oracle.py": "399a81568011ccfdf7ba69c5f70b69c697874a7d78971cf5c8f12ec390eba241",
    "mex2_generator.py": "70eba6705b02a67f9dde08d162c492324c8cac8d7fe66d3f898c398be2e66ef8",
    "mex2_parents.py": "211da544f95ffffa7eb381e67ca607f7fc6e29c0a48857e865268357d562b923",
    "mex2_arms.py": "fb56bedc5a00c4cf7889b338b867fbcc7557f979d184233c2738174b738342db",
    "mex2_run.py": "818b7f4d345673d2a238278aac689876d5410afdb9599d50cdff7312ce16e5cf",
    "ME_X2_LOCUS_DIAGNOSIS_EXACT_STUDY_DESIGN_V1.json": "bb63685c02da55e7c7ebdf72541e862bcc92661b07a1074e33b8371a35e5d7c9",
}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check() -> dict:
    """Every frozen V1 file present and byte-identical to its published hash."""
    files = {}
    ok = True
    for name, expected in sorted(V1_FROZEN_SHA256.items()):
        p = V1_DIR / name
        got = sha256_file(p) if p.exists() else None
        match = got == expected
        ok &= match
        files[name] = {"expected_sha256": expected, "sha256": got, "matches": bool(match)}
    return {"v1_dir": str(V1_DIR), "all_match": bool(ok), "files": files}
