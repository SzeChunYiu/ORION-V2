"""The receipt machine/hand-written boundary guard, checked against its own controls
and against the real receipt in the repository.

`scripts/check_receipt_boundaries.py` exists because `PC_R6_OUTCOME_RECEIPT.md` separated
generated output from hand-written commentary with an HTML comment: not machine-readable,
not visible in rendered output, and two figures from the hand-written half were quoted
downstream as analysis output. A guard that cannot fail would be worse than none, so the
negative controls are asserted here as well as the positive one.
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "check_receipt_boundaries.py"
RECEIPT = REPO / "research/experiments/results/issue45/pc-r6/PC_R6_OUTCOME_RECEIPT.md"


def _load():
    spec = importlib.util.spec_from_file_location("check_receipt_boundaries", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


guard = _load()


def test_self_test_controls_all_pass():
    """Positive control, six negative controls, and the no-alarm case."""
    assert guard.self_test() == 0


def test_repository_is_clean():
    violations, checked = guard.check_paths(sorted((REPO / "research").rglob("*.md")))
    assert checked > 0, "could not check: no Markdown files found under research/"
    assert violations == []


def test_pc_r6_receipt_declares_a_verifiable_boundary():
    raw = RECEIPT.read_bytes()
    match = guard.MARKER_RE.search(raw)
    assert match is not None, "PC-R6 receipt must carry the canonical boundary marker"
    fields = guard._parse_marker_body(match.group("body"))
    n = int(fields["generated_bytes"])
    assert hashlib.sha256(raw[:n]).hexdigest() == fields["generated_sha256"]
    assert guard._check_declaring_file(RECEIPT, raw) == []


def test_editing_the_generated_region_of_the_real_receipt_is_caught(tmp_path):
    """Negative control on the real artifact, not only on a fixture."""
    raw = RECEIPT.read_bytes()
    n = int(guard._parse_marker_body(guard.MARKER_RE.search(raw).group("body"))["generated_bytes"])
    tampered = raw[:n].replace(b"PASS", b"FAIL", 1) + raw[n:]
    assert tampered != raw, "the fixture must actually change the generated region"
    target = tmp_path / RECEIPT.name
    target.write_bytes(tampered)
    violations, _ = guard.check_paths([target])
    assert any("machine-generated region has changed" in v for v in violations)


@pytest.mark.parametrize("argv, expected", [
    (["--self-test"], 0),
    ([str(REPO / "research")], 0),
])
def test_exit_codes(argv, expected):
    assert guard.main(argv) == expected


def test_missing_path_reports_could_not_check_not_success():
    """'could not check' must never be reported as 'checked and fine'."""
    assert guard.main([str(REPO / "no-such-directory")]) == 3
